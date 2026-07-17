# llms.txt split-tree fix

Short version: Mattermost publishes a machine-readable index of its handbook at
[handbook.mattermost.com/llms.txt](https://handbook.mattermost.com/llms.txt),
and that one file carries two versions of the index at the same time. An AI
agent reading it cannot tell which version is current, so it reads both.

I verified everything below against the live file on 17 July 2026.

## What llms.txt is

llms.txt is a plain-text file a website publishes to tell large language model
agents which pages to read. It is a simple convention: an H1 title, an optional
summary line, then H2 sections, each with a list of links to the pages that
matter. An agent can read one short file instead of crawling the whole site.

Mattermost goes further than most vendors here. The file is served as
`text/markdown`, and every page it lists is available as clean markdown by
appending `.md` to the URL. That part is genuinely useful and ahead of where
most handbooks are. The problem is not the idea; it is that the file ships two
copies of the index.

## The defect

The file publishes two version trees at once, with nothing that tells a machine
which one is live:

- `## 0.2.0` — 22 entries. Every link is pinned to a versioned path, for
  example `handbook.mattermost.com/0.2.0/master.md`.
- `## 0.2.1` — 281 entries. Every link points to the current, unversioned path,
  for example `handbook.mattermost.com/company/about-mattermost.md`.

That is 303 link entries in one file, split across two version-labelled
sections. The convention treats an H2 heading as a section label, so a parser
reads `0.2.0` and `0.2.1` as two ordinary sections and ingests both. There is
no marker — no "current", no "deprecated", no canonical field — that says which
tree to trust.

The two trees are not just duplicate links. They describe the same pages with
different content. The 0.2.0 "About Mattermost" page and the live one are
different documents (about 16.5 KB against 11.8 KB when I fetched them), so an
agent that reads both ends up holding two conflicting descriptions of the
company.

## Why it matters

Mattermost sells AI agents into defense and other regulated markets, where an
agent's answers have to trace back to a single, current source. A public index
that hands every agent two versions of the handbook works against that, and it
is the kind of thing a buyer's own tooling will flag. It is also a small,
contained fix.

## What is in this folder

- `validate_llms_txt.py` — a runnable checker (standard library only) that
  fetches the file, or reads a local copy with `--file`, and exits non-zero
  when two or more version trees are present.
- `test_validate_llms_txt.py` — tests with small inline fixtures: a dual-tree
  file that must fail, a single-tree file that must pass, and a standard
  topic-section file that must also pass, so the checker does not fire on a
  normal index.
- `observed-llms.txt` — the copy of the live file I checked, so the checker has
  an offline target and there is a record of what I saw.
- `proposed-fix.md` — the concrete before-and-after fix a maintainer could
  apply.

## Running it

```
python3 validate_llms_txt.py                          # check the live file
python3 validate_llms_txt.py --file observed-llms.txt # check the saved copy, offline
python3 -m unittest test_validate_llms_txt -v         # run the tests
```

When I ran it against the live file it found 22 entries under `0.2.0` and 281
under `0.2.1`, and exited 1. The checker fails on the file as it stands today.
If Mattermost publishes a single tree, the same checker exits 0 with no other
change. Its passing is the acceptance test for the fix.
