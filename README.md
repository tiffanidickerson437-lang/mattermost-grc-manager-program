# Mattermost, onboarded

**Short version:** most people applying for a GRC job describe what they would do. This repo does it — on Mattermost, before day one.

It has two halves. **[Findings](findings/)** is what is observably true about Mattermost's compliance program from what Mattermost publishes. **[Deliverables](deliverables/)** is what those findings turn into — eight of them, one already running against their live site.

Nothing here claims to know anything about their internal security posture. Everything traces to a public primary source checked 17 July 2026, and where the public record runs out that is written down as an [open question](findings/open-questions.md) rather than filled in with an assumption.

---

## The shortest path in

**One finding, and the thing it became.**

Mattermost publishes its customer-questionnaire answer bank in the open — about 90 questions, served as clean markdown. It is good material. It is also **96% "Yes"**, and a reviewer's eye slides down a column of Yes.

Buried in that column, question 8 asks whether internet-facing privileged accounts contain PII, social security numbers, or patient health records. The published answer is **"Yes."** It is a question where Yes is an admission, sitting in a run of questions where Yes is the good answer — and it contradicts question 9 on the same page, which says all PII is encrypted.

Almost certainly a copy-paste error. Which is exactly why it matters: it survives because nobody reads a Yes column closely, that file has no CODEOWNER, and the repo has no merge gate. It does not block revenue loudly. It blocks it one security reviewer at a time, and nobody traces the slow deal back to line 87 of a markdown file.

So I wrote the linter that catches it. Against their live page, in about a second:

```bash
pip install pyyaml
python3 deliverables/questionnaire-linter/lint_answers.py
```

```
80 questions · 96% Yes · 1 negative-polarity · 61 unclassified

2 question(s) need a human:
  [POLARITY]      Governance Q8 (NEG-PII-EXPOSURE) -> answer 'Yes'
  [CONTRADICTION] Governance Q8 (XOR-PII-EXPOSED-VS-PII-PROTECTED)
```

**It never decides.** Polarity is a judgment about what a question means, so the rules live in a [committed YAML](deliverables/questionnaire-linter/polarity-rules.yaml) the answer-owner can read and argue with. It routes a human and says why. And **61 of 80 questions are reported as unclassified rather than counted as clean** — a linter that treats *unclassified* as *fine* is the fail-open defect it exists to catch.

That is the shape of everything in this repo: find it in public, turn it into something that runs, and let a person decide.

## The rest of the findings

| # | Finding | Deliverable |
|---|---|---|
| 01 | [Policies live in Drata, not in git](findings/#01--the-policies-are-in-drata-not-in-git) | [Drata as a gateway, not a rip-out](deliverables/#6-drata-as-an-evidence-gateway--the-so-what-happens-to-drata-answer) |
| 02 | [No merge gate; security isn't in CODEOWNERS](findings/#02--no-merge-gate-and-security-isnt-in-codeowners) | [CODEOWNERS patch](deliverables/#4-codeowners--merge-gate-patch) |
| 03 | [No internal AI policy, while publishing AI risk guidance for other CISOs](findings/#03--no-internal-ai-policy-while-publishing-ai-risk-guidance-for-other-people) | [AI policy in their own HITL vocabulary](deliverables/#2-internal-ai-policy-written-in-their-own-vocabulary) |
| 04 | [The public docs contradict each other](findings/#04--the-public-docs-contradict-each-other) | [Claims consistency check](deliverables/#3-public-claims-consistency-check) |
| 05 | [The questionnaire answer bank has a defect](findings/#05--the-questionnaire-answer-bank-has-a-defect--shipped) | **[Shipped: the linter](deliverables/questionnaire-linter/)** |
| 06 | [`llms.txt` publishes two conflicting trees](findings/#06--llmstxt-publishes-two-conflicting-trees) | [Split-tree fix](deliverables/#5-llmstxt-split-tree-fix) |

Four of the six are the same defect wearing different clothes: **a machine-readable surface that no machine checks.** They built the plumbing; nothing runs through it. That is a good problem to inherit — the expensive half is already done.

## The federal instruments

Separate from the findings, because they are built for the obligation rather than drawn from an observation. → **[`assessment/`](assessment/)**

**[The CMMC affirmation gate](assessment/affirmation-packet.md).** Any defense contractor holding a CMMC status has to do this every year: a named senior executive personally signs a statement to the government saying the company is *still* compliant — [32 CFR 170.22](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.22), under False Claims Act liability. The July 2026 suspension of third-party assessment made that sharper, not softer: the C3PAO who used to stand between the company's claim and the government is gone, and the claim is still due. At most companies the signature is assembled every July from a spreadsheet nobody can reproduce. This makes it a computation.

**Where Mattermost sits on that is a question, not a claim** — no CMMC badge on the trust center, and the CMMC page they publish is [product guidance for contractors](https://docs.mattermost.com/security-guide/cmmc-compliance.html), not a company certification. That is [question 1](findings/open-questions.md). The instrument is the deliverable *because* every answer to that question needs the same thing.

Three things about it matter more than the score:

1. **It never signs.** The regulation gives that act to a person. AI drafts, humans decide, code computes evidence.
2. **It reads the law on every run.** A task force reports around mid-September; whatever it changes lands as an amendment to 32 CFR 170, and eCFR publishes that with a date. Affirming against a rule that changed underneath you is the quiet version of a false claim.
3. **It fails closed.** Unknown state, an expired POA&M, an unreachable regulation — every one blocks.

Also here: the [110-requirement 800-171 workbook](assessment/nist-800-171-rev2-workbook.md) with SPRS weights, the [46-KSI FedRAMP 20x map](assessment/fedramp-20x-ksi-map.md), and a [drift check](assessment/upstream-conformance-receipt.md) that reconciles that map against FedRAMP's live ruleset so it cannot rot unnoticed — currently 46/46, zero drift.

**Everything is tested by attacking it.** Each instrument ships mutation tests that plant a defect and check it gets caught. Two of the gate's tests are arithmetic identities from the DoD methodology rather than opinions: everything implemented must score exactly 110, nothing implemented must score exactly −203 — which proves the weights file itself. Gut any checker to always pass and its suite goes red. A checker nobody checks is a checker that gets quietly gutted.

## How the repo works

One configuration file describes Mattermost. Everything else is rendered from it.

```
companies/mattermost.config.yaml        one file: frameworks, stack, data types,
        │                               AI posture, risk tolerances — every value
        │                               traced to a public source
        ▼
tools/scaffold.py            ──────▶    generated/in-scope-controls.yaml
  filters the engine's                  45 controls, each with the reason it is in
  Living Control Set                    scope and the frameworks it satisfies
        │                               generated/profile-selection.yaml
        ▼
tools/onboard_company.py     ──────▶    generated/companies/mattermost/data.json
  + companies/mattermost/value.json     the rendered program: pillars, controls with
                                        Mattermost-specific narratives, roadmap
```

Change the config and the program re-renders. Adding a framework is a mapping exercise, not a rebuild. The engine is separate and public: **[`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program)**.

## Where to look

| | |
|---|---|
| [`findings/`](findings/) | What is observably true, from public sources. Six findings, each with verbatim evidence, plus the [open questions](findings/open-questions.md) that can't be resolved from outside |
| [`deliverables/`](deliverables/) | What the findings turned into. Eight, scored buildable-today vs needs-day-one. One shipped |
| [`assessment/`](assessment/) | The federal instruments: affirmation gate, 800-171 workbook, KSI map, drift check |
| [`runbooks/`](runbooks/) | Executable procedures: the L2 self-assessment under the suspension, the continuous-monitoring pilot, the customer-assurance pass, the internal AI policy |
| [`companies/`](companies/) | The single input — Mattermost as an engine configuration |
| [`generated/`](generated/) | What the engine rendered from it, including the [first 90 days](generated/30-60-90/) mapped to the role's five published success metrics |
| [`context/`](context/) | The regulatory clock, their GitHub org mapped, the framework landscape, and how the engine bridges to this role |

## Ground rules

1. **Public sources only.** Every claim traces to a public primary source checked 17 July 2026. Nothing is claimed about their internal posture. Where something could not be verified, it is absent or flagged as an open question.
2. **Gaps are the work, never the criticism.** If it is visible to me it is visible to an auditor, a customer's security team, and a competitor. Finding and closing exactly these is what the role is for.
3. **Evidence is computed, never authored.** No Mattermost evidence exists in this repo and none is claimed. The `evidence_in_repo: none` line in the config is load-bearing.

## Running it

```bash
pip install pyyaml

# the findings, turned into things that run
python3 deliverables/questionnaire-linter/lint_answers.py          # their live answer bank
python3 assessment/data/affirmation_gate.py --state assessment/data/examples/worked-example.state.yaml
python3 assessment/data/upstream_drift.py                          # vs FedRAMP's live ruleset

# every checker, attacked
python3 deliverables/questionnaire-linter/test_lint_answers.py     # 16 tests
python3 assessment/data/test_affirmation_gate.py                   # 15 tests
python3 assessment/data/test_upstream_drift.py                     #  9 tests
```

Same config, same library, same output. That property is the whole point.
