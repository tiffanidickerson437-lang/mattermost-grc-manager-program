# Mattermost GRC: Day One

My working repo for the GRC Manager role at Mattermost. Everything here exists so that on my first day I am executing, and before that, so I walk into every interview conversation already carrying the plan.

## Why this repo exists

The role's job description was published on 2 July 2026. Its first success metric reads, verbatim: *"CMMC Level 2 gap assessment and readiness roadmap delivered within first 90 days."* Eleven days after it was posted, the DoW CIO suspended CMMC's third-party assessment phase. In the same ten-week window, FedRAMP renamed its entire designation scheme, shipped a consolidated machine-readable ruleset, and opened its 20x submission pipeline.

In short: the ground under this job moved between the day the req was written and the day someone will start it. A generic onboarding plan would execute the old world. This repo holds a plan built for the world as it actually is, with explicit decision points for the ways it may move again.

The method behind the plan is my compliance engine, [`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program): controls defined once as code, evidence computed from systems of record, AI drafting under human approval, CI proving all of it. This repo applies that method to Mattermost specifically, with the company's actual calendar, obligations, and tooling filled in.

## How to read this repo

| Where | What | Read it when |
|---|---|---|
| [`30-60-90/`](30-60-90/) | The first-90-days plan, phase by phase, mapped to the role's five published success metrics | Before any conversation about the role |
| [`hiring-manager-questions.md`](hiring-manager-questions.md) | My questions for the hiring manager, ranked, with what each answer changes | Interview prep |
| [`context/the-role.md`](context/the-role.md) | The req decoded: metrics, requirements, and what the posting reveals | Background |
| [`context/regulatory-clock.md`](context/regulatory-clock.md) | Every date that governs the plan, past and forward | Whenever a date matters |
| [`context/mattermost-github-map.md`](context/mattermost-github-map.md) | Their GitHub org, mapped: where engineering rigor lives today and where GRC can extend it | Before day one |
| [`context/engine-bridge.md`](context/engine-bridge.md) | How the compliance engine's capabilities map onto this role's responsibilities | When connecting method to job |
| [`runbooks/`](runbooks/) | Executable work plans for the four biggest workstreams | Day one onward |

## Ground rules for everything in here

1. Every factual claim about Mattermost, CMMC, or FedRAMP traces to a public primary source, checked 16 July 2026. Where something could not be verified, it is either absent or explicitly marked as an open question.
2. Findings about Mattermost's current posture are framed as what they are: the work. A gap observed from outside is a first-90-days priority, and several of them are why this role exists.
3. This is a private working repo. It is written to be shareable in a conversation, and nothing in it depends on information that is not public.

## Status

| Item | State |
|---|---|
| Recruiter screen | Cleared |
| Hiring manager round | Scheduled (July 2026) |
| Plan basis | Public sources as of 16 July 2026 |
| Next revision trigger | CMMC Reform Task Force report (~11 September 2026) or new Mattermost disclosure |
