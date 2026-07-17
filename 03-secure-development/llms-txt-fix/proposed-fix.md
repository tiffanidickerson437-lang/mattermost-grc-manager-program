# Proposed fix

The fix is to publish one tree. Everything else about the file stays as it is:
the markdown serving and the `.md` suffix convention are good and should not
change.

## The problem, restated

`llms.txt` currently carries two version-labelled H2 sections:

```
# Mattermost Handbook

## 0.2.0
- [About Mattermost (90%)](https://handbook.mattermost.com/0.2.0/master.md)
  ... 22 entries total, all pinned under /0.2.0/ ...

## 0.2.1
- [Mattermost Handbook](https://handbook.mattermost.com/readme.md)
  ... 281 entries total, all on the current, unversioned paths ...
```

A machine has no way to know that `0.2.1` supersedes `0.2.0`. Both are just H2
sections, so both get read.

## Option 1 (recommended): publish only the current tree

Drop the legacy `0.2.0` section and publish a single index built from the live
pages.

Before:

```
# Mattermost Handbook

## 0.2.0
- [About Mattermost (90%)](https://handbook.mattermost.com/0.2.0/master.md)
  ... 21 more legacy entries ...

## 0.2.1
- [Mattermost Handbook](https://handbook.mattermost.com/readme.md)
  ... 280 more live entries ...
```

After:

```
# Mattermost Handbook

> The complete handbook index. Markdown versions of any page are available by
> appending .md to its URL.

## Docs
- [Mattermost Handbook](https://handbook.mattermost.com/readme.md)
  ... the 281 live entries ...
```

Notes:

- The H2 heading does not need to be a version number. The convention uses
  topic labels such as "Docs" and "Optional". A plain "Docs" heading is clearer
  than a version and cannot be mistaken for a second tree. If you want the
  version visible, put it in the summary line or an HTML comment, not in a
  second H2 section.
- Whatever generates this file should emit exactly one tree per publish. If the
  generator appends a new version section on each release, that is the root
  cause, and the fix is to make it replace the tree rather than append a new
  one.

## Option 2: keep both, but mark which is canonical

If there is a reason to keep the legacy tree reachable, make the current one
unambiguous to a machine. The convention does not define a "canonical version"
field, so the clearest signal is structural:

- Put the live tree first under a plain topic heading (`## Docs`), and move the
  legacy tree under an explicitly named heading such as
  `## Archived (0.2.0, do not use)`, so no heading is a bare version number, or
- Serve the legacy tree at its own URL, for example
  `handbook.mattermost.com/0.2.0/llms.txt`, and leave the root `llms.txt` with
  the current tree only.

Option 1 is simpler, and it is what I would do.

## How to confirm the fix

Run the checker in this folder against the file:

```
python3 validate_llms_txt.py
```

It exits 1 today because two version trees are present. Once the file carries a
single tree, it exits 0. That is the whole acceptance test, and it needs no
change to the checker.
