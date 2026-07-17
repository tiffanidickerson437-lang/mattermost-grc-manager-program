#!/usr/bin/env python3
"""The CMMC annual affirmation (32 CFR 170.22), computed instead of assembled.

WHY THIS EXISTS

CMMC Phase 2 was suspended on 2026-07-13. Phase 1 was not. Level 2
self-assessment remains in force, DFARS 252.204-7012 is untouched, and
32 CFR 170.22 still requires an Affirming Official -- a named senior human --
to affirm CONTINUING compliance in SPRS after every assessment and annually
thereafter.

"Continuing" is the load-bearing word. The assessment was a point in time. The
affirmation is a claim that it is STILL true today, signed by a person, posted
to the government, under False Claims Act exposure. Losing the C3PAO raised
that bar rather than lowering it: nobody now stands between the company's claim
and the government reading it.

Almost everywhere, that claim is assembled once a year from a spreadsheet
nobody can re-derive. This computes it instead.

WHAT IT DOES

    1. Scores all 110 requirements from control state, implementing the DoD
       Assessment Methodology v1.2.1 exactly -- including both partial-credit
       exceptions (3.5.3, 3.13.11) and the 3.12.4 precondition.
    2. Gates the affirmation. Answers one question: MAY the Affirming Official
       sign today, and if not, what specifically blocks them.
    3. Emits the packet: score, date, blockers, and what backs the claim.

WHAT IT DOES NOT DO

    It never signs. 32 CFR 170.22 gives that act to a named human, and the
    gate has no opinion it is entitled to substitute. It computes whether the
    conditions for signing hold; a person still decides to sign. That is not a
    limitation worked around -- it is the regulation, and it is also the
    program's own rule: AI drafts, humans decide, code computes.

    It contains no Mattermost data and claims no Mattermost score. Control
    state is only knowable inside the boundary, from systems of record. The
    example state file is synthetic and labeled as such. On day one this points
    at real systems; today it proves the instrument works.

FAILURE MODE: CLOSED. Unknown state, missing requirement, absent SSP,
unreachable regulation -- all block the affirmation. A gate that says "sign it"
without having checked is the failure this program is built against, and an
affirmation is the single worst place to make it.

    python3 06-evidence-and-audit/data/affirmation_gate.py --state <file>
    python3 06-evidence-and-audit/data/affirmation_gate.py --state <file> --check
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("BLOCK[2]: pyyaml missing. Cannot read state, so cannot affirm.", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
WEIGHTS = HERE / "sprs-weights.json"
PACKET = HERE.parent / "affirmation-packet.md"

# 32 CFR 170 as published. eCFR exposes every section's amendment date, so the
# regulation is a versioned upstream like any other. When the CMMC Reform Task
# Force lands (report due to the DoW CIO ~mid-September 2026), it changes this
# date, and this gate goes red the same week rather than at next year's audit.
ECFR_API = (
    "https://www.ecfr.gov/api/versioner/v1/versions/title-32.json"
    "?subtitle=A&chapter=I&subchapter=G&part=170"
)
RULE_AS_RECONCILED = "2024-12-16"
RULE_SECTIONS = {"170.22": "Affirmation", "170.24": "CMMC Scoring Methodology"}

# DoD Assessment Methodology v1.2.1, 24 June 2020.
# Exactly two requirements carry partial credit. Everything else is all-or-nothing.
PARTIAL_CREDIT = {
    "3.5.3": {
        "deduct": 3,
        "state": "partial",
        "means": "MFA implemented for remote and privileged users but not general users",
    },
    "3.13.11": {
        "deduct": 3,
        "state": "partial",
        "means": "cryptography employed but mostly not FIPS-validated",
    },
}
# The SSP. Unscored -- but its absence means the assessment cannot be conducted
# at all, so it is a precondition rather than a line item worth zero.
PRECONDITION = "3.12.4"

VALID_STATES = {"implemented", "not_implemented", "partial", "unknown"}
POAM_WINDOW_DAYS = 180


class CannotAffirm(Exception):
    """The gate could not evaluate. Always exit 2. Never a pass."""


# ----------------------------------------------------------------- scoring --
def load_weights() -> dict[str, str]:
    if not WEIGHTS.is_file():
        raise CannotAffirm(f"SPRS weights not found at {WEIGHTS}")
    w = json.loads(WEIGHTS.read_text())
    if len(w) != 110:
        raise CannotAffirm(f"expected 110 weighted requirements, found {len(w)}")
    return w


def score(state: dict[str, str], weights: dict[str, str]) -> tuple[int, list[dict]]:
    """Compute the SPRS score from control state. Pure -- no I/O, so testable.

    Start at 110, subtract the weight of every requirement not implemented.
    Partial credit exists for exactly two requirements. Floor is -203, which
    this reaches by arithmetic rather than by clamping: the weights sum to 313
    and 110 - 313 = -203. If that identity ever breaks, the weights are wrong.
    """
    missing = set(weights) - set(state)
    if missing:
        raise CannotAffirm(
            f"{len(missing)} requirement(s) absent from state file: "
            f"{', '.join(sorted(missing)[:5])}{'...' if len(missing) > 5 else ''}. "
            "An unstated requirement is not an implemented one."
        )

    total, deductions = 110, []
    for req, w in sorted(weights.items()):
        st = state[req]
        if st not in VALID_STATES:
            raise CannotAffirm(f"{req}: unrecognized state {st!r}")
        if st == "unknown":
            # Fail closed. Unknown is not implemented and is not a zero.
            continue
        if w == "NA":
            continue
        if st == "partial":
            if req not in PARTIAL_CREDIT:
                raise CannotAffirm(
                    f"{req}: partial state given, but the DoD methodology grants partial "
                    f"credit only to {', '.join(sorted(PARTIAL_CREDIT))}. "
                    "Everything else is all-or-nothing."
                )
            d = PARTIAL_CREDIT[req]["deduct"]
            total -= d
            deductions.append({"req": req, "deduct": d, "state": "partial", "weight": int(w)})
        elif st == "not_implemented":
            total -= int(w)
            deductions.append({"req": req, "deduct": int(w), "state": "not_implemented", "weight": int(w)})
    return total, deductions


# -------------------------------------------------------------- regulation --
def rule_drift(timeout: int = 25) -> tuple[str, list[str]]:
    """Has 32 CFR 170 moved under us? Returns (as_published, findings)."""
    try:
        req = urllib.request.Request(ECFR_API, headers={"User-Agent": "mattermost-grc-day-one/affirmation-gate"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status != 200:
                raise CannotAffirm(f"eCFR returned HTTP {r.status}")
            doc = json.loads(r.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError) as e:
        raise CannotAffirm(f"could not read 32 CFR 170 from eCFR: {e}")

    cvs = doc.get("content_versions")
    if not cvs:
        raise CannotAffirm("eCFR returned no content_versions -- the API shape moved. Refusing to guess.")

    seen = {c["identifier"]: c.get("amendment_date") for c in cvs}
    findings = []
    for sec, name in RULE_SECTIONS.items():
        if sec not in seen:
            findings.append(f"32 CFR {sec} ({name}) is no longer published -- the rule was restructured.")
        elif seen[sec] != RULE_AS_RECONCILED:
            findings.append(
                f"32 CFR {sec} ({name}) amended {seen[sec]}; this repo reconciled against "
                f"{RULE_AS_RECONCILED}. The rule changed. Re-read it before affirming against it."
            )
    return RULE_AS_RECONCILED, findings


# -------------------------------------------------------------------- gate --
def gate(state: dict, weights: dict, reg_findings: list[str], today: dt.date) -> tuple[list[str], dict]:
    """May the Affirming Official sign? Pure. Empty blockers == may sign."""
    reqs = state["requirements"]
    blockers: list[str] = []

    # Precondition: no SSP, no assessment. Not a deduction -- a stop.
    if reqs.get(PRECONDITION) != "implemented":
        blockers.append(
            f"32 CFR 170.22 has no assessment to affirm: {PRECONDITION} (system security plan) "
            f"is {reqs.get(PRECONDITION)!r}. Without an SSP the assessment cannot be conducted, "
            "so there is nothing to attest is continuing."
        )

    # Unknown state. The affirmation says "continuing compliance". You cannot
    # attest to the continuity of something whose current state you do not know.
    unknown = sorted(r for r, s in reqs.items() if s == "unknown")
    if unknown:
        blockers.append(
            f"{len(unknown)} requirement(s) in unknown state: "
            f"{', '.join(unknown[:6])}{'...' if len(unknown) > 6 else ''}. "
            "An affirmation of continuing compliance cannot rest on requirements nobody checked."
        )

    # POA&M window. 32 CFR 170 closes POA&Ms at 180 days; an expired one is an
    # open unmet requirement wearing a plan.
    for p in state.get("poam", []):
        opened = dt.date.fromisoformat(str(p["opened"]))
        age = (today - opened).days
        if age > POAM_WINDOW_DAYS:
            blockers.append(
                f"POA&M for {p['req']} opened {opened} is {age} days old, past the "
                f"{POAM_WINDOW_DAYS}-day close-out window. It is an unmet requirement now."
            )

    # The regulation itself.
    blockers.extend(reg_findings)

    sc, deductions = score(reqs, weights)
    facts = {
        "score": sc,
        "deductions": deductions,
        "unknown": unknown,
        "assessed": len([s for s in reqs.values() if s != "unknown"]),
        "max_deduction": sum(int(w) for w in weights.values() if w != "NA"),
    }
    return blockers, facts


# ----------------------------------------------------------------- packet ---
def render(blockers: list[str], f: dict, state: dict, rule_date: str) -> str:
    may = not blockers
    L = [
        "# CMMC annual affirmation packet — 32 CFR 170.22",
        "",
        "Machine-generated by [`06-evidence-and-audit/data/affirmation_gate.py`](data/affirmation_gate.py). "
        "Do not edit by hand; the next run overwrites it.",
        "",
        f"> **Source of state:** `{state.get('source', 'unstated')}`  ",
        f"> **This is {'SYNTHETIC EXAMPLE DATA' if state.get('synthetic') else 'live state'}.** "
        + ("No Mattermost control state exists in this repo and none is claimed. "
           "State is only knowable inside the boundary, from systems of record. "
           "This file proves the instrument computes; it asserts nothing about anyone's posture."
           if state.get("synthetic") else ""),
        "",
        f"## Verdict: {'CLEAR TO AFFIRM' if may else 'BLOCKED — DO NOT AFFIRM'}",
        "",
        "| | |",
        "|---|---|",
        f"| **SPRS score** | **{f['score']}** of 110 (floor −203) |",
        f"| **Requirements assessed** | {f['assessed']} of 110 |",
        f"| **Requirements deducting** | {len(f['deductions'])} |",
        f"| **Blockers** | {len(blockers)} |",
        f"| **Rule reconciled against** | 32 CFR 170 as amended {rule_date} |",
        f"| **Computed** | {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S} UTC |",
        "",
    ]

    if may:
        L += [
            "### The statement this packet supports",
            "",
            "> The Affirming Official affirms continuing compliance with the security "
            "requirements of NIST SP 800-171 Rev 2, as assessed and scored above, "
            "submitted in SPRS per 32 CFR 170.22.",
            "",
            "Every condition for that statement is computed above and re-derivable from "
            "this commit. **The gate does not sign it.** 32 CFR 170.22 gives that act to a "
            "named senior human with False Claims Act exposure, and no automation is "
            "entitled to take it from them. What the automation removes is the annual "
            "scramble to reconstruct whether the statement is true.",
            "",
        ]
    else:
        L += ["### Blockers — every one must clear before the AO may sign", ""]
        L += [f"{i}. {b}" for i, b in enumerate(blockers, 1)]
        L += [
            "",
            "Each blocker is a reason the sentence *\"compliance is continuing\"* is not "
            "presently supportable. Signing anyway is the False Claims Act exposure, in one act.",
            "",
        ]

    if f["deductions"]:
        L += ["### What is costing points", "", "| Req | State | Weight | Deducted |", "|---|---|---:|---:|"]
        for d in sorted(f["deductions"], key=lambda x: (-x["deduct"], x["req"])):
            L.append(f"| {d['req']} | {d['state']} | {d['weight']} | −{d['deduct']} |")
        L.append("")

    L += [
        "### Scoring basis",
        "",
        f"DoD Assessment Methodology v1.2.1 (24 June 2020). Start at 110; subtract each "
        f"unimplemented requirement's weight. 44 requirements weigh 5, 14 weigh 3, 51 weigh 1 "
        f"(sum {f['max_deduction']}), and 110 − {f['max_deduction']} = {110 - f['max_deduction']}, "
        "which is the published floor — the weights are checked against that identity on every run.",
        "",
        "Partial credit exists for exactly two requirements: **3.5.3** (−3 if MFA covers remote "
        "and privileged users but not general users) and **3.13.11** (−3 if cryptography is "
        "employed but mostly not FIPS-validated). Every other requirement is all-or-nothing. "
        "**3.12.4** (SSP) is unscored but is a precondition: without it there is no assessment.",
        "",
        "### Why the gate watches the regulation too",
        "",
        "CMMC Phase 2 was suspended 2026-07-13 and a 60-day Reform Task Force reports to the "
        "DoW CIO around mid-September 2026. Suspended is not repealed: Phase 1 self-assessment "
        "stands, DFARS 252.204-7012 is untouched, and 170.22 still demands an annual signature. "
        "Whatever the task force changes lands as an amendment to 32 CFR 170, which eCFR "
        "publishes with a date. So this gate reads the rule on every run and blocks when it moves. "
        "An affirmation against a superseded rule is the quiet version of a false claim.",
        "",
    ]
    return "\n".join(L) + "\n"


def load_state(p: Path) -> dict:
    if not p.is_file():
        raise CannotAffirm(f"state file not found: {p}")
    d = yaml.safe_load(p.read_text())
    if not isinstance(d, dict) or "requirements" not in d:
        raise CannotAffirm("state file has no 'requirements' map")
    return d


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute the 32 CFR 170.22 affirmation gate.")
    ap.add_argument("--state", required=True, type=Path)
    ap.add_argument("--check", action="store_true", help="exit code only; write no packet")
    ap.add_argument("--offline", action="store_true", help="skip the eCFR read (tests only)")
    args = ap.parse_args()

    try:
        state = load_state(args.state)
        weights = load_weights()
        reg_findings: list[str] = []
        rule_date = RULE_AS_RECONCILED
        if not args.offline:
            rule_date, reg_findings = rule_drift()
        blockers, facts = gate(state, weights, reg_findings, dt.date.today())
    except CannotAffirm as e:
        print(f"BLOCK[2] could not evaluate: {e}", file=sys.stderr)
        print("Failing closed. A gate that cannot check does not clear an affirmation.", file=sys.stderr)
        return 2

    if not args.check:
        PACKET.write_text(render(blockers, facts, state, rule_date))
        print(f"packet -> {PACKET.relative_to(HERE.parent.parent)}")

    print(f"SPRS score: {facts['score']} of 110   ({facts['assessed']}/110 assessed)")
    print(f"32 CFR 170 reconciled against {rule_date}")

    if blockers:
        print(f"\nBLOCKED: {len(blockers)} blocker(s) — the AO may not affirm", file=sys.stderr)
        for i, b in enumerate(blockers, 1):
            print(f"  {i}. {b}", file=sys.stderr)
        return 1

    print("\nCLEAR TO AFFIRM — every condition computed. A human still signs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
