# Days 1 to 30: Discover and verify

Objective: know the real state of every program I now own, agree the recalibrated 90-day target in writing, and land two or three visible fixes that cost little and signal how the function will run.

A September start puts the CMMC Reform Task Force report (~11 September) inside week two. Workstream C exists to absorb it.

---

## Workstream A: People and systems (week 1)

| Action | Detail | Feeds metric |
|---|---|---|
| Manager alignment session | Walk through this plan with the hiring manager. Agree the day-90 deliverable definition in writing, especially the recalibrated CMMC target (see [open question 4](../00-governance/open-questions.md)) | 1 |
| Stakeholder tour | Security leadership, security operations, product security, the federal subsidiary's leadership, sales and revenue ops (questionnaire flow), legal (export compliance, contracts), people ops (training and attestation) | all |
| Access requests, day one | Drata, Conveyor, the cloud consoles, ticketing, the handbook repo, SPRS (or whoever holds the SPRS relationship), the trust center admin | 3 |
| Entity scoping answer | Pin down where federal compliance lives (parent vs. Mattermost Federal, Inc.) and what that means for assessment boundaries | 1 |

## Workstream B: Inventory what exists (weeks 1 to 3)

The discipline for this phase is reading everything before changing anything.

| Inventory | What I am establishing |
|---|---|
| Drata contents | Which policies exist, review dates, attestation coverage, which automated tests are live and which are stubs |
| SOC 2 and ISO calendar | Where we are in the current Type II period, next ISO surveillance date, auditor relationships, last cycle's evidence-collection pain points |
| CMMC / 800-171 state | Any existing SSP, POA&M, SPRS score, prior gap analyses; which boundary they assumed; whether the evidence behind any posted score can be re-derived today |
| Risk register | Format, freshness, ownership, whether treatment decisions have named acceptors |
| TPRM | Vendor inventory, tiering, assessment cadence, where it lives |
| Questionnaire operation | Intake channels, answer bank location, volume, turnaround, who answers what |
| Public claims surface | Docs pages, trust center, handbook security content: one pass cataloging every public compliance claim and its source of truth |
| Contract obligations | With legal: which live contracts carry DFARS 252.204-7012 / 7021 clauses and what they currently require |

Output: a current-state map, one page per program, each ending in a red/amber/green and the single biggest risk.

## Workstream C: The regulatory response memo (week 2, timed to the Task Force report)

One memo, for the security leadership audience, that does three jobs:

1. States Mattermost's position under the suspension: what we are obligated to today (800-171 Rev 2, DFARS 7012, SPRS self-assessment currency), what we are no longer able to buy (C3PAO certification), and what we do about it (nothing panicked; the evidence standard rises, see [runbook](../04-evidence-and-audit/cmmc-l2-self-assessment.md)).
2. Reads the Task Force report the day it lands and maps its recommendations onto the roadmap fork in the [plan overview](README.md).
3. Flags the FedRAMP vocabulary change and the Class A / 20x situation as a strategy decision the company should make deliberately rather than by default. Not a recommendation yet; a decision brief with the options priced.

This memo is the first artifact the leadership team sees from the new GRC function. It should demonstrate the house style: primary sources cited, dates exact, no claim that cannot be shown.

## Workstream D: Visible early fixes (weeks 2 to 4)

These are chosen to be small, fast, and high-signal, and each one gets routed through its content owner rather than pushed unilaterally.

| Fix | What it looks like |
|---|---|
| Claims-consistency pass | The catalog from Workstream B turned into a short findings doc: public pages whose compliance claims disagree with each other or use vocabulary FedRAMP retired in May. Handed to the docs owner with exact corrections drafted and sourced |
| Questionnaire answer-bank review | A semantic-consistency pass over the public answer bank: does each answer match the control it claims? At least one probable copy-paste defect spotted from outside to verify and correct. Establishes review-gate discipline for anything customer-facing |
| Audit calendar, published internally | One page, every certification and surveillance date for the next 18 months, owners named. Kills the class of surprise where an audit window opens and evidence collection starts that week |

## Day-30 exit criteria

- [ ] Current-state map delivered and walked through with my manager
- [ ] Recalibrated day-90 deliverable agreed in writing
- [ ] Regulatory response memo delivered, Task Force report absorbed
- [ ] CMMC assessment boundary agreed (entity, systems, data flows) and the self-assessment scheduled
- [ ] Three visible fixes landed or routed with owners and dates
- [ ] Access to every system of record I need for phase two
