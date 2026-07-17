# The first 90 days

One plan in three phases, built against the role's five published success metrics and the regulatory calendar as it stands on 16 July 2026. The engine rendered these artifacts from the 16 July 2026 research snapshot, and every public source they rest on was re-checked on 17 July 2026, the check date the rest of the repo cites.

## The five metrics, verbatim from the posting

1. "CMMC Level 2 gap assessment and readiness roadmap delivered within first 90 days"
2. "SOC 2 Type II and ISO 27001 audit cycles completed on time without slippage"
3. "Manual evidence collection replaced with automated, continuously monitored controls"
4. "Customer security questionnaires and trust center content maintained to unblock deal cycles"
5. "GRC team grown and operating as a scalable, program-driven function"

Every line item in the three phase files maps back to one of these five numbers, so nothing in the plan exists for its own sake.

## The one thing this plan does that a generic plan cannot

Metric 1 was written on or before 2 July 2026. On 13 July the DoW CIO suspended CMMC's Phase II implementation: third-party (C3PAO) and government-led (DIBCAC) assessments may not currently be required in contracts, active solicitations are being amended to remove them, and no waivers are being granted during a 60-day program review. What did not change: NIST SP 800-171 Rev 2 remains the enforced baseline, DFARS 252.204-7012 remains in force, and Level 1 and Level 2 self-assessments posted to SPRS remain a live contract gate.

So the gap assessment is still exactly the right work, and it got more serious, because a self-assessment score is now signed and posted with no third party standing between the company and the government. The Department of Justice runs an active enforcement initiative against contractors who overstate their cybersecurity, and the False Claims Act attaches treble damages and whistleblower provisions to a false claim. The deliverable therefore shifts from "get ready for an auditor" to "produce a score every line of which is backed by evidence we could hand to the government tomorrow."

The roadmap half of the deliverable forks on the CMMC Reform Task Force, which reports around 11 September, likely inside the first two weeks of this plan. The plan handles all three outcomes:

| Task Force outcome | Roadmap response |
|---|---|
| Third-party assessment returns (as-was or modified) | The evidence chain built for the self-assessment is already C3PAO-grade; roadmap adds assessor procurement and scheduling |
| Self-assessment regime continues | Roadmap hardens the SPRS position: evidence refresh cadence, POA&M closure dates, affirmation workflow |
| A restructured framework ("CMMC 3.0") | The 800-171 Rev 2 baseline work transfers whole; roadmap re-maps deltas when the new model publishes |

The plan is deliberately built so the work of the first 90 days stays identical in all three branches until roughly day 75.

## Phase structure

| Phase | File | Theme | Anchor deliverable |
|---|---|---|---|
| Days 1 to 30 | [`days-1-30.md`](days-1-30.md) | Discover and verify | Current-state map, recalibrated 90-day contract with my manager, first visible fixes |
| Days 31 to 60 | [`days-31-60.md`](days-31-60.md) | Execute the assessment, pilot the automation | CMMC L2 self-assessment executed on the agreed boundary; continuous-monitoring pilot live on one control family |
| Days 61 to 90 | [`days-61-90.md`](days-61-90.md) | Deliver and institutionalize | Metric 1 delivered; pilot extended; team proposal; 90-day report |

## Standing assumptions

- Start date modeled as September 2026. If it moves, the relative day numbers hold; the Task Force collision point moves with the calendar.
- The plan assumes answers to the first four [hiring manager questions](../../findings/open-questions.md) arrive before or during week one. Where an answer would change the plan, the phase files say so at that step.
- Method throughout is the one my [compliance engine](https://github.com/tiffanidickerson437-lang/compliance-program) demonstrates: controls defined once, evidence computed from systems of record rather than screenshotted, AI drafting narratives under human approval, every status claim checkable. The engine's generic phases (discover, design, operate) are the skeleton; this plan is that skeleton dressed in Mattermost's actual calendar and obligations.

## What I will not do in the first 90 days

Stated up front because restraint is part of the plan:

- No tooling migrations. Drata stays the system of record unless and until its owner decides otherwise; automation is built to read from it, without ripping anything out mid-audit-cycle.
- No public claims changes without an owner's sign-off. Findings about public-page inconsistencies get routed with receipts, never pushed unilaterally.
- No AI anywhere near evidence. AI drafts prose for human review. Evidence is computed from systems, and anything a machine cannot re-derive does not go in the SPRS score.
