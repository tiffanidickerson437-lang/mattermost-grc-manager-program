# 01 · Third-party risk management

The role owns the third-party and vendor risk management program, including security assessments and supply chain risk. This folder holds the third-party picture as the public record shows it, because based on my research the most consequential third-party relationships in Mattermost's compliance story are already visible from outside.

## The inherited FedRAMP boundary is a vendor dependency

Based on my research of the [live FedRAMP Marketplace feed](https://www.fedramp.gov/marketplace/products.json) (checked 16 July 2026), Mattermost's federal cloud position runs through a partner: it appears as a named service inside [FedHIVE's](https://www.fedramp.gov/marketplace/products/FR1802451335/) Class D package rather than under a package ID of its own. FedRAMP's own [minimum assessment scope](https://www.fedramp.gov/2026/reference/minimum-assessment-scope/) now says third-party information resources must be addressed regardless of whether those resources hold a certification of their own. Read together, an inherited boundary is a supply-chain dependency for the TPRM program to track like any other critical vendor, with its own review cadence and exit thinking. The full analysis, sources, and what stays a question live in [finding 04](../00-governance/README.md#04--the-public-docs-contradict-each-other) and [deliverable 7](../docs/deliverables.md#7-the-framework-selection-business-case--should-we-get-fedramp-next).

## The vendors the compliance program itself runs on

Based on the public record, three vendors carry compliance-critical load today, which puts them at the top of any vendor-tiering exercise:

| Vendor | What the public record shows it holds | Source |
|---|---|---|
| Drata | The policies themselves: the handbook says company policies are published and maintained there | [handbook policies page](https://handbook.mattermost.com/operations/security/policies) |
| Conveyor | The trust center: certificates, reports, and questionnaire answers customers rely on | [trust.mattermost.com](https://trust.mattermost.com/) |
| Ironclad | Contracts, as the handbook's named CLM system of record | [handbook](https://handbook.mattermost.com/operations/legal/contracts) |

Deliverable 6, [Drata as an evidence gateway](../docs/deliverables.md#6-drata-as-an-evidence-gateway--the-so-what-happens-to-drata-answer), is the TPRM-flavored answer to the biggest of these: the system of record gets read, never ripped out.

## What cannot be known from outside

The vendor inventory, tiering, assessment cadence, and any fourth-party mapping are internal by nature. Nothing here claims to know them. Day-one work in this pillar starts from the [30/60/90 plans](../30-60-90/) and the questions in [open-questions.md](../00-governance/open-questions.md).
