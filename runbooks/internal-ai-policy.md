# Runbook: the internal AI usage policy

The draft outline for an internal AI policy, ready to go the moment the day-one answer to "does one exist?" comes back as no (or as "yes, but thin"). Built to speak the company's own vocabulary rather than importing a consultant template.

## Why this lands differently at Mattermost

Three facts make this policy sharper here than at a typical SaaS company:

1. **The data is not ordinary.** A meaningful slice of company data is export-controlled (EAR/ITAR) or CUI-adjacent. Staff pasting the wrong content into the wrong model is a potential export violation, which is a different league from a confidentiality slip.
2. **The customers will ask.** Mattermost sells AI to defense and regulated buyers and publishes AI risk guidance for customers' security leaders. "How do you govern AI internally?" arrives through the questionnaire queue this role owns. The answer needs to exist and be true.
3. **The company already solved the hard part, in the product.** The Agents V2 approval model (published June 2026) established the tiers: tools that must `ask` a human per call, tools that auto-run privately but need approval in shared spaces, tools safe to `auto_run_everywhere`, plus a separate decision about whether output enters shared context, and automation that fails closed when no human is in the loop. That is an AI governance policy written by their own engineers. The internal policy's job is to extend those settled principles from product to workplace.

## The outline

**1. Scope and definitions.** What counts as AI use (hosted LLMs, embedded assistants, agents including Mattermost's own, code assistants), who is covered, and what data classes exist (public, internal, customer, export-controlled/CUI-adjacent).

**2. The data rules (the non-negotiable core).**
- Export-controlled and CUI-adjacent data: only in environments approved for that data class, enumerated by name. Everything else is prohibited by default.
- Customer data: only in tooling covered by our contracts and DPAs, enumerated.
- A named path for asking "can I use X for Y?" with an answer SLA, because a policy without a fast question channel becomes a policy people route around.

**3. The approval tiers, inherited from the product's model.**
- Read-only, no side effects, output stays private: may run automatically.
- Anything with side effects or shared output: a human approves the action, and separately decides whether output enters shared context.
- Anything that asserts compliance or company position (an answer to a customer, an attestation, evidence): a human owns it, always. Drafting assistance is fine; authorship accountability does not transfer to the model.

**4. Evidence and records (the GRC-specific hard line).** AI never authors evidence. Evidence is computed from systems of record. AI-drafted narratives are labeled as drafts until a human approves them into record. (This is the same rule my [engine](../context/engine-bridge.md) enforces mechanically; the policy states it, and the tooling makes it hard to violate.)

**5. Tooling inventory and approval.** The list of approved AI tools and models, each with its data-class ceiling, plus the intake path for adding one. Shadow-AI discovery treated like shadow-IT discovery: findable, correctable, no ambushes.

**6. Vendor and model-provider risk.** AI vendors enter the same TPRM process as any vendor, with the additional questions: training-data usage, retention, tenancy, and the export-control posture of where inference runs.

**7. Incidents.** What to do when the rules break (wrong data in the wrong model): report path, containment steps, and the explicit no-blame framing that makes self-reporting rational.

**8. Review cadence.** This policy ages fast by nature; it gets a quarterly review with a named owner, and its version history lives in git.

## Rollout notes

- Draft in weeks 6 to 8, review with security leadership, legal (export control especially), and engineering; target adoption by day 90.
- Ship the one-page version alongside the full policy. The one-pager is what people actually follow; the full policy is what auditors and questionnaires consume.
- Add the corresponding answer-bank entries the same week the policy adopts, so the customer-facing answer and the internal reality are born synchronized.
