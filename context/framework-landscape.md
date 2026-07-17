# The full framework landscape

Every framework and regime this role touches, what Mattermost's relationship to each one actually is, and where each lives in the 90-day plan. The CMMC and FedRAMP files get the most depth elsewhere in this repo because those two regimes moved in the ten weeks before the req posted, but the role owns all of the below, and the plan treats them accordingly.

## Held and operated (the commercial certifications, metric 2)

| Framework | Mattermost's position | Where it lives in the plan |
|---|---|---|
| **SOC 2 Type II** | Held. 2025 report plus a 2026 bridge letter and a SOC 3 on the trust center. Since March 2026 it is also the accepted entry framework for a FedRAMP Class A certification, which makes it strategically heavier than a routine commercial audit | [Audit-cycles runbook](../runbooks/soc2-iso-audit-cycles.md); calendar and evidence inventory in [days 1 to 30](../30-60-90/days-1-30.md); steady-state in phases two and three |
| **ISO 27001:2022** | Held. A real certificate from an accredited body sits on the trust center, while a public docs page describes ISO as "alignment," which understates a certification they paid for. That wording goes on the claims-consistency list | Same runbook; surveillance-cycle discipline plus the ISMS artifacts (scope, Statement of Applicability, management review, internal audit) that surveillance auditors actually check |

## Contract and legal obligations

| Regime | Mattermost's position | Where it lives in the plan |
|---|---|---|
| **NIST 800-171 Rev 2 / DFARS 7012 and 7021 / CMMC** | Obligated as a DIB contractor handling federal contract information. The enforced baseline today is 800-171 Rev 2 by self-assessment | [CMMC runbook](../runbooks/cmmc-l2-self-assessment.md), metric 1, the anchor deliverable |
| **EAR / ITAR export control** | Live obligation with an Export Compliance Program Manual in the handbook (linking out to internal docs). It is why the role requires US citizenship, and it intersects the AI policy directly, since staff LLM use touching export-controlled data is an export question | Inventory in days 1 to 30 with legal; sections 1 and 2 of the [AI policy runbook](../runbooks/internal-ai-policy.md); a standing lane in questionnaire answers |
| **GDPR** | Live obligation: a published DPA on the trust center, a privacy@ intake, and handbook stubs for data-subject access and deletion requests. EU-side entities (UK, Netherlands, Sweden) keep this real rather than theoretical | Privacy-operations inventory in days 1 to 30; DSAR and deletion runbook maturity assessed there and roadmapped if thin; DPA freshness in the [customer-assurance pass](../runbooks/customer-assurance-pass.md) |

## Inherited and platform-based (the federal posture)

| Regime | Mattermost's position | Where it lives in the plan |
|---|---|---|
| **FedRAMP** | Not a certified CSP; present as a named service inside a partner's Class D Rev5 package. The strategy question this raises is [open question 5](../hiring-manager-questions.md) | [Regulatory clock](regulatory-clock.md); the strategy decision brief in the day-30 regulatory memo |
| **DoD Impact Levels / Platform One CATO** | Certificate to Field under Platform One's continuous ATO; deployments described at IL4 through IL6 | Precision language in the customer-assurance pass, since inherited-versus-held is exactly the distinction that gets flattened in the field |
| **NIST 800-53** | The catalog underneath FedRAMP baselines and a named JD requirement. My engine renders an 800-53 profile from the same control set that renders everything else | [Engine bridge](engine-bridge.md); becomes primary the moment the FedRAMP strategy question gets a real answer |

## Customer-driven and marketed-against

| Regime | Mattermost's position | Where it lives in the plan |
|---|---|---|
| **CMMC, as a product story** | Their customers are defense contractors who need CMMC, and Mattermost publishes guidance supporting them. This is a different relationship than Mattermost's own CMMC obligation, and public docs blur the two, which matters in questionnaires | The claims-consistency pass keeps "our obligation" and "our product's support for yours" cleanly separated everywhere they appear |
| **NIS2 / DORA** | European market positioning: they market collaboration governance against both. Customer security teams in the EU will ask questionnaire questions in this vocabulary | Answer-bank coverage in the customer-assurance pass; no certification program to run, but the answers need owners |
| **FFIEC** | Their published disaster-recovery and business-continuity plan cites FFIEC guidance | Business-resiliency evidence in the audit-cycles runbook, since both SOC 2 and ISO consume it |

## Product capabilities that feed compliance (evidence sources, not audit programs)

FIPS-validated cryptography and STIG-hardened container images (shipped in v11), attribute-based access control, classification banners, and data-spillage reporting are product features. For this role they matter as evidence sources and as questionnaire answers with artifacts behind them, and they belong to product security rather than to the GRC audit calendar.

## TPRM, which cuts across everything above

Third-party and vendor risk is a named JD responsibility and a named area in the GRC charter, and it is not its own framework so much as the connective tissue: subservice organizations in the SOC 2 report, supplier controls in ISO, the partner dependency in the federal posture, AI vendors in the AI policy, and supply-chain questions in customer questionnaires. The day-30 inventory establishes what vendor tiering and assessment cadence exist today; the vendor-risk lane then runs through every runbook rather than in a silo, with the AI-vendor additions specified in the [AI policy runbook](../runbooks/internal-ai-policy.md).
