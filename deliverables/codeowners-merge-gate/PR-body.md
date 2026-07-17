#### Summary

This adds a CODEOWNERS rule for Security so that changes under
`/operations/security/` request a review from the owner the handbook already
names for that area.

The contributor guide, under "Official Handbook reviewers," lists:
"8. @dschalla: Signs off on changes to Security"
([how-to-update-handbook.md](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/company/how-to-guides-for-staff/how-to-update-handbook.md)).
The current CODEOWNERS file has three rules, and none of them cover
`operations/security`
([CODEOWNERS](https://github.com/mattermost/mattermost-handbook/blob/0.2.1/CODEOWNERS)),
so today a change to a Security page does not automatically route to @dschalla.
This change lines the file up with what the guide already says.

#### What changed

- Added `/operations/security/ @dschalla`. The trailing slash makes it
  recursive, so it covers `operations/security` and its subdirectories
  (`privacy/`, `product-security/`, `security-operations/`), matching the style
  of the existing rules.
- Added an optional line giving `CODEOWNERS` itself a named owner
  (`@jasonblais @amyblais @cwarnermm`, the write-access holders listed in the
  contributor guide), so ownership rules cannot be changed without a review.
  Happy to drop this line if you would rather not include it.

The three existing rules are unchanged.

#### A note for reviewers

A CODEOWNERS rule only takes effect once branch protection on `0.2.1` requires
code owner review. The guide notes that a required-review build check is planned
("A build check requiring at least one approved review prior to a merge is
planned"). If it is useful, I have written up the exact branch-protection
settings and `gh api` calls to enable that, in a companion file. Two small
dependencies worth flagging: a status check has to exist before it can be
required (the repository currently has no CI workflows), and @dschalla would
need review access on the repository for the routing to work in practice, since
he is named as the Security sign-off in prose but is not on the documented
write-access list.

#### Contributor checklist

- I have read the handbook update guide:
  [How to update the handbook](https://handbook.mattermost.com/company/how-to-guides-for-staff/how-to-update-handbook)
  and the
  [contribution guidelines](https://github.com/mattermost/mattermost-handbook/tree/0.2.1/contributors).
- I have signed, or will sign, the
  [Mattermost Contributor Agreement](https://mattermost.com/mattermost-contributor-agreement/).
- This change touches only `CODEOWNERS`; it does not add, remove, or move any
  handbook page, so no `SUMMARY.md` or redirect update is needed.
