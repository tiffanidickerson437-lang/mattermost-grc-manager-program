# Questions for the hiring manager

Ranked by how much the answer changes the job. Each entry has the question as I would ask it, why I am asking, and what the answer decides. The first four are the ones I most need answered before I could commit to a 90-day plan with confidence.

---

## 1. Where does CMMC Level 2 stand today, and is it still the target?

**Ask:** "I've heard Level 2 described as complete in one conversation, and the posting lists a gap assessment and readiness roadmap as the first 90-day deliverable. Can you walk me through where it really stands: what scope, what boundary, self-assessment or assessor-based, and for which entity? And with Phase II suspended, is CMMC still the federal target you want prioritized, or does FedRAMP move ahead of it?"

**Why:** These describe two different jobs. "Maintain a completed program" and "build the assessment from scratch" need different first months. The 13 July suspension also changed what "done" means: a completed self-assessment posted to SPRS is current and valid, while a roadmap that targeted a C3PAO assessment now points at a process that cannot currently be purchased. It also reopens the CMMC-versus-FedRAMP sequencing question that question 5 below takes up in detail.

**The answer decides:** whether my first 30 days are verification work (re-derive the evidence behind an existing SPRS score) or scoping work (define the boundary and start the assessment), and which federal target leads the 90-day plan.

## 2. Does federal compliance live in Mattermost Federal, Inc. or in the parent security org?

**Ask:** "Mattermost Federal is a separate entity with its own leadership. Does this role's federal readiness scope sit there, in the parent, or across both? And is the clearance-eligibility requirement about accessing customer environments or about signing on behalf of an entity?"

**Why:** The public GRC charter names SOC 2 as its compliance scope. The federal artifacts (the partner FedRAMP relationship, the Platform One deployment, CMMC obligations as a DIB contractor) have to live somewhere, and whether that is one program or two determines the entire operating model, plus which entity's systems are in boundary for any assessment.

**The answer decides:** whether I am building one program with two markets or two programs with a shared control library. My engine handles both, but the config differs on day one.

## 3. What is the intended future of Drata here?

**Ask:** "The handbook says policies are published and maintained in Drata. The posting asks for GRC engineering, continuous controls monitoring, and AI-native workflows. Do you see the modernization happening around Drata, through it, or eventually out of it? Has anyone already made that call?"

**Why:** This is the biggest architectural decision in the role and it may already be decided. Everything I would build (evidence pipelines, policy-as-code, control monitoring) either treats Drata as the system of record with automation layered on top, or migrates toward a git-native source of truth with Drata as one consumer. Both are viable. Ripping out a working system to satisfy a philosophy is not something I would do, so I want to know the appetite before designing anything.

**The answer decides:** the shape of the continuous-monitoring pilot in my first 60 days.

## 4. How has the 90-day expectation changed since 2 July?

**Ask:** "The first success metric was written before the CMMC Phase II suspension. How are you thinking about it now? Is the deliverable still a gap assessment and roadmap, and against which target: the current self-assessment regime, a possible return of third-party assessment, or whatever the Reform Task Force produces in September?"

**Why:** The Task Force reports roughly 11 September, which lands inside the first two weeks of a September start. The 800-171 Rev 2 baseline is still fully enforced and DFARS 7012 never moved, so the underlying work stands regardless. But the roadmap's destination changed, and I would rather agree on the recalibrated target with you in week one than discover a mismatch in week twelve.

**The answer decides:** the day-90 deliverable definition, in writing, in my first week.

## 5. What does the FedRAMP position look like from the inside?

**Ask:** "Publicly, Mattermost's FedRAMP posture runs through a partner's package. Is the long-term intent to keep inheriting through partners, or to pursue Mattermost's own listing? I ask because two doors opened this year: the SOC 2 Type II entry path with no agency sponsor required, and the 20x submission pipeline that is open right now."

**Why:** Mattermost holds SOC 2 Type II, which since March is an accepted entry framework for a FedRAMP Class A certification obtained directly from the program office. That path comes with real limits (pilot-use scope, a two-year clock to a full class, and no reciprocity granted), so it is an option to price, and it may already have been evaluated and declined for reasons I cannot see from outside. The market context: the direct competitors hold their own package IDs.

**The answer decides:** whether federal readiness in this role means CMMC and 800-171 only, or includes building a FedRAMP certification program. Those are very different resourcing pictures.

## 6. Is there an internal AI usage policy today?

**Ask:** "I couldn't find a published internal AI policy, and I know policies live in Drata where I can't see them. Does one exist? And who currently answers when a defense customer's questionnaire asks how Mattermost governs its own AI use internally?"

**Why:** The company ships an AI product to regulated buyers and publishes AI risk guidance for customers' CISOs, so the internal-governance question will arrive through the questionnaire queue this role owns, if it has not already. The export-control angle makes it sharper than usual: staff LLM use touching EAR/ITAR-scoped data is a live policy question, and the Agents V2 approval model shipping in the product is a ready-made vocabulary for the internal policy. If none exists, drafting one is a fast, visible early win.

**The answer decides:** whether runbook four in this repo starts from zero or from review.

## 7. Who owns public compliance claims?

**Ask:** "Between docs, the trust center, the handbook, and what gets said in the field, who owns the accuracy of Mattermost's public compliance claims today? Would that consolidate under this role?"

**Why:** Public pages currently make claims in tension with each other about federal status, and some use FedRAMP vocabulary that was retired in May. That is a normal artifact of fast-moving programs without a single owner, and it is squarely the kind of thing a claims-consistency pass fixes in a week. I want to know whether fixing it is in my lane or someone else's.

**The answer decides:** whether the customer-assurance runbook includes public-claims reconciliation or hands findings to another owner.

## 8. What does "grow and lead the GRC team" mean on a headcount plan?

**Ask:** "The posting says the team grows as the program scales. Is there a headcount plan behind that, and what would trigger the first hire?"

**Why:** The five ownership areas in the GRC charter are a lot of surface for a small function. I plan and sequence very differently if the first hire is six months out versus eighteen.

**The answer decides:** how much of the 90-day plan leans on automation versus deferred hiring, and how I frame the team proposal due at day 90.

## 9. When are the next SOC 2 and ISO 27001 cycle dates?

**Ask:** "Where are we in the SOC 2 Type II period right now, and when is the next ISO surveillance audit? Any known evidence-collection pain from the last cycle?"

**Why:** Metric two is on-time audit cycles with no slippage. The calendar dictates what is urgent in month one, and last cycle's pain points tell me where continuous monitoring pays back fastest.

**The answer decides:** the audit-calendar portion of the 30-day plan, and which control family the monitoring pilot targets first.

---

## Holding for later rounds

Worth asking eventually, wrong altitude for this conversation:

- Which systems of record would the GRC function get API access to in week one (Drata, cloud consoles, HRIS, ticketing), and what is the approval path?
- How do security questionnaires arrive today (Conveyor queue, sales escalation, shared inbox) and what is the current volume and turnaround?
- What did the last pentest remediation cycle look like from the GRC side?
- Is there appetite for publishing more of the security program publicly (the handbook pattern extended to GRC artifacts), or is the posture deliberately private?

## A note on tone

None of the gap-shaped questions above are gotchas, and I will not frame them that way live. Every one of them is a version of "here is what I could see from outside; show me the inside." The gaps I found are the reason the role exists, and finding them is the first thing I will be doing on the payroll.
