# Mattermost GRC: findings and deliverables

Short version: this repo is how I would begin the GRC Manager role, built from what Mattermost already publishes. I wanted to be able to showcase how I think during my interviewing process.

This repo has two halves. [Findings](findings/) is what is observably true about Mattermost's compliance program from public sources. [Deliverables](deliverables/) is what those findings turn into. There are eight of them, and one already runs against your live site. The commands to run everything yourself are under Running it at the end.

Nothing here claims to know anything about Mattermost's internal security posture. Every claim traces to a public primary source I have researched and found current as of 17 July 2026, and where the public record runs out I wrote that down as an [open question](findings/open-questions.md) instead of filling it in.

The program is further along than most I have seen at this stage. Which is exciting! You hold various compliance certifications today, the handbook is genuinely docs-as-code, and your own engineers have already written a human-in-the-loop AI model. I am excited to contribute to the groundwork already done by adding some of my build work into it. The role, as it was described to me, is to inherit a working GRC program and scale/maintain it rather than start one from scratch.

That is the spirit of everything here. Where I point at a gap, I mean it as the next piece of work and something to hand over. I never mean it as a criticism of the work completed thus far as it is highly impressive.

## A Gap Surfaced From My Research

Mattermost publishes its customer-questionnaire answer bank in the open: about 80 questions, served as clean markdown. It is good material. It is also 96% "Yes," and a single problem answer is easy to miss in a long column of "Yes."

Question 8 in that column asks whether internet-facing privileged accounts contain PII, social security numbers, or patient health records. The published answer is "Yes." That is an answer where "Yes" is a disclosure, and it sits in a run of questions where "Yes" is the good answer. It also contradicts question 9 on the same page, which says all PII is encrypted.

It is almost certainly a copy-paste error, and that is exactly why it matters. It survives because nobody reads a "Yes" column closely, because that file has no CODEOWNER, and because the repo has no merge gate. It rarely stops a deal outright. More often it adds friction in one security review after another, and nobody traces the slow deal back to line 87 of a markdown file.

So I wrote the linter that catches it. It runs against your live page in about a second:

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

The linter never decides anything. Polarity is a judgment about what a question means, so the rules live in a [committed YAML file](deliverables/questionnaire-linter/polarity-rules.yaml) that the answer owner can read and argue with. The linter routes a person and says why. It also reports 61 of 80 questions as unclassified rather than counting them as clean, because a linter that treats "unclassified" as "fine" is the fail-open defect it exists to catch.

Everything in this repo works this way. I find something in Mattermost's public material and build it into something that runs, and a person makes the call.

## Other Gaps I Noted

Each row carries the live source I read it from, so you can check every one at its origin rather than take my word for it.

| # | Finding | Primary source | Deliverable |
|---|---|---|---|
| 01 | Policies live in Drata, not in git | [handbook policies page](https://handbook.mattermost.com/operations/security/policies) | [Drata as a gateway, not a rip-out](deliverables/#6-drata-as-an-evidence-gateway--the-so-what-happens-to-drata-answer) |
| 02 | No merge gate, and security is not in CODEOWNERS | [CODEOWNERS on branch 0.2.1](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/CODEOWNERS) | [CODEOWNERS and merge-gate patch](deliverables/#4-codeowners--merge-gate-patch) |
| 03 | No internal AI policy, while publishing AI risk guidance for other CISOs | [llms.txt](https://handbook.mattermost.com/llms.txt) · [your CISO-facing blog](https://mattermost.com/blog/sovereign-ai-risk-assessment-ciso-questions/) | [AI policy in your own vocabulary](deliverables/#2-internal-ai-policy-written-in-their-own-vocabulary) |
| 04 | The public docs contradict each other | [certifications page](https://docs.mattermost.com/product-overview/certifications-and-compliance.html) · [federal FAQ](https://docs.mattermost.com/product-overview/faq-federal-procurement.html) | [Public claims consistency check](deliverables/#3-public-claims-consistency-check) |
| 05 | The questionnaire answer bank has a defect | [live answer bank](https://handbook.mattermost.com/operations/operations/company-policies/security-policies) | Shipped: [the linter](deliverables/questionnaire-linter/) |
| 06 | `llms.txt` publishes two conflicting trees | [handbook llms.txt](https://handbook.mattermost.com/llms.txt) | [Split-tree fix](deliverables/#5-llmstxt-split-tree-fix) |

Four of the six findings share one cause: a machine-readable surface that no machine checks. The structure is published, and nothing runs against it yet. That is a good problem to inherit, because the hard part is already built.

## One control set, many frameworks

The engine behind this repo holds one control set and renders it into whatever framework the business decides it would like to attain next. Nothing here ranks one framework over another, because framework choice is a rendering rather than a bet. CMMC/NIST are one rendering. SOC 2 and ISO 27001 are another. FedRAMP is another. Underneath they are the same controls, described in the language each audience needs.

That is what a program-ownership role is in practice. You define the truth once, and you keep every rendering of it accurate as the audience changes, whether that audience is a federal assessor, a commercial auditor, a customer's security team, or the C-suite. The sections below show a few of those renderings running against Mattermost's real, public situation.

## Federal readiness

### CMMC Updates

On 13 July the DoW CIO [suspended CMMC Phase II](https://dowcio.war.gov/CMMC/). The work the metric describes still stands, and its destination moved. Contracts can now name only Level 1 (Self) or Level 2 (Self), and no one can require a third-party C3PAO assessment during the review. A Reform Task Force reports to the DoW CIO around 11 September, which is roughly week two of a September start.

However, the underlying obligation did not soften. A named senior executive still signs the [32 CFR 170.22](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.22) affirmation under False Claims Act liability, and the third-party assessor who used to stand behind that signature is now gone. That makes a self-assessment heavier, and it is a reason to run controls continuously rather than assemble them once a year.

The only public CMMC reference I can find is a [product page](https://docs.mattermost.com/security-guide/cmmc-compliance.html) written as guidance for contractors, not a company certification. With Phase II suspended, the first thing I would want to settle with you is where CMMC actually stands and whether it is still the target, or whether FedRAMP is now the better path. That is [question 1](findings/open-questions.md).

### The federal instruments

These sit in [`assessment/`](assessment/). They are built for an obligation rather than drawn from an observation, so they are separate from the findings.

The [CMMC affirmation gate](assessment/affirmation-packet.md) is the main one. Any defense contractor that holds a CMMC status has to do this every year: a named senior executive personally signs a statement to the government that the company is still compliant, under [32 CFR 170.22](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.22) and False Claims Act liability.

At most companies that signature is assembled every July from a spreadsheet nobody can reproduce. This makes it a computation instead. Three properties matter more than the score it produces:

- It never signs. The regulation gives that act to a person, so the tool drafts and computes, and a human decides.
- It reads the law on every run. When the September task force changes 32 CFR 170, eCFR publishes the amendment with a date, and affirming against a rule that changed underneath you is the quiet version of a false claim.
- It fails closed. An unknown control state, an expired POA&M, or a regulation it cannot reach all block the affirmation.

Also here: the [110-requirement 800-171 workbook](assessment/nist-800-171-rev2-workbook.md) with SPRS weights, the [46-KSI FedRAMP 20x map](assessment/fedramp-20x-ksi-map.md), and a [drift check](assessment/upstream-conformance-receipt.md) that reconciles that map against FedRAMP's live ruleset so it cannot rot unnoticed. It currently reads 46 of 46, zero drift.

Every instrument is tested by attacking it. Each one ships mutation tests that plant a defect and confirm it gets caught, so gutting any checker to always pass turns its suite red.

### The one that is not CMMC and not FedRAMP

The same DoW CIO office that suspended the credential also publishes [Brilliant at the Basics](https://dowcio.war.gov/BrilliantBasics/), a Top 10 of IT practices it asks the Defense Industrial Base to actually do, framed as stripping away "administrative complexity and compliance overhead." No assessment, no contract clause, and nobody will audit against it. It is the clearest public statement of what the customer thinks good looks like.

So [`brilliant_basics.py`](assessment/data/brilliant_basics.py) asks what the enforced baseline can see of it. Eight of the ten practices are reachable from NIST 800-171 Rev 2. One is not:

```
  [08] Secure AI Adoption and Data Protection   <- (BLIND SPOT) -> AAT-01, AAT-02
```

NIST SP 800-171 Rev 2 contains no artificial-intelligence requirement. It was published in February 2020, the 110 requirements predate the workforce LLM, and Rev 3 does not add one.

A contractor can score a perfect 110 in SPRS, sign the affirmation, and still be non-conformant with a practice the same office calls a Top 10 basic. The score is accurate, and it still cannot reflect a practice that 800-171 does not contain.

The control set behind this repo can, because `AAT-01` and `AAT-02` are in scope from `ai-products: true` in the config, satisfying NIST AI RMF 1.0 and ISO/IEC 42001. That is the argument for one control set rendered into many frameworks, made by the customer's own CIO rather than by me. It also lands on [finding 03](findings/#03--no-internal-ai-policy-while-publishing-ai-risk-guidance-for-other-people), since Mattermost sells sovereign AI to the department that published the list.

### FedRAMP, as a priced option

FedRAMP is the framework-selection rendering: a costed "should we?" rather than a foregone conclusion. It comes last here on purpose, and the engine renders it from the same control set as everything else.

Two things are worth a conversation.

First, the vocabulary changed and the public pages have not caught up. On 4 May 2026 FedRAMP renamed "Authorized" to "Certified" and replaced the old impact levels with Classes A through D, so "FedRAMP High authorized" is now retired language, and the [certifications overview](https://docs.mattermost.com/product-overview/certifications-and-compliance.html) and [federal FAQ](https://docs.mattermost.com/product-overview/faq-federal-procurement.html) still use it. Reconciling them is a claims-consistency pass, and it sits inside the fourth success metric.

Second, a door opened this year for a SOC 2 Type II holder. Since [NTC-0007](https://www.fedramp.gov/notices/0007/) on 3 March 2026, SOC 2 Type II is an approved entry framework to a FedRAMP Class A certification granted directly by the program office with no agency sponsor, and Mattermost [holds SOC 2 Type II today](https://trust.mattermost.com/).

Two honest limits travel with it: Class A grants no reciprocity toward the higher classes, and FedRAMP has stated concerns about SOC 2 audit quality. So it is an option to price against the deals it opens, not a bar to chase for its own sake, and it may already have been evaluated and set aside for reasons I cannot see from outside. That is why I wrote it up as [question 5](findings/open-questions.md) rather than a recommendation.

## How the AI works

Every instrument here is written so a machine can draft and triage, and only a person can assert. AI writes narrative and flags gaps, and a human holds the veto. AI never generates evidence, because evidence is computed from systems of record. And it never signs, because signing is not a function the affirmation gate has.

The model for that is Mattermost's own, [multiplayer tool-calling specification](https://mattermost.com/blog/multiplayer-tool-calling-for-secure-operations-who-approves-who-sees-who-runs-the-tool/) behind Agents V2 sets three tool policies, keeps approval with the initiator, and fails closed when no human owns the decision. Mapped onto compliance work it reads cleanly:

| Mattermost tool policy | Compliance equivalent |
|---|---|
| `auto_run_everywhere` | observation automates |
| `ask` | assertion asks for a human |
| bot flows filtered out | attestation never automates |

The point is that the compliance work speaks in the vocabulary your engineers already settled on.

## How the repo works

One configuration file describes Mattermost. Everything else is rendered from it by the public engine, which lives in a separate repo.

```
companies/mattermost.config.yaml       one file, in this repo: frameworks, stack, data
        │                              types, AI posture, risk tolerances. Every value
        │                              traces to a public source.
        │
        │   run through the public engine (compliance-program),
        │   which holds tools/scaffold.py and tools/onboard_company.py
        ▼
generated/                             the rendered program, in this repo: 45 in-scope
                                       controls, each with the reason it is in scope and
                                       the frameworks it satisfies, plus Mattermost-
                                       specific narratives and the first 90 days
```

Change the config and the program re-renders. Adding a framework is a mapping exercise rather than a rebuild. The tools themselves stay in the engine so that any company is only ever a config file: [`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program).

## Contributions I could send upstream

Your handbook and docs are open source, so three of the deliverables are not mockups. They are pull requests I could open against Mattermost's own repositories, written to your [contributor guidelines](https://github.com/mattermost/mattermost-handbook/tree/0.2.1/contributors):

- The [CODEOWNERS and merge-gate patch](deliverables/#4-codeowners--merge-gate-patch), which adds `/operations/security/` to the file and turns on the review check the handbook says is planned.
- The [`llms.txt` split-tree fix](deliverables/#5-llmstxt-split-tree-fix), which resolves the two conflicting handbook trees the index publishes at once.
- The [public claims consistency check](deliverables/#3-public-claims-consistency-check), which reconciles the certifications overview and the federal FAQ so they stop contradicting each other.

Each one branches from Mattermost's repo and follows your review process. The engine and the federal instruments stay in this separate, access-gated instance, and only the handbook fixes are meant to land upstream.

## Where to look

| | |
|---|---|
| [`findings/`](findings/) | What is observably true, from public sources. Six findings, each with verbatim evidence, plus the [open questions](findings/open-questions.md) that cannot be resolved from outside |
| [`deliverables/`](deliverables/) | What the findings turned into. Eight, scored buildable-today or needs-day-one. One shipped |
| [`assessment/`](assessment/) | The federal instruments: affirmation gate, 800-171 workbook, KSI map, drift check |
| [`runbooks/`](runbooks/) | Executable procedures: the Level 2 self-assessment under the suspension, the continuous-monitoring pilot, the customer-assurance pass, the internal AI policy |
| [`companies/`](companies/) | The single input, Mattermost expressed as one engine configuration |
| [`generated/`](generated/) | What the engine rendered from it, including the [first 90 days](generated/30-60-90/) mapped to the role's five published success metrics |
| [`context/`](context/) | The regulatory clock, your GitHub org mapped, the framework landscape, and how the engine bridges to this role |

## Ground rules

1. Public sources only. Every claim traces to a public primary source checked 17 July 2026. Nothing is claimed about your internal posture, and where something could not be verified it is absent or flagged as an open question.
2. Gaps are the work, never the criticism. If it is visible to me, it is visible to an auditor, a customer's security team, and a competitor. Finding and closing exactly these is what the role is for.
3. Evidence is computed, never authored. No Mattermost evidence exists in this repo and none is claimed. The `evidence_in_repo: none` line in the config is load-bearing.

## Running it

```bash
pip install pyyaml

# the findings, turned into things that run
python3 deliverables/questionnaire-linter/lint_answers.py          # your live answer bank
python3 assessment/data/affirmation_gate.py --state assessment/data/examples/worked-example.state.yaml
python3 assessment/data/upstream_drift.py                          # vs FedRAMP's live ruleset
python3 assessment/data/brilliant_basics.py                        # vs the DoW CIO's own Top 10

# every checker, attacked
python3 deliverables/questionnaire-linter/test_lint_answers.py     # 16 tests
python3 assessment/data/test_affirmation_gate.py                   # 15 tests
python3 assessment/data/test_upstream_drift.py                     #  9 tests
python3 assessment/data/test_brilliant_basics.py                   # 15 tests
```

Same config, same library, same output on every run.

## If any of this is useful

I would love to walk you through it on a call. The first thing I would want to do in the seat is turn the [open questions](findings/open-questions.md) into a written 90-day plan we both agree on, starting with where CMMC really stands and how the September report changes the target. Thank you for reading this far.
