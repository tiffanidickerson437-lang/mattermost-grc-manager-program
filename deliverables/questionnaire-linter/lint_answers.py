#!/usr/bin/env python3
"""Semantic-consistency linter for a published questionnaire answer bank.

THE PROBLEM, FROM THE RESEARCH

Mattermost publishes its customer-questionnaire answer bank in the open, at
handbook.mattermost.com/operations/operations/company-policies/security-policies
— nine sections, about 80 questions, served as clean markdown. It is genuinely good
written material and it is the richest public GRC artifact they have.

Nearly every answer is "Yes." And a reviewer's eye slides down a column of Yes.

Buried in that column, under ### Governance, question 8 asks whether
internet-facing privileged accounts contain PII, SSNs, or patient health
records. The published answer is "Yes." It is a question where Yes is an
admission, sitting in a run of questions where Yes is the good answer. It is
almost certainly a copy-paste error — which is exactly why it matters: it is
the class of defect that survives because nobody reads a Yes column closely,
and because that file has no CODEOWNER and no merge gate.

It also contradicts question 9 on the same page, which says all PII and PHI is
protected by industry-standard encryption.

WHAT THIS DOES

Routes a human to every question where "Yes" would be a disclosure, and to every
pair of answers that cannot both be comfortable. It does not decide. Polarity is
a judgment about what a question means, and the rules it follows are committed
in polarity-rules.yaml so the person who owns the answer can read, argue with,
and change them.

WHY IT IS A DELIVERABLE AND NOT A CRITIQUE

The posting's fourth success metric is "customer security questionnaires and
trust center content maintained to unblock deal cycles." Questionnaires block
revenue. An answer bank with a polarity inversion in it does not block revenue
loudly — it blocks it quietly, one security reviewer at a time, and nobody
attributes the slow deal to line 87 of a markdown file. This runs in CI in about
a second.

FAILURE MODE: CLOSED. Unfetchable source, unparseable document, zero questions
extracted, unreadable rules: all exit 2. A linter that cannot read the document
does not report it clean.

    python3 lint_answers.py --url <handbook .md url>
    python3 lint_answers.py --file answers.md --check
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL[2]: pyyaml missing. Cannot read the rules, so cannot lint.", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
RULES = HERE / "polarity-rules.yaml"

DEFAULT_URL = (
    "https://handbook.mattermost.com/operations/operations/"
    "company-policies/security-policies.md"
)


class CannotLint(Exception):
    """The linter could not run. Always exit 2. Never a pass."""


# ------------------------------------------------------------------- parse --
QUESTION = re.compile(r"^\s*(\d+)\.\s+(.*?)\s*$")
ANSWER = re.compile(r"^\s*\*\s+(.*?)\s*$")
SECTION = re.compile(r"^#{2,4}\s+(.*?)\s*$")


def parse(md: str) -> list[dict]:
    """Extract (section, number, question, answer) from the published markdown."""
    items, section, pending = [], "(none)", None
    for line in md.splitlines():
        if m := SECTION.match(line):
            section, pending = m.group(1).strip(), None
            continue
        if m := QUESTION.match(line):
            pending = {"section": section, "n": int(m.group(1)), "q": m.group(2), "a": None}
            items.append(pending)
            continue
        if pending and pending["a"] is None and (m := ANSWER.match(line)):
            pending["a"] = m.group(1)
            pending = None
    if not items:
        raise CannotLint("parsed zero questions -- broken parse, not an empty document")
    return items


def normalize_answer(a: str | None) -> str:
    if not a:
        return "none"
    t = a.strip().lower().rstrip(".")
    if t in ("yes", "yes.") or t.startswith("yes"):
        return "yes"
    if t in ("no", "no.") or t.startswith("no "):
        return "no"
    if t.startswith("n/a") or t.startswith("not applicable"):
        return "n/a"
    return "prose"


# ------------------------------------------------------------------ rules ---
def matches(rule: dict, q: str) -> bool:
    ql = q.lower()
    for pat in rule.get("all_of", []):
        if not re.search(pat, ql, re.I):
            return False
    any_of = rule.get("any_of", [])
    if any_of and not any(re.search(p, ql, re.I) for p in any_of):
        return False
    return bool(rule.get("all_of") or any_of)


def classify(item: dict, rules: dict) -> tuple[str, str | None, str | None]:
    for r in rules.get("negative_polarity", []):
        if matches(r, item["q"]):
            return "negative", r["id"], r.get("why")
    for r in rules.get("positive_polarity", []):
        if matches(r, item["q"]):
            return "positive", r["id"], None
    return "unknown", None, None


def lint(items: list[dict], rules: dict) -> tuple[list[dict], list[dict], dict]:
    """Pure. Returns (findings, review_queue, facts)."""
    findings, unknown = [], []
    counts = {"yes": 0, "no": 0, "prose": 0, "n/a": 0, "none": 0}
    pol_counts = {"negative": 0, "positive": 0, "unknown": 0}

    for it in items:
        ans = normalize_answer(it["a"])
        counts[ans] = counts.get(ans, 0) + 1
        pol, rid, why = classify(it, rules)
        pol_counts[pol] += 1
        it["_pol"], it["_ans"] = pol, ans

        if pol == "negative" and ans == "yes":
            findings.append({
                "kind": "POLARITY",
                "section": it["section"], "n": it["n"], "rule": rid,
                "q": it["q"], "a": it["a"], "why": why,
            })
        elif pol == "unknown":
            unknown.append(it)

    # contradictions -- facts about the document, not judgments about it
    for c in rules.get("contradictions", []):
        left = next((i for i in items if re.search(c["left"]["match"], i["q"], re.I)), None)
        right = next((i for i in items if re.search(c["right"]["match"], i["q"], re.I)), None)
        if not (left and right):
            continue
        lbad = normalize_answer(left["a"]) != c["left"]["expect_answer"]
        rbad = normalize_answer(right["a"]) != c["right"]["expect_answer"]
        if lbad or rbad:
            findings.append({
                "kind": "CONTRADICTION", "rule": c["id"],
                "section": left["section"], "n": left["n"],
                "q": f"Q{left['n']}: {left['q']}", "a": f"{left['a']!r}",
                "why": c["why"].strip(),
                "pair": f"Q{right['n']}: {right['q']} -> {right['a']!r}",
            })

    facts = {
        "questions": len(items), "answers": counts, "polarity": pol_counts,
        "yes_rate": round(100 * counts["yes"] / max(1, len(items))),
        "checked_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    return findings, unknown, facts


# ------------------------------------------------------------------ output --
def render(findings, unknown, facts, source) -> str:
    ok = not findings
    L = [
        "# Questionnaire answer-bank lint",
        "",
        f"Source: [{source}]({source})  ",
        f"Checked: {facts['checked_at']} · {facts['questions']} questions · "
        f"{facts['yes_rate']}% answered Yes",
        "",
        f"## {'No polarity findings' if ok else f'{len(findings)} question(s) need a human'}",
        "",
    ]
    if not ok:
        for f in findings:
            L += [
                f"### {f['kind']} — {f['section']} Q{f['n']}  `{f['rule']}`",
                "",
                f"> {f['q']}",
                "",
                f"**Published answer:** `{f['a']}`",
                "",
                f"{f['why']}",
                "",
            ]
            if f.get("pair"):
                L += [f"**Paired with:** {f['pair']}", ""]
        L += [
            "**None of the above is a verdict.** Each is a question where the published "
            "answer would be read by a customer's security reviewer as a disclosure. The "
            "answer may be correct and deliberate — but if it is not, this is where a deal "
            "slows down and nobody traces it back to the file.",
            "",
        ]

    L += [
        "## Coverage",
        "",
        "| | |",
        "|---|---:|",
        f"| Questions parsed | {facts['questions']} |",
        f"| Negative polarity (Yes = admission) | {facts['polarity']['negative']} |",
        f"| Positive polarity (Yes = good) | {facts['polarity']['positive']} |",
        f"| Polarity unknown — not classified, not cleared | {facts['polarity']['unknown']} |",
        f"| Answered Yes | {facts['answers']['yes']} |",
        f"| Answered No | {facts['answers']['no']} |",
        f"| Prose / other | {facts['answers']['prose'] + facts['answers']['n/a']} |",
        "",
        f"**{facts['polarity']['unknown']} questions could not be classified** and are reported "
        "here rather than counted as clean. A linter that treats *unclassified* as *fine* is the "
        "fail-open defect it exists to catch. Curating those into `polarity-rules.yaml` is the "
        "work; the rules file is committed so the person who owns the answers can argue with it.",
        "",
    ]
    if unknown:
        L += ["<details><summary>Unclassified questions</summary>", ""]
        for u in unknown[:40]:
            L.append(f"- {u['section']} Q{u['n']}: {u['q'][:110]} → `{u['_ans']}`")
        L += ["", "</details>", ""]
    return "\n".join(L) + "\n"


def fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "questionnaire-linter"})
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status != 200:
                raise CannotLint(f"source returned HTTP {r.status}")
            body = r.read().decode()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        raise CannotLint(f"could not fetch source: {e}") from e
    if len(body) < 500:
        raise CannotLint(f"source returned {len(body)} bytes -- too short to be the answer bank")
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint a published questionnaire answer bank.")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--file", type=Path)
    ap.add_argument("--check", action="store_true", help="exit code only")
    ap.add_argument("--out", type=Path, default=HERE / "lint-report.md")
    args = ap.parse_args()

    try:
        if not RULES.is_file():
            raise CannotLint(f"rules not found at {RULES}")
        rules = yaml.safe_load(RULES.read_text())
        if not rules or "negative_polarity" not in rules:
            raise CannotLint("rules file has no negative_polarity section")
        src = str(args.file) if args.file else args.url
        md = args.file.read_text() if args.file else fetch(args.url)
        findings, unknown, facts = lint(parse(md), rules)
    except CannotLint as e:
        print(f"FAIL[2] could not lint: {e}", file=sys.stderr)
        print("Failing closed. A linter that cannot read the document does not report it clean.",
              file=sys.stderr)
        return 2

    if not args.check:
        args.out.write_text(render(findings, unknown, facts, src))
        print(f"report -> {args.out}")

    print(f"{facts['questions']} questions · {facts['yes_rate']}% Yes · "
          f"{facts['polarity']['negative']} negative-polarity · "
          f"{facts['polarity']['unknown']} unclassified")

    if findings:
        print(f"\n{len(findings)} question(s) need a human:", file=sys.stderr)
        for f in findings:
            print(f"  [{f['kind']}] {f['section']} Q{f['n']} ({f['rule']}) -> answer {f['a']!r}",
                  file=sys.stderr)
        return 1

    print("\nNo polarity findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
