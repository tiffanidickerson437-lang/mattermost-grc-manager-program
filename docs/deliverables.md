# Deliverables

Things the research turned into work, rather than into observations. This page is the
catalog; the artifacts themselves live in the folders it links to.

## In your hands today

These exist now, in this repo, and you can run or read each one without waiting on me:

| Deliverable | Status | Where it lives | Hold it in your hand |
|---|---|---|---|
| 1. Questionnaire answer-bank linter | **Shipped, runs live** | [`04-evidence-and-audit/questionnaire-linter/`](../04-evidence-and-audit/questionnaire-linter/) | `python3 04-evidence-and-audit/questionnaire-linter/lint_answers.py` |
| 2. Internal AI policy draft | **Drafted** | [`02-ai-governance/internal-ai-policy.md`](../02-ai-governance/internal-ai-policy.md) | Read it; it is written in Mattermost's own HITL vocabulary |
| 3. Public claims consistency check | **Built** | [`05-stakeholder-management/public-claims-consistency/`](../05-stakeholder-management/public-claims-consistency/) | A [redline](../05-stakeholder-management/public-claims-consistency/claims-redline.md) plus `python3 05-stakeholder-management/public-claims-consistency/check_claims.py` |
| 4. CODEOWNERS + merge-gate patch | **Built, PR-ready** | [`03-secure-development/codeowners-merge-gate/`](../03-secure-development/codeowners-merge-gate/) | The [corrected file](../03-secure-development/codeowners-merge-gate/proposed-CODEOWNERS), settings, and [PR body](../03-secure-development/codeowners-merge-gate/PR-body.md) |
| 5. `llms.txt` split-tree fix | **Built, PR-ready** | [`03-secure-development/llms-txt-fix/`](../03-secure-development/llms-txt-fix/) | The [proposed fix](../03-secure-development/llms-txt-fix/proposed-fix.md) plus `python3 03-secure-development/llms-txt-fix/validate_llms_txt.py` |
| 6. The Drata answer | **Written** | [Below](#6-drata-as-an-evidence-gateway--the-so-what-happens-to-drata-answer) | The day-one answer to "so what happens to Drata?" |
| 7. FedRAMP business case | Needs day-one data | [Below](#7-the-framework-selection-business-case--should-we-get-fedramp-next) | The framing and the public half of the case |
| 8. Affirmation gate on real state | Built, needs day-one access | [`04-evidence-and-audit/`](../04-evidence-and-audit/) | `python3 04-evidence-and-audit/data/affirmation_gate.py --state 04-evidence-and-audit/data/examples/worked-example.state.yaml` |

Every item starts from something Mattermost publishes. Nothing here rests on
knowledge of their internal posture, because there isn't any, and the ones that
would need it are listed as such rather than guessed at.

The rule the whole directory follows: **gaps are the work, never the criticism.**
Finding and closing exactly these is what the role is for. Every one of them is
framed as something to hand over, not something to point at.

---

## Shipped

### 1. Questionnaire answer-bank linter → [`questionnaire-linter/`](../04-evidence-and-audit/questionnaire-linter/)

**Buildable from public data.** Runs today, against their live page, in about a second.

Their answer bank is public, about 80 questions across nine sections, served as clean
markdown. It is genuinely good material. It is also **96% "Yes"** — and a reviewer's
eye slides down a column of Yes.

Buried in that column, `### Governance` question 8 asks whether internet-facing
privileged accounts contain PII, SSNs, or patient health records. **The published
answer is "Yes."** It is a question where Yes is an admission, sitting in a run of
questions where Yes is the good answer. It also contradicts question 9 on the same
page, which says all PII and PHI is encrypted.

Almost certainly a copy-paste error — which is why it matters. It is the class of
defect that survives because nobody reads a Yes column closely, that file has no
CODEOWNER, and the repo has no merge gate. It does not block revenue loudly. It
blocks it one security reviewer at a time, and nobody traces the slow deal back to
line 87 of a markdown file.

The linter routes a human to every question where Yes would be a disclosure, and to
every pair of answers that can't both be comfortable. It never decides — polarity is
a judgment, and the rules live in a committed YAML the answer-owner can argue with.
**16 mutation tests**, including the one that matters most: twenty consecutive Yes
answers must produce zero findings, because a linter that fires on healthy answers
gets muted by lunchtime.

> Maps to success metric 4 — *"customer security questionnaires and trust center
> content maintained to unblock deal cycles."*

---

## Built from public data

Three of these are not write-ups. They are real artifacts in their own folders — a
corrected file, a runnable checker, a redline — that could be opened as pull requests
against Mattermost's own repositories today. Two more are specified and wait only on the
decision to build them.

### 2. Internal AI policy, written in their own vocabulary

*Specified. Draft procedure in [`../02-ai-governance/internal-ai-policy.md`](../02-ai-governance/internal-ai-policy.md).*

**The sharpest gap in the research, and the one with a ready-made answer.**

Their handbook's `llms.txt` index — all 281 pages — contains no AI usage policy, no
LLM data-handling standard, no AI governance page. Meanwhile they ship an LLM
product to defense buyers, and on 9 Dec 2025 published *"[Sovereign AI Risk
Assessment: 10 Questions CISOs Must Answer](https://mattermost.com/blog/sovereign-ai-risk-assessment-ciso-questions/)"* — AI risk guidance for **other
people's** CISOs. The exposure compounds: staff use LLMs on company data with no
published standard, in a company where a material slice of that data is CUI-adjacent
or export-controlled under EAR/ITAR. Pasting export-controlled data into a
foreign-hosted model is a plausible violation, and "how do you govern AI internally?"
lands in the questionnaire queue this role owns.

The reason this is a deliverable and not a lecture: **they already wrote the hard
part.** Nick Misasi's *"[Multiplayer Tool Calling for Secure Operations](https://mattermost.com/blog/multiplayer-tool-calling-for-secure-operations-who-approves-who-sees-who-runs-the-tool/)"* (17 Jun
2026) is the most rigorous HITL specification found anywhere in this research, and
it's theirs. It ships three tool policies — `ask`, `auto_run_in_dm`,
`auto_run_everywhere` — and four structural rules, including automation that fails
closed. The tiering maps onto compliance work exactly:

> **observation automates · assertion asks · attestation never automates**

So the policy doesn't need inventing. It needs writing down in the vocabulary their
engineers already settled on, four weeks ago, in their own product. The argument
about whether AI should be gated is already won internally.

Draft procedure: [`../02-ai-governance/internal-ai-policy.md`](../02-ai-governance/internal-ai-policy.md)

### 3. Public claims consistency check → [`public-claims-consistency/`](../05-stakeholder-management/public-claims-consistency/)

**Built.** A redline for every statement and a runnable checker that flags retired FedRAMP
vocabulary and routes a human. Two live, public, indexed pages reachable from the same nav
contradict each other:

| Page | Says |
|---|---|
| [Certifications & Compliance Overview](https://docs.mattermost.com/product-overview/certifications-and-compliance.html) | *"We are in the process of acquiring Authority to Operate (ATO)…"* |
| [U.S. Federal Procurement FAQ](https://docs.mattermost.com/product-overview/faq-federal-procurement.html) | *"Yes. Certificate to Field under Platform One's Continuous ATO."* |

A federal buyer doing diligence can land on the first one. The same overview page
describes ISO 27001 as *"alignment"* while the trust center carries a real
ISO 27001:2022 certificate — describing a certification you hold as an aspiration.

The federal FAQ also uses vocabulary FedRAMP retired under [NTC-0004](https://www.fedramp.gov/notices/0004/) on 25 February 2026:
"FedRAMP High authorized" should be **Class D (High)** and **Certified**, not Authorized —
and the same FAQ answers in IL4/IL5/IL6, which is the exact collision the rename existed to
prevent. (The certifications overview uses DoD-side ATO/CON language, not FedRAMP terms, so
the retired-vocabulary fix lands on the FAQ.)

The precision worth preserving: *"authorized via partner FedHIVE"* is **carefully
worded and correct.** Mattermost, Inc. is not a FedRAMP-certified CSP; it inherits
FedHIVE's Class D Rev5 package as a hosted workload. That distinction is the whole
ballgame in a federal questionnaire, and it's what gets flattened to "we're FedRAMP
High" on a sales call. The deliverable protects the correct claim, not just the
wrong ones.

### 4. CODEOWNERS + merge gate patch → [`codeowners-merge-gate/`](../03-secure-development/codeowners-merge-gate/)

**Built.** A corrected CODEOWNERS file, the exact branch-protection settings, and a PR body
written to their contributor guide. A pull request, not a proposal. Verified against the
public GitHub API on 17 July 2026:

- `mattermost-handbook` CODEOWNERS carries **3 path rules** (the repo holds 354 Markdown
  files; the current `0.2.1` tree publishes 281 pages)
- `/operations/security/` is **not one of them** — despite the handbook stating in
  prose that @dschalla *"Signs off on changes to Security"*
- `GET /actions/workflows` → `total_count: 0` — there is no check to enforce a review
- The handbook's own admission: a review gate *"is planned"* (branch-protection detail is
  not readable without maintainer access, so this rests on the zero-workflow count and the
  handbook's own words, not an asserted setting)

So approval today is a social convention held by three people with write access, and
ownership stated in prose isn't enforced by the file that enforces ownership. Deliverable
#1 exists because of exactly this: no owner on the answer-bank file, no gate on the merge.

### 5. `llms.txt` split-tree fix → [`llms-txt-fix/`](../03-secure-development/llms-txt-fix/)

**Built.** A runnable validator that fails on the live file today, a saved copy of that
file, and the concrete fix. Their `llms.txt` is real, served as `text/markdown`, with every
page retrievable by appending `.md` — genuinely ahead of most vendors. But it publishes
**two trees at once**: `0.2.0` (22 entries, legacy) and `0.2.1` (281 entries, current),
simultaneously, with no signal about which is live. Any agent ingesting the handbook gets
two conflicting versions of the company.

They built the machine-readable index; nothing tells the machine which half to trust.
For a company selling AI agents to defense buyers, the handbook their own agents would
read is ambiguous.

### 6. Drata as an evidence gateway — the "so what happens to Drata?" answer

*Specified — the day-one answer, not a build.* The entire content of their policies page: *"Mattermost company policies are published
and maintained in DRATA. Available only to internal staff members."*

They are **handbook-as-code, not policy-as-code.** The plumbing is excellent — public
git, markdown source, PR workflow open to outside contributors — but the governed
artifacts live behind a SaaS login, and the Drata↔handbook boundary is undocumented
in both directions.

Any policy-as-code proposal must answer *"so what happens to Drata?"* on day one, and
the answer is: **nothing.** Drata is the system of record and systems of record get
read, not replaced. It becomes an evidence gateway like any other. Drata holds
*state*; git holds *definition, change history, and the regulator diff*. No overlap,
no migration, no rip-out.

Worth knowing cold: Drata itself is FedRAMP Certified — FR2600167032, Class B, **Type
20x**. The platform they keep their policies in took the 20x route and is on the
marketplace. Mattermost is not.

---

## Needs day-one access

### 7. The framework-selection business case — *"should we get FedRAMP next?"*

The strongest strategic finding in the research, and the one the role is most
expected to spot.

Based on my sweep of the [live FedRAMP Marketplace feed](https://www.fedramp.gov/marketplace/products.json),
I found no Mattermost record across all 670 products (checked 16 July 2026). In the same
feed, every direct competitor holds a package ID: Slack (Class C), GovSlack
(Class D), M365 GCC-High (Class D), Zoom (Class C), Atlassian Gov Cloud (Class C).
The only Mattermost presence I found is a line item inside FedHIVE's Class D boundary,
and the vendor that historically carried the listing (Contegix, now Valiantys Federal)
no longer mentions Mattermost in its own listing description.

Meanwhile, a path opened this year that the public record suggests they are well
positioned for:

- **Class A** certification takes **SOC 2 Type II** as an approved external framework
- Available via **Program Certification** — no agency sponsor required
- Assessed via **Key Security Indicators**, not control narratives
- The [trust center](https://trust.mattermost.com/) **publishes a SOC 2 Type II report today** (checked 17 July 2026)
- The 20x submission pipeline is **open now** (FY26 Q4)
- **Class A products on the marketplace: 0 of 670.** Nobody has done it yet

Carry the two hard limits with the opportunity, or the case isn't honest: FedRAMP
grants **no reciprocity** from Class A to any other class, and is openly on record
about *"concerns about the quality and reliability of SOC 2 Type II audits."* Class A
buys a listing and two years, not a shortcut.

This is deliverable #7 rather than #1 because doing it properly means costing it —
time and spend to attain, against the deals and markets it unlocks. That needs
their pipeline, not public data. **Compliance ROI, not a vanity bar.**

### 8. The affirmation gate, pointed at real state → [`../04-evidence-and-audit/`](../04-evidence-and-audit/)

Built and running against a synthetic worked example. Needs day-one access to compute
anything true, because control state is only knowable inside the boundary.

Also unresolved from outside: **where Mattermost stands on CMMC.** Based on my research,
no CMMC certification appears in the public record I can reach: the [trust center](https://trust.mattermost.com/)
lists no CMMC badge or document among its public six (checked 17 July 2026), and the
[CMMC page](https://docs.mattermost.com/security-guide/cmmc-compliance.html) they publish
is product guidance for contractor customers, not a company certification. I have heard
Level 2 described as complete in one conversation, while the posting lists a gap
assessment as the first 90-day deliverable. Those describe different jobs, and only the
inside view resolves it. That's [question 1](../00-governance/open-questions.md).

---

## Deliberately not a deliverable

- **The CVE stream.** Recurring path-traversal and SSO/OIDC findings, patches shipped
  each time, responsible disclosure program running. Worth noticing: the vendor
  consistently **self-scores above NVD** (9.9 vendor vs 7.5 NVD on CVE-2025-25279).
  A vendor scoring itself harder than the national database is not downplaying
  anything — that's a favorable read, and the opposite of what "heavy CVE stream"
  suggests at a glance. Nothing to fix here; it's evidence the disclosure program
  works as published.
