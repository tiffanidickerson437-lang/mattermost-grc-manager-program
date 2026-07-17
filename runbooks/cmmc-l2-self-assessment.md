# Runbook: CMMC Level 2 self-assessment under the suspension

The procedure behind metric 1. Written for the regime as it stands after 13 July 2026 and built to survive the September Task Force outcome.

## Ground truth first

- **What is enforced today:** NIST SP 800-171 **Rev 2** (the suspension procedures name Rev 2 explicitly), via CMMC Level 1 and Level 2 self-assessment and select government-led assessments. DFARS 252.204-7012 (safeguarding + 72-hour incident reporting) remains fully in force. DFARS 252.204-7021 remains a contract gate.
- **What cannot currently be bought:** a C3PAO certification. Contracts may not require one during the review; active solicitations are being amended to remove the requirement; no waivers.
- **What that means for rigor:** the score we post to SPRS is a signed claim to the federal government with False Claims Act exposure and an active DOJ enforcement initiative behind it. The absent auditor raises the internal evidence bar; nothing about the suspension lowers it.

## Step 1: Boundary (this decides everything)

Document the assessment boundary before assessing anything:

1. Which entity holds the DFARS-clause contracts (parent, the federal subsidiary, or both) — from the day-one entity answer.
2. Where CUI actually lives and flows: systems, storage, processing, the people with access, any enclave separation. If analysis shows FCI only and no CUI, that is a Level 1 conversation and the finding goes to my manager before proceeding.
3. In-boundary inventory: every system, service, and vendor inside the CUI boundary, including any inherited controls (cloud provider responsibilities documented, shared-responsibility matrices collected).

Output: a boundary document the SSP references, signed off by the manager and legal.

## Step 2: Assess all 110 requirements against 800-171 Rev 2

Per requirement, one of three dispositions, no fourth option:

| Disposition | Standard |
|---|---|
| **Met** | Backed by evidence computed from a system of record: config export, access listing, log query, screenshot only as a last resort and dated. Test: could a third party re-derive this artifact tomorrow? If not, it is not met yet |
| **Not met** | Goes on the POA&M with an owner, a date, and an interim risk note. Honest beats optimistic: an unmet requirement with a credible plan is defensible; an overstated "met" is the FCA surface |
| **Not applicable** | Documented rationale tied to the boundary. N/A without a written why is a finding waiting to happen |

Method notes:

- Use the DoD assessment methodology's scoring weights when computing the SPRS score; reconcile the arithmetic independently before anything is posted.
- Where a prior SSP, POA&M, or SPRS score exists, treat it as a claim to verify, never as a baseline to inherit. Divergence between an old score and re-derived evidence is a risk item for the manager at day 45.
- Every requirement's assessment record links: the requirement, the implementation statement, the evidence artifact, the evidence source system, and the collection date. This index is the deliverable's spine.

## Step 3: SSP and POA&M

- SSP updated or written to current state: boundary, system description, and per-requirement implementation statements that match the evidence (not aspiration).
- POA&M carries every "not met" with owner, milestone dates, and interim mitigations. The POA&M is a promise with dates; it gets a monthly review cadence from the day it exists.

## Step 4: SPRS position and affirmation

1. Compute the score; reconcile against anything previously posted and document any delta with reasons.
2. Define the affirmation workflow in writing: who signs, what evidence package they sign over, and the refresh cadence that keeps the affirmation current. The signer sees the evidence index, not a summary.
3. Nothing is affirmed that cannot be re-derived on demand. This sentence is the whole runbook.

## Step 5: The roadmap (the deliverable's second half)

Regime-aware, per the fork in the [plan overview](../30-60-90/README.md):

- **Common to all branches (through ~day 75):** close POA&M items by date, wire the highest-value requirements into the continuous-monitoring pipeline so evidence stays current without a fire drill, keep the SSP living.
- **Branch: third-party assessment returns.** The evidence chain built above is already assessor-grade. Roadmap adds C3PAO procurement, scheduling lead times, and budget.
- **Branch: self-assessment continues.** Roadmap hardens cadence: quarterly evidence refresh, affirmation renewals, and an internal adversarial review (someone whose job is to attack the score before the government could).
- **Branch: restructured framework.** The 800-171 Rev 2 baseline transfers; roadmap adds a delta-mapping exercise when the new model publishes, run through the engine's crosswalk tooling.

## Failure modes this runbook is designed against

- Inheriting a prior score's optimism. (Step 2's verify-not-inherit rule.)
- Boundary creep discovered mid-assessment. (Step 1 sign-off before step 2 starts.)
- Evidence that exists once and rots. (Step 5's monitoring hand-off.)
- A signer affirming what they have not seen. (Step 4's evidence-index rule.)
