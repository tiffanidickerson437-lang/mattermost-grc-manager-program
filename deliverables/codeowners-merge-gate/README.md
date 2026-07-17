# CODEOWNERS and merge-gate patch

This folder is a small, real change I would open as a pull request against the
Mattermost handbook. The handbook is open source, so this is a patch a
maintainer could review and merge, not a proposal about work someone else has
to do.

The change closes one gap the handbook already documents about itself: it names
an owner who signs off on Security changes, but nothing in the repository routes
Security pull requests to that owner or requires their review. I add the
missing ownership rule and write down the exact settings that would turn on the
review gate the handbook says is planned.

Everything below traces to a public page or a public API response I checked on
17 July 2026. Where I could not read something from the outside, I say so and
do not guess.

## What I verified

**1. The CODEOWNERS file has three path rules.**
Live file:
[github.com/mattermost/mattermost-handbook/blob/0.2.1/CODEOWNERS](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/CODEOWNERS)
(the repository's default branch is literally named `0.2.1`). The three rules
are:

```
/operations/legal/ @it33
/operations/finance/ @TQuock
/operations/operations/company-processes/ @it33
```

**2. The handbook names @dschalla as the Security sign-off, but no rule covers Security.**
The contributor guide, under "Official Handbook reviewers," reads:
"8. @dschalla: Signs off on changes to Security." Live page:
[company/how-to-guides-for-staff/how-to-update-handbook.md](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/company/how-to-guides-for-staff/how-to-update-handbook.md).
The Security section it points to is a real directory with real content
(`README.md`, `policies.md`, `privacy/`, `product-security/`,
`security-operations/`):
[operations/security](https://github.com/mattermost/mattermost-handbook/tree/0.2.1/operations/security).
None of the three CODEOWNERS rules match that path, so a change to a Security
page does not automatically request @dschalla's review.

**3. The handbook says the review gate is planned, not yet in place.**
The same contributor guide states: "Each PR should be reviewed by at least one
approved reviewer. A build check requiring at least one approved review prior to
a merge is planned, similar to other Mattermost repositories." Same live page as
above.

**4. There are no CI workflows yet, so there is no status check to require.**
`gh api repos/mattermost/mattermost-handbook/actions/workflows --jq '.total_count'`
returns `0`. Public Actions tab:
[github.com/mattermost/mattermost-handbook/actions](https://github.com/mattermost/mattermost-handbook/actions).
This matters for the branch-protection step: you cannot require a status check
that does not exist, so one has to be added before it can be required.

**5. The default branch reports as protected, but I cannot read its protection detail from outside.**
`gh api repos/mattermost/mattermost-handbook/branches/0.2.1` returns
`"protected": true`. The protection-detail endpoint
(`.../branches/0.2.1/protection`) returns `404 Not Found` to my token, which is
expected without admin or maintainer access on the repository. So I do not
assert what is or is not enforced today. What I rely on instead are two facts I
can see: the handbook's own "planned" wording, and the zero-workflow count that
means there is currently no check to enforce.

For scale, the repository holds 354 Markdown files, and CODEOWNERS carries three
path rules. Most of the tree, including Security, is not routed to a named owner.

## What the patch changes

The core of it is one line, grounded in the handbook's own prose:

```
/operations/security/ @dschalla
```

The trailing slash makes the rule recursive, so it covers the Security
directory and everything under it (`privacy/`, `product-security/`,
`security-operations/`). That matches the style of the existing rules.

I also include an optional, clearly commented line that gives the CODEOWNERS
file itself a named owner, so ownership rules cannot be changed without a review
from someone on the documented write-access list. It is easy to drop if a
maintainer would rather not add it.

## An honest note on how the two pieces fit

A CODEOWNERS rule only has teeth when branch protection is set to require code
owner review, and when the named owner actually has access to review in the
repository. The handbook lists write permissions for @jasonblais, @amyblais, and
@cwarnermm; @dschalla is named as the Security sign-off in prose but is not on
that documented write list. So the CODEOWNERS line and the branch-protection
settings are a pair, and access for the named owner is part of making the gate
real. I did not want to imply that one line enforces itself.

## Files in this folder

- `proposed-CODEOWNERS` — the corrected CODEOWNERS file: the three real rules,
  plus the Security rule and the optional self-protection line, each commented.
- `branch-protection.md` — the exact GitHub settings and `gh api` calls to turn
  on required review and, once a check exists, required status checks.
- `PR-body.md` — a pull-request description written to the handbook's own
  contributor guide and PR template, for a maintainer to read.

## Scope

These four files are the artifact. I have not opened a pull request against
`mattermost/mattermost-handbook`; whether and when to submit it is not my call
to make from here.
