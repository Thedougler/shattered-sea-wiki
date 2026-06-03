#!/usr/bin/env python3
"""Tests for tag_taxonomy, regen_index, archive_source, wiki_common."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import archive_source
import regen_index
import tag_taxonomy
import wiki_common

# ---------------------------------------------------------------------------
# tag_taxonomy
# ---------------------------------------------------------------------------


class TagTaxonomyClassifyTests(unittest.TestCase):
    def test_canonical_tags(self):
        for tag in ["dravosi", "tessarine", "passage", "maritime", "combat", "undead"]:
            cat, _ = tag_taxonomy.classify(tag)
            self.assertEqual(cat, "canonical", f"expected canonical for {tag!r}")

    def test_canonical_case_insensitive(self):
        cat, _ = tag_taxonomy.classify("Dravosi")
        self.assertEqual(cat, "canonical")

    def test_alias_dravosi_crown(self):
        cat, canon = tag_taxonomy.classify("dravosi-crown")
        self.assertEqual(cat, "alias")
        self.assertEqual(canon, "dravosi")

    def test_alias_maw(self):
        cat, canon = tag_taxonomy.classify("maw")
        self.assertEqual(cat, "alias")
        self.assertEqual(canon, "drowned-maw")

    def test_alias_dm_notes(self):
        cat, canon = tag_taxonomy.classify("dm-notes")
        self.assertEqual(cat, "alias")
        self.assertEqual(canon, "dm-prep")

    def test_deprecated_frontmatter_situation(self):
        cat, _ = tag_taxonomy.classify("situation")
        self.assertEqual(cat, "deprecated-fm")

    def test_deprecated_frontmatter_session(self):
        cat, _ = tag_taxonomy.classify("session")
        self.assertEqual(cat, "deprecated-fm")

    def test_deprecated_entity_perrin(self):
        cat, _ = tag_taxonomy.classify("perrin")
        self.assertEqual(cat, "deprecated-entity")

    def test_deprecated_entity_calveno(self):
        cat, _ = tag_taxonomy.classify("calveno")
        self.assertEqual(cat, "deprecated-entity")

    def test_deprecated_source_phb(self):
        cat, _ = tag_taxonomy.classify("phb")
        self.assertEqual(cat, "deprecated-source")

    def test_deprecated_source_bestiary(self):
        cat, _ = tag_taxonomy.classify("bestiary")
        self.assertEqual(cat, "deprecated-source")

    def test_deprecated_system_lint(self):
        cat, _ = tag_taxonomy.classify("lint")
        self.assertEqual(cat, "deprecated-system")

    def test_deprecated_system_review(self):
        cat, _ = tag_taxonomy.classify("review")
        self.assertEqual(cat, "deprecated-system")

    def test_unknown_tag(self):
        cat, _ = tag_taxonomy.classify("completely-unknown-xyz-999")
        self.assertEqual(cat, "unknown")

    def test_visibility_prefix(self):
        cat, _ = tag_taxonomy.classify("visibility/public")
        self.assertEqual(cat, "visibility")

    def test_visibility_any_suffix(self):
        cat, _ = tag_taxonomy.classify("visibility/dm-only")
        self.assertEqual(cat, "visibility")

    def test_tag_limit_constant(self):
        self.assertEqual(tag_taxonomy.TAG_LIMIT, 5)

    def test_canonical_is_frozenset(self):
        self.assertIsInstance(tag_taxonomy.CANONICAL, frozenset)
        self.assertIn("maritime", tag_taxonomy.CANONICAL)

    def test_aliases_dict(self):
        self.assertIsInstance(tag_taxonomy.ALIASES, dict)
        self.assertIn("maw", tag_taxonomy.ALIASES)

    def test_deprecated_fm_frozenset(self):
        self.assertIn("situation", tag_taxonomy.DEPRECATED_FRONTMATTER)

    def test_deprecated_entity_frozenset(self):
        self.assertIn("perrin", tag_taxonomy.DEPRECATED_ENTITY_NAMES)

    def test_deprecated_source_frozenset(self):
        self.assertIn("phb", tag_taxonomy.DEPRECATED_SOURCE)

    def test_deprecated_system_frozenset(self):
        self.assertIn("lint", tag_taxonomy.DEPRECATED_SYSTEM)


# ---------------------------------------------------------------------------
# regen_index
# ---------------------------------------------------------------------------


def _make_wiki_file(root, relpath, content):
    abs_path = os.path.join(root, relpath)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return abs_path


class RegenIndexPureFunctionTests(unittest.TestCase):
    def test_slug_of(self):
        self.assertEqual(regen_index.slug_of("/some/path/foo-bar.md"), "foo-bar")

    def test_title_of_from_h1(self):
        body = "# The Great Serpent\n\nSome text"
        self.assertEqual(
            regen_index.title_of("the-great-serpent", body), "The Great Serpent"
        )

    def test_title_of_from_slug_when_no_h1(self):
        title = regen_index.title_of("foo-bar-baz", "No heading here")
        self.assertEqual(title, "Foo Bar Baz")

    def test_marker_of_stub(self):
        self.assertEqual(regen_index.marker_of({"status": "stub"}), "[stub] ")

    def test_marker_of_dm_only_subtype(self):
        self.assertEqual(regen_index.marker_of({"subtype": "secret"}), "[DM-only] ")

    def test_marker_of_dm_only_tag(self):
        self.assertEqual(
            regen_index.marker_of({"tags": ["dm-only", "other"]}), "[DM-only] "
        )

    def test_marker_of_dm_only_stub(self):
        marker = regen_index.marker_of({"status": "stub", "subtype": "secret"})
        self.assertEqual(marker, "[DM-only stub] ")

    def test_marker_of_normal(self):
        self.assertEqual(regen_index.marker_of({}), "")

    def test_group_key_nested(self):
        gk = regen_index.group_key("wiki/entities/characters/npcs/bob.md")
        self.assertEqual(gk, "entities/characters/npcs")

    def test_group_key_root(self):
        gk = regen_index.group_key("wiki/hot.md")
        self.assertEqual(gk, "(root)")

    def test_group_sort_key_priority(self):
        k1 = regen_index.group_sort_key("entities/characters/pcs")
        k2 = regen_index.group_sort_key("zzz-unknown")
        self.assertLess(k1[0], k2[0])

    def test_group_sort_key_unlisted_alphabetical(self):
        k1 = regen_index.group_sort_key("alpha-group")
        k2 = regen_index.group_sort_key("zeta-group")
        self.assertLess(k1, k2)

    def test_is_compact_exact(self):
        self.assertTrue(regen_index.is_compact("entities/items"))

    def test_is_compact_prefix(self):
        self.assertTrue(regen_index.is_compact("entities/items/weapons"))

    def test_is_compact_false(self):
        self.assertFalse(regen_index.is_compact("entities/characters/npcs"))


class RegenIndexBuildTests(unittest.TestCase):
    def _make_minimal_wiki(self, tmp):
        wiki = os.path.join(tmp, "wiki")
        npc_dir = os.path.join(wiki, "entities", "characters", "npcs")
        os.makedirs(npc_dir)
        _make_wiki_file(
            tmp,
            "wiki/entities/characters/npcs/bob.md",
            "---\ntype: entity\nsubtype: npc\nsummary: A test NPC\nstatus: active\n---\n\n# Bob\n",
        )
        _make_wiki_file(
            tmp,
            "wiki/entities/items/sword.md",
            "---\ntype: entity\nsubtype: item\nsummary: A sword\nstatus: active\n---\n\n# The Sword\n",
        )
        return wiki

    def test_build_produces_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_minimal_wiki(tmp)
            with patch("wiki_common.WIKI_DIR", os.path.join(tmp, "wiki")):
                result = regen_index.build()
        self.assertIsInstance(result, str)
        self.assertIn("bob", result)

    def test_build_includes_compact_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_minimal_wiki(tmp)
            with patch("wiki_common.WIKI_DIR", os.path.join(tmp, "wiki")):
                result = regen_index.build()
        self.assertIn("entities/items", result)

    def test_build_skips_index_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_minimal_wiki(tmp)
            _make_wiki_file(tmp, "wiki/index.md", "---\ntype: system\n---\n# Index\n")
            with patch("wiki_common.WIKI_DIR", os.path.join(tmp, "wiki")):
                result = regen_index.build()
        self.assertNotIn("[[index", result)

    def test_build_includes_stub_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(os.path.join(wiki, "entities", "characters", "npcs"))
            _make_wiki_file(
                tmp,
                "wiki/entities/characters/npcs/stub-npc.md",
                "---\ntype: entity\nsubtype: npc\nsummary: Stub\nstatus: stub\n---\n\n# Stub NPC\n",
            )
            with patch("wiki_common.WIKI_DIR", wiki):
                result = regen_index.build()
        self.assertIn("[stub]", result)

    def test_main_writes_to_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(os.path.join(wiki, "entities", "characters", "npcs"))
            _make_wiki_file(
                tmp,
                "wiki/entities/characters/npcs/bob.md",
                "---\ntype: entity\nsubtype: npc\nsummary: Bob\nstatus: active\n---\n\n# Bob\n",
            )
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("regen_index.today", return_value="2026-01-01"),
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = regen_index.main([])
            self.assertEqual(code, 0)
            self.assertIn("bob", out.getvalue())

    def test_main_write_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            dm_dir = os.path.join(wiki, "entities", "characters", "npcs")
            os.makedirs(dm_dir)
            _make_wiki_file(
                tmp,
                "wiki/entities/characters/npcs/bob.md",
                "---\ntype: entity\nsubtype: npc\nsummary: Bob\nstatus: active\n---\n\n# Bob\n",
            )
            with (
                patch("wiki_common.WIKI_DIR", wiki),
                patch("regen_index.WIKI_DIR", wiki),
                patch("regen_index.today", return_value="2026-01-01"),
            ):
                code = regen_index.main(["--write"])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(os.path.join(wiki, "index.md")))


# ---------------------------------------------------------------------------
# archive_source
# ---------------------------------------------------------------------------


class ArchiveSourceSubdirTests(unittest.TestCase):
    def test_session_type(self):
        self.assertEqual(archive_source.subdir_for("session"), "sessions")

    def test_transcript_type(self):
        self.assertEqual(archive_source.subdir_for("transcript"), "sessions")

    def test_entity_source(self):
        self.assertEqual(archive_source.subdir_for("entity-source"), "characters")

    def test_homebrew_type(self):
        self.assertEqual(archive_source.subdir_for("homebrew"), "homebrew")

    def test_asset_type(self):
        self.assertEqual(archive_source.subdir_for("asset"), "assets")

    def test_unknown_type_default(self):
        self.assertEqual(archive_source.subdir_for("faction-source"), "reference")

    def test_empty_type_default(self):
        self.assertEqual(archive_source.subdir_for(""), "reference")

    def test_rules_type(self):
        self.assertEqual(archive_source.subdir_for("rules-or-homebrew"), "homebrew")


class ArchiveSourceSidecarTests(unittest.TestCase):
    def test_no_sidecar_when_no_pdf_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "source.md")
            with open(path, "w") as fh:
                fh.write("---\ntype: entity\n---\n# No sidecar\n")
            result = archive_source.find_pdf_sidecar(path)
            self.assertIsNone(result)

    def test_finds_existing_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = os.path.join(tmp, "sheet.pdf")
            open(pdf_path, "wb").write(b"%PDF")
            md_path = os.path.join(tmp, "source.md")
            with open(md_path, "w") as fh:
                fh.write("---\ntype: entity\npdf_sidecar: sheet.pdf\n---\n# Source\n")
            result = archive_source.find_pdf_sidecar(md_path)
            self.assertEqual(result, os.path.abspath(pdf_path))

    def test_returns_none_for_missing_sidecar_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "source.md")
            with open(md_path, "w") as fh:
                fh.write("---\ntype: entity\npdf_sidecar: missing.pdf\n---\n# Source\n")
            result = archive_source.find_pdf_sidecar(md_path)
            self.assertIsNone(result)


class ArchiveSourceMainTests(unittest.TestCase):
    def test_main_file_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = archive_source.main([os.path.join(tmp, "nonexistent.md")])
            self.assertEqual(code, 1)
            self.assertIn("not found", err.getvalue())

    def test_main_destination_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            dest_dir = os.path.join(tmp, ".raw", "reference")
            os.makedirs(dest_dir)
            open(src, "w").write("content")
            open(os.path.join(dest_dir, "source.md"), "w").write("already there")
            with patch("archive_source.REPO_ROOT", tmp):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    code = archive_source.main([src, "--type", "faction-source"])
            self.assertEqual(code, 1)
            self.assertIn("destination exists", err.getvalue())

    def test_main_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            open(src, "w").write("content")
            with patch("archive_source.REPO_ROOT", tmp):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = archive_source.main([src, "--type", "session", "--dry-run"])
            self.assertEqual(code, 0)
            self.assertIn("would move", out.getvalue())

    def test_main_dry_run_no_type_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            open(src, "w").write("content")
            with patch("archive_source.REPO_ROOT", tmp):
                err = io.StringIO()
                out = io.StringIO()
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
                    code = archive_source.main([src, "--dry-run"])
            self.assertEqual(code, 0)
            self.assertIn("defaulting", err.getvalue())

    def test_main_dry_run_with_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            pdf = os.path.join(tmp, "sheet.pdf")
            open(pdf, "wb").write(b"%PDF")
            with open(src, "w") as fh:
                fh.write("---\npdf_sidecar: sheet.pdf\n---\n# Source\n")
            with patch("archive_source.REPO_ROOT", tmp):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = archive_source.main([src, "--type", "session", "--dry-run"])
            self.assertEqual(code, 0)
            self.assertIn("pdf sidecar", out.getvalue())

    def test_main_moves_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            open(src, "w").write("content")

            def fake_git(*args, check=True):
                m = MagicMock()
                m.returncode = 0
                return m

            with (
                patch("archive_source.REPO_ROOT", tmp),
                patch("archive_source.git", side_effect=fake_git),
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = archive_source.main([src, "--type", "session"])
            self.assertEqual(code, 0)
            self.assertIn("archived", out.getvalue())

    def test_main_falls_back_to_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source.md")
            open(src, "w").write("content")

            def fake_git(*args, check=True):
                m = MagicMock()
                m.returncode = 1
                return m

            with (
                patch("archive_source.REPO_ROOT", tmp),
                patch("archive_source.git", side_effect=fake_git),
            ):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = archive_source.main([src, "--type", "session"])
            self.assertEqual(code, 0)
            dest = os.path.join(tmp, ".raw", "sessions", "source.md")
            self.assertTrue(os.path.exists(dest))


# ---------------------------------------------------------------------------
# wiki_common
# ---------------------------------------------------------------------------


class WikiCommonTests(unittest.TestCase):
    def test_today_returns_date_string(self):
        result = wiki_common.today()
        self.assertRegex(result, r"^\d{4}-\d{2}-\d{2}$")

    def test_split_frontmatter_normal(self):
        text = "---\ntype: entity\n---\n\n# Body"
        fm, body, had = wiki_common.split_frontmatter(text)
        self.assertTrue(had)
        self.assertIn("type: entity", fm)
        self.assertIn("# Body", body)

    def test_split_frontmatter_no_closing_delimiter(self):
        text = "---\ntype: entity\nno closing delimiter"
        _fm, body, had = wiki_common.split_frontmatter(text)
        self.assertFalse(had)
        self.assertEqual(body, text)

    def test_split_frontmatter_no_leading_delimiter(self):
        text = "# Just a heading\nNo frontmatter"
        _fm, _body, had = wiki_common.split_frontmatter(text)
        self.assertFalse(had)

    def test_parse_fields(self):
        lines = ["type: entity", "subtype: npc", "status: active"]
        fields = wiki_common.parse_fields(lines)
        self.assertEqual(fields["type"], "entity")
        self.assertEqual(fields["subtype"], "npc")

    def test_parse_fields_ignores_continuation(self):
        lines = ["type: entity", "  continuation line"]
        fields = wiki_common.parse_fields(lines)
        self.assertNotIn("  continuation", fields)

    def test_get_summary_strips_quotes(self):
        fields = {"summary": '"A quoted summary"'}
        self.assertEqual(wiki_common.get_summary(fields), "A quoted summary")

    def test_get_summary_empty(self):
        self.assertEqual(wiki_common.get_summary({}), "")

    def test_first_h1(self):
        body = "# My Title\n\nSome text"
        self.assertEqual(wiki_common.first_h1(body), "My Title")

    def test_first_h1_strips_stub_suffix(self):
        body = "# My Title — Stub\n\nText"
        self.assertEqual(wiki_common.first_h1(body), "My Title")

    def test_first_h1_none_when_absent(self):
        self.assertIsNone(wiki_common.first_h1("No heading here"))

    def test_first_h1_skips_h2(self):
        body = "## H2\n\n# H1 Title"
        self.assertEqual(wiki_common.first_h1(body), "H1 Title")

    def test_rel_returns_relative_path(self):
        result = wiki_common.rel(os.path.join(wiki_common.REPO_ROOT, "wiki", "test.md"))
        self.assertEqual(result, "wiki/test.md")

    def test_infer_type_entity(self):
        self.assertEqual(
            wiki_common.infer_type("wiki/entities/places/foo.md"), "entity"
        )

    def test_infer_type_situation(self):
        self.assertEqual(
            wiki_common.infer_type("wiki/situations/active/foo.md"), "situation"
        )

    def test_infer_type_session(self):
        self.assertEqual(
            wiki_common.infer_type("wiki/sessions/session-01.md"), "session"
        )

    def test_infer_type_system(self):
        self.assertEqual(wiki_common.infer_type("wiki/system/index.md"), "system")

    def test_infer_type_lore(self):
        self.assertEqual(wiki_common.infer_type("wiki/lore/foo.md"), "lore")

    def test_infer_type_dm(self):
        self.assertEqual(wiki_common.infer_type("wiki/dm/foo.md"), "dm-intelligence")

    def test_infer_type_raw(self):
        self.assertEqual(wiki_common.infer_type(".raw/sessions/foo.md"), "raw")

    def test_infer_type_governance_root(self):
        self.assertEqual(wiki_common.infer_type("CLAUDE.md"), "governance")

    def test_infer_type_unknown(self):
        self.assertEqual(wiki_common.infer_type("some/other/path.md"), "unknown")

    def test_infer_subtype_pc(self):
        self.assertEqual(
            wiki_common.infer_subtype("wiki/entities/characters/pcs/bob.md"), "pc"
        )

    def test_infer_subtype_npc(self):
        self.assertEqual(
            wiki_common.infer_subtype("wiki/entities/characters/npcs/bob.md"), "npc"
        )

    def test_infer_subtype_faction(self):
        self.assertEqual(
            wiki_common.infer_subtype("wiki/entities/factions/foo.md"), "faction"
        )

    def test_infer_subtype_island_place(self):
        self.assertEqual(
            wiki_common.infer_subtype("wiki/entities/places/islands/foo.md"),
            "island-place",
        )

    def test_infer_subtype_unknown(self):
        self.assertEqual(wiki_common.infer_subtype("some/weird/path.md"), "unknown")

    def test_infer_subtype_session_note(self):
        self.assertEqual(
            wiki_common.infer_subtype("wiki/sessions/session-01.md"), "session-note"
        )

    def test_iter_wiki_files_returns_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(os.path.join(wiki, "entities"))
            open(os.path.join(wiki, "entities", "foo.md"), "w").write("x")
            open(os.path.join(wiki, "entities", "bar.txt"), "w").write("x")
            with patch("wiki_common.WIKI_DIR", wiki):
                files = list(wiki_common.iter_wiki_files())
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith("foo.md"))


if __name__ == "__main__":
    unittest.main()
