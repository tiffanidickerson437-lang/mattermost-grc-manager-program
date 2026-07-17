#!/usr/bin/env python3
"""Tests for validate_llms_txt.

Run:  python3 -m unittest test_validate_llms_txt -v

Standard library only (unittest). No pytest, no network. Every fixture is a
small inline string so the checker's detection logic is exercised directly.
"""

import unittest

import validate_llms_txt as v

# Two version-labelled trees in one file. This is the defect: an agent cannot
# tell which tree is current. The checker must FAIL (ok == False).
DUAL_TREE = """\
# Example Handbook

## 0.2.0

- [About](https://example.com/0.2.0/about.md)
- [Ops](https://example.com/0.2.0/ops.md)

## 0.2.1

- [About](https://example.com/about.md)
- [Ops](https://example.com/ops.md)
- [Sales](https://example.com/sales.md)
"""

# One version-labelled tree. Clean and unambiguous. Must PASS (ok == True).
SINGLE_TREE = """\
# Example Handbook

## 0.2.1

- [About](https://example.com/about.md)
- [Ops](https://example.com/ops.md)
- [Sales](https://example.com/sales.md)
"""

# A standard llms.txt using topic sections (the convention's own pattern).
# Multiple H2 sections here are correct, not a defect. Must PASS -- this proves
# the checker keys on version-like headings, not on "more than one section".
STANDARD_TOPICS = """\
# Example Handbook

> A short summary line.

## Docs

- [Getting started](https://example.com/start.md)
- [Configuration](https://example.com/config.md)

## Optional

- [Changelog](https://example.com/changelog.md)
"""

# No H2 sections at all. Nothing to check; must PASS.
EMPTY_SECTIONS = """\
# Example Handbook

Just a paragraph, no index sections.
"""


class TestVersionDetection(unittest.TestCase):
    def test_dual_tree_fails(self):
        result = v.analyze(DUAL_TREE)
        self.assertFalse(result["ok"], "two version trees must fail")
        self.assertEqual(len(result["version_sections"]), 2)
        self.assertEqual(main_exit(DUAL_TREE), 1)

    def test_dual_tree_entry_counts(self):
        result = v.analyze(DUAL_TREE)
        counts = {s.heading: s.entry_count for s in result["version_sections"]}
        self.assertEqual(counts, {"0.2.0": 2, "0.2.1": 3})

    def test_single_tree_passes(self):
        result = v.analyze(SINGLE_TREE)
        self.assertTrue(result["ok"], "one version tree must pass")
        self.assertEqual(len(result["version_sections"]), 1)
        self.assertEqual(main_exit(SINGLE_TREE), 0)

    def test_standard_topic_sections_pass(self):
        # Two H2 sections, but neither is a version number -> not a defect.
        result = v.analyze(STANDARD_TOPICS)
        self.assertTrue(result["ok"], "topic sections must not be flagged")
        self.assertEqual(len(result["sections"]), 2)
        self.assertEqual(len(result["version_sections"]), 0)
        self.assertEqual(main_exit(STANDARD_TOPICS), 0)

    def test_no_sections_pass(self):
        result = v.analyze(EMPTY_SECTIONS)
        self.assertTrue(result["ok"])
        self.assertEqual(result["sections"], [])


class TestVersionHeadingClassifier(unittest.TestCase):
    def test_version_headings_recognised(self):
        for heading in ["0.2.0", "0.2.1", "v1.0", "1.2.3", "10.4"]:
            s = v.Section(heading, 1)
            self.assertTrue(s.is_version, "%r should be a version" % heading)

    def test_prose_headings_not_versions(self):
        for heading in ["Docs", "Optional", "Examples", "0.2.0 archive", "API"]:
            s = v.Section(heading, 1)
            self.assertFalse(s.is_version, "%r should not be a version" % heading)


def main_exit(text):
    """Run the same pass/fail decision main() would, without I/O."""
    return 0 if v.analyze(text)["ok"] else 1


if __name__ == "__main__":
    unittest.main(verbosity=2)
