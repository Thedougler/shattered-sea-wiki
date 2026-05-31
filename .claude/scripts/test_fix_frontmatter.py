#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

import fix_frontmatter


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


TODAY = "2026-01-15"


@patch("fix_frontmatter.today", return_value=TODAY)
class FixFrontmatterTests(unittest.TestCase):
    def test_adds_missing_fields_to_partial_frontmatter(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            write(path, "---\ntype: entity\nsubtype: npc\n---\n\n# Bob\n")

            with patch("wiki_common.REPO_ROOT", tmp):
                changed = fix_frontmatter.process(path)

            self.assertTrue(changed)
            result = read(path)
            self.assertIn("campaign: shattered-sea", result)
            self.assertIn("status: unknown", result)
            self.assertIn(f"updated: {TODAY}", result)
            self.assertIn("confidence_level: medium", result)
            self.assertIn("# Bob", result)

    def test_idempotent_on_complete_file(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            complete = (
                "---\n"
                "type: entity\n"
                "subtype: npc\n"
                "campaign: shattered-sea\n"
                "status: active\n"
                "audience: dm\n"
                "publish: false\n"
                'summary: "Bob the builder"\n'
                f"created: {TODAY}\n"
                f"updated: {TODAY}\n"
                "tags: []\n"
                "sources: []\n"
                "confidence_level: high\n"
                "---\n\n# Bob\n"
            )
            write(path, complete)

            with patch("wiki_common.REPO_ROOT", tmp):
                changed = fix_frontmatter.process(path)

            self.assertFalse(changed)
            self.assertEqual(read(path), complete)

    def test_synthesizes_frontmatter_for_bare_file(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "lore", "history", "old-wars.md")
            write(path, "# Old Wars\n\nSome lore content.\n")

            with patch("wiki_common.REPO_ROOT", tmp):
                changed = fix_frontmatter.process(path)

            self.assertTrue(changed)
            result = read(path)
            self.assertTrue(result.startswith("---\n"))
            self.assertIn("type: lore", result)
            self.assertIn("subtype: history", result)
            self.assertIn("# Old Wars", result)

    def test_updates_stale_date(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            complete = (
                "---\n"
                "type: entity\n"
                "subtype: npc\n"
                "campaign: shattered-sea\n"
                "status: active\n"
                "audience: dm\n"
                "publish: false\n"
                'summary: "Bob"\n'
                "created: 2025-01-01\n"
                "updated: 2025-01-01\n"
                "tags: []\n"
                "sources: []\n"
                "confidence_level: high\n"
                "---\n\n# Bob\n"
            )
            write(path, complete)

            with patch("wiki_common.REPO_ROOT", tmp):
                changed = fix_frontmatter.process(path)

            self.assertTrue(changed)
            result = read(path)
            self.assertIn(f"updated: {TODAY}", result)
            self.assertNotIn("updated: 2025-01-01", result)

    def test_adds_type_specific_fields_for_situation(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "situations", "active", "trouble.md")
            write(path, "---\ntype: situation\n---\n\n# Trouble\n")

            with patch("wiki_common.REPO_ROOT", tmp):
                fix_frontmatter.process(path)

            result = read(path)
            self.assertIn("lifecycle: dormant", result)
            self.assertIn("narrative_island: null", result)

    def test_flags_stub_summary_on_stderr(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            write(
                path,
                '---\ntype: entity\nsummary: "Stub — no summary yet."\nupdated: '
                + TODAY
                + "\n---\n\n# Bob\n",
            )

            stderr = io.StringIO()
            with (
                patch("wiki_common.REPO_ROOT", tmp),
                contextlib.redirect_stderr(stderr),
            ):
                fix_frontmatter.process(path)

            self.assertIn("FLAG: summary-stale", stderr.getvalue())

    def test_never_overwrites_existing_values(self, _mock_today) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wiki", "entities", "characters", "npcs", "bob.md")
            write(
                path,
                "---\ntype: entity\nstatus: active\ncampaign: other-campaign\nupdated: "
                + TODAY
                + "\n---\n\n# Bob\n",
            )

            with patch("wiki_common.REPO_ROOT", tmp):
                fix_frontmatter.process(path)

            result = read(path)
            self.assertIn("status: active", result)
            self.assertIn("campaign: other-campaign", result)


if __name__ == "__main__":
    unittest.main()
