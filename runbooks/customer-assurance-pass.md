# Runbook: the customer-assurance pass

The procedure behind metric 4: questionnaires, trust center, and public claims brought to a single evidence-linked standard, with review gates so they stay there.

## Why this is early-priority work

Questionnaires block revenue, which makes this the workstream where the GRC function's speed is most visible to the rest of the company. It is also where inconsistency is most dangerous: answers and public claims are representations to customers, and in the federal market, representations carry legal weight. The bar for every assertion: traceable to a control or an evidence artifact, owned by someone, and reviewed before it changes.

## Pass 1: Inventory the surface (week one of the pass)

Catalog every place a compliance claim lives:

- The trust center (Conveyor) and each document in it, with its date and owner.
- The questionnaire answer bank, wherever it lives, and the intake channels questionnaires arrive through.
- Public docs pages making certification or federal-status claims.
- The handbook's public security content.
- What sales says: the deck or one-pager claims the field actually uses.

## Pass 2: Semantic consistency (the high-value pass)

This pass goes beyond checking that links resolve and asks whether each answer is true and consistent with its neighbors. Three checks per item:

1. **Internal consistency.** Does the answer contradict another answer or a published control? Long runs of identical short answers deserve the closest read; that is where copy-paste defects survive, precisely because nobody reads them closely. At least one probable defect of this class was visible from outside before day one; verifying and correcting it is an early win with a story attached.
2. **Vocabulary currency.** FedRAMP renamed its designations on 4 May 2026 (Certification, Classes A through D). Claims using retired vocabulary get corrected, and the correction note explains the rename since most readers will not know it happened.
3. **Precision on inherited status.** Where federal claims rest on a partner's certification or a platform's authorization, the wording must carry the distinction accurately. Carefully-worded true claims exist on some pages already; the pass makes that precision uniform everywhere, including in what the field says live.

Every finding routes to its content owner with the correction drafted and the source cited, so nothing changes unilaterally and every change arrives with receipts.

## Pass 3: Wire answers to evidence

The end-state for the answer bank: each answer carries a pointer to the control it rests on and, where one exists, the evidence artifact behind that control. This is the stakeholder-management pattern from [the engine](../context/engine-bridge.md): one posture, rendered per audience, from a single source of truth. Once wired, three things fall out:

- Questionnaire turnaround drops, because answers assemble from maintained parts.
- Answers stop drifting from reality, because they update when the control state updates.
- The AI-assist question becomes safe: a model can draft a response from evidence-linked parts for human review, which is very different from a model improvising answers.

## Pass 4: Gates and cadence

- Review gate on the answer bank and trust center: no customer-facing compliance content changes without a second reviewer. The gate stays lightweight so it never becomes a bottleneck, and it applies without exception.
- Refresh cadence per artifact (bridge letters, pentest summaries, certificates) with calendar owners.
- Turnaround metric live: arrival to response, reported monthly, so metric 4 has a number.

## Done looks like

A customer asks a hard question, and the answer comes back fast, matches every public page they might check it against, and can be backed with an artifact if the deal team needs it. It works that way every time, no matter who happens to be answering.
