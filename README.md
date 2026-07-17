# Mattermost, onboarded

This repo is Mattermost already running through my compliance engine, [`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program), before day one. The engine's premise is that one configuration file drives the whole program: controls defined once and rendered into every framework's view, evidence computed from systems of record, AI drafting under human approval, coverage computed rather than asserted. So instead of describing what I would do here, this repo does it.

```
companies/mattermost.config.yaml        one file: Mattermost's frameworks, stack,
        │                               data types, AI posture, risk tolerances,
        │                               all from public sources
        ▼
tools/scaffold.py            ──────▶    generated/in-scope-controls.yaml
  filters the engine's                  45 controls selected, each with the reason
  Living Control Set                    it is in scope and the frameworks it satisfies
        │                               generated/profile-selection.yaml
        ▼                               the per-framework OSCAL profile selection
tools/onboard_company.py     ──────▶    generated/companies/mattermost/data.json
  + companies/mattermost/value.json     the fully rendered program: pillars, controls
  (friction research, the real          with Mattermost-specific narratives, friction
  30/60/90, collateral)                 points, roadmap, stack, guardrails
```

Change the config and the program re-renders. Adding a framework is a crosswalk mapping, never a rebuild. That is the operating model the GRC Manager posting asks for, demonstrated on Mattermost itself.

## What the engine resolved for Mattermost

| | |
|---|---|
| **Frameworks in scope** | SOC 2 and ISO 27001:2022 as held certifications on annual cycles; NIST 800-53, NIST AI RMF, ISO 42001, and GDPR as the obligations and build targets this role owns |
| **Controls selected** | 45 from the Living Control Set, each carrying the reason it is in scope; the minors-consent control is correctly excluded from the rendered program because Mattermost does not process children's data |
| **Hero surfaces** | MON-01 (continuous monitoring, the drift-opens-a-ticket loop) and the evidence-and-audit pillar, because the posting's center of gravity is replacing manual evidence collection with continuous controls monitoring |
| **Stack as evidence sources** | GitHub, Jira, GitBook, Drata, and Mattermost itself, all named from their public handbook and org; the IdP is deliberately unset until discovery confirms it |
| **The federal obligation, mapped** | NIST 800-171 Rev 2 is Mattermost's most time-sensitive obligation under the CMMC suspension, and it is now carried in the engine as a first-class framework. All 110 requirements resolve to 36 controls, and the [SPRS-weighted self-assessment workbook](assessment/nist-800-171-rev2-workbook.md) is rendered and ready to walk. The instrument most programs would spend month two building is already in this repo |

## Why this repo exists

The GRC Manager posting was published prior to the DoW CIO's suspension of CMMC's third-party assessment phase, and its first success metric, a CMMC Level 2 gap assessment and readiness roadmap in 90 days, was written for the regime that suspension changed. In the same ten-week window, FedRAMP renamed its designation scheme, shipped a consolidated machine-readable ruleset, and opened its 20x submission pipeline with the words "continuous evidence of what is happening is stronger than a policy saying it should happen." The regulators now write the thesis this engine was built on.

So the plan in this repo is regime-aware by construction: it holds the same evidence standard through every branch of the September Task Force outcome, and it treats the suspension as what it is, a transfer of the assessment burden in-house that raises the bar for computed, re-derivable evidence.

## How to read this repo

| Where | What |
|---|---|
| [`companies/mattermost.config.yaml`](companies/mattermost.config.yaml) | The single input: Mattermost expressed as an engine configuration, every value traced to public sources |
| [`companies/mattermost/value.json`](companies/mattermost/value.json) | The value overlay: six friction points from the research, the real 30/60/90, and the collateral map |
| [`assessment/`](assessment/) | The federal readiness instruments: the [110-requirement 800-171 workbook](assessment/nist-800-171-rev2-workbook.md) with SPRS weights, and the [46-KSI FedRAMP 20x map](assessment/fedramp-20x-ksi-map.md). Both generate from source-of-truth data by `assessment/data/render.py` |
| [`generated/`](generated/) | What the engine rendered: the in-scope control selection with reasons, the OSCAL profile selection, and the full Mattermost data payload |
| [`30-60-90/`](30-60-90/) | The first-90-days plan in full, phase by phase, mapped to the role's five published success metrics |
| [`hiring-manager-questions.md`](hiring-manager-questions.md) | The questions whose answers change the plan, ranked, with what each answer decides |
| [`runbooks/`](runbooks/) | Executable procedures: the L2 self-assessment under the suspension, the continuous-monitoring pilot, the customer-assurance pass, the internal AI policy |
| [`context/`](context/) | The req decoded, the regulatory clock, Mattermost's GitHub org mapped, the [full framework landscape](context/framework-landscape.md), and the engine bridge |

## Ground rules

1. **Public sources only.** Every claim about Mattermost, CMMC, or FedRAMP traces to a public primary source checked 16 July 2026, and no claim is made about Mattermost's internal security posture. Where something could not be verified it is absent or marked as an open question.
2. **Gaps are the work, never the criticism.** Everything observed from outside is framed as a first-90-days priority, because finding and closing exactly these things is what the role is for.
3. **Evidence is computed, never authored.** No Mattermost evidence exists in this repo and none is claimed. The `evidence_in_repo: none` line in the config is load-bearing: evidence begins computing on day one, inside their boundary, from their systems of record.

## Regenerating

```bash
# from a compliance-program clone
python3 tools/scaffold.py <this-repo>/companies/mattermost.config.yaml
ENGINE_ROOT=<clone> OUTPUT_ROOT=<this-repo> \
  python3 tools/onboard_company.py --config <this-repo>/companies/mattermost.config.yaml --slug mattermost
```

The run is deterministic: same config, same library, same output. That property is the whole point.
