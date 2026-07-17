# companies

The single input. [`mattermost.config.yaml`](mattermost.config.yaml) describes Mattermost as one engine configuration: frameworks, stack, data types, AI posture, and risk tolerances, with every value traced to a public source checked in July 2026. [`mattermost/value.json`](mattermost/value.json) carries the company-specific narrative values the renderer uses.

The `evidence_in_repo: none` line in the config is load-bearing. No Mattermost evidence exists anywhere in this repo and none is claimed.

Everything in [`generated/`](../generated/) is rendered from this folder by the [engine](https://github.com/tiffanidickerson437-lang/compliance-program). Change the config and the program re-renders; a different company is a different config file, never a fork.
