#!/usr/bin/env python3
"""Tests for check_taxonomy_sync."""

from __future__ import annotations

import contextlib
import io
import types
import unittest
from unittest.mock import patch

import check_taxonomy_sync as cts


def _fake_module(
    canonical, aliases, dep_fm=None, dep_entity=None, dep_src=None, dep_sys=None
):
    m = types.SimpleNamespace()
    m.CANONICAL = frozenset(canonical)
    m.ALIASES = dict(aliases)
    m.DEPRECATED_FRONTMATTER = frozenset(dep_fm or set())
    m.DEPRECATED_ENTITY_NAMES = frozenset(dep_entity or set())
    m.DEPRECATED_SOURCE = frozenset(dep_src or set())
    m.DEPRECATED_SYSTEM = frozenset(dep_sys or set())
    return m


SAMPLE_MD = """---
title: x
---

# Tag Taxonomy

intro prose

## Canonical Tags

### Faction (2)

| Tag | Covers |
|---|---|
| `dravosi` | Crown |
| `passage` | Rats |

## Alias Map

| Alias | Canonical |
|---|---|
| `crown` (as faction) | `dravosi` |
| `the-passage` | `passage` |

## Deprecated Tags

Remove these:

`npc`, `place`, `bestiary`

## Choosing Tags

done
"""


class SplitSectionsTests(unittest.TestCase):
    def test_splits_on_h2_only(self):
        secs = cts.split_sections(SAMPLE_MD)
        self.assertIn("Canonical Tags", secs)
        self.assertIn("Alias Map", secs)
        self.assertIn("Deprecated Tags", secs)
        # h3 "### Faction (2)" must not become its own section
        self.assertNotIn("Faction (2)", secs)

    def test_preamble_captured(self):
        secs = cts.split_sections("no headers here\njust text")
        self.assertIn("_preamble", secs)


class TokenExtractionTests(unittest.TestCase):
    def test_first_backtick_tokens_skips_divider_and_header(self):
        secs = cts.split_sections(SAMPLE_MD)
        toks = cts._first_backtick_tokens(secs["Canonical Tags"])
        self.assertEqual(toks, {"dravosi", "passage"})

    def test_all_backtick_tokens(self):
        secs = cts.split_sections(SAMPLE_MD)
        dep = cts._all_backtick_tokens(secs["Deprecated Tags"])
        self.assertEqual(dep, {"npc", "place", "bestiary"})

    def test_lowercases(self):
        self.assertEqual(cts._all_backtick_tokens("`Homebrew`"), {"homebrew"})


class ParseMarkdownTests(unittest.TestCase):
    def test_parse(self):
        parsed = cts.parse_markdown(SAMPLE_MD)
        self.assertEqual(parsed["canonical"], {"dravosi", "passage"})
        self.assertIn("crown", parsed["aliases"])
        self.assertIn("dravosi", parsed["aliases"])  # canonical target also backticked
        self.assertEqual(parsed["deprecated"], {"npc", "place", "bestiary"})


class CheckTests(unittest.TestCase):
    def test_in_sync(self):
        mod = _fake_module(
            canonical={"dravosi", "passage"},
            aliases={"crown": "dravosi", "the-passage": "passage"},
            dep_fm={"npc", "place"},
            dep_src={"bestiary"},
        )
        self.assertEqual(cts.check(mod, SAMPLE_MD), [])

    def test_canonical_missing_in_md(self):
        mod = _fake_module(canonical={"dravosi", "passage", "tessarine"}, aliases={})
        probs = cts.check(mod, SAMPLE_MD)
        self.assertTrue(any("not taxonomy.md" in p and "tessarine" in p for p in probs))

    def test_canonical_extra_in_md(self):
        mod = _fake_module(canonical={"dravosi"}, aliases={})
        probs = cts.check(mod, SAMPLE_MD)
        self.assertTrue(
            any("not tag_taxonomy.py" in p and "passage" in p for p in probs)
        )

    def test_alias_missing(self):
        mod = _fake_module(
            canonical={"dravosi", "passage"},
            aliases={"crown": "dravosi", "ghost-alias": "passage"},
        )
        probs = cts.check(mod, SAMPLE_MD)
        self.assertTrue(any("aliases:" in p and "ghost-alias" in p for p in probs))

    def test_deprecated_missing(self):
        mod = _fake_module(
            canonical={"dravosi", "passage"},
            aliases={"crown": "dravosi", "the-passage": "passage"},
            dep_sys={"ghost-dep"},
        )
        probs = cts.check(mod, SAMPLE_MD)
        self.assertTrue(any("deprecated:" in p and "ghost-dep" in p for p in probs))

    def test_real_files_in_sync(self):
        # The shipped taxonomy.py and taxonomy.md must stay in sync.
        self.assertEqual(cts.check(), [])


class MainTests(unittest.TestCase):
    def test_main_in_sync(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cts.main([])
        self.assertEqual(code, 0)
        self.assertIn("in sync", out.getvalue())

    def test_main_quiet_in_sync(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cts.main(["--quiet"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "")

    def test_main_reports_drift(self):
        with patch.object(cts, "check", return_value=["canonical: boom"]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = cts.main([])
        self.assertEqual(code, 1)
        self.assertIn("DRIFT", out.getvalue())
        self.assertIn("boom", out.getvalue())


if __name__ == "__main__":
    unittest.main()
