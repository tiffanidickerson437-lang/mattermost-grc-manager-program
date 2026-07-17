#!/usr/bin/env python3
"""Check a handbook's llms.txt for the dual version-tree defect.

llms.txt is a machine-readable index that tells LLM agents which pages of a
site to read. The convention (llmstxt.org) uses H2 headings (lines starting
with "## ") as section labels, and markdown links underneath them as the pages
an agent should ingest.

This checker flags one specific problem. When a single llms.txt publishes two
or more *version-labelled* H2 sections at once -- for example "## 0.2.0" and
"## 0.2.1" -- an agent has no machine-readable way to tell which tree is
current. It ingests both and ends up holding two copies of the company, one of
them stale.

The check is deliberately narrow. Multiple H2 sections are normal and correct
in llms.txt: the convention itself uses sections like "Docs" and "Optional".
This checker only counts a section as a problem when its heading looks like a
version number, so a standard multi-section file passes.

Usage:
    python3 validate_llms_txt.py                       # fetch the live file
    python3 validate_llms_txt.py --url <URL>           # fetch a specific URL
    python3 validate_llms_txt.py --file observed-llms.txt   # read a local copy

Exit codes:
    0  pass  -- zero or one version-labelled section
    1  fail  -- two or more version-labelled sections (the dual-tree ambiguity)
    2  error -- could not fetch or read the input

Standard library only. No pip install required.
"""

import argparse
import re
import sys
import urllib.request

DEFAULT_URL = "https://handbook.mattermost.com/llms.txt"

# An H2 heading: a line that starts with exactly "## " (not "###").
_H2_RE = re.compile(r"^##\s+(?P<heading>.+?)\s*$")

# An llms.txt entry: a markdown list item whose text is a link, "- [Title](url)".
_ENTRY_RE = re.compile(r"^\s*-\s+\[")

# A version-number heading: optional leading "v", then two or more
# dot-separated integers. Matches "0.2.0", "0.2.1", "v1.0", "1.2.3".
# Does not match "Docs", "Optional", "Examples", or any prose heading.
_VERSION_RE = re.compile(r"^v?\d+(?:\.\d+)+$")


class Section:
    """One H2 section of an llms.txt file."""

    def __init__(self, heading, line_no):
        self.heading = heading
        self.line_no = line_no
        self.entry_count = 0

    @property
    def is_version(self):
        return bool(_VERSION_RE.match(self.heading.strip()))


def parse_sections(text):
    """Return the list of H2 sections found in *text*, with entry counts.

    Pure string parsing -- no network, no files. Entries that appear before the
    first H2 heading are ignored, matching how the convention groups links
    under their section.
    """
    sections = []
    current = None
    for i, line in enumerate(text.splitlines(), start=1):
        h2 = _H2_RE.match(line)
        if h2:
            current = Section(h2.group("heading"), i)
            sections.append(current)
            continue
        if current is not None and _ENTRY_RE.match(line):
            current.entry_count += 1
    return sections


def analyze(text):
    """Analyse llms.txt *text* and return a result dict.

    Keys:
        sections          -- every H2 section (list of Section)
        version_sections  -- the subset whose heading is a version number
        ok                -- True unless two or more version sections exist
        total_entries     -- total llms.txt link entries across all sections
    """
    sections = parse_sections(text)
    version_sections = [s for s in sections if s.is_version]
    return {
        "sections": sections,
        "version_sections": version_sections,
        "ok": len(version_sections) < 2,
        "total_entries": sum(s.entry_count for s in sections),
    }


def format_report(result, source):
    """Render a human-readable report from an analyze() result."""
    lines = []
    lines.append("llms.txt version-tree check")
    lines.append("source: %s" % source)
    lines.append("")

    sections = result["sections"]
    if not sections:
        lines.append("No H2 (## ) sections found. Nothing to check.")
        return "\n".join(lines)

    lines.append("sections found (%d):" % len(sections))
    for s in sections:
        tag = "version tree" if s.is_version else "topic section"
        lines.append(
            "  line %-4d  ## %-12s  %3d entries  [%s]"
            % (s.line_no, s.heading, s.entry_count, tag)
        )
    lines.append("")

    version_sections = result["version_sections"]
    if len(version_sections) >= 2:
        headings = ", ".join(s.heading for s in version_sections)
        lines.append("FAIL: %d version-labelled trees published at once (%s)."
                     % (len(version_sections), headings))
        lines.append(
            "An agent reading this file cannot tell which tree is current, so"
        )
        lines.append(
            "it ingests both and holds two copies of the handbook -- one stale."
        )
        lines.append("")
        lines.append("Entry counts by tree:")
        for s in version_sections:
            lines.append("  %s: %d entries" % (s.heading, s.entry_count))
    elif len(version_sections) == 1:
        s = version_sections[0]
        lines.append(
            "PASS: exactly one version tree (%s, %d entries). No ambiguity."
            % (s.heading, s.entry_count)
        )
    else:
        lines.append(
            "PASS: no version-labelled trees. Sections read as topic labels."
        )
    return "\n".join(lines)


def fetch(url):
    """Fetch *url* and return its text. Raises on failure."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "llms-txt-validator/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def load(args):
    """Return (text, source_label) from --file or --url, or raise."""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            return fh.read(), args.file
    return fetch(args.url), args.url


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check an llms.txt for the dual version-tree defect."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="URL of the llms.txt to check (default: %(default)s)",
    )
    parser.add_argument(
        "--file",
        help="read a local copy instead of fetching (offline)",
    )
    args = parser.parse_args(argv)

    try:
        text, source = load(args)
    except Exception as exc:  # noqa: BLE001 -- report any load failure cleanly
        print("error: could not read llms.txt: %s" % exc, file=sys.stderr)
        return 2

    result = analyze(text)
    print(format_report(result, source))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
