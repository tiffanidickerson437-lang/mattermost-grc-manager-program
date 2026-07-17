#!/usr/bin/env python3
"""Public claims consistency checker.

Scans page text for retired FedRAMP vocabulary and a few related
claims-consistency issues, then prints each hit with the corrected term and
the source line. It flags wording for a person to decide on. It never edits a
page, and it never decides whether Mattermost holds any federal status --
that is a question for the claim owner, not a regex.

Two ways to run it:

  Offline (default) -- scans the saved fixtures in ./fixtures, no network,
  no dependencies:
      python3 check_claims.py

  A saved file:
      python3 check_claims.py --file path/to/page.txt

  A live URL (needs `pip install requests`):
      python3 check_claims.py --url https://docs.mattermost.com/product-overview/faq-federal-procurement.html

Exit code is 0 by default, because the tool routes a human rather than
gating a pipeline. Pass --strict to exit 2 when there are findings, for
teams that want it in CI.

Background: FedRAMP notice NTC-0004 (published 25 February 2026,
https://www.fedramp.gov/notices/0004/) sets the single official label for a
FedRAMP authorization to "Certified", and replaces the Low / Moderate / High
baselines with Class A-D:
  Class B = current Low and Li-SaaS baselines
  Class C = current Moderate baseline
  Class D = current High baseline
The notice states FedRAMP will stop using "levels" or numbers for baseline
labels to avoid confusion with the DoD Impact Level (IL) system. Those
changes are carried in the FedRAMP Consolidated Rules for 2026 (CR26).
"""

import argparse
import os
import re
import sys

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

# Baseline -> current correct label under NTC-0004.
BASELINE_TO_CLASS = {
    "high": "Class D (High)",
    "moderate": "Class C (Moderate)",
    "low": "Class B (Low / Li-SaaS)",
    "li-saas": "Class B (Low / Li-SaaS)",
    "lisaas": "Class B (Low / Li-SaaS)",
}


def _class_for(baseline):
    return BASELINE_TO_CLASS.get(baseline.lower().replace(" ", ""), "the matching Class (A-D)")


# Each rule finds a span and explains it. `needs_fedramp` rules only fire when
# a FedRAMP token appears somewhere in the same document, because the term on
# its own (for example IL5) is correct in its own context.
RULES = [
    {
        "id": "FEDRAMP-BASELINE-AUTHORIZED",
        "label": "Retired FedRAMP baseline + 'authorized'",
        "pattern": re.compile(r"FedRAMP\s+(High|Moderate|Low|Li[- ]?SaaS)\s+authoriz\w*", re.I),
        "explain": lambda m: (
            "'{found}' uses two retired terms. Under NTC-0004 the baseline is "
            "'{cls}' and the status word is 'Certified'. Suggested: "
            "'FedRAMP {cls} Certified'. Keep any 'via partner FedHIVE' wording -- "
            "that is the correct inherited-package framing and should not be dropped."
        ).format(found=m.group(0), cls=_class_for(m.group(1))),
        "needs_fedramp": False,
    },
    {
        "id": "FEDRAMP-AUTHORIZED-WORD",
        "label": "'Authorized' where 'Certified' is now correct",
        "pattern": re.compile(r"FedRAMP[\w /(),-]{0,40}?authoriz(?:ed|ation)", re.I),
        "explain": lambda m: (
            "'{found}' -- under NTC-0004 the current term is 'Certified' / "
            "'Certification'. 'Authorized' / 'Authorization' is legacy FedRAMP "
            "wording carried over from before CR26."
        ).format(found=m.group(0).strip()),
        "needs_fedramp": False,
    },
    {
        "id": "IL-FEDRAMP-COLLISION",
        "label": "DoD Impact Level next to a FedRAMP claim",
        "pattern": re.compile(r"\bIL\s?[2-6]\b|\bImpact Level\b", re.I),
        "explain": lambda m: (
            "DoD Impact Level terms (IL4/IL5/IL6, Impact Level) are correct on "
            "their own -- do not change them. This line is flagged only because a "
            "FedRAMP claim appears on the same page. NTC-0004 renamed FedRAMP "
            "baselines specifically to stop readers conflating a FedRAMP baseline "
            "with a DoD Impact Level. Label the DoD usage clearly (for example "
            "'DoD IL4/IL5/IL6') and keep it separate from the FedRAMP Class statement."
        ),
        "needs_fedramp": True,
    },
    {
        "id": "ISO-ALIGNMENT-UNDERSTATEMENT",
        "label": "ISO 27001 described as 'alignment'",
        "pattern": re.compile(r"ISO\s*/?\s*(?:IEC\s*)?27001[\w ,]{0,80}?alignment", re.I),
        "explain": lambda m: (
            "'{found}' describes ISO 27001 as alignment. The trust center "
            "(https://trust.mattermost.com/) lists a current ISO/IEC 27001:2022 "
            "certificate, so this understates a certification the company holds. "
            "Suggested: 'certified to ISO/IEC 27001:2022'."
        ).format(found=m.group(0).strip()),
        "needs_fedramp": False,
    },
    {
        "id": "ATO-STATUS-RECONCILE",
        "label": "DoD authorization status stated two ways",
        "pattern": re.compile(r"in the process of acquiring Authority to Operate", re.I),
        "explain": lambda m: (
            "'{found}' states there is no DoD authorization yet. The U.S. Federal "
            "Procurement FAQ instead states 'Mattermost has received a Certificate "
            "to Field under Platform One's Continuous Authority to Operate (CATO).' "
            "A federal reader can land on either page and reach the opposite "
            "conclusion. Reconcile so both pages say the same thing. The exact "
            "scope of any standalone ATO / CON is an owner question, not something "
            "this tool resolves."
        ).format(found=m.group(0).strip()),
        "needs_fedramp": False,
    },
]

FEDRAMP_TOKEN = re.compile(r"fedramp", re.I)


class Finding:
    def __init__(self, rule, line_no, line_text, message):
        self.rule = rule
        self.line_no = line_no
        self.line_text = line_text
        self.message = message


def scan(text, source_label):
    """Return a list of Finding objects for one document."""
    fedramp_present = bool(FEDRAMP_TOKEN.search(text))
    lines = text.splitlines()
    # map absolute char offset -> line number
    findings = []
    seen_spans = []          # (start, end) already reported, to dedupe overlaps
    seen_rule_line = set()   # (rule_id, line_no), so a rule reports once per line

    for rule in RULES:
        if rule["needs_fedramp"] and not fedramp_present:
            continue
        for m in rule["pattern"].finditer(text):
            span = (m.start(), m.end())
            if any(s <= span[0] < e for s, e in seen_spans):
                continue  # already covered by an earlier, more specific rule
            line_no = text.count("\n", 0, m.start()) + 1
            key = (rule["id"], line_no)
            if key in seen_rule_line:
                continue  # same rule already fired on this line; don't repeat
            seen_spans.append(span)
            seen_rule_line.add(key)
            line_text = lines[line_no - 1].strip() if line_no - 1 < len(lines) else ""
            findings.append(Finding(rule, line_no, line_text, rule["explain"](m)))
    findings.sort(key=lambda f: f.line_no)
    return findings


def read_source(args):
    """Yield (label, text) pairs for whatever the caller asked to scan."""
    if args.url:
        try:
            import requests  # noqa: local import so offline mode needs no deps
        except ImportError:
            sys.exit("--url mode needs the requests library. Run: pip install requests")
        resp = requests.get(args.url, timeout=30, headers={"User-Agent": "claims-checker/1.0"})
        resp.raise_for_status()
        raw = resp.text
        # crude tag strip so the checker sees page text, not markup
        raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", " ", raw)
        raw = re.sub(r"[ \t]+", " ", raw)
        yield args.url, raw
        return
    if args.file:
        with open(args.file, encoding="utf-8", errors="ignore") as fh:
            yield args.file, fh.read()
        return
    # default: the saved fixtures
    if not os.path.isdir(FIXTURES_DIR):
        sys.exit("No fixtures directory found next to this script, and no --file/--url given.")
    names = sorted(n for n in os.listdir(FIXTURES_DIR) if n.endswith(".txt"))
    if not names:
        sys.exit("No .txt fixtures found in {}".format(FIXTURES_DIR))
    for name in names:
        path = os.path.join(FIXTURES_DIR, name)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            yield path, fh.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", help="Scan a saved text or HTML file.")
    parser.add_argument("--url", help="Fetch and scan a live URL (needs requests).")
    parser.add_argument("--strict", action="store_true", help="Exit 2 if any findings (for CI). Default exit is 0.")
    args = parser.parse_args()

    total = 0
    print("Public claims consistency check")
    print("This tool routes findings to a person. It does not edit pages and does")
    print("not decide Mattermost's federal status.\n")

    for label, text in read_source(args):
        findings = scan(text, label)
        print("=" * 78)
        print("SOURCE: {}".format(label))
        if not findings:
            print("  No retired vocabulary or flagged wording found.\n")
            continue
        print("  {} item(s) for review:\n".format(len(findings)))
        for f in findings:
            total += 1
            print("  [{}] line {}".format(f.rule["id"], f.line_no))
            print("      rule : {}".format(f.rule["label"]))
            if f.line_text:
                print("      text : {}".format(f.line_text))
            # wrap the message for readability, indent continuation lines
            wrapped = _wrap(f.message, 70)
            for i, chunk in enumerate(wrapped):
                prefix = "      note : " if i == 0 else "             "
                print(prefix + chunk)
            print("      -> REVIEW REQUIRED. A human decides the final wording.\n")

    print("=" * 78)
    print("Total items for review: {}".format(total))
    if total and args.strict:
        sys.exit(2)


def _wrap(text, width):
    words, line = text.split(), ""
    out = []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    main()
