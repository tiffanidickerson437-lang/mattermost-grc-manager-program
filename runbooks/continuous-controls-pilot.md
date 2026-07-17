# Runbook: the continuous-controls-monitoring pilot

The procedure behind metric 3. One control family, end to end, in 30 days, producing the artifact the next audit consumes.

## Design principles

1. **Read from systems of record; write around nothing.** Drata remains the system of record for policies and its existing tests. The pilot adds computed evidence where humans currently collect by hand, and feeds status back where the team already looks.
2. **Evidence only counts when it is computed.** Every artifact the pilot produces comes from an API call or query against the source system, is validated against a schema, and carries its collection timestamp and source. Nothing is hand-assembled and nothing is AI-authored, since drafts and narratives live in a different lane entirely.
3. **Drift is a ticket the day it happens.** The pilot's monitor runs on a schedule; a failed check opens a tracked item with the failing evidence attached. The open ticket is itself the due-diligence record.
4. **Success is counted in retired manual work.** The pilot ends with a number: these N evidence items, previously collected by hand each cycle, now compute on schedule.

## Choosing the family

Decided by the day-30 inventory, on three inputs: where last audit cycle's evidence pain was worst, which family the next audit window needs freshest, and which sources offer clean API access on day one. The usual winner is access review (joiner/mover/leaver evidence, privileged access listings, MFA state); asset or vendor inventory is the usual runner-up.

## Build sequence (roughly two weeks of build inside the 30)

| Step | Work |
|---|---|
| 1. Define | For each control in the family: what checks, against which system of record, what schema the evidence must satisfy, what threshold means drift |
| 2. Wire | Read-only credentials to the source systems, requested through the standard access process, scoped to least privilege, inventoried |
| 3. Compute | Scheduled collection producing schema-validated artifacts to a versioned store with history |
| 4. Gate | Validation failure or threshold breach opens the ticket automatically, assigned to the control owner |
| 5. Render | Status summary lands where the team already works (a channel post; later, if the pattern earns it, a Playbook run per drift event, which is the native Mattermost shape for process) |

## The pilot's exit report

One page: controls covered, evidence items automated (the before/after count), drift events caught during the pilot with time-to-ticket, false-positive rate, and the cost honestly stated (build hours, run cost, review overhead). Plus the extension list: which families are next and what each needs.

## What this is deliberately not

- Not a Drata replacement, and not a shadow GRC system. The architecture question is decided in the [60-day memo](../generated/30-60-90/days-31-60.md) with its owner in the room, on the pilot's real data.
- Not an AI project. The pipeline is deterministic. AI enters only where it belongs: drafting the remediation narrative on a drift ticket for a human to review, never producing the evidence.
- Not a big-bang. One control family proven end to end teaches more and earns more trust than five families sketched in parallel.
