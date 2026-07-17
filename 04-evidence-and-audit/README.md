# 06 · Evidence and audit

The instruments that run. Everything here computes rather than asserts, drafts rather than signs, and fails closed when it cannot verify.

## The instruments

| What | Where | What it does |
|---|---|---|
| Questionnaire linter | [`questionnaire-linter/`](questionnaire-linter/) | Runs against Mattermost's [live public answer bank](https://handbook.mattermost.com/operations/operations/company-policies/security-policies) and routes a human to any answer where "Yes" would be a disclosure, and to any pair of answers that contradict each other. Output: [`lint-report.md`](questionnaire-linter/lint-report.md) |
| CMMC affirmation gate | [`data/affirmation_gate.py`](data/affirmation_gate.py) | Computes an SPRS score from control state, reads [32 CFR 170](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170) live on every run, and blocks on anything unverifiable. It structurally cannot sign; the regulation gives that act to a person. Output: [`affirmation-packet.md`](affirmation-packet.md) |
| FedRAMP drift check | [`data/upstream_drift.py`](data/upstream_drift.py) | Reconciles the repo's 46-KSI map against FedRAMP's live consolidated ruleset in both directions. Output: [`upstream-conformance-receipt.md`](upstream-conformance-receipt.md) |
| Brilliant Basics map | [`data/brilliant_basics.py`](data/brilliant_basics.py) | Maps the DoW CIO's [Top 10 IT practices](https://dowcio.war.gov/BrilliantBasics/) through NIST 800-171 Rev 2 and reports what the enforced baseline can and cannot see |

## The runbooks

| File | Procedure |
|---|---|
| [`cmmc-l2-self-assessment.md`](cmmc-l2-self-assessment.md) | Executing the Level 2 self-assessment under the current suspension regime |
| [`continuous-controls-pilot.md`](continuous-controls-pilot.md) | Standing up continuous controls monitoring on one control family first |

## Trust boundary

Every checker ships mutation tests that plant a defect and confirm it gets caught, so gutting any checker to always pass turns its own suite red. Run them all from the repo root; the commands are in the [root README](../README.md#run-it). Two of the workflows in `.github/workflows/` run the gate and the drift check weekly in CI and open an issue when they cannot come back clean.
