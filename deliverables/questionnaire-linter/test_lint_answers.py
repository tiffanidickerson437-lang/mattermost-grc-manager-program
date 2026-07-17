#!/usr/bin/env python3
"""Tests that the linter finds the planted defect and stays quiet on a clean bank.

The control test is the one that matters most here. This linter runs against a
document that is 96% "Yes" — if it fires on healthy answers it becomes noise
inside a week, and noise is how the original defect survived in the first place.

    python3 test_lint_answers.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from lint_answers import CannotLint, lint, normalize_answer, parse  # noqa: E402

RULES = yaml.safe_load((Path(__file__).resolve().parent / "polarity-rules.yaml").read_text())
R: list[tuple[bool, str]] = []


def check(name, cond, detail=""):
    R.append((cond, name if cond else f"{name} -- {detail}"))


def kinds(fs):
    return {f["kind"] for f in fs}


CLEAN = """### Governance
1. Are all system passwords encrypted using an industry standard algorithm?
   * Yes.
2. Do you maintain a quality management system (QMS) approved by management?
   * Yes.
3. Is all sensitive, protected health information (PHI) and personally identifiable information (PII) protected using an industry standard encryption algorithm where technically feasible?
   * Yes.
"""

# The real defect, reproduced from the published document.
DEFECT = CLEAN + """4. For all IT systems including but not limited to servers, routers, switches, firewalls, and databases, do privileged accounts (e.g., system or security administrator) that communicate directly with the internet, contain any personally identifiable information (PII) such as: social security numbers, credit card numbers, patient health record information, or other confidential records?
   * Yes
"""

FIXED = DEFECT.replace("? \n   * Yes", "?\n   * No").rsplit("* Yes", 1)[0] + "* No\n"

# == parsing ===============================================================
items = parse(DEFECT)
check("parses question/answer pairs", len(items) == 4, f"got {len(items)}")
check("captures the section header", items[0]["section"] == "Governance", items[0]["section"])
check("captures the answer", normalize_answer(items[3]["a"]) == "yes", items[3]["a"])

# == the control: healthy answers must be silent ===========================
f, _, _ = lint(parse(CLEAN), RULES)
check("a clean answer bank produces zero findings", f == [], f"got {f}")

# == the planted defect ====================================================
f, _, _ = lint(parse(DEFECT), RULES)
check("catches Yes on a negative-polarity question", "POLARITY" in kinds(f), f"got {kinds(f)}")
check("catches the PII-exposed vs PII-encrypted contradiction",
      "CONTRADICTION" in kinds(f), f"got {kinds(f)}")
check("names the rule that fired",
      any(x["rule"] == "NEG-PII-EXPOSURE" for x in f), f"got {[x['rule'] for x in f]}")

# == fixing the answer clears it ==========================================
f, _, _ = lint(parse(FIXED), RULES)
check("answering No clears the polarity finding", "POLARITY" not in kinds(f), f"got {f}")

# == 'Yes' in a run of Yes is not itself a finding ========================
# 96% of the real document is Yes. If a Yes streak triggered anything, every
# question would fire and the linter would be muted by lunchtime.
YES_RUN = "### Ops\n" + "".join(
    f"{i}. Are backups tested at least annually?\n   * Yes.\n" for i in range(1, 21)
)
f, _, facts = lint(parse(YES_RUN), RULES)
check("twenty consecutive Yes answers produce zero findings", f == [], f"got {f}")
check("yes_rate is computed", facts["yes_rate"] == 100, facts["yes_rate"])

# == unclassified is reported, never cleared ==============================
UNK = "### X\n1. Does your mascot enjoy long walks on the beach?\n   * Yes.\n"
f, unknown, facts = lint(parse(UNK), RULES)
check("an unclassifiable question is not a finding", f == [], f"got {f}")
check("an unclassifiable question IS surfaced as unknown", len(unknown) == 1, f"got {unknown}")
check("unknown is counted separately from positive",
      facts["polarity"]["unknown"] == 1 and facts["polarity"]["positive"] == 0, facts["polarity"])

# == fail closed ==========================================================
try:
    parse("no questions here, just prose")
    check("refuses a document with zero questions", False, "parsed anyway")
except CannotLint:
    check("refuses a document with zero questions", True)

# == other negative-polarity rules fire ===================================
for text, rid in [
    ("### S\n1. Are there any known unpatched vulnerabilities in production?\n   * Yes.\n",
     "NEG-KNOWN-WEAKNESS"),
    ("### S\n1. Are shared accounts used by administrators?\n   * Yes.\n",
     "NEG-KNOWN-WEAKNESS"),
]:
    f, _, _ = lint(parse(text), RULES)
    check(f"{rid} fires", any(x["rule"] == rid for x in f), f"got {[x['rule'] for x in f]}")


if __name__ == "__main__":
    passed = sum(1 for ok, _ in R if ok)
    for ok, name in R:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{passed}/{len(R)} tests passed")
    if passed != len(R):
        print("\nThe linter does not lint. Failing closed.", file=sys.stderr)
        sys.exit(1)
    print("Finds the planted defect; silent on a clean bank and on a Yes streak.")
