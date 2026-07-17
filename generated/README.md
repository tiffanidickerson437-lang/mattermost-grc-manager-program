# generated

The config that describes Mattermost, and what the [engine](https://github.com/tiffanidickerson437-lang/compliance-program) rendered from it. The rendered files are outputs; edit the config and re-render rather than editing them by hand.

| File | What it is |
|---|---|
| [`companies/mattermost/mattermost.config.yaml`](companies/mattermost/mattermost.config.yaml) | The single input: Mattermost as one engine configuration, every value traced to a public source |
| [`companies/mattermost/value.json`](companies/mattermost/value.json) | The company-specific narrative values the renderer uses |
| [`in-scope-controls.yaml`](in-scope-controls.yaml) | The 45 controls the config put in scope, each carrying the reason it is in scope and the frameworks it satisfies |
| [`profile-selection.yaml`](profile-selection.yaml) | Which engine profiles the config selected and why |
| [`companies/mattermost/data.json`](companies/mattermost/data.json) | The fully rendered program: pillars, controls with Mattermost-specific narratives, and the roadmap |
| [`engine-bridge.md`](engine-bridge.md) | How this instance connects to the public engine |

The `evidence_in_repo: none` line in the config is load-bearing. No Mattermost evidence exists anywhere in this repo and none is claimed. Change the config and the program re-renders; a different company is a different config file, never a fork.
