# 05 · Secure development

The two handbook fixes that could be opened as pull requests against Mattermost's own repositories, written to their [contributor guidelines](https://github.com/mattermost/mattermost-handbook/tree/0.2.1/contributors). These are real artifacts, not write-ups.

| Folder | What it holds |
|---|---|
| [`codeowners-merge-gate/`](codeowners-merge-gate/) | A corrected CODEOWNERS file that adds `/operations/security/`, the branch-protection settings to turn on the review gate the handbook says is planned, and a ready PR body |
| [`llms-txt-fix/`](llms-txt-fix/) | A runnable validator that fails on the live `llms.txt` today, a saved copy of the observed file, and the proposed fix for the two conflicting handbook trees it publishes |

Each subfolder has its own README with the evidence and the exact change.

The folder number follows the engine's pillar layout; see [the engine](https://github.com/tiffanidickerson437-lang/compliance-program) for the generic version of this pillar.
