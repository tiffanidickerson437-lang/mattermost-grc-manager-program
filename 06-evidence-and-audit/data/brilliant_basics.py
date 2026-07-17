#!/usr/bin/env python3
"""
Brilliant at the Basics -> 800-171 reachability check.

Answers one question the SPRS score cannot: of the ten IT practices the DoW CIO
publishes for the Defense Industrial Base, how many can the 800-171 lens even
see?

The check RESOLVES controls through nist-800-171-rev2-mapping.yaml rather than
restating them, so this view and the assessment workbook cannot disagree about
which control carries which requirement. If they ever do, that is a bug in one
file, not a difference of opinion between two.

Fails closed:
  - a practice citing a requirement ID absent from 800-171      -> exit 1
  - a practice declaring an unreachable control not in scope    -> exit 1
  - a practice whose cited requirements resolve to no controls  -> exit 1
  - an unreachable control that 800-171 CAN in fact reach       -> exit 1

That last one is the guard that matters. It is what stops the headline finding
from rotting into a lie if a future mapping edit gives 800-171 a route to AAT-01.
The claim is only allowed to stand while it is still true.

Usage:
    python3 06-evidence-and-audit/data/brilliant_basics.py            # report to stdout
    python3 06-evidence-and-audit/data/brilliant_basics.py --render   # write the .md
"""

import sys
import pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent

MAP = HERE / "brilliant-basics-map.yaml"
NIST = HERE / "nist-800-171-rev2-mapping.yaml"
SCOPE = REPO / "generated" / "in-scope-controls.yaml"
OUT = REPO / "frameworks" / "brilliant-basics-map.md"


class Fail(Exception):
    """Any condition that must block. Never warn where you can fail."""


def load(path):
    if not path.exists():
        raise Fail(f"missing required input: {path}")
    with open(path) as fh:
        return yaml.safe_load(fh)


def build_index(nist):
    """requirement id -> (controls, anchor, family name). Flattened once."""
    idx = {}
    for fam in nist.get("families", []):
        for req in fam.get("requirements", []):
            idx[str(req["id"])] = {
                "controls": list(req.get("controls", [])),
                "anchor": req.get("anchor", ""),
                "family": fam.get("name", ""),
            }
    return idx


def in_scope_ids(scope):
    return {c["id"] for c in scope.get("in_scope_controls", [])}


def scope_titles(scope):
    return {c["id"]: c.get("title", "") for c in scope.get("in_scope_controls", [])}


def resolve(bb, nist, scope):
    """Resolve every practice. Raises Fail on any inconsistency."""
    idx = build_index(nist)
    scoped = in_scope_ids(scope)

    # Every control 800-171 can reach, anywhere in the mapping.
    reachable_anywhere = set()
    for meta in idx.values():
        reachable_anywhere.update(meta["controls"])

    rows = []
    for p in bb.get("practices", []):
        reqs = [str(r) for r in (p.get("reqs") or [])]
        unreachable = list(p.get("unreachable_controls") or [])

        for rid in reqs:
            if rid not in idx:
                raise Fail(
                    f"practice {p['num']} cites 800-171 {rid}, which does not "
                    f"exist in {NIST.name}. A map that can cite a phantom "
                    f"requirement can conceal a real gap."
                )

        controls = []
        for rid in reqs:
            for c in idx[rid]["controls"]:
                if c not in controls:
                    controls.append(c)

        if reqs and not controls:
            raise Fail(
                f"practice {p['num']} cites {reqs} but they resolve to zero "
                f"controls. A requirement that carries no control is not "
                f"coverage."
            )

        for c in unreachable:
            if c not in scoped:
                raise Fail(
                    f"practice {p['num']} declares unreachable control {c}, "
                    f"which is not in scope for this company. The gap claim "
                    f"only means something if the control is real and selected."
                )
            if c in reachable_anywhere:
                raise Fail(
                    f"practice {p['num']} claims {c} is unreachable from "
                    f"800-171, but the mapping resolves it. The finding is "
                    f"stale — fix the claim, not the test."
                )

        rows.append(
            {
                "num": p["num"],
                "name": p["name"],
                "dow_says": (p.get("dow_says") or "").strip(),
                "reqs": reqs,
                "controls": controls,
                "unreachable": unreachable,
                "gap_class": p.get("gap_class"),
                "note": (p.get("note") or "").strip(),
                "anchors": [idx[r]["anchor"] for r in reqs],
            }
        )
    return rows


def summarize(rows):
    reachable = [r for r in rows if r["reqs"]]
    blind = [r for r in rows if r["gap_class"] == "framework-blind-spot"]
    not_control = [r for r in rows if r["gap_class"] == "not-a-control"]
    return {
        "total": len(rows),
        "reachable": len(reachable),
        "blind_spots": blind,
        "not_controls": not_control,
    }


def report(rows, s):
    print()
    print(f"{s['total']} DoW CIO IT practices · {s['reachable']} reachable "
          f"from NIST 800-171 Rev 2 · {len(s['blind_spots'])} framework "
          f"blind spot(s) · {len(s['not_controls'])} not-a-control")
    print()
    for r in rows:
        if r["reqs"]:
            print(f"  [{r['num']}] {r['name'][:52]:54} <- {', '.join(r['reqs'])}")
        else:
            tag = "BLIND SPOT" if r["gap_class"] == "framework-blind-spot" else "not a control"
            extra = f" -> {', '.join(r['unreachable'])}" if r["unreachable"] else ""
            print(f"  [{r['num']}] {r['name'][:52]:54} <- ({tag}){extra}")
    print()
    for b in s["blind_spots"]:
        print(f"  Practice {b['num']}: no 800-171 requirement reaches "
              f"{', '.join(b['unreachable'])}.")
        print(f"  A perfect 110 SPRS score proves nothing about it.")
    print()


def render(rows, s, titles):
    L = []
    A = L.append
    A("# Brilliant at the Basics, mapped\n")
    A("> Generated by `06-evidence-and-audit/data/brilliant_basics.py` from")
    A("> `brilliant-basics-map.yaml`. Controls are resolved through")
    A("> `nist-800-171-rev2-mapping.yaml`, never restated here.\n")
    A("On 13 July 2026 the DoW CIO suspended CMMC Phase II. The same office")
    A("publishes **[Brilliant at the Basics](https://dowcio.war.gov/BrilliantBasics/)**")
    A("— a Top 10 of IT practices it tells the Defense Industrial Base to")
    A("actually do, framed explicitly as stripping away *\"administrative")
    A("complexity and compliance overhead.\"*\n")
    A("It is not a framework. It carries no assessment, appears in no contract")
    A("clause, and nobody will ever audit against it. It is something more")
    A("useful: the clearest public statement of what the customer thinks good")
    A("looks like — published by the office that just took the credential away.\n")
    A("So it is worth asking what the enforced baseline can see of it.\n")
    A("---\n")
    A(f"## {s['reachable']} of {s['total']} reachable\n")
    A("| # | Practice | 800-171 Rev 2 | Resolves to |")
    A("|---|---|---|---|")
    for r in rows:
        if r["reqs"]:
            reqs = ", ".join(f"`{x}`" for x in r["reqs"])
            ctrls = ", ".join(f"`{c}`" for c in r["controls"])
        else:
            reqs = "**— none —**"
            ctrls = (", ".join(f"`{c}`" for c in r["unreachable"])
                     + " *(in scope, unreachable)*") if r["unreachable"] else "*n/a*"
        A(f"| {r['num']} | {r['name']} | {reqs} | {ctrls} |")
    A("")
    for b in s["blind_spots"]:
        A("---\n")
        A(f"## The finding — practice {b['num']}: {b['name']}\n")
        A("> " + b["dow_says"].replace("\n", "\n> ") + "\n")
        A("**NIST SP 800-171 Rev 2 contains no artificial-intelligence")
        A("requirement.** Not a weak one — none. Rev 2 was published in")
        A("February 2020; its 110 requirements predate the workforce LLM")
        A("entirely, and Rev 3 does not add one either.\n")
        A("So a contractor can score a perfect **110** in SPRS, sign the")
        A("[32 CFR 170.22](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.22)")
        A("affirmation under False Claims Act liability, and be wholly")
        A("non-conformant with a practice the same CIO office publishes as a")
        A("Top 10 basic for the DIB.\n")
        A("The score is not wrong. **The lens has a blind spot, and the")
        A("credential cannot see through it.**\n")
        for c in b["unreachable"]:
            A(f"- `{c}` — {titles.get(c, '')}")
        A("")
        A("Both are already among Mattermost's 45 in-scope controls, fired by")
        A("`ai-products: true` in the config, satisfying NIST AI RMF 1.0 and")
        A("ISO/IEC 42001:2023. **The control set can see this practice. The")
        A("800-171 view of that same control set cannot.**\n")
        A("That is the argument for one control set rendered into many")
        A("frameworks — made by the customer's own CIO, not by me.\n")
        A("It also lands exactly on [finding 03](../00-governance/README.md#03--no-internal-ai-policy-while-publishing-ai-risk-guidance-for-other-people):")
        A("Mattermost publishes AI risk guidance for other organizations' CISOs")
        A("and has no published internal AI policy of its own — while selling")
        A("sovereign AI to the department that just published this list.\n")
    A("---\n")
    A("## Reachable is not the same as covered\n")
    A("Three practices resolve to a requirement that is materially weaker than")
    A("the practice itself. Counting them as clean would be the fail-open")
    A("defect this repo exists to catch.\n")
    for r in rows:
        if r["reqs"] and ("thin" in r["note"].lower() or "not equivalent" in r["note"].lower()
                          or "barely" in r["note"].lower()):
            A(f"**{r['num']} — {r['name']}**\n")
            A(r["note"] + "\n")
    A("---\n")
    A("## What this is not\n")
    A("This computes **reachability**, not conformance. Nothing here asserts")
    A("Mattermost's implementation state of any practice — that is knowable")
    A("only on day one, inside the boundary, from systems of record. Whether")
    A("the 800-171 lens can see a practice at all is knowable from public")
    A("documents, and that is the only thing computed here.\n")
    A("The OT Top 10 is deliberately unmapped: Mattermost has no operational")
    A("technology in its boundary, and mapping it would manufacture ten")
    A("findings out of nothing.\n")
    OUT.write_text("\n".join(L))
    return OUT


def main():
    try:
        bb = load(MAP)
        nist = load(NIST)
        scope = load(SCOPE)
        rows = resolve(bb, nist, scope)
    except Fail as e:
        print(f"\nBLOCKED: {e}\n", file=sys.stderr)
        return 1

    s = summarize(rows)
    report(rows, s)

    if "--render" in sys.argv:
        p = render(rows, s, scope_titles(scope))
        print(f"rendered -> {p}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
