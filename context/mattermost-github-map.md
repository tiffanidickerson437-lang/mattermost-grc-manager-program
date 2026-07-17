# Mattermost on GitHub, mapped

What their public GitHub org tells a GRC operator. Surveyed via the GitHub API on 16 July 2026. Org: [github.com/mattermost](https://github.com/mattermost), 263 public repositories, on GitHub since 2014.

## The repos that matter for this role

| Repo | What it is | GRC relevance |
|---|---|---|
| [`mattermost/mattermost`](https://github.com/mattermost/mattermost) | The product monorepo (server + webapp), ~38k stars, default branch `master` | The engineering culture benchmark: 86 GitHub Actions workflows, a real `SECURITY.md` routing researchers to responsibledisclosure@, a mandatory upgrade policy (updates for the latest 3 releases plus the current ESR), and security-update details announced 30 days after availability |
| [`mattermost/mattermost-handbook`](https://github.com/mattermost/mattermost-handbook) | The company handbook source (GitBook), default branch `0.2.1` | Where governance content lives as code. Currently: no CI workflows, CODEOWNERS with three path rules none of which cover `/operations/security/`, and a required-review build check described in the handbook itself as planned. The handbook's security policies page points to Drata for the actual policies |
| [`mattermost/mattermost-security`](https://github.com/mattermost/mattermost-security) | Small security tooling repo, dormant since 2023 | Contains an exported Security Vulnerability Playbook JSON: their vuln process, shipped as an importable artifact |
| [`mattermost/mattermost-plugin-playbooks`](https://github.com/mattermost/mattermost-plugin-playbooks) | Playbooks: repeatable, checklist-driven process runs inside Mattermost | They dogfood this for security processes. Any process artifact the GRC function ships (incident steps, audit prep, drift response) can ship as a Playbook and feel native |
| [`mattermost/mattermost-plugin-agents`](https://github.com/mattermost/mattermost-plugin-agents) | The Agents plugin (multi-LLM) | The product home of the Agents V2 approval model: per-tool policies (`ask`, `auto_run_in_dm`, `auto_run_everywhere`), initiator-owned approval, a separate share/keep-private decision, and automation that fails closed. This is the company's own HITL vocabulary, and the natural frame for an internal AI policy |
| [`mattermost/docs`](https://github.com/mattermost/docs) | Product documentation source | Where the public compliance claims live in git. The claims-consistency findings from the first 30 days route here as concrete PRs, which is the tidiest possible form for that conversation |
| [`mattermost/mattermost-helm`](https://github.com/mattermost/mattermost-helm), [`mattermost-operator`](https://github.com/mattermost/mattermost-operator) | Kubernetes deployment surface | The self-hosted/regulated deployment story (STIG-hardened, FIPS images as of v11) is delivered through these. Configuration baselines here are future evidence sources |
| [`mattermost/mattermost-developer-documentation`](https://github.com/mattermost/mattermost-developer-documentation) | developers.mattermost.com source | Secure SDLC content and contributor process live here and in the handbook |

## The pattern a GRC operator should notice

The product side runs like a serious engineering organization: dozens of CI workflows on the monorepo, disclosure policy in the repo, monthly releases, an ESR discipline, public security advisories with patches. The governance side publishes as code (handbook in git, docs in git, markdown everywhere, an `llms.txt` machine index) but does not yet enforce as code: the merge gates, ownership rules, and automated checks that protect the product do not yet protect the governance content, and the policies themselves live in Drata rather than in the git surface.

That is not a criticism; it is the job. The plumbing for policy-as-code is already there and already culturally normal at this company. The work is extending the enforcement patterns the product side proved onto the governance surface, and deciding deliberately what stays in Drata versus what renders from source. Which is, almost word for word, what the posting asks for.

## Useful cultural signals

- Their engineering blog demonstrates LLM evaluation work in their own toolchain (extending `go test` for LLM evaluation). The engineering organization is already fluent in the AI-quality conversation the GRC function will need to have.
- Everything public is PR-driven, including the handbook, and outside contributors are normal. A GRC function that ships findings as pull requests with sources will read as native rather than foreign.
- Their own product vocabulary (Playbooks for process, Agents approval tiers for automation trust) gives the GRC program ready-made, internally legitimate names for its operating patterns. Speaking it beats importing consultant vocabulary.
