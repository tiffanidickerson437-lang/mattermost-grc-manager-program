# Turning on the review gate

The handbook says a merge gate is planned: "A build check requiring at least one
approved review prior to a merge is planned, similar to other Mattermost
repositories." Source:
[company/how-to-guides-for-staff/how-to-update-handbook.md](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/company/how-to-guides-for-staff/how-to-update-handbook.md).

This file is the exact settings that turn that gate on, in the order they have
to happen. Everything here targets the default branch, `0.2.1`, and needs admin
or maintainer access on the repository to apply.

## What I can observe from outside

- The `0.2.1` branch reports `"protected": true`
  (`gh api repos/mattermost/mattermost-handbook/branches/0.2.1`).
- The protection-detail endpoint returns `404 Not Found` to a non-admin token
  (`gh api repos/mattermost/mattermost-handbook/branches/0.2.1/protection`),
  which is expected without admin access, so I cannot read the current rule set
  from the outside and do not assert it.
- There are no CI workflows:
  `gh api repos/mattermost/mattermost-handbook/actions/workflows --jq '.total_count'`
  returns `0`. That is why step 2 below has to add a check before it can require
  one.

## Step 1 — require a pull-request review, including code owner review

This is the piece that makes the CODEOWNERS change actually bite. It requires at
least one approving review on every PR to `0.2.1`, and, because
`require_code_owner_reviews` is on, a review from the owner named in CODEOWNERS
when a matching path changes (so @dschalla for anything under
`/operations/security/`).

The branch-protection API replaces the whole configuration in one call, so all
four top-level keys have to be present, even when null. Put the body in a file
and pass it with `--input` rather than scattering `-f` flags.

`protection.json`:

```json
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}
```

Apply it:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  repos/mattermost/mattermost-handbook/branches/0.2.1/protection \
  --input protection.json
```

Notes on the choices:

- `required_approving_review_count: 1` matches the handbook's own wording ("at
  least one approved reviewer").
- `require_code_owner_reviews: true` is the switch that connects branch
  protection to CODEOWNERS. Without it, the CODEOWNERS file is documentation
  only.
- `dismiss_stale_reviews: true` re-requests review if new commits land after
  approval. It is a reasonable default and can be set to `false` if the team
  prefers.
- `enforce_admins: false` keeps this from blocking the write-access holders in
  an emergency. Set it to `true` if the team wants the rule to apply to
  everyone.
- For the CODEOWNERS routing to work in practice, the named owner needs review
  access on the repository. @dschalla is named as the Security sign-off in the
  handbook prose but is not on the documented write-access list, so confirming
  his access is part of this step.

## Step 2 — add a check, then require it

`required_status_checks` is `null` above on purpose: there are zero workflows
today, and you cannot require a status check that does not exist. So a minimal
check has to be added first.

A lightweight, low-risk check for a docs repository is Markdown lint or link
checking on pull requests. Add a workflow such as
`.github/workflows/lint.yml` that runs on `pull_request` and reports a named
check (for example, `markdown-lint`). Once that workflow has run on at least one
PR so GitHub knows the check name, require it by re-applying the protection with
the check filled in.

`protection-with-checks.json`:

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["markdown-lint"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}
```

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  repos/mattermost/mattermost-handbook/branches/0.2.1/protection \
  --input protection-with-checks.json
```

`strict: true` means a branch has to be up to date with `0.2.1` before it can
merge. `contexts` has to match the exact check name the workflow reports.

## Doing it in the UI instead

The same settings live under Settings, then Branches, then the `0.2.1` branch
protection rule:

- Require a pull request before merging, with 1 required approval.
- Require review from Code Owners.
- Require status checks to pass before merging (after the check exists), and
  select the check by name.

## Payload reference

The request-body shape above is from GitHub's live REST documentation for
"Update branch protection":
[docs.github.com/en/rest/branches/branch-protection](https://docs.github.com/en/rest/branches/branch-protection?apiVersion=2022-11-28).
The four top-level keys (`required_status_checks`, `enforce_admins`,
`required_pull_request_reviews`, `restrictions`) are all required and each is
nullable.
