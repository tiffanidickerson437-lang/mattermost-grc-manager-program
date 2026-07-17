# Days 31 to 60: Execute the assessment, pilot the automation

Objective: run the CMMC Level 2 self-assessment on the agreed boundary to an evidence standard a third party could re-derive, and prove the continuous-monitoring model on one control family end to end.

---

## Workstream A: The CMMC Level 2 self-assessment (metric 1)

Full procedure in the [runbook](../04-evidence-and-audit/cmmc-l2-self-assessment.md). The shape of it:

| Step | Detail |
|---|---|
| Boundary locked | The scoping decision from day 30 documented as the assessment boundary: systems, data flows, people, and the CUI (or FCI-only) determination that drives Level 1 vs. Level 2 treatment |
| Assess against 800-171 Rev 2 | Rev 2 is what the Department currently enforces, stated explicitly in the suspension procedures. Requirement by requirement, three dispositions: met with evidence, not met (POA&M), not applicable (documented) |
| Evidence standard | Every "met" is backed by an artifact computed from a system of record: a config export, an access listing, a log query. If the evidence cannot be re-derived on demand, the requirement is not met yet. This is the FCA-aware standard the suspension made necessary |
| SSP and POA&M | The System Security Plan updated (or written) to describe the boundary and each requirement's implementation; the POA&M carrying every gap with an owner and a date |
| SPRS scoring | Score computed per the DoD assessment methodology, reconciled against anything previously posted, and the affirmation workflow documented: who signs, on what evidence, on what cadence |

Decision point at day 45: if the inventory found a previously posted SPRS score whose evidence cannot be re-derived, that goes to my manager as a risk item with options, before anything is re-affirmed.

## Workstream B: The continuous-monitoring pilot (metric 3)

Full procedure in the [runbook](../04-evidence-and-audit/continuous-controls-pilot.md). Design constraints:

- One control family, chosen where last cycle's audit pain was worst (access review is the usual winner, asset inventory the usual runner-up; the day-30 inventory decides).
- Drata stays the system of record. The pilot reads from it and from the underlying systems; it does not write around it. The architecture decision memo (below) is where any bigger change gets decided.
- The pilot's output is the artifact the next audit consumes: evidence generated on schedule, validated against a schema, with drift surfacing as a ticket the same day it happens rather than at audit time.
- Success is measured in retired manual work: named evidence items that no human collects by hand anymore.

## Workstream C: The architecture decision memo (weeks 6 to 8)

The Drata question from the [hiring manager questions](../00-governance/open-questions.md) answered as a formal decision brief, informed by 30 days of living in the real stack:

1. What Drata does well here today, kept.
2. What the pilot proved about computing evidence directly from systems of record.
3. Three options priced (automate around Drata, deepen Drata's own automation, migrate toward git-native policy and control definitions with Drata as a consumer) with cost, risk, and audit-continuity implications for each.
4. A recommendation, and the explicit note that mid-cycle migrations are off the table for the current audit period regardless of the choice.

## Workstream D: Two policy artifacts (metric 4, metric 2)

| Artifact | Why now |
|---|---|
| Internal AI usage policy, drafted | If the day-one answer was "none exists," this is the fastest meaningful gap to close. Drafted using the approval-tier vocabulary the product itself shipped in Agents V2, so the policy speaks the company's own language. Outline in the [runbook](../02-ai-governance/internal-ai-policy.md). Routed for review, targeted for adoption by day 90 |
| Vulnerability-process control family | Mattermost's published Product Vulnerability Process is genuinely strong. This step adopts it into the GRC control library as a proper control family with evidence expectations, so the next audit inherits what product security already does well instead of re-documenting it |

## Workstream E: Audit cycle steady-state (metric 2)

- Evidence freshness check against the audit calendar from phase one: everything due in the next 90 days identified and owner-assigned now.
- Auditor touchpoint: introduce myself as the new single point of contact, confirm scope and dates for the next SOC 2 period and ISO surveillance visit.

## Day-60 exit criteria

- [ ] Level 2 self-assessment executed across the full 110 requirements on the agreed boundary
- [ ] SSP current; POA&M live with owners and dates; SPRS position reconciled and documented
- [ ] Monitoring pilot producing schema-valid evidence on schedule for one control family, with at least one real drift event caught and ticketed
- [ ] Architecture decision memo delivered
- [ ] AI usage policy in review; vulnerability control family drafted
- [ ] No audit calendar item inside 90 days without a named owner
