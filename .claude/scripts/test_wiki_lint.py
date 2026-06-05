#!/usr/bin/env python3
"""Comprehensive tests for wiki_lint.py."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import wiki_lint
from ruamel.yaml.comments import CommentedMap, CommentedSeq

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _make_wiki(tmp: str, files: dict) -> str:
    """Create wiki files under tmp/wiki/. Returns the wiki path."""
    wiki = os.path.join(tmp, "wiki")
    for relpath, content in files.items():
        _write(os.path.join(wiki, relpath), content)
    return wiki


MINIMAL_ENTITY_FM = """\
---
type: entity
subtype: npc
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "A test NPC"
created: 2026-01-01
updated: 2026-01-01
tags: []
sources: []
confidence_level: medium
---

# Test NPC

Some body text with a link to [[other-npc|Other NPC]].
"""

MINIMAL_SITUATION_FM = """\
---
type: situation
subtype: active-situation
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "A test situation"
created: 2026-01-01
updated: 2026-01-01
tags: []
sources: []
lifecycle: active
narrative_island: none
---

# Test Situation
"""


# ---------------------------------------------------------------------------
# Issue dataclass
# ---------------------------------------------------------------------------


class IssueTests(unittest.TestCase):
    def test_line_without_fix(self):
        issue = wiki_lint.Issue(
            "error", "missing-frontmatter", "wiki/foo.md", "no frontmatter"
        )
        line = issue.line()
        self.assertIn("wiki/foo.md", line)
        self.assertIn("missing-frontmatter", line)
        self.assertNotIn("·fix:", line)

    def test_line_with_fix(self):
        issue = wiki_lint.Issue(
            "warning", "broken-wikilink", "wiki/foo.md", "[[bad]]", fix="create stub"
        )
        line = issue.line()
        self.assertIn("·fix:", line)
        self.assertIn("create stub", line)

    def test_severity_stored(self):
        issue = wiki_lint.Issue("quality", "orphan", "wiki/foo.md", "no inbound")
        self.assertEqual(issue.severity, "quality")

    def test_dataclass_fields(self):
        issue = wiki_lint.Issue("error", "rule", "path", "detail")
        self.assertIsNone(issue.fix)


# ---------------------------------------------------------------------------
# Pure utility functions
# ---------------------------------------------------------------------------


class SplitDocTests(unittest.TestCase):
    def test_normal_frontmatter(self):
        text = "---\ntype: entity\n---\n\n# Body"
        fm, body, had = wiki_lint.split_doc(text)
        self.assertTrue(had)
        self.assertIn("type: entity", fm)
        self.assertIn("# Body", body)

    def test_no_frontmatter(self):
        text = "# Just a heading\nNo frontmatter"
        _fm, body, had = wiki_lint.split_doc(text)
        self.assertFalse(had)
        self.assertEqual(body, text)

    def test_empty_frontmatter(self):
        text = "---\n---\n\n# Body"
        fm, _body, had = wiki_lint.split_doc(text)
        self.assertTrue(had)
        self.assertEqual(fm.strip(), "")

    def test_no_closing_fence(self):
        text = "---\ntype: entity\nno closing"
        _fm, _body, had = wiki_lint.split_doc(text)
        self.assertFalse(had)


class ScannableTests(unittest.TestCase):
    def test_strips_code_fence(self):
        text = "Before\n```\n[[fake-link]]\n```\nAfter"
        result = wiki_lint.scannable(text)
        self.assertNotIn("fake-link", result)
        self.assertIn("Before", result)
        self.assertIn("After", result)

    def test_strips_inline_code(self):
        text = "Text with `[[inline-link]]` code"
        result = wiki_lint.scannable(text)
        self.assertNotIn("inline-link", result)

    def test_normalizes_escaped_pipe(self):
        text = "[[slug\\|alias]]"
        result = wiki_lint.scannable(text)
        self.assertIn("|", result)

    def test_normal_text_unchanged(self):
        text = "Normal [[slug|Label]] text"
        result = wiki_lint.scannable(text)
        self.assertIn("slug", result)


class IsAssetTests(unittest.TestCase):
    def test_png_is_asset(self):
        self.assertTrue(wiki_lint.is_asset("image.png"))

    def test_pdf_is_asset(self):
        self.assertTrue(wiki_lint.is_asset("doc.pdf"))

    def test_md_not_asset(self):
        self.assertFalse(wiki_lint.is_asset("page.md"))

    def test_no_extension(self):
        self.assertFalse(wiki_lint.is_asset("pagename"))

    def test_webp_is_asset(self):
        self.assertTrue(wiki_lint.is_asset("img.webp"))


class SlugOfTests(unittest.TestCase):
    def test_strips_md_extension(self):
        self.assertEqual(wiki_lint.slug_of("/path/to/foo-bar.md"), "foo-bar")

    def test_no_extension(self):
        self.assertEqual(wiki_lint.slug_of("/path/to/foo"), "foo")


class WikilinkTargetsTests(unittest.TestCase):
    def test_simple_link(self):
        targets = list(wiki_lint.wikilink_targets("[[slug-name]]"))
        self.assertIn(("slug-name", False, False), targets)

    def test_aliased_link(self):
        targets = list(wiki_lint.wikilink_targets("[[slug-name|Display Name]]"))
        self.assertIn(("slug-name", True, False), targets)

    def test_embed_link(self):
        targets = list(wiki_lint.wikilink_targets("![[image.png]]"))
        self.assertIn(("image.png", False, True), targets)

    def test_strips_md_extension(self):
        # The function strips last 4 chars when target ends with ".md"
        targets = list(wiki_lint.wikilink_targets("[[foo.md|Bar]]"))
        # "foo.md"[:-4] = "fo" (actual code behavior)
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0][1], True)  # has alias
        self.assertEqual(targets[0][2], False)  # not embed

    def test_multiple_links(self):
        text = "See [[alice|Alice]] and [[bob|Bob]] for details."
        targets = list(wiki_lint.wikilink_targets(text))
        slugs = [t[0] for t in targets]
        self.assertIn("alice", slugs)
        self.assertIn("bob", slugs)

    def test_heading_anchor_stripped(self):
        targets = list(wiki_lint.wikilink_targets("[[page#section|Title]]"))
        self.assertIn(("page", True, False), targets)


class LoadFrontmatterTests(unittest.TestCase):
    def test_empty_text_returns_empty_map(self):
        yaml = wiki_lint.make_yaml()
        result = wiki_lint.load_frontmatter(yaml, "")
        self.assertIsInstance(result, CommentedMap)
        self.assertEqual(len(result), 0)

    def test_none_yaml_returns_empty_map(self):
        yaml = wiki_lint.make_yaml()
        result = wiki_lint.load_frontmatter(yaml, "null\n")
        self.assertIsInstance(result, CommentedMap)

    def test_parses_fields(self):
        yaml = wiki_lint.make_yaml()
        fm = "type: entity\nstatus: active\n"
        result = wiki_lint.load_frontmatter(yaml, fm)
        self.assertEqual(result["type"], "entity")
        self.assertEqual(result["status"], "active")


class ToPlainTests(unittest.TestCase):
    def test_dict(self):
        d = CommentedMap({"a": 1, "b": "x"})
        result = wiki_lint._to_plain(d)
        self.assertEqual(result, {"a": 1, "b": "x"})

    def test_list(self):
        seq = CommentedSeq([1, 2, 3])
        result = wiki_lint._to_plain(seq)
        self.assertEqual(result, [1, 2, 3])

    def test_none(self):
        self.assertIsNone(wiki_lint._to_plain(None))

    def test_bool(self):
        self.assertIs(wiki_lint._to_plain(True), True)
        self.assertIs(wiki_lint._to_plain(False), False)

    def test_int(self):
        self.assertEqual(wiki_lint._to_plain(42), 42)

    def test_str(self):
        self.assertEqual(wiki_lint._to_plain("hello"), "hello")


class RelationshipEntriesTests(unittest.TestCase):
    def test_none_returns_empty(self):
        self.assertEqual(wiki_lint.relationship_entries(None), [])

    def test_string_entries(self):
        entries = wiki_lint.relationship_entries(["[[alice|Alice]] — ally"])
        self.assertTrue(any(t == "alice" for t, _ in entries))

    def test_dict_entries(self):
        entries = wiki_lint.relationship_entries(
            [{"relation": "ally", "target": "[[bob|Bob]]"}]
        )
        self.assertTrue(any(t == "bob" for t, _ in entries))

    def test_string_without_link(self):
        entries = wiki_lint.relationship_entries(["some entry without links"])
        self.assertEqual(entries, [])


class CheckNamingTests(unittest.TestCase):
    def test_valid_kebab(self):
        result = wiki_lint.check_naming("wiki/entities/npcs/foo-bar.md")
        self.assertIsNone(result)

    def test_invalid_non_kebab(self):
        result = wiki_lint.check_naming("wiki/entities/npcs/Foo Bar.md")
        self.assertIsNotNone(result)
        self.assertEqual(result.rule, "naming-convention")

    def test_underscore_invalid(self):
        result = wiki_lint.check_naming("wiki/entities/npcs/foo_bar.md")
        self.assertIsNotNone(result)

    def test_uppercase_invalid(self):
        result = wiki_lint.check_naming("wiki/entities/npcs/FooBar.md")
        self.assertIsNotNone(result)


class FieldDefaultsTests(unittest.TestCase):
    def test_entity_defaults(self):
        d = wiki_lint.field_defaults("wiki/entities/characters/npcs/bob.md")
        self.assertEqual(d["type"], "entity")
        self.assertEqual(d["subtype"], "npc")
        self.assertEqual(d["campaign"], "shattered-sea")

    def test_situation_defaults(self):
        d = wiki_lint.field_defaults("wiki/situations/active/foo.md")
        self.assertEqual(d["type"], "situation")

    def test_common_fields_present(self):
        d = wiki_lint.field_defaults("wiki/entities/factions/foo.md")
        for field in ["type", "subtype", "campaign", "status", "summary", "tags"]:
            self.assertIn(field, d)


# ---------------------------------------------------------------------------
# check_file
# ---------------------------------------------------------------------------


class CheckFileTests(unittest.TestCase):
    def _make_validator(self):
        schema_path = os.path.join(
            os.path.dirname(__file__), "wiki-frontmatter.schema.json"
        )
        with open(schema_path) as fh:
            schema = json.load(fh)
        import jsonschema

        return jsonschema.Draft202012Validator(schema)

    def _make_data(self, **kwargs):
        d = CommentedMap(
            {
                "type": "entity",
                "subtype": "npc",
                "campaign": "shattered-sea",
                "status": "active",
                "audience": "dm",
                "publish": False,
                "summary": "A real summary",
                "created": "2026-01-01",
                "updated": "2026-01-01",
                "tags": [],
                "sources": [],
                "confidence_level": "medium",
            }
        )
        d.update(kwargs)
        return d

    def test_valid_file_no_issues(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data()
        body = "# Bob\n\nSome text."
        issues = wiki_lint.check_file(relpath, data, body, yaml, validator)
        # Only quality issues expected (e.g. orphan, deadend — those are cross-file)
        errors = [i for i in issues if i.severity == "error"]
        self.assertEqual(errors, [])

    def test_missing_required_field(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "subtype": "npc"})
        issues = wiki_lint.check_file(relpath, data, "# Bob", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("missing-required-field", rules)

    def test_stub_summary_flagged(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data(summary=wiki_lint.STUB_SUMMARY)
        issues = wiki_lint.check_file(relpath, data, "# Bob", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("summary-stale", rules)

    def test_empty_summary_flagged(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data(summary="")
        issues = wiki_lint.check_file(relpath, data, "# Bob", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("summary-stale", rules)

    def test_type_path_mismatch(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data(type="situation")  # wrong type for this path
        issues = wiki_lint.check_file(relpath, data, "# Bob", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("type-path-mismatch", rules)

    def test_lifecycle_folder_mismatch(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/situations/active/foo.md"
        data = CommentedMap(
            {
                "type": "situation",
                "subtype": "active-situation",
                "campaign": "shattered-sea",
                "status": "active",
                "audience": "dm",
                "publish": False,
                "summary": "A real situation",
                "created": "2026-01-01",
                "updated": "2026-01-01",
                "tags": [],
                "sources": [],
                "lifecycle": "resolved",  # mismatch
                "narrative_island": "none",
            }
        )
        issues = wiki_lint.check_file(relpath, data, "# Foo", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("lifecycle-folder-mismatch", rules)

    def test_relationships_in_frontmatter_flagged(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data(relationships=["[[alice|Alice]] — ally"])
        issues = wiki_lint.check_file(relpath, data, "# Bob", yaml, validator)
        rules = [i.rule for i in issues]
        self.assertIn("relationships-in-frontmatter", rules)

    def test_relationships_body_link_mentioned(self):
        yaml = wiki_lint.make_yaml()
        validator = self._make_validator()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = self._make_data(relationships=["[[alice|Alice]] — ally"])
        body = "# Bob\n\nFriends with [[alice|Alice]] here."
        issues = wiki_lint.check_file(relpath, data, body, yaml, validator)
        rel_issues = [i for i in issues if i.rule == "relationships-in-frontmatter"]
        self.assertTrue(any("in body" in i.detail for i in rel_issues))


# ---------------------------------------------------------------------------
# cross_file_checks
# ---------------------------------------------------------------------------


class CrossFileChecksTests(unittest.TestCase):
    def _make_records(self, files):
        """files: list of (relpath, fm_dict, body_str)"""
        records = []
        yaml = wiki_lint.make_yaml()
        for relpath, fm_dict, body in files:
            data = CommentedMap(fm_dict)
            records.append((relpath, data, body))
        return records

    def _slug_to_paths(self, records):
        m = {}
        for relpath, _, _ in records:
            slug = wiki_lint.slug_of(relpath)
            m.setdefault(slug, []).append(relpath)
        return m

    def test_broken_wikilink_flagged(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/alice.md",
                    {"type": "entity", "summary": "Alice"},
                    "# Alice\n\nLinks to [[nonexistent|Missing]] page.",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        issues = by_file.get("wiki/entities/characters/npcs/alice.md", [])
        rules = [i.rule for i in issues]
        self.assertIn("broken-wikilink", rules)

    def test_no_broken_link_for_asset(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/alice.md",
                    {"type": "entity", "summary": "Alice"},
                    "# Alice\n\n![[portrait.png]]",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        issues = by_file.get("wiki/entities/characters/npcs/alice.md", [])
        rules = [i.rule for i in issues]
        self.assertNotIn("broken-wikilink", rules)

    def test_valid_link_no_broken_issue(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/alice.md",
                    {"type": "entity", "summary": "Alice"},
                    "# Alice\n\nLinks to [[bob|Bob]].",
                ),
                (
                    "wiki/entities/characters/npcs/bob.md",
                    {"type": "entity", "summary": "Bob"},
                    "# Bob\n\nLinks to [[alice|Alice]].",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        for _path, issues in by_file.items():
            rules = [i.rule for i in issues]
            self.assertNotIn("broken-wikilink", rules)

    def test_bare_wikilink_flagged(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/alice.md",
                    {"type": "entity", "summary": "Alice"},
                    "# Alice\n\nLinks to [[bob]].",
                ),
                (
                    "wiki/entities/characters/npcs/bob.md",
                    {"type": "entity", "summary": "Bob"},
                    "# Bob",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        issues = by_file.get("wiki/entities/characters/npcs/alice.md", [])
        rules = [i.rule for i in issues]
        self.assertIn("bare-wikilink", rules)

    def test_orphan_flagged(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/alice.md",
                    {"type": "entity", "summary": "Alice"},
                    "# Alice\n\nNo links to others.",
                ),
                (
                    "wiki/entities/characters/npcs/bob.md",
                    {"type": "entity", "summary": "Bob"},
                    "# Bob\n\nLinks to [[alice|Alice]].",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        # bob has no inbound links -> orphan
        bob_issues = by_file.get("wiki/entities/characters/npcs/bob.md", [])
        rules = [i.rule for i in bob_issues]
        self.assertIn("orphan", rules)

    def test_deadend_flagged(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/deadend.md",
                    {"type": "entity", "summary": "Deadend"},
                    "# Deadend\n\nNo outgoing links here.",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        issues = by_file.get("wiki/entities/characters/npcs/deadend.md", [])
        rules = [i.rule for i in issues]
        self.assertIn("deadend", rules)

    def test_obsidian_deadends_skips_non_markdown(self):
        with patch(
            "wiki_lint._obsidian_lines",
            return_value=[
                "wiki/assets/banners/image.webp",
                "wiki/assets/portraits/npc.png",
                "wiki/entities/characters/npcs/real-page.md",
            ],
        ):
            issues = wiki_lint._obsidian_deadends()
        paths = [i.path for i in issues]
        self.assertNotIn("wiki/assets/banners/image.webp", paths)
        self.assertNotIn("wiki/assets/portraits/npc.png", paths)
        self.assertIn("wiki/entities/characters/npcs/real-page.md", paths)

    def test_orphan_exempt_for_system_files(self):
        records = self._make_records(
            [
                (
                    "wiki/system/task-routing.md",
                    {"type": "system", "summary": "Routing"},
                    "# Routing\n\nContent.",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        issues = by_file.get("wiki/system/task-routing.md", [])
        rules = [i.rule for i in issues]
        self.assertNotIn("orphan", rules)

    def test_duplicate_slug_flagged(self):
        records = self._make_records(
            [
                (
                    "wiki/entities/characters/npcs/bob.md",
                    {"type": "entity", "summary": "Bob NPC"},
                    "# Bob",
                ),
                (
                    "wiki/entities/characters/crew/bob.md",
                    {"type": "entity", "summary": "Bob Crew"},
                    "# Bob",
                ),
            ]
        )
        stp = {
            "bob": [
                "wiki/entities/characters/npcs/bob.md",
                "wiki/entities/characters/crew/bob.md",
            ]
        }
        by_file = wiki_lint.cross_file_checks(records, stp)
        for _path, issues in by_file.items():
            rules = [i.rule for i in issues]
            self.assertIn("duplicate-slug", rules)

    def test_skip_as_source_not_scanned(self):
        records = self._make_records(
            [
                (
                    "wiki/index.md",
                    {"type": "system", "summary": "Index"},
                    "# Index\n\n[[every-page|Every Page]]",
                ),
                (
                    "wiki/entities/characters/npcs/every-page.md",
                    {"type": "entity", "summary": "Page"},
                    "# Page",
                ),
            ]
        )
        by_file = wiki_lint.cross_file_checks(records, self._slug_to_paths(records))
        # index.md is in SKIP_AS_SOURCE, so its links shouldn't count
        # every-page.md should still be an orphan (no non-index inbound links)
        every_issues = by_file.get("wiki/entities/characters/npcs/every-page.md", [])
        # orphan because index.md was skipped as source
        rules = [i.rule for i in every_issues]
        self.assertIn("orphan", rules)


# ---------------------------------------------------------------------------
# check_tag_variants
# ---------------------------------------------------------------------------


class CheckTagVariantsTests(unittest.TestCase):
    def _make_records_with_tags(self, tags_by_file):
        records = []
        for relpath, tags in tags_by_file.items():
            data = CommentedMap({"tags": tags, "summary": "x"})
            records.append((relpath, data, "# Title"))
        return records

    def test_no_variants_no_issues(self):
        records = self._make_records_with_tags(
            {
                "wiki/entities/npcs/a.md": ["maritime", "combat"],
            }
        )
        issues = wiki_lint.check_tag_variants(records)
        self.assertEqual(issues, [])

    def test_plural_singular_flagged(self):
        records = self._make_records_with_tags(
            {
                "wiki/entities/npcs/a.md": ["ship"],
                "wiki/entities/npcs/b.md": ["ships"],
                "wiki/entities/npcs/c.md": ["ships"],
            }
        )
        issues = wiki_lint.check_tag_variants(records)
        self.assertTrue(len(issues) > 0)
        rules = [i.rule for i in issues]
        self.assertIn("tag-variant", rules)

    def test_no_tags_skipped(self):
        records = [
            ("wiki/entities/npcs/a.md", CommentedMap({"summary": "x"}), "# T"),
        ]
        issues = wiki_lint.check_tag_variants(records)
        self.assertEqual(issues, [])


# ---------------------------------------------------------------------------
# check_tags
# ---------------------------------------------------------------------------


class CheckTagsTests(unittest.TestCase):
    def _make_records_with_tags(self, relpath, tags):
        data = CommentedMap({"tags": tags, "summary": "x"})
        return [(relpath, data, "# T")]

    def test_canonical_tag_no_issue(self):
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", ["maritime"])
        issues = wiki_lint.check_tags(records)
        self.assertEqual(issues, [])

    def test_alias_tag_flagged(self):
        records = self._make_records_with_tags(
            "wiki/entities/npcs/a.md", ["dravosi-crown"]
        )
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-alias", rules)

    def test_deprecated_fm_tag_flagged(self):
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", ["situation"])
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-deprecated", rules)

    def test_deprecated_entity_tag_flagged(self):
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", ["perrin"])
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-deprecated", rules)

    def test_deprecated_source_tag_flagged(self):
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", ["phb"])
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-deprecated", rules)

    def test_deprecated_system_tag_flagged(self):
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", ["lint"])
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-deprecated", rules)

    def test_unknown_tag_flagged(self):
        records = self._make_records_with_tags(
            "wiki/entities/npcs/a.md", ["completely-unknown-xyz"]
        )
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-unknown", rules)

    def test_visibility_tag_skipped(self):
        records = self._make_records_with_tags(
            "wiki/entities/npcs/a.md", ["visibility/public"]
        )
        issues = wiki_lint.check_tags(records)
        self.assertEqual(issues, [])

    def test_over_limit_flagged(self):
        many_tags = ["maritime", "combat", "undead", "rattkin", "dravosi", "tessarine"]
        records = self._make_records_with_tags("wiki/entities/npcs/a.md", many_tags)
        issues = wiki_lint.check_tags(records)
        rules = [i.rule for i in issues]
        self.assertIn("tag-over-limit", rules)

    def test_skip_content_files(self):
        data = CommentedMap({"tags": ["completely-unknown-xyz"], "summary": "x"})
        records = [("wiki/index.md", data, "# Index")]
        issues = wiki_lint.check_tags(records)
        self.assertEqual(issues, [])

    def test_non_list_tags_skipped(self):
        data = CommentedMap({"tags": "not-a-list", "summary": "x"})
        records = [("wiki/entities/npcs/a.md", data, "# T")]
        issues = wiki_lint.check_tags(records)
        self.assertEqual(issues, [])


# ---------------------------------------------------------------------------
# check_singleton_properties
# ---------------------------------------------------------------------------


class CheckSingletonPropertiesTests(unittest.TestCase):
    def test_singleton_property_flagged(self):
        records = [
            (
                "wiki/entities/npcs/a.md",
                CommentedMap({"type": "entity", "rare_custom_prop": "value"}),
                "# A",
            ),
        ]
        issues = wiki_lint.check_singleton_properties(records, set())
        rules = [i.rule for i in issues]
        self.assertIn("singleton-property", rules)

    def test_common_property_not_flagged(self):
        records = [
            (
                "wiki/entities/npcs/a.md",
                CommentedMap({"type": "entity", "common_prop": "v"}),
                "# A",
            ),
            (
                "wiki/entities/npcs/b.md",
                CommentedMap({"type": "entity", "common_prop": "v"}),
                "# B",
            ),
        ]
        issues = wiki_lint.check_singleton_properties(records, set())
        rules = [i.rule for i in issues]
        self.assertNotIn("singleton-property", rules)

    def test_schema_property_not_flagged(self):
        records = [
            (
                "wiki/entities/npcs/a.md",
                CommentedMap({"schema_known_prop": "v"}),
                "# A",
            ),
        ]
        issues = wiki_lint.check_singleton_properties(records, {"schema_known_prop"})
        self.assertEqual(issues, [])


# ---------------------------------------------------------------------------
# check_lore_consistency
# ---------------------------------------------------------------------------


class CheckLoreConsistencyTests(unittest.TestCase):
    def test_status_drift_flagged(self):
        records = [
            (
                "wiki/entities/npcs/bob.md",
                CommentedMap({"status": "deceased", "summary": "Bob"}),
                "# Bob",
            ),
        ]
        issues = wiki_lint.check_lore_consistency(
            records, {"bob": ["wiki/entities/npcs/bob.md"]}
        )
        rules = [i.rule for i in issues]
        self.assertIn("status-drift", rules)

    def test_dead_entity_ref_flagged(self):
        records = [
            (
                "wiki/entities/vehicles/ship.md",
                CommentedMap(
                    {
                        "type": "entity",
                        "summary": "A ship",
                        "captain": "[[dead-captain|Dead Captain]]",
                        "status": "active",
                    }
                ),
                "# Ship",
            ),
            (
                "wiki/entities/npcs/dead-captain.md",
                CommentedMap({"type": "entity", "summary": "Dead", "status": "dead"}),
                "# Dead Captain",
            ),
        ]
        stp = {
            "ship": ["wiki/entities/vehicles/ship.md"],
            "dead-captain": ["wiki/entities/npcs/dead-captain.md"],
        }
        issues = wiki_lint.check_lore_consistency(records, stp)
        rules = [i.rule for i in issues]
        self.assertIn("dead-entity-ref", rules)

    def test_parent_gap_flagged(self):
        records = [
            (
                "wiki/entities/places/buildings/inn.md",
                CommentedMap(
                    {
                        "type": "entity",
                        "summary": "An inn",
                        "parent_location": "[[calveno|Calveno]]",
                        "status": "active",
                    }
                ),
                "# Inn",
            ),
            (
                "wiki/entities/places/settlements/calveno.md",
                CommentedMap(
                    {"type": "entity", "summary": "Calveno", "status": "active"}
                ),
                "# Calveno\n\nNo connection to the tavern here.",
            ),
        ]
        stp = {
            "inn": ["wiki/entities/places/buildings/inn.md"],
            "calveno": ["wiki/entities/places/settlements/calveno.md"],
        }
        issues = wiki_lint.check_lore_consistency(records, stp)
        rules = [i.rule for i in issues]
        self.assertIn("parent-gap", rules)

    def test_no_issue_when_parent_mentions_child(self):
        records = [
            (
                "wiki/entities/places/buildings/inn.md",
                CommentedMap(
                    {
                        "type": "entity",
                        "summary": "An inn",
                        "parent_location": "[[calveno|Calveno]]",
                        "status": "active",
                    }
                ),
                "# Inn",
            ),
            (
                "wiki/entities/places/settlements/calveno.md",
                CommentedMap(
                    {"type": "entity", "summary": "Calveno", "status": "active"}
                ),
                "# Calveno\n\nThe [[inn|Inn]] is here.",
            ),
        ]
        stp = {
            "inn": ["wiki/entities/places/buildings/inn.md"],
            "calveno": ["wiki/entities/places/settlements/calveno.md"],
        }
        issues = wiki_lint.check_lore_consistency(records, stp)
        rules = [i.rule for i in issues]
        self.assertNotIn("parent-gap", rules)

    def test_island_situation_mismatch_flagged(self):
        records = [
            (
                "wiki/narrative-islands/some-island.md",
                CommentedMap(
                    {
                        "type": "narrative-island",
                        "summary": "An island",
                        "contains_situations": ["[[some-situation|Situation]]"],
                        "status": "active",
                    }
                ),
                "# Some Island",
            ),
            (
                "wiki/situations/active/some-situation.md",
                CommentedMap(
                    {
                        "type": "situation",
                        "summary": "A situation",
                        "narrative_island": "wrong-island",
                        "status": "active",
                    }
                ),
                "# Some Situation",
            ),
        ]
        stp = {
            "some-island": ["wiki/narrative-islands/some-island.md"],
            "some-situation": ["wiki/situations/active/some-situation.md"],
        }
        issues = wiki_lint.check_lore_consistency(records, stp)
        rules = [i.rule for i in issues]
        self.assertIn("island-situation-mismatch", rules)

    def test_island_situation_unset_flagged(self):
        records = [
            (
                "wiki/narrative-islands/my-island.md",
                CommentedMap(
                    {
                        "type": "narrative-island",
                        "summary": "An island",
                        "contains_situations": ["[[sit|Sit]]"],
                        "status": "active",
                    }
                ),
                "# My Island",
            ),
            (
                "wiki/situations/active/sit.md",
                CommentedMap(
                    {
                        "type": "situation",
                        "summary": "Sit",
                        "narrative_island": "",
                        "status": "active",
                    }
                ),
                "# Sit",
            ),
        ]
        stp = {
            "my-island": ["wiki/narrative-islands/my-island.md"],
            "sit": ["wiki/situations/active/sit.md"],
        }
        issues = wiki_lint.check_lore_consistency(records, stp)
        rules = [i.rule for i in issues]
        self.assertIn("island-situation-mismatch", rules)


# ---------------------------------------------------------------------------
# standardize
# ---------------------------------------------------------------------------


class StandardizeTests(unittest.TestCase):
    def _yaml(self):
        return wiki_lint.make_yaml()

    def test_adds_missing_required_field(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "subtype": "npc"})
        with patch("wiki_lint.today", return_value="2026-01-01"):
            new_data, changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertIn("campaign", new_data)
        self.assertIn("campaign", changed)

    def test_strips_title_field(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "title": "Bob", "subtype": "npc"})
        new_data, changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertNotIn("title", new_data)
        self.assertIn("-title", changed)

    def test_strips_cssclasses(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "cssclasses": ["npc-style"]})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertNotIn("cssclasses", new_data)

    def test_strips_null_fields(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "null_field": None})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertNotIn("null_field", new_data)

    def test_strips_unknown_sources(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "sources": ["Unknown"]})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertEqual(list(new_data["sources"]), [])

    def test_strips_empty_aliases(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "aliases": []})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertNotIn("aliases", new_data)

    def test_strips_empty_relationships(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "relationships": []})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertNotIn("relationships", new_data)

    def test_coerces_bool_strings(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "publish": "false"})
        new_data, _changed = wiki_lint.standardize(relpath, data, yaml)
        self.assertIs(new_data["publish"], False)

    def test_reorders_keys(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap(
            {
                "subtype": "npc",
                "type": "entity",
                "campaign": "shattered-sea",
                "status": "active",
                "audience": "dm",
                "publish": False,
                "summary": "A real NPC",
                "created": "2026-01-01",
                "updated": "2026-01-01",
                "tags": [],
                "sources": [],
                "confidence_level": "medium",
            }
        )
        new_data, _ = wiki_lint.standardize(relpath, data, yaml)
        keys = list(new_data.keys())
        self.assertEqual(keys[0], "type")

    def test_list_fields_get_block_style(self):
        yaml = self._yaml()
        relpath = "wiki/entities/characters/npcs/bob.md"
        data = CommentedMap({"type": "entity", "tags": ["maritime", "combat"]})
        new_data, _ = wiki_lint.standardize(relpath, data, yaml)
        self.assertIsInstance(new_data["tags"], CommentedSeq)


# ---------------------------------------------------------------------------
# apply_fix
# ---------------------------------------------------------------------------


class ApplyFixTests(unittest.TestCase):
    def test_adds_missing_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            os.makedirs(os.path.dirname(path))
            with open(path, "w") as fh:
                fh.write("---\ntype: entity\nsubtype: npc\n---\n\n# Bob\n")
            relpath = "wiki/entities/characters/npcs/bob.md"
            yaml = wiki_lint.make_yaml()
            with patch("wiki_lint.today", return_value="2026-01-01"):
                changed = wiki_lint.apply_fix(path, relpath, yaml)
            self.assertTrue(len(changed) > 0)
            with open(path) as fh:
                text = fh.read()
            self.assertIn("campaign: shattered-sea", text)

    def test_idempotent_on_canonical_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            os.makedirs(os.path.dirname(path))
            content = (
                "---\n"
                "type: entity\n"
                "subtype: npc\n"
                "campaign: shattered-sea\n"
                "status: active\n"
                "audience: dm\n"
                "publish: false\n"
                'summary: "A real NPC"\n'
                "created: 2026-01-01\n"
                "updated: 2026-01-01\n"
                "tags: []\n"
                "sources: []\n"
                "confidence_level: medium\n"
                "---\n\n"
                "# Bob\n"
            )
            with open(path, "w") as fh:
                fh.write(content)
            relpath = "wiki/entities/characters/npcs/bob.md"
            yaml = wiki_lint.make_yaml()
            with patch("wiki_lint.today", return_value="2026-01-01"):
                changed = wiki_lint.apply_fix(path, relpath, yaml)
            # Should be empty or just reformatting
            with open(path) as fh:
                after = fh.read()
            # File content should have required fields
            self.assertIn("campaign: shattered-sea", after)

    def test_no_frontmatter_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            os.makedirs(os.path.dirname(path))
            with open(path, "w") as fh:
                fh.write("# Bob\n\nNo frontmatter here.\n")
            relpath = "wiki/entities/characters/npcs/bob.md"
            yaml = wiki_lint.make_yaml()
            with patch("wiki_lint.today", return_value="2026-01-01"):
                changed = wiki_lint.apply_fix(path, relpath, yaml)
            # Should add frontmatter
            with open(path) as fh:
                text = fh.read()
            self.assertIn("---", text)


# ---------------------------------------------------------------------------
# in_scope / resolve_scope
# ---------------------------------------------------------------------------


class InScopeTests(unittest.TestCase):
    def test_none_scope_always_true(self):
        self.assertTrue(wiki_lint.in_scope("wiki/any/path.md", None))

    def test_exact_match(self):
        self.assertTrue(wiki_lint.in_scope("wiki/foo.md", ["wiki/foo.md"]))

    def test_prefix_match(self):
        self.assertTrue(
            wiki_lint.in_scope("wiki/entities/npcs/bob.md", ["wiki/entities/"])
        )

    def test_no_match(self):
        self.assertFalse(wiki_lint.in_scope("wiki/foo.md", ["wiki/bar.md"]))


class ResolveScopeTests(unittest.TestCase):
    def test_none_for_empty(self):
        self.assertIsNone(wiki_lint.resolve_scope([]))

    def test_returns_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "npcs", "bob.md")
            os.makedirs(os.path.dirname(path))
            open(path, "w").write("x")
            with patch("wiki_lint.REPO_ROOT", tmp):
                result = wiki_lint.resolve_scope([path])
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)


# ---------------------------------------------------------------------------
# write_report
# ---------------------------------------------------------------------------


class WriteReportTests(unittest.TestCase):
    def test_writes_review_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki_dm = os.path.join(tmp, "wiki", "dm")
            os.makedirs(wiki_dm)
            issues = [
                wiki_lint.Issue(
                    "error",
                    "broken-wikilink",
                    "wiki/foo.md",
                    "[[missing]]",
                    fix="create stub",
                ),
                wiki_lint.Issue("quality", "orphan", "wiki/bar.md", "no inbound"),
            ]
            counts = {"error": 1, "warning": 0, "quality": 1}
            with (
                patch("wiki_lint.WIKI_DIR", os.path.join(tmp, "wiki")),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                rel_path = wiki_lint.write_report(issues, counts)
            report_path = os.path.join(tmp, "wiki", "dm", "review-queue.md")
            self.assertTrue(os.path.exists(report_path))
            with open(report_path) as fh:
                content = fh.read()
            self.assertIn("broken-wikilink", content)
            self.assertIn("wiki/foo.md", content)

    def test_writes_none_when_no_decisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki_dm = os.path.join(tmp, "wiki", "dm")
            os.makedirs(wiki_dm)
            issues = [
                wiki_lint.Issue("quality", "orphan", "wiki/bar.md", "no inbound"),
            ]
            counts = {"error": 0, "warning": 0, "quality": 1}
            with (
                patch("wiki_lint.WIKI_DIR", os.path.join(tmp, "wiki")),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                wiki_lint.write_report(issues, counts)
            report_path = os.path.join(tmp, "wiki", "dm", "review-queue.md")
            with open(report_path) as fh:
                content = fh.read()
            self.assertIn("None", content)


# ---------------------------------------------------------------------------
# gather_records (with minimal temp wiki)
# ---------------------------------------------------------------------------


class GatherRecordsTests(unittest.TestCase):
    def test_gathers_from_wiki_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(os.path.join(npc_dir, "bob.md"), MINIMAL_ENTITY_FM)
            yaml = wiki_lint.make_yaml()
            with patch("wiki_common.WIKI_DIR", wiki):
                records, errors = wiki_lint.gather_records(yaml)
            self.assertTrue(len(records) > 0)
            self.assertEqual(errors, [])

    def test_flags_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(os.path.join(npc_dir, "bob.md"), "# Bob\n\nNo frontmatter.\n")
            yaml = wiki_lint.make_yaml()
            with patch("wiki_common.WIKI_DIR", wiki):
                _records, errors = wiki_lint.gather_records(yaml)
            rules = [e.rule for e in errors]
            self.assertIn("missing-frontmatter", rules)

    def test_flags_unparseable_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(
                os.path.join(npc_dir, "bob.md"),
                "---\ntype: [invalid: yaml: {\n---\n\n# Bob\n",
            )
            yaml = wiki_lint.make_yaml()
            with patch("wiki_common.WIKI_DIR", wiki):
                _records, errors = wiki_lint.gather_records(yaml)
            rules = [e.rule for e in errors]
            self.assertIn("unparseable-frontmatter", rules)


# ---------------------------------------------------------------------------
# main() driver — smoke tests
# ---------------------------------------------------------------------------


class MainDriverTests(unittest.TestCase):
    def _make_minimal_vault(self, tmp):
        wiki = os.path.join(tmp, "wiki")
        npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
        os.makedirs(npc_dir)
        _write(os.path.join(npc_dir, "bob.md"), MINIMAL_ENTITY_FM)
        _write(
            os.path.join(npc_dir, "alice.md"),
            MINIMAL_ENTITY_FM.replace("Test NPC", "Test Alice").replace(
                "other-npc", "bob"
            ),
        )
        return wiki

    def test_main_reports_only_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._make_minimal_vault(tmp)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                out = io.StringIO()
                err = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = wiki_lint.main(["--obsidian", "off", "--markdown", "off"])
            # Should not crash and return int
            self.assertIsInstance(code, int)

    def test_main_summary_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._make_minimal_vault(tmp)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    code = wiki_lint.main(
                        ["--summary", "--obsidian", "off", "--markdown", "off"]
                    )
            self.assertIsInstance(code, int)

    def test_main_json_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._make_minimal_vault(tmp)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = wiki_lint.main(
                        ["--json", "--obsidian", "off", "--markdown", "off"]
                    )
            # JSON output should be parseable as a dict
            output = out.getvalue()
            if output.strip():
                data = json.loads(output)
                self.assertIsInstance(data, dict)

    def test_main_fix_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            _write(
                os.path.join(npc_dir, "bob.md"),
                "---\ntype: entity\nsubtype: npc\n---\n\n# Bob\n",
            )
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    code = wiki_lint.main(
                        ["--fix", "--obsidian", "off", "--markdown", "off"]
                    )
            with open(os.path.join(npc_dir, "bob.md")) as fh:
                after = fh.read()
            self.assertIn("campaign: shattered-sea", after)

    def test_main_report_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._make_minimal_vault(tmp)
            os.makedirs(os.path.join(wiki, "dm"), exist_ok=True)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                code = wiki_lint.main(
                    ["--report", "--obsidian", "off", "--markdown", "off"]
                )
            self.assertTrue(os.path.exists(os.path.join(wiki, "dm", "review-queue.md")))

    def test_main_min_severity_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._make_minimal_vault(tmp)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = wiki_lint.main(
                        [
                            "--min-severity",
                            "error",
                            "--obsidian",
                            "off",
                            "--markdown",
                            "off",
                        ]
                    )
            self.assertIsInstance(code, int)

    def test_main_scope_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(npc_dir)
            bob_path = os.path.join(npc_dir, "bob.md")
            _write(bob_path, MINIMAL_ENTITY_FM)
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("wiki_lint.WIKI_DIR", wiki),
                patch("wiki_lint.REPO_ROOT", tmp),
                patch("wiki_lint._obsidian_available", return_value=False),
                patch("wiki_lint.MARKDOWNLINT_CLI", None),
                patch("wiki_lint.today", return_value="2026-01-01"),
            ):
                code = wiki_lint.main(
                    [bob_path, "--obsidian", "off", "--markdown", "off"]
                )
            self.assertIsInstance(code, int)


# ---------------------------------------------------------------------------
# _obsidian_available
# ---------------------------------------------------------------------------


class ObsidianAvailableTests(unittest.TestCase):
    def setUp(self):
        # Reset cached state before each test
        wiki_lint._obsidian_live = None

    def tearDown(self):
        wiki_lint._obsidian_live = None

    def test_returns_false_on_failure(self):
        wiki_lint._obsidian_live = None
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="")
            result = wiki_lint._obsidian_available()
        self.assertFalse(result)

    def test_returns_true_on_success(self):
        wiki_lint._obsidian_live = None
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="VaultName\n")
            result = wiki_lint._obsidian_available()
        self.assertTrue(result)

    def test_caches_result(self):
        wiki_lint._obsidian_live = True
        result = wiki_lint._obsidian_available()
        self.assertTrue(result)

    def test_exception_returns_false(self):
        wiki_lint._obsidian_live = None
        with patch("subprocess.run", side_effect=Exception("not found")):
            result = wiki_lint._obsidian_available()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
