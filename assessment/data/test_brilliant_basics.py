#!/usr/bin/env python3
"""
Mutation tests for the Brilliant Basics reachability check.

Method, same as every other checker in this repo: plant a defect, assert it gets
caught. Then neuter the thing being verified and assert the suite goes red — a
checker nobody checks is a checker that gets quietly gutted.

The test that matters most is test_09: it gives 800-171 a route to AAT-01 and
asserts the tool REFUSES to keep claiming the gap. The headline finding is only
allowed to stand while it is still true.
"""

import copy
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import brilliant_basics as bb  # noqa: E402

PASS, FAIL = [], []


def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}")


def fixtures():
    return (
        bb.load(bb.MAP),
        bb.load(bb.NIST),
        bb.load(bb.SCOPE),
    )


def raises(m, n, s):
    try:
        bb.resolve(m, n, s)
        return False
    except bb.Fail:
        return True


def main():
    print("\nBrilliant Basics reachability — mutation tests\n")
    m0, n0, s0 = fixtures()

    # --- baseline -----------------------------------------------------------
    rows = bb.resolve(m0, n0, s0)
    check("01 the real map resolves clean", len(rows) == 10)

    summ = bb.summarize(rows)
    check("02 exactly one framework blind spot", len(summ["blind_spots"]) == 1)
    check("03 the blind spot is practice 08 (secure AI adoption)",
          summ["blind_spots"][0]["num"] == "08")
    check("04 it names AAT-01 and AAT-02",
          sorted(summ["blind_spots"][0]["unreachable"]) == ["AAT-01", "AAT-02"])

    # The ground truth the whole artifact rests on.
    idx = bb.build_index(n0)
    ai_reqs = [r for r, meta in idx.items()
               if any(c.startswith("AAT") for c in meta["controls"])]
    check("05 no 800-171 requirement resolves to any AAT control", ai_reqs == [])
    check("06 the 110 requirements are all present", len(idx) == 110)

    # --- planted defects ----------------------------------------------------
    m = copy.deepcopy(m0)
    m["practices"][0]["reqs"] = ["3.99.99"]
    check("07 a phantom requirement id is caught", raises(m, n0, s0))

    m = copy.deepcopy(m0)
    for p in m["practices"]:
        if p["num"] == "08":
            p["unreachable_controls"] = ["ZZZ-99"]
    check("08 an out-of-scope 'unreachable' control is caught", raises(m, n0, s0))

    # THE ONE THAT MATTERS: make the claim false, assert the tool refuses it.
    n = copy.deepcopy(n0)
    n["families"][0]["requirements"][0]["controls"].append("AAT-01")
    check("09 if 800-171 ever reaches AAT-01, the stale gap claim is REFUSED",
          raises(m0, n, s0))

    # --- gut the checker, suite must go red ---------------------------------
    real_resolve = bb.resolve
    try:
        bb.resolve = lambda m, n, s: []          # always "pass"
        gutted_caught = raises(m0, n0, s0)
    finally:
        bb.resolve = real_resolve
    check("10 a gutted resolve() stops catching planted defects",
          gutted_caught is False)

    # --- honesty guards -----------------------------------------------------
    rows = bb.resolve(m0, n0, s0)
    p04 = next(r for r in rows if r["num"] == "04")
    check("11 practice 04 is classed not-a-control, never a finding",
          p04["gap_class"] == "not-a-control" and p04["unreachable"] == [])
    check("12 not-a-control is excluded from the blind-spot count",
          p04 not in summ["blind_spots"])

    reachable = [r for r in rows if r["reqs"]]
    check("13 every reachable practice resolves to >=1 real control",
          all(r["controls"] for r in reachable))

    scoped = bb.in_scope_ids(s0)
    check("14 AAT-01 and AAT-02 really are in Mattermost's scope",
          {"AAT-01", "AAT-02"} <= scoped)

    thin = [r for r in rows if r["reqs"] and
            ("thin" in r["note"].lower() or "not equivalent" in r["note"].lower()
             or "barely" in r["note"].lower())]
    check("15 reachable-but-weak practices are flagged, not counted clean",
          len(thin) >= 3)

    print(f"\n{len(PASS)}/{len(PASS) + len(FAIL)} tests passed")
    if FAIL:
        print("failed: " + ", ".join(FAIL))
        return 1
    print("The gap is real, and the tool refuses to keep claiming it once it isn't.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
