# Open questions

Everything in the findings and deliverables rests on public sources. These are the
questions the public record cannot answer. Each one states what is visible from outside and
where the public trail ends, so the boundary between observed fact and internal knowledge
stays explicit. None of them is an assumption dressed as a finding; they are the things a
first conversation with the team would settle.

---

## 1. Where does CMMC Level 2 stand, and is it still the target?

**Public record:** The only CMMC reference Mattermost publishes is a
[product page](https://docs.mattermost.com/security-guide/cmmc-compliance.html) written as
guidance for contractor customers, not a company certification. No CMMC status appears in
any public artifact. On 13 July 2026 the DoW CIO [suspended CMMC Phase II](https://dowcio.war.gov/CMMC/):
contracts can name only Level 1 (Self) or Level 2 (Self), and no third-party C3PAO
assessment can be required during the review.

**Unresolvable from outside:** whether Mattermost holds or is pursuing a CMMC status at all,
against what scope and boundary, and whether it is still the priority now that a completed
self-assessment posted to SPRS is the current path and a C3PAO assessment cannot presently
be purchased. NIST SP 800-171 Rev 2 and DFARS 252.204-7012 remain fully in force regardless,
so the underlying work stands; the destination is the open question.

## 2. Does federal compliance sit in Mattermost Federal, Inc. or the parent security org?

**Public record:** Mattermost Federal, Inc. is a separate U.S. federal subsidiary (Reston,
VA) with its own leadership. The role requires U.S. citizenship and clearance eligibility.

**Unresolvable from outside:** whether federal readiness scope lives in the subsidiary, the
parent, or across both, and whether the clearance-eligibility requirement is about accessing
customer environments or signing on behalf of an entity.

## 3. What is the intended future of Drata?

**Public record:** The handbook states that company policies are published and maintained in
Drata and are available only to internal staff. The posting lists automation tooling "such
as Vanta or Drata" as a nice-to-have. Drata is the incumbent; Vanta appears nowhere in the
handbook.

**Unresolvable from outside:** whether modernization is meant to happen around Drata, through
it, or eventually out of it — and whether that call has already been made.

## 4. What does success look like, now that the ground has moved?

**Public record:** The posting's first success metric is a CMMC Level 2 gap assessment and
readiness roadmap within 90 days. It was published on or before 2 July 2026 — before the
13 July suspension. The CMMC Reform Task Force reports around 11 September 2026, roughly the
first two weeks of a September start.

**Unresolvable from outside:** which target the roadmap should point at — the current
self-assessment regime, a possible return of third-party assessment, or whatever the Task
Force produces in September. The gap assessment is the right work either way; its destination
is what a first conversation would recalibrate.

## 5. What does the FedRAMP position look like from the inside?

**Public record:** Mattermost is not on the FedRAMP Marketplace under its own listing; its
only presence is a named workload inside a partner's Class D package. Since
[NTC-0007](https://www.fedramp.gov/notices/0007/) (3 March 2026), SOC 2 Type II is an
approved entry framework to a FedRAMP Class A certification granted by the program office
with no agency sponsor, and Mattermost [holds SOC 2 Type II today](https://trust.mattermost.com/).

**Unresolvable from outside:** whether the intent is to keep inheriting through partners or
to pursue Mattermost's own listing, and whether the Class A path has already been evaluated
and set aside for reasons not visible externally.

## 6. Is there an internal AI governance roadmap, including ISO 42001?

**Public record:** The handbook's `llms.txt` index, all 281 pages, contains no AI usage
policy, no LLM data-handling standard, and no AI governance page — while Mattermost ships an
AI product to defense buyers and publishes
[AI risk guidance for other organizations' CISOs](https://mattermost.com/blog/sovereign-ai-risk-assessment-ciso-questions/).

**Unresolvable from outside:** whether an internal AI policy exists in Drata rather than the
public handbook, who answers a defense customer's questionnaire about internal AI governance
today, and whether the GRC roadmap includes ISO/IEC 42001.

## 7. Who owns the accuracy of public compliance claims?

**Public record:** Two live, public, indexed pages contradict each other about federal
status, and both use FedRAMP vocabulary retired on 25 February 2026 (see
[finding 04](README.md#04--the-public-docs-contradict-each-other)).

**Unresolvable from outside:** who owns the accuracy of Mattermost's public compliance claims
today, and whether that ownership would consolidate under this role.

## 8. What does "grow and lead the GRC team" mean on a headcount plan?

**Public record:** The GRC function is one analyst. The posting says the team grows as the
program scales.

**Unresolvable from outside:** whether there is a headcount plan behind that, and what would
trigger the first hire.

## 9. Where are the SOC 2 and ISO 27001 cycles right now?

**Public record:** The trust center carries a SOC 2 Type II report, SOC 3, and an ISO/IEC
27001:2022 certificate.

**Unresolvable from outside:** where the current SOC 2 Type II period sits, when the next ISO
surveillance audit falls, and whether the last cycle surfaced any evidence-collection pain.
Also open: whether there is appetite to publish more of the security program publicly — the
handbook pattern extended to GRC artifacts — or whether that posture is deliberately private.
