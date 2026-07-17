#!/usr/bin/env python3
"""Tests that the affirmation gate actually blocks.

A gate nobody attacks is a gate that can be quietly gutted to `return []` and
will clear every affirmation forever after. That is not a hypothetical: the
first adversarial pass on the sibling drift checker did exactly that, and the
live run still printed a clean receipt and exited 0.

So these are mutation tests. Each hands the scorer or the gate an input with a
planted defect and asserts the defect is caught. Gut score() or gate() and this
suite goes red, which fails CI. The gate does not get an exemption from the
program's own rule.

Two of these are arithmetic identities from the DoD Assessment Methodology
v1.2.1 rather than opinions: everything implemented is exactly 110, and nothing
implemented is exactly -203. If the weights are ever wrong, those two break.

    python3 04-evidence-and-audit/data/test_affirmation_gate.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from affirmation_gate import (  # noqa: E402
    PRECONDITION,
    CannotAffirm,
    gate,
    load_weights,
    score,
)

W = load_weights()
ALL_REQS = sorted(W)
TODAY = dt.date(2026, 7, 17)

R: list[tuple[bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    R.append((cond, name if cond else f"{name} -- {detail}"))


def st(**overrides) -> dict[str, str]:
    s = {r: "implemented" for r in ALL_REQS}
    s.update(overrides)
    return s


def blockers_for(state_reqs, poam=None, reg=None):
    return gate({"requirements": state_reqs, "poam": poam or []}, W, reg or [], TODAY)[0]


# == the two arithmetic identities ==========================================
# These are the methodology, not a preference. If either breaks, the weights
# file is wrong and every score derived from it is wrong.

s, _ = score(st(), W)
check("everything implemented scores exactly 110", s == 110, f"got {s}")

s, _ = score({r: "not_implemented" for r in ALL_REQS}, W)
check("nothing implemented scores exactly -203 (published floor)", s == -203, f"got {s}")

# == partial credit: exactly two requirements, no more ======================

s, _ = score(st(**{"3.5.3": "partial"}), W)
check("3.5.3 partial deducts 3, not 5", s == 107, f"got {s}")

s, _ = score(st(**{"3.13.11": "partial"}), W)
check("3.13.11 partial deducts 3, not 5", s == 107, f"got {s}")

s, _ = score(st(**{"3.5.3": "not_implemented"}), W)
check("3.5.3 absent deducts the full 5", s == 105, f"got {s}")

try:
    score(st(**{"3.1.1": "partial"}), W)
    check("partial credit is refused for any other requirement", False, "3.1.1 partial was accepted")
except CannotAffirm:
    check("partial credit is refused for any other requirement", True)

# == the SSP precondition ===================================================

b = blockers_for(st(**{PRECONDITION: "not_implemented"}))
check("absent SSP blocks the affirmation entirely", any("170.22" in x for x in b), f"got {b}")

s, _ = score(st(**{PRECONDITION: "not_implemented"}), W)
check("absent SSP costs 0 points (unscored, but a stop)", s == 110, f"got {s}")

# == fail closed ============================================================

b = blockers_for(st(**{"3.1.1": "unknown"}))
check("an unknown requirement blocks the affirmation", any("unknown" in x for x in b), f"got {b}")

try:
    partial_state = {r: "implemented" for r in ALL_REQS[:-1]}
    score(partial_state, W)
    check("a requirement missing from state is refused", False, "silently accepted")
except CannotAffirm:
    check("a requirement missing from state is refused", True)

try:
    score(st(**{"3.1.1": "probably_fine"}), W)
    check("an unrecognized state string is refused", False, "silently accepted")
except CannotAffirm:
    check("an unrecognized state string is refused", True)

# == POA&M window ===========================================================

fresh = [{"req": "3.3.5", "opened": "2026-04-01"}]  # 107 days at TODAY
b = blockers_for(st(), poam=fresh)
check("a POA&M inside 180 days does not block", b == [], f"got {b}")

stale = [{"req": "3.3.5", "opened": "2025-11-01"}]  # 258 days at TODAY
b = blockers_for(st(), poam=stale)
check("a POA&M past 180 days blocks", any("180-day" in x for x in b), f"got {b}")

# == the regulation itself ==================================================

b = blockers_for(st(), reg=["32 CFR 170.22 (Affirmation) amended 2026-09-30; this repo reconciled against 2024-12-16."])
check("a rule amendment blocks the affirmation", len(b) == 1 and "amended" in b[0], f"got {b}")

# == the control: a clean program clears ====================================
# If this fails the gate cries wolf, and a gate that always blocks gets ignored
# exactly as fast as one that never does.

b = blockers_for(st())
check("a clean program with no drift clears", b == [], f"got {b}")


if __name__ == "__main__":
    passed = sum(1 for ok, _ in R if ok)
    for ok, name in R:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{passed}/{len(R)} mutation tests passed")
    if passed != len(R):
        print("\nThe affirmation gate does not gate. Failing closed.", file=sys.stderr)
        sys.exit(1)
    print("The gate blocks what it should and clears what it should.")
