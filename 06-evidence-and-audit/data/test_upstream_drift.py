#!/usr/bin/env python3
"""Tests that the drift checker actually detects drift.

Why this file exists, plainly: a checker nobody checks is a checker that can be
quietly gutted to `return []` and will report "reconciled" forever after. The
first adversarial pass on this tool did exactly that -- neutered the comparison
so it always passed -- and the live run still exited 0 and printed a clean
receipt. Nothing noticed. That is the same defect class the whole program is
built against, so the checker does not get an exemption from its own rule.

These tests are mutation tests. Each one hands compare() an upstream/mapping
pair with a known planted defect and asserts the defect is reported. Gut
compare() and every test here fails, which fails CI, which is the point.

    python3 06-evidence-and-audit/data/test_upstream_drift.py     # standalone, no pytest needed
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from upstream_drift import compare  # noqa: E402

VERSION = "2026.07.14.01"

# A miniature stand-in for the real ruleset. Small enough to reason about,
# same shape as the real thing.
UPSTREAM = {
    "Cybersecurity Education": ["KSI-CED-RAT"],
    "Change Management": ["KSI-CMT-LMC", "KSI-CMT-RMV"],
    "Supply Chain Risk": ["KSI-SCR-MIT", "KSI-SCR-MON"],
}

RESULTS: list[tuple[bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    RESULTS.append((cond, name if cond else f"{name} -- {detail}"))


def only(findings: list[str], token: str) -> bool:
    return any(token in f for f in findings)


# -- control: identical inputs must produce no findings ----------------------
# If this fails, the checker cries wolf and nobody will trust the green ones.
f = compare(VERSION, UPSTREAM, dict(UPSTREAM), VERSION)
check("clean input reports no drift", f == [], f"got {f}")

# -- mutation 1: upstream adds a KSI this repo has not mapped ----------------
up = {**UPSTREAM, "Change Management": ["KSI-CMT-LMC", "KSI-CMT-RMV", "KSI-CMT-NEW"]}
f = compare(VERSION, up, dict(UPSTREAM), VERSION)
check("detects a KSI added upstream", only(f, "ADDED") and only(f, "KSI-CMT-NEW"), f"got {f}")

# -- mutation 2: this repo claims a KSI upstream does not publish ------------
mine = {**UPSTREAM, "Supply Chain Risk": ["KSI-SCR-MIT", "KSI-SCR-MON", "KSI-SCR-GHOST"]}
f = compare(VERSION, UPSTREAM, mine, VERSION)
check("detects a phantom KSI in the mapping", only(f, "KSI-SCR-GHOST"), f"got {f}")

# -- mutation 3: upstream retires a KSI still mapped here --------------------
up = {**UPSTREAM, "Supply Chain Risk": ["KSI-SCR-MIT"]}
f = compare(VERSION, up, dict(UPSTREAM), VERSION)
check("detects a KSI retired upstream", only(f, "KSI-SCR-MON"), f"got {f}")

# -- mutation 4: version moved, contents identical (the silent one) ----------
# The dangerous case: FedRAMP revises wording or scope without changing any id.
# Ids reconcile perfectly and the mapping is still stale.
f = compare("2026.09.01.01", UPSTREAM, dict(UPSTREAM), VERSION)
check("detects a version bump even when every id still matches", only(f, "VERSION"), f"got {f}")

# -- mutation 5: a whole category disappears from the mapping ----------------
mine = {k: v for k, v in UPSTREAM.items() if k != "Change Management"}
f = compare(VERSION, UPSTREAM, mine, VERSION)
check("detects a dropped category", only(f, "CATEGORY"), f"got {f}")

# -- mutation 6: count mismatch inside a category ----------------------------
mine = {**UPSTREAM, "Change Management": ["KSI-CMT-LMC"]}
f = compare(VERSION, UPSTREAM, mine, VERSION)
check("detects a per-category count mismatch", only(f, "KSI-CMT-RMV"), f"got {f}")

# -- mutation 7: empty mapping must not read as agreement -------------------
# The fail-open trap: zero mapped entries compared against a real upstream
# must be loud, not silent.
f = compare(VERSION, UPSTREAM, {}, VERSION)
check("an empty mapping is drift, not agreement", len(f) > 0, f"got {f}")

# -- mutation 8: empty upstream must not read as agreement ------------------
f = compare(VERSION, {}, dict(UPSTREAM), VERSION)
check("an empty upstream is drift, not agreement", len(f) > 0, f"got {f}")


if __name__ == "__main__":
    passed = sum(1 for ok, _ in RESULTS if ok)
    for ok, name in RESULTS:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{passed}/{len(RESULTS)} mutation tests passed")
    if passed != len(RESULTS):
        print("\nThe drift checker does not detect drift. Failing closed.", file=sys.stderr)
        sys.exit(1)
    print("The drift checker detects drift. Gut compare() and this suite goes red.")
