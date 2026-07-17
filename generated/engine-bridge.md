# The engine bridge

How [`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program), my controls-as-code GRC engine, maps onto this role. The engine is public; this file exists so the connection is explicit rather than implied.

## What the engine is, in one paragraph

A compliance program that lives in git and proves itself in CI: a 45-control library mapped to SCF 2026.1 and expressed in OSCAL (catalog, 13 framework profiles including NIST SP 800-171 Rev 2, and an SSP that all pass validation), FAIR Monte Carlo risk quantification with loss-exceedance curves, framework crosswalks whose coverage percentages are computed rather than asserted, policy-as-code with tested allow/deny fixtures, and a drift monitor that opens timestamped issues as due-diligence records. AI drafts narratives and remediations; a human approves everything that becomes record; and evidence is the hard exception: computed from systems of record, with `ai_generated: true` rejected at the schema, hook, and CI layers.

## Posting responsibility → engine capability

| The posting asks me to | The engine already demonstrates |
|---|---|
| Maintain the control library, SSPs, POA&Ms, and policies | OSCAL-native control library with audit-depth specifications; SSP validated in CI; POA&M-as-issues pattern |
| Replace manual evidence collection with continuous controls monitoring | Evidence gateways reading systems of record over MCP; schema-validated evidence; scheduled drift monitor opening tickets on failure |
| Apply GRC engineering and automation | The whole repo: 6 CI workflows, 70 OSCAL checks, linted crosswalks, tested policy rules |
| Build AI-native workflows for recurring compliance work | AI drafting under human gates, enforced by hooks at the tool level, with the one hard rule (AI never authors evidence) machine-enforced |
| Own risk management end to end | FAIR Monte Carlo with p50/p90/p95 loss exceedance, CI-tested; risk acceptance modeled as a named human decision, never automated |
| Lead certification and surveillance cycles across frameworks | One control set rendered to 12 profiles; adding a framework is a mapping exercise, no longer a project |
| Own questionnaires and trust center content | The stakeholder-management pillar: one posture rendered for many audiences, answers linked to controls and evidence rather than asserted |

## What gets adapted for Mattermost, specifically

1. **Drata as an evidence gateway, not a rip-out.** The engine's gateway pattern (read from the system of record, validate against schema, record) points at Drata exactly the way it points at any other source. The architecture decision about Drata's long-term role belongs to the company, and the [60-day memo](../30-60-90/phase-2-design.md) prices the options honestly.
2. **A vulnerability-response control family, sourced from them.** Mattermost's published Product Vulnerability Process is the strongest public GRC artifact they have, and it deserves a formal place in the control library. The engine gains a control family built from it (intake, scoring, remediation SLAs, backporting, advisory publication, post-incident review), with evidence expectations attached, so the next audit inherits what product security already does well.
3. **Drift response as a Playbook run.** The engine opens GitHub issues on drift. At Mattermost, drift can open a Playbook run in Mattermost itself, which is both operationally better there and the kind of dogfooding the company values.
4. **The HITL vocabulary swap.** The engine's human-gate tiers translate directly into the approval language their Agents V2 model shipped: read-only checks can run automatically, anything that asserts compliance status waits for a person, and formal attestations are always and only human. Their engineers already settled this argument in the product; the compliance program gets to inherit the win.
5. **800-171 Rev 2 as the rendered profile of record** for the CMMC work, per the [runbook](../04-evidence-and-audit/cmmc-l2-self-assessment.md), with the SPRS score derived from control state rather than from a spreadsheet nobody can reproduce. This is now a shipped engine capability, not a promise: the [110-requirement workbook](../04-evidence-and-audit/frameworks/nist-800-171-rev2-workbook.md) is rendered, and the [FedRAMP 20x KSI map](../04-evidence-and-audit/frameworks/fedramp-20x-ksi-map.md) scores the control set against all 46 CR26 indicators for the day the own-listing question resolves.

## The short version

The engine proves the method in public, and this repo aims that method at one company's actual calendar, obligations, and tooling. That is what makes a fast start realistic: most of what day one needs has already been built and tested, and the remaining work is pointing it at Mattermost's systems.
