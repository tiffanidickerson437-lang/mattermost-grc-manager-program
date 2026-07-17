# Research Findings

What is observably true about Mattermost's compliance program, from what Mattermost
publishes. Every item traces to a primary source checked 17 July 2026 — their handbook,
their docs, their GitHub, their trust center, the FedRAMP Marketplace, the Federal
Register.

Two rules govern this directory:

1. **Nothing here is a claim about their internal posture.** There is no way to know it
   from outside and no attempt is made. Where the public record runs out, that is written
   down as an open question — see [`open-questions.md`](open-questions.md) — rather than
   filled in with an assumption.
2. **Gaps are the work, never the criticism.** If it is visible to me it is visible to an
   auditor, a customer's security team, and a competitor. Every finding below ends in
   something to hand over, because finding and closing exactly these is what the role is
   for.

| # | Finding | Evidence | Deliverable |
|---|---|---|---|
| 01 | Policies are maintained in Drata (internal-only) | [handbook](https://handbook.mattermost.com/operations/security/policies) | [Drata as a gateway](../docs/deliverables.md#6-drata-as-an-evidence-gateway--the-so-what-happens-to-drata-answer) |
| 02 | No merge gate; security isn't in CODEOWNERS | [GitHub API](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/CODEOWNERS) | [CODEOWNERS patch](../03-secure-development/codeowners-merge-gate/) |
| 03 | No internal AI policy, while publishing AI risk guidance for others | [llms.txt](https://handbook.mattermost.com/llms.txt), [blog](https://mattermost.com/blog/sovereign-ai-risk-assessment-ciso-questions/) | [AI policy in their own vocabulary](../docs/deliverables.md#2-internal-ai-policy-written-in-their-own-vocabulary) |
| 04 | The public docs contradict each other | [certifications](https://docs.mattermost.com/product-overview/certifications-and-compliance.html), [federal FAQ](https://docs.mattermost.com/product-overview/faq-federal-procurement.html) | [Claims consistency check](../05-stakeholder-management/public-claims-consistency/) |
| 05 | The questionnaire answer bank has a defect | [live page](https://handbook.mattermost.com/operations/operations/company-policies/security-policies) | **[Shipped: the linter](../04-evidence-and-audit/questionnaire-linter/)** |
| 06 | `llms.txt` publishes two conflicting trees | [llms.txt](https://handbook.mattermost.com/llms.txt) | [Split-tree fix](../03-secure-development/llms-txt-fix/) |

---

## 01 — Policies are maintained in Drata (internal-only)

The entire content of [`handbook.mattermost.com/operations/security/policies`](https://handbook.mattermost.com/operations/security/policies):

> ```
> # Policies
> Mattermost company policies are published and maintained in [DRATA]*
> * Available only to internal staff members.
> ```

**What the public record shows.** The public handbook is docs-as-code and the plumbing is
genuinely good — public git repo, markdown source, a PR workflow open to outside
contributors, an `llms.txt` index, `.md` content negotiation on every URL. Most companies
do not have this. The governed policy artifacts are maintained in Drata, a commercial GRC
platform, and are available only to internal staff. That is a normal system-of-record
choice. It does mean the policies themselves are not publicly inspectable the way the
handbook is, and the Drata↔handbook boundary is undocumented and unlinked in both directions.

**Why it matters for the role.** Any automation proposal has to answer *"so what happens to
Drata?"* on day one. The right answer treats Drata as the system of record to read from, not
something to rip out.

**Corroborating signal.** The posting lists *"compliance automation tooling such as Vanta
or Drata"* as nice-to-have. Vanta appears nowhere in the handbook. Drata is the incumbent.

**Worth knowing cold:** Drata itself is FedRAMP Certified — FR2600167032, Class B, **Type
20x**. The platform they keep their policies in took the 20x route and is on the
marketplace. Mattermost is not.

**Not found publicly (likely held in Drata or another internal system):** the ISMS as a named artifact, acceptable use
policy, control library, control mappings, TPRM policy, vendor tiering, the security risk
register, evidence collection procedures, audit calendar, internal audit procedures, any
control test results.

---

## 02 — No merge gate, and security isn't in CODEOWNERS

Based on my research against the public GitHub API, checked 17 July 2026:

```
repo:                    github.com/mattermost/mattermost-handbook
default_branch:          0.2.1            (not main)
GET /actions/workflows:  total_count: 0
.github/:                PULL_REQUEST_TEMPLATE.md only

CODEOWNERS — every rule in the file:
  /operations/legal/                          @it33
  /operations/finance/                        @TQuock
  /operations/operations/company-processes/   @it33
```

**Three path rules across 281 published pages.** `/operations/security/` is not one of
them, while the handbook states in prose that @dschalla *"Signs off on changes to
Security."* Ownership asserted in prose, not enforced by the file whose whole job is
enforcing ownership. The handbook's own words: a review gate *"is planned."* Branch
protection settings are not readable without maintainer access, so this finding rests
on the zero-workflow count and the handbook's own admission, not on an asserted setting.

So approval today is a social convention held by three people with write access.

**Review latency, stated exactly:** 4 open PRs against 1,421 closed — and all four have
been sitting. Two since March 2025, one since May 2025, one since January 2026. That is
the entire open set; nothing is queued behind them. A handbook nobody merges into is a
handbook that stops describing the company.

**This finding is why finding 05 exists.** No owner on the file, no gate on the merge.

---

## 03 — No internal AI policy, while publishing AI risk guidance for other people

The handbook's `llms.txt` index — all 281 pages — contains **no AI usage policy, no LLM
data-handling standard, no AI governance page.** Verified via full index read and
site-scoped search. The only AI references are product.

**The sharpest version:** on 9 Dec 2025 they published *"[Sovereign AI Risk Assessment: 10
Questions CISOs Must Answer](https://mattermost.com/blog/sovereign-ai-risk-assessment-ciso-questions/)"* on the Mattermost blog — AI risk-assessment guidance for
**other organizations'** CISOs.

**Why the exposure compounds.** No published standard for staff LLM use is visible from
outside, in a company where the job posting itself says a material slice of data is
export-controlled under EAR/ITAR. Pasting export-controlled data into a foreign-hosted
model is a plausible violation, which is why the absence of a visible standard is worth
asking about rather than assuming either way — whether one exists internally is
[question 6](open-questions.md). Externally, they sell sovereign AI to defense buyers who
will ask how they govern AI internally, and that question lands in the questionnaire
queue this role owns.

Closest adjacent governance in the handbook: an Electronic Monitoring Policy and
Confidentiality guidelines. Neither addresses AI.

**Why this is the most tractable gap in the list: they already wrote the hard part.**
Nick Misasi's *"[Multiplayer Tool Calling for Secure Operations](https://mattermost.com/blog/multiplayer-tool-calling-for-secure-operations-who-approves-who-sees-who-runs-the-tool/)"* (17 Jun 2026) is the most
rigorous human-in-the-loop specification found anywhere in this research, and it is
theirs. Three tool policies — `ask`, `auto_run_in_dm`, `auto_run_everywhere` — four
structural rules, and automation that fails closed:

> "Mattermost does not walk backward through the automation chain looking for a human to
> approve the call… If a tool should run from automation in a shared channel, an
> administrator has to make the explicit decision that its output is safe."

That tiering maps onto compliance work directly:

> **observation automates · assertion asks · attestation never automates**

The policy does not need inventing. It needs writing down in the vocabulary their own
engineers settled on, in their own product, four weeks ago. The argument about whether AI
should be gated is already won internally.

---

## 04 — The public docs contradict each other

Two live, public, indexed pages, reachable from the same nav:

| | |
|---|---|
| **Certifications & Compliance Overview** | *"Q: Do you have Fed or Department of Defense (DOD) Certification?* <br> *A: We are in the process of acquiring Authority to Operate (ATO) and Certificate of Networthiness (CON) certifications."* |
| **U.S. Federal Procurement FAQ** | *"Q: Has it been granted a DoD ATO?* <br> *A: Yes. Certificate to Field under Platform One's Continuous ATO (CATO)."* |

Page A says they are seeking an ATO that Page B says they hold. A federal buyer doing
diligence can land on Page A first. The same overview page describes ISO 27001 as
*"alignment"* while the [trust center](https://trust.mattermost.com/) publishes an
ISO 27001 (2022) certificate as a featured document (checked 17 July 2026) — a
certification the trust center presents as held, described on the docs page as an
aspiration.

**The federal FAQ uses vocabulary FedRAMP retired under NTC-0004 on 25 February 2026.**
"FedRAMP High authorized" is doubly wrong: it should be **Class D (High)**, and
**Certified**, not Authorized. And the same FAQ answers in IL4/IL5/IL6 — which is the exact
vocabulary collision the rename existed to prevent. (The certifications overview uses
DoD-side ATO/CON language, not FedRAMP terms.) FedRAMP said so outright: it dropped
the word "levels" *"to avoid confusion with the DOD/DOW Impact Level/IL system."*

**The precision that must survive the fix.** *"Authorized via partner FedHIVE"* is
**carefully worded and correct.** Mattermost, Inc. is not a FedRAMP-certified CSP; it
inherits FedHIVE's Class D Rev5 package (FR1802451335) as a hosted workload. That
distinction is the whole ballgame in a federal questionnaire, and it is exactly what gets
flattened to "we're FedRAMP High" on a sales call. The deliverable protects the correct
claim, not just the wrong ones.

---

## 05 — The questionnaire answer bank has a defect · **shipped**

The richest public GRC artifact they have: `/operations/operations/company-policies/security-policies`
— a customer-questionnaire answer bank across nine sections, plus infrastructure security
policies and a full DR/BC plan informed by FFIEC guidance. Genuinely good written
material.

Measured live, 17 Jul 2026: **80 questions, 96% answered "Yes."**

Under `### Governance`, question 8:

> For all IT systems including but not limited to servers, routers, switches, firewalls,
> and databases, do privileged accounts (e.g., system or security administrator) that
> communicate directly with the internet, contain any personally identifiable information
> (PII) such as: social security numbers, credit card numbers, patient health record
> information, or other confidential records?
>
> **→ Yes**

A question where *Yes* is an admission, sitting in a run of questions where *Yes* is the
good answer. It also contradicts question 9 on the same page, which says all PII and PHI
is protected by industry-standard encryption.

**It is almost certainly a copy-paste error — which is exactly why it matters.** It is the
class of defect that survives because nobody reads a Yes column closely, and because
findings 01 and 02 are showing up in the wild: no CODEOWNER on that file, no merge gate on
that repo.

**What it costs.** The posting's fourth success metric is *"customer security
questionnaires and trust center content maintained to unblock deal cycles."* This does not
block revenue loudly. It blocks it one security reviewer at a time, and nobody attributes
the slow deal to line 87 of a markdown file.

→ **[The linter](../04-evidence-and-audit/questionnaire-linter/)** — runs against their live page in
about a second, finds it both ways (polarity and contradiction), and never decides.

---

## 06 — `llms.txt` publishes two conflicting trees

[`handbook.mattermost.com/llms.txt`](https://handbook.mattermost.com/llms.txt) is real, served as `text/markdown`, and every page is
retrievable by appending `.md`. This is genuinely ahead of most vendors, and it is why
finding 05's deliverable could be built at all.

But the index is split into **`0.2.0` (~22 entries, legacy/orphaned) and `0.2.1` (~281
entries, current) — both published simultaneously.** Any agent ingesting the handbook gets
two conflicting versions of the company and no signal about which is live.

They built the machine-readable index; nothing tells the machine which half to trust. For
a company selling AI agents to defense buyers, the handbook their own agents would read is
ambiguous about itself.

The index also advertises a query API — `GET /readme.md?ask=<question>` — in an Agent
Instructions footer. It did not return answers in testing: it silently returned plain page
markdown, or nothing. An advertised endpoint that silently no-ops is worse than an absent
one, because an agent cannot tell the difference between "no answer" and "no such thing."

---

## What the findings have in common

Four of the six are the same defect wearing different clothes: **a machine-readable
surface that no machine checks.** The handbook is docs-as-code with no CI. The CODEOWNERS
file omits the directory its prose says is owned. The `llms.txt` index publishes two
truths. The answer bank inverts a polarity in a column nobody reads.

They built the plumbing. Nothing runs through it.

That is a good problem to inherit, because the expensive half is already done — and it is
the specific thing the posting asks for: *"apply GRC engineering and automation to replace
manual evidence collection with continuous controls monitoring."*
