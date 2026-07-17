#!/usr/bin/env python3
"""Reconcile the committed FedRAMP 20x KSI mapping against FedRAMP's live ruleset.

The KSI mapping in this repo is authored. Authored means it was correct on the
day it was written and silently rots on every day after. FedRAMP publishes its
ruleset as versioned, machine-readable data and revises it on its own schedule,
so "the mapping is current" is a claim that has to be recomputed, not asserted.

This is the recomputation. It fetches the upstream ruleset, reconciles it
against the committed mapping on three axes, and writes a receipt recording
what was compared, against which upstream version, and when.

    upstream   github.com/FedRAMP/rules :: fedramp-consolidated-rules.json
    committed  04-evidence-and-audit/data/fedramp-20x-ksi-mapping.yaml
    receipt    04-evidence-and-audit/upstream-conformance-receipt.md

Three axes:
    1. version   the upstream version string vs. the version last reconciled
    2. identity  the upstream KSI id set vs. the mapped id set (both directions)
    3. structure the upstream per-category indicator counts vs. the mapping's

FAILURE MODE: CLOSED. Every unexpected condition exits non-zero -- network
failure, malformed upstream, schema change, zero KSIs parsed, unreadable
mapping. A checker that cannot check must never report "pass"; that failure is
the entire reason this program exists, so this file does not get to commit it.

    python3 04-evidence-and-audit/data/upstream_drift.py            # reconcile, write receipt
    python3 04-evidence-and-audit/data/upstream_drift.py --check    # CI: no write, exit code only

Exit codes:  0 reconciled  |  1 drift detected  |  2 could not check
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL[2]: pyyaml not installed. Cannot read the mapping, so cannot check.", file=sys.stderr)
    sys.exit(2)

UPSTREAM_URL = (
    "https://raw.githubusercontent.com/FedRAMP/rules/main/fedramp-consolidated-rules.json"
)
UPSTREAM_HUMAN = "github.com/FedRAMP/rules :: fedramp-consolidated-rules.json"

HERE = Path(__file__).resolve().parent
MAPPING = HERE / "fedramp-20x-ksi-mapping.yaml"
RECEIPT = HERE.parent / "upstream-conformance-receipt.md"

# The upstream version this repo's mapping was last reconciled against.
# Bumping this is a human act: it means someone re-read the diff and re-derived
# the mapping. CI cannot bump it, which is the point.
RECONCILED_AGAINST = "2026.07.14.01"


class CannotCheck(Exception):
    """Raised when the check itself could not be performed. Always exit 2."""


def fetch_upstream(url: str = UPSTREAM_URL, timeout: int = 30) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mattermost-grc-day-one/drift-check"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status != 200:
                raise CannotCheck(f"upstream returned HTTP {r.status}")
            raw = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        raise CannotCheck(f"could not reach upstream: {e}") from e

    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CannotCheck(f"upstream is not valid JSON: {e}") from e

    if not isinstance(doc, dict) or "KSI" not in doc or "info" not in doc:
        raise CannotCheck(
            "upstream JSON lacks the expected 'info'/'KSI' shape -- the schema moved. "
            "Refusing to guess."
        )
    return doc


def upstream_ksis(doc: dict) -> tuple[str, dict[str, list[str]]]:
    version = str(doc["info"].get("version") or "").strip()
    if not version:
        raise CannotCheck("upstream carries no version string")

    by_cat: dict[str, list[str]] = {}
    for short, body in doc["KSI"].items():
        if not isinstance(body, dict):
            raise CannotCheck(f"upstream KSI category {short!r} is not an object")
        inds = body.get("indicators")
        if not isinstance(inds, dict):
            raise CannotCheck(f"upstream KSI category {short!r} has no indicators map")
        by_cat[body.get("name", short)] = sorted(inds.keys())

    total = sum(len(v) for v in by_cat.values())
    if total == 0:
        # Fail closed: zero parsed means the parse broke, not that FedRAMP
        # deleted every indicator.
        raise CannotCheck("parsed zero KSIs from upstream -- treating as a broken parse, not an empty ruleset")
    return version, by_cat


def committed_ksis() -> tuple[dict, dict[str, list[str]]]:
    if not MAPPING.is_file():
        raise CannotCheck(f"committed mapping not found at {MAPPING}")
    try:
        doc = yaml.safe_load(MAPPING.read_text())
    except yaml.YAMLError as e:
        raise CannotCheck(f"committed mapping is not valid YAML: {e}") from e
    if not isinstance(doc, dict) or "categories" not in doc:
        raise CannotCheck("committed mapping lacks a 'categories' key")

    by_cat: dict[str, list[str]] = {}
    for cat in doc["categories"]:
        ids = [k["id"] for k in cat.get("ksis", [])]
        by_cat[cat["category"]] = sorted(ids)
    if sum(len(v) for v in by_cat.values()) == 0:
        raise CannotCheck("committed mapping parsed to zero KSIs")
    return doc.get("metadata", {}), by_cat


def flat(by_cat: dict[str, list[str]]) -> set[str]:
    return {i for ids in by_cat.values() for i in ids}


def git_sha() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=HERE, capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def compare(
    up_version: str,
    up_cats: dict[str, list[str]],
    mine_cats: dict[str, list[str]],
    reconciled_against: str = RECONCILED_AGAINST,
) -> list[str]:
    """The whole comparison, as a pure function. No I/O, so it is testable.

    This is deliberately separated from reconcile(): the drift logic is the
    thing being trusted, so it is the thing that has to be provable against
    fixtures. See test_upstream_drift.py -- which fails if this function is
    ever gutted to return no findings.
    """
    up_ids, mine_ids = flat(up_cats), flat(mine_cats)
    findings: list[str] = []

    # axis 1 -- version
    if up_version != reconciled_against:
        findings.append(
            f"VERSION: upstream is now {up_version}; this repo was last reconciled "
            f"against {reconciled_against}. A human must re-derive the mapping and "
            f"bump RECONCILED_AGAINST."
        )

    # axis 2 -- identity, both directions
    added = sorted(up_ids - mine_ids)
    removed = sorted(mine_ids - up_ids)
    if added:
        findings.append(f"ADDED upstream, absent from mapping ({len(added)}): {', '.join(added)}")
    if removed:
        findings.append(f"MAPPED here, absent upstream ({len(removed)}): {', '.join(removed)}")

    # axis 3 -- structure
    for cat, ids in sorted(up_cats.items()):
        mine = mine_cats.get(cat)
        if mine is None:
            findings.append(f"CATEGORY missing from mapping: {cat!r} ({len(ids)} KSIs)")
        elif len(mine) != len(ids):
            findings.append(f"COUNT {cat!r}: upstream {len(ids)}, mapping {len(mine)}")

    return findings


def reconcile() -> tuple[list[str], dict]:
    """Return (drift_findings, facts). Empty findings == reconciled."""
    doc = fetch_upstream()
    up_version, up_cats = upstream_ksis(doc)
    meta, mine_cats = committed_ksis()

    findings = compare(up_version, up_cats, mine_cats)
    up_ids, mine_ids = flat(up_cats), flat(mine_cats)

    facts = {
        "upstream_version": up_version,
        "upstream_updated": doc["info"].get("last_updated", "unknown"),
        "upstream_title": doc["info"].get("title", "unknown"),
        "reconciled_against": RECONCILED_AGAINST,
        "upstream_total": len(up_ids),
        "mapping_total": len(mine_ids),
        "categories": {c: (len(up_cats[c]), len(mine_cats.get(c, []))) for c in sorted(up_cats)},
        "mapping_basis_checked": meta.get("basis_checked", "unstated"),
        "checked_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "commit": git_sha(),
    }
    return findings, facts


def render_receipt(findings: list[str], f: dict) -> str:
    ok = not findings
    verdict = "RECONCILED" if ok else "DRIFT DETECTED"
    mark = "reconciled" if ok else "**drift**"

    L = [
        "# Upstream conformance receipt",
        "",
        "Machine-generated by [`04-evidence-and-audit/data/upstream_drift.py`](data/upstream_drift.py).",
        "Do not edit by hand: the next run overwrites it.",
        "",
        f"## {verdict}",
        "",
        "| | |",
        "|---|---|",
        f"| **Upstream** | [{UPSTREAM_HUMAN}]({UPSTREAM_URL}) |",
        f"| **Upstream version** | `{f['upstream_version']}` (published {f['upstream_updated']}) |",
        f"| **Last reconciled against** | `{f['reconciled_against']}` |",
        f"| **KSIs upstream** | {f['upstream_total']} |",
        f"| **KSIs mapped here** | {f['mapping_total']} |",
        f"| **Result** | {f['mapping_total']}/{f['upstream_total']} reconciled, {len(findings)} finding(s) |",
        f"| **Checked** | {f['checked_at']} at commit `{f['commit']}` |",
        "",
    ]

    if ok:
        L += [
            "Every KSI id published in the current FedRAMP ruleset is present in this "
            "repo's mapping, and this repo's mapping claims no KSI that FedRAMP does "
            "not publish. Verified in both directions, per category, at the version "
            "stamped above.",
            "",
        ]
    else:
        L += ["### Findings", ""]
        L += [f"{i}. {x}" for i, x in enumerate(findings, 1)]
        L += [
            "",
            "The mapping is stale until a human re-derives it and bumps "
            "`RECONCILED_AGAINST`. CI cannot bump it; that is deliberate.",
            "",
        ]

    L += ["### Per category", "", "| Category | Upstream | Mapped | |", "|---|---:|---:|---|"]
    for cat, (u, m) in f["categories"].items():
        L.append(f"| {cat} | {u} | {m} | {'ok' if u == m else mark} |")

    L += [
        "",
        "---",
        "",
        "### Why this file exists",
        "",
        "The KSI mapping in this repo is authored by a human, which means it was true "
        "on the day it was written. FedRAMP revises its ruleset on its own schedule and "
        "publishes every revision as versioned machine-readable data. So the claim "
        "\"this mapping is current\" has an expiry date that nobody is notified about.",
        "",
        "This check gives that claim a computation instead of a promise. It runs on a "
        "schedule and on every push, and it fails the build when FedRAMP moves and this "
        "repo has not. The mapping does not become correct by being checked -- a person "
        "still has to re-derive it. What the check removes is the possibility of not "
        "noticing.",
        "",
        "It fails **closed**. Network failure, moved schema, malformed upstream, or zero "
        "KSIs parsed all exit non-zero rather than reporting a pass. A gate that reports "
        "\"pass\" without having checked is the specific failure this whole program is "
        "built against, and this checker does not get an exemption from its own rule.",
        "",
    ]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="CI mode: exit code only, no receipt written")
    args = ap.parse_args()

    try:
        findings, facts = reconcile()
    except CannotCheck as e:
        print(f"FAIL[2] could not check: {e}", file=sys.stderr)
        print("Failing closed. A checker that cannot check does not report a pass.", file=sys.stderr)
        return 2

    if not args.check:
        RECEIPT.write_text(render_receipt(findings, facts))
        print(f"receipt -> {RECEIPT.relative_to(HERE.parent.parent)}")

    print(f"upstream {facts['upstream_version']} (published {facts['upstream_updated']})")
    print(f"reconciled against {facts['reconciled_against']}")
    print(f"{facts['mapping_total']}/{facts['upstream_total']} KSIs reconciled, both directions")

    if findings:
        print(f"\nDRIFT: {len(findings)} finding(s)", file=sys.stderr)
        for i, x in enumerate(findings, 1):
            print(f"  {i}. {x}", file=sys.stderr)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
                fh.write(render_receipt(findings, facts))
        return 1

    print("\nRECONCILED: no drift.")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
            fh.write(render_receipt(findings, facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
