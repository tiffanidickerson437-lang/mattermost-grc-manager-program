# Deliverables

Things the research turned into work, rather than into observations.

Every item below starts from something Mattermost publishes. Nothing here rests on
knowledge of their internal posture, because there isn't any — and the ones that
would need it are listed as such rather than guessed at. Each is scored on whether
it can be **built from public data today** or has to wait for day one.

The rule the whole directory follows: **gaps are the work, never the criticism.**
Finding and closing exactly these is what the role is for. Every one of them is
framed as something to hand over, not something to point at.

---

## Shipped

### 1. Questionnaire answer-bank linter → [`questionnaire-linter/`](questionnaire-linter/)

**Buildable from public data.** Runs today, against their live page, in about a second.

Their answer bank is public, ~90 questions across nine sections, served as clean
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

## Buildable from public data — not yet built

### 2. Internal AI policy, written in their own vocabulary

**The sharpest gap in the research, and the one with a ready-made answer.**

Their handbook's `llms.txt` index — all 281 pages — contains no AI usage policy, no
LLM data-handling standard, no AI governance page. Meanwhile they ship an LLM
product to defense buyers, and on 9 Dec 2025 published *"Sovereign AI Risk
Assessment: 10 Questions CISOs Must Answer"* — AI risk guidance for **other
people's** CISOs. The exposure compounds: staff use LLMs on company data with no
published standard, in a company where a material slice of that data is CUI-adjacent
or export-controlled under EAR/ITAR. Pasting export-controlled data into a
foreign-hosted model is a plausible violation, and "how do you govern AI internally?"
lands in the questionnaire queue this role owns.

The reason this is a deliverable and not a lecture: **they already wrote the hard
part.** Nick Misasi's *"Multiplayer Tool Calling for Secure Operations"* (17 Jun
2026) is the most rigorous HITL specification found anywhere in this research, and
it's theirs. It ships three tool policies — `ask`, `auto_run_in_dm`,
`auto_run_everywhere` — and four structural rules, including automation that fails
closed. The tiering maps onto compliance work exactly:

> **observation automates · assertion asks · attestation never automates**

So the policy doesn't need inventing. It needs writing down in the vocabulary their
engineers already settled on, four weeks ago, in their own product. The argument
about whether AI should be gated is already won internally.

Draft procedure: [`../runbooks/internal-ai-policy.md`](../runbooks/internal-ai-policy.md)

### 3. Public claims consistency check

Two live, public, indexed pages reachable from the same nav contradict each other:

| Page | Says |
|---|---|
| Certifications & Compliance Overview | *"We are in the process of acquiring Authority to Operate (ATO)…"* |
| U.S. Federal Procurement FAQ | *"Yes. Certificate to Field under Platform One's Continuous ATO."* |

A federal buyer doing diligence can land on the first one. The same overview page
describes ISO 27001 as *"alignment"* while the trust center carries a real
ISO 27001:2022 certificate — describing a certification you hold as an aspiration.

Both pages also use vocabulary FedRAMP retired on 4 May 2026: "FedRAMP High
authorized" should be **Class D (High)** and **Certified**, not Authorized — and the
FAQ answers in IL4/IL5/IL6 on the same page, which is the exact collision the rename
existed to prevent.

The precision worth preserving: *"authorized via partner FedHIVE"* is **carefully
worded and correct.** Mattermost, Inc. is not a FedRAMP-certified CSP; it inherits
FedHIVE's Class D Rev5 package as a hosted workload. That distinction is the whole
ballgame in a federal questionnaire, and it's what gets flattened to "we're FedRAMP
High" on a sales call. The deliverable protects the correct claim, not just the
wrong ones.

### 4. CODEOWNERS + merge gate patch

A pull request, not a proposal. Verified against the GitHub API:

- `mattermost-handbook` CODEOWNERS carries **3 path rules across 281 published pages**
- `/operations/security/` is **not one of them** — despite the handbook stating in
  prose that @dschalla *"Signs off on changes to Security"*
- `required_status_checks.enforcement_level: "off"` on a branch reporting `protected: true`
- `GET /actions/workflows` → `total_count: 0`
- The handbook's own admission: a review gate *"is planned"*

So approval today is a social convention held by three people with write access, and
ownership stated in prose isn't enforced by the file that enforces ownership. Deliverable
#1 exists because of exactly this: no owner on the answer-bank file, no gate on the merge.

### 5. `llms.txt` split-tree fix

Their `llms.txt` is real, served as `text/markdown`, with every page retrievable by
appending `.md` — genuinely ahead of most vendors. But it publishes **two trees at
once**: `0.2.0` (~22 entries, legacy) and `0.2.1` (~281, current), simultaneously,
with no signal about which is live. Any agent ingesting the handbook gets two
conflicting versions of the company.

They built the machine-readable index; nothing tells the machine which half to trust.
For a company selling AI agents to defense buyers, the handbook their own agents would
read is ambiguous.

### 6. Drata as an evidence gateway — the "so what happens to Drata?" answer

The entire content of their policies page: *"Mattermost company policies are published
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

Mattermost is **not on the FedRAMP Marketplace** — zero records across all 670
products. Every direct competitor holds a package ID: Slack (Class C), GovSlack
(Class D), M365 GCC-High (Class D), Zoom (Class C), Atlassian Gov Cloud (Class C).
Mattermost's only presence is a line item inside FedHIVE's Class D boundary, and the
vendor that historically carried the listing (Contegix → Valiantys Federal) has
dropped the association entirely.

Meanwhile, a path opened this year that they are unusually well-positioned for:

- **Class A** certification takes **SOC 2 Type II** as an approved external framework
- Available via **Program Certification** — no agency sponsor required
- Assessed via **Key Security Indicators**, not control narratives
- Mattermost **holds SOC 2 Type II today**
- The 20x submission pipeline is **open now** (FY26 Q4)
- **Class A products on the marketplace: 0 of 670.** Nobody has done it yet

Carry the two hard limits with the opportunity, or the case isn't honest: FedRAMP
grants **no reciprocity** from Class A to any other class, and is openly on record
about *"concerns about the quality and reliability of SOC 2 Type II audits."* Class A
buys a listing and two years, not a shortcut.

This is deliverable #7 rather than #1 because doing it properly means costing it —
time and spend to attain, against the deals and markets it unlocks. That needs
their pipeline, not public data. **Compliance ROI, not a vanity bar.**

### 8. The affirmation gate, pointed at real state → [`../assessment/`](../assessment/)

Built and running against a synthetic worked example. Needs day-one access to compute
anything true, because control state is only knowable inside the boundary.

Also unresolved from outside: **whether Mattermost holds a CMMC status at all.** No
CMMC certification appears in the public record I can see, and the CMMC
page they publish is product guidance for contractor customers — not a company
certification. The recruiter says Level 2 is complete; the posting says a gap
assessment is the first 90-day deliverable. Those describe different jobs. That's
[question 1](../findings/open-questions.md).

---

## Deliberately not deliverables

- **The CVE stream.** Recurring path-traversal and SSO/OIDC findings, patches shipped
  each time, responsible disclosure program running. Worth noticing: they consistently
  **self-score above NVD** (9.9 vendor vs 7.5 NVD on CVE-2025-25279). A vendor scoring
  itself harder than the national database is not downplaying anything — that's a
  favorable read, and the opposite of what "heavy CVE stream" suggests at a glance.
- **The Series B tension.** Seven years post-round, no new raise, aggressive 2026
  C-suite buildout with a finance bench citing "investor due diligence readiness."
  Reads like a company preparing to raise or exit — which would make compliance
  posture diligence material. Worth understanding, not worth raising.
- **The req's disappearance from the public job board.** The Greenhouse link resolves
  and renders "New"; the board index doesn't list it. Innocuous readings exist
  (unlisted during late-stage interviews, index lag). A neutral question for the
  recruiter, never an assumption.
