#!/usr/bin/env python3
"""Tests for ingest_packet.py."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

import ingest_packet


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------


class SlugifyTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(ingest_packet.slugify("Foo Bar"), "foo-bar")

    def test_strips_punctuation(self):
        self.assertEqual(ingest_packet.slugify("Bob's Inn!"), "bobs-inn")

    def test_strips_quotes(self):
        self.assertEqual(ingest_packet.slugify('"Quoted Name"'), "quoted-name")

    def test_multiple_spaces(self):
        self.assertEqual(ingest_packet.slugify("Foo  Bar  Baz"), "foo-bar-baz")

    def test_already_slug(self):
        self.assertEqual(ingest_packet.slugify("foo-bar"), "foo-bar")

    def test_empty(self):
        self.assertEqual(ingest_packet.slugify(""), "")


# ---------------------------------------------------------------------------
# wikilink_targets
# ---------------------------------------------------------------------------


class WikilinkTargetsTests(unittest.TestCase):
    def test_simple_link(self):
        targets = ingest_packet.wikilink_targets("[[foo-bar]]")
        self.assertIn("foo-bar", targets)

    def test_aliased_link(self):
        targets = ingest_packet.wikilink_targets("[[foo-bar|Foo Bar]]")
        self.assertIn("foo-bar", targets)

    def test_path_style_link(self):
        targets = ingest_packet.wikilink_targets("[[wiki/entities/npcs/bob|Bob]]")
        self.assertIn("bob", targets)

    def test_section_link(self):
        targets = ingest_packet.wikilink_targets("[[page#section|Title]]")
        self.assertIn("page", targets)

    def test_multiple_links(self):
        text = "See [[alice|Alice]] and [[bob|Bob]]."
        targets = ingest_packet.wikilink_targets(text)
        self.assertIn("alice", targets)
        self.assertIn("bob", targets)

    def test_no_links(self):
        targets = ingest_packet.wikilink_targets("No links here.")
        self.assertEqual(targets, [])


# ---------------------------------------------------------------------------
# frontmatter_targets
# ---------------------------------------------------------------------------


class FrontmatterTargetsTests(unittest.TestCase):
    def test_extracts_from_parent_location(self):
        fm_lines = ["parent_location: [[calveno|Calveno]]"]
        targets = ingest_packet.frontmatter_targets(fm_lines)
        self.assertIn("calveno", targets)

    def test_extracts_bare_parent_location(self):
        fm_lines = ["parent_location: Calveno"]
        targets = ingest_packet.frontmatter_targets(fm_lines)
        self.assertIn("Calveno", targets)

    def test_ignores_none_values(self):
        fm_lines = ["parent_location: none"]
        targets = ingest_packet.frontmatter_targets(fm_lines)
        # "none" should be ignored
        self.assertNotIn("none", targets)

    def test_extracts_from_aliases_list(self):
        fm_lines = [
            "aliases:",
            "  - [[foo-bar|Foo]]",
        ]
        targets = ingest_packet.frontmatter_targets(fm_lines)
        self.assertIn("foo-bar", targets)


# ---------------------------------------------------------------------------
# body_proper_nouns
# ---------------------------------------------------------------------------


class BodyProperNounsTests(unittest.TestCase):
    def test_finds_two_word_proper_noun(self):
        body = "He met Captain Scarlet in the tavern."
        nouns = ingest_packet.body_proper_nouns(body)
        # "Captain Scarlet" should be found
        self.assertTrue(any("Captain Scarlet" in n or "Scarlet" in n for n in nouns))

    def test_filters_stopwords(self):
        body = "The Black Market is a place."
        nouns = ingest_packet.body_proper_nouns(body)
        # "The" stripped from "The Black Market"
        self.assertTrue(any("Black Market" in n for n in nouns))

    def test_no_proper_nouns(self):
        body = "a simple lowercase sentence with no names."
        nouns = ingest_packet.body_proper_nouns(body)
        # No multi-word capitalized phrases
        multi_word = [n for n in nouns if " " in n or len(n.split()) > 1]
        self.assertEqual(multi_word, [])

    def test_skips_wikilinks(self):
        body = "She visited [[calveno|Calveno Town]] last week."
        nouns = ingest_packet.body_proper_nouns(body)
        # Wikilinks are stripped before scanning
        self.assertTrue(all("calveno" not in n.lower() for n in nouns))


# ---------------------------------------------------------------------------
# resolve
# ---------------------------------------------------------------------------


class ResolveTests(unittest.TestCase):
    def test_resolves_by_slug(self):
        by_slug = {"calveno": "A port city"}
        title_to_slug = {"calveno": "calveno"}
        result = ingest_packet.resolve("calveno", by_slug, title_to_slug)
        self.assertEqual(result, "calveno")

    def test_resolves_by_title(self):
        by_slug = {"calveno": "A port city"}
        title_to_slug = {"calveno city": "calveno"}
        result = ingest_packet.resolve("Calveno City", by_slug, title_to_slug)
        self.assertEqual(result, "calveno")

    def test_returns_none_when_not_found(self):
        result = ingest_packet.resolve("unknown-entity-xyz", {}, {})
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# build_index (with temp wiki)
# ---------------------------------------------------------------------------


class BuildIndexTests(unittest.TestCase):
    def test_builds_from_wiki_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(
                os.path.join(npc_dir, "bob.md"),
                '---\ntype: entity\nsummary: "Bob the sailor"\n---\n\n# Bob\n',
            )
            with patch("wiki_common.WIKI_DIR", wiki):
                by_slug, _title_to_slug = ingest_packet.build_index()
        self.assertIn("bob", by_slug)
        self.assertEqual(by_slug["bob"], "Bob the sailor")

    def test_maps_title_to_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(
                os.path.join(npc_dir, "big-bob.md"),
                '---\ntype: entity\nsummary: "Big Bob"\n---\n\n# Big Bob\n',
            )
            with patch("wiki_common.WIKI_DIR", wiki):
                _by_slug, title_to_slug = ingest_packet.build_index()
        self.assertIn("big bob", title_to_slug)
        self.assertEqual(title_to_slug["big bob"], "big-bob")


# ---------------------------------------------------------------------------
# packet_for (with temp wiki + source)
# ---------------------------------------------------------------------------


class PacketForTests(unittest.TestCase):
    def _setup_wiki_and_source(self, tmp):
        wiki = os.path.join(tmp, "wiki")
        npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
        os.makedirs(npc_dir)
        _write(
            os.path.join(npc_dir, "alice.md"),
            '---\ntype: entity\nsummary: "Alice the mage"\n---\n\n# Alice\n',
        )
        source = os.path.join(tmp, "Inbox", "session.md")
        _write(
            source,
            "---\ntype: session\n---\n\n# Session 01\n\n[[alice|Alice]] appeared.\n",
        )
        return wiki, source

    def test_packet_includes_existing_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki, source = self._setup_wiki_and_source(tmp)
            with patch("wiki_common.WIKI_DIR", wiki):
                by_slug, title_to_slug = ingest_packet.build_index()
                packet = ingest_packet.packet_for(source, by_slug, title_to_slug)
        self.assertIn("alice", packet)
        self.assertIn("EXISTING PAGES", packet)

    def test_packet_includes_candidate_stubs(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(os.path.join(wiki, "entities", "characters", "npcs"))
            source = os.path.join(tmp, "Inbox", "session.md")
            _write(
                source,
                "---\ntype: session\n---\n\n# Session 01\n\n[[unknown-npc|Unknown NPC]] appeared.\n",
            )
            with patch("wiki_common.WIKI_DIR", wiki):
                by_slug, title_to_slug = ingest_packet.build_index()
                packet = ingest_packet.packet_for(source, by_slug, title_to_slug)
        self.assertIn("CANDIDATE STUBS", packet)
        self.assertIn("unknown-npc", packet)

    def test_packet_header_includes_source_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki, source = self._setup_wiki_and_source(tmp)
            with patch("wiki_common.WIKI_DIR", wiki):
                by_slug, title_to_slug = ingest_packet.build_index()
                packet = ingest_packet.packet_for(source, by_slug, title_to_slug)
        self.assertIn("Context packet", packet)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class MainTests(unittest.TestCase):
    def test_main_missing_file(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ingest_packet.main(["/nonexistent/source.md"])
        self.assertNotEqual(code, 0)

    def test_main_no_args_shows_usage(self):
        try:
            code = ingest_packet.main([])
        except SystemExit as e:
            code = e.code
        self.assertNotEqual(code, 0)

    def test_main_produces_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(
                os.path.join(npc_dir, "alice.md"),
                '---\ntype: entity\nsummary: "Alice"\n---\n\n# Alice\n',
            )
            source = os.path.join(tmp, "Inbox", "session.md")
            _write(
                source,
                "---\ntype: session\n---\n\n# Session 01\n\n[[alice|Alice]] was there.\n",
            )
            with patch("wiki_common.WIKI_DIR", wiki):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = ingest_packet.main([source])
            self.assertEqual(code, 0)
            self.assertIn("alice", out.getvalue())


if __name__ == "__main__":
    unittest.main()
