#!/usr/bin/env python3
"""Direct unit tests for wiki_health_snapshot.py functions.

The existing test_wiki_health_snapshot.py runs the script as a subprocess,
which doesn't count toward coverage. These tests import functions directly.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import wiki_health_snapshot as whs


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


STUB_FILE = """\
---
type: entity
summary: Stub — no summary yet.
status: active
---

# Test NPC
"""

FULL_FILE = """\
---
type: entity
summary: "A real NPC with full details"
status: active
---

# Real NPC

Some content here.
"""

NO_FM_FILE = "# No frontmatter\n\nJust content.\n"


# ---------------------------------------------------------------------------
# _extract_summary
# ---------------------------------------------------------------------------


class ExtractSummaryTests(unittest.TestCase):
    def test_extracts_quoted_summary(self):
        text = '---\ntype: entity\nsummary: "A quoted summary"\n---\n\n# Body'
        result = whs._extract_summary(text)
        self.assertEqual(result, "A quoted summary")

    def test_extracts_unquoted_summary(self):
        text = "---\ntype: entity\nsummary: A plain summary\n---\n\n# Body"
        result = whs._extract_summary(text)
        self.assertEqual(result, "A plain summary")

    def test_returns_none_when_no_summary(self):
        text = "---\ntype: entity\nstatus: active\n---\n\n# Body"
        result = whs._extract_summary(text)
        self.assertIsNone(result)

    def test_returns_none_when_no_frontmatter(self):
        text = "# Just a heading\nNo frontmatter."
        result = whs._extract_summary(text)
        self.assertIsNone(result)

    def test_strips_quotes(self):
        text = "---\nsummary: 'single quoted'\n---\n# B"
        result = whs._extract_summary(text)
        self.assertEqual(result, "single quoted")


# ---------------------------------------------------------------------------
# count_wiki_files
# ---------------------------------------------------------------------------


class CountWikiFilesTests(unittest.TestCase):
    def test_counts_md_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(os.path.join(wiki, "entities", "npcs"))
            _write(os.path.join(wiki, "entities", "npcs", "bob.md"), FULL_FILE)
            _write(os.path.join(wiki, "entities", "npcs", "stub.md"), STUB_FILE)
            _write(os.path.join(wiki, "entities", "npcs", "other.txt"), "not md")
            with patch.object(whs, "WIKI_DIR", wiki):
                count, chars, stubs = whs.count_wiki_files()
        self.assertEqual(count, 2)
        self.assertGreater(chars, 0)
        self.assertEqual(stubs, 1)

    def test_empty_wiki(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(wiki)
            with patch.object(whs, "WIKI_DIR", wiki):
                count, chars, stubs = whs.count_wiki_files()
        self.assertEqual(count, 0)
        self.assertEqual(chars, 0)
        self.assertEqual(stubs, 0)

    def test_stub_patterns_match(self):
        stub_contents = [
            "---\nsummary: Stub — no summary yet.\n---\n# X",
            "---\nsummary: no summary provided\n---\n# X",
            "---\nsummary: TBD\n---\n# X",
            "---\nsummary: placeholder content\n---\n# X",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            os.makedirs(wiki)
            for i, content in enumerate(stub_contents):
                _write(os.path.join(wiki, f"file{i}.md"), content)
            with patch.object(whs, "WIKI_DIR", wiki):
                count, _, stubs = whs.count_wiki_files()
        self.assertEqual(count, len(stub_contents))
        self.assertEqual(stubs, len(stub_contents))


# ---------------------------------------------------------------------------
# count_hooks
# ---------------------------------------------------------------------------


class CountHooksTests(unittest.TestCase):
    def test_counts_hooks_from_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = {
                "hooks": {
                    "PostToolUse": [
                        {"hooks": ["hook1", "hook2"]},
                        {"hooks": ["hook3"]},
                    ]
                }
            }
            settings_path = os.path.join(tmp, ".claude", "settings.json")
            _write(settings_path, json.dumps(settings))
            with patch.object(whs, "REPO_ROOT", tmp):
                count = whs.count_hooks()
        self.assertEqual(count, 3)

    def test_returns_zero_when_no_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(whs, "REPO_ROOT", tmp):
                count = whs.count_hooks()
        self.assertEqual(count, 0)

    def test_returns_zero_on_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings_path = os.path.join(tmp, ".claude", "settings.json")
            _write(settings_path, "not valid json {")
            with patch.object(whs, "REPO_ROOT", tmp):
                count = whs.count_hooks()
        self.assertEqual(count, 0)

    def test_no_post_tool_use_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = {"hooks": {}}
            settings_path = os.path.join(tmp, ".claude", "settings.json")
            _write(settings_path, json.dumps(settings))
            with patch.object(whs, "REPO_ROOT", tmp):
                count = whs.count_hooks()
        self.assertEqual(count, 0)


# ---------------------------------------------------------------------------
# count_script_tests
# ---------------------------------------------------------------------------


class CountScriptTestsTests(unittest.TestCase):
    def test_counts_test_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ["test_foo.py", "test_bar.py", "not_test.py"]:
                open(os.path.join(tmp, name), "w").write("x")
            with patch.object(whs, "SCRIPTS_DIR", tmp):
                count = whs.count_script_tests()
        self.assertEqual(count, 2)

    def test_zero_when_no_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "script.py"), "w").write("x")
            with patch.object(whs, "SCRIPTS_DIR", tmp):
                count = whs.count_script_tests()
        self.assertEqual(count, 0)


# ---------------------------------------------------------------------------
# _file_tokens
# ---------------------------------------------------------------------------


class FileTokensTests(unittest.TestCase):
    def test_counts_chars_divided_by_4(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "test.md")
            _write(path, "a" * 400)
            result = whs._file_tokens(path)
        self.assertEqual(result, 100)

    def test_returns_zero_for_missing_file(self):
        result = whs._file_tokens("/nonexistent/file.md")
        self.assertEqual(result, 0)


# ---------------------------------------------------------------------------
# inventory_infrastructure
# ---------------------------------------------------------------------------


class InventoryInfrastructureTests(unittest.TestCase):
    def test_basic_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Create minimal directory structure
            scripts_dir = os.path.join(tmp, ".claude", "scripts")
            skills_dir = os.path.join(tmp, ".claude", "skills")
            hooks_dir = os.path.join(tmp, ".claude", "hooks")
            rules_dir = os.path.join(tmp, ".claude", "rules")
            os.makedirs(scripts_dir)
            os.makedirs(skills_dir)
            os.makedirs(hooks_dir)
            os.makedirs(rules_dir)

            _write(os.path.join(tmp, "CLAUDE.md"), "# CLAUDE\n")
            _write(os.path.join(scripts_dir, "script.py"), "# script\n")
            _write(os.path.join(scripts_dir, "test_script.py"), "# test\n")
            _write(os.path.join(hooks_dir, "hook.sh"), "#!/bin/sh\n")
            _write(os.path.join(rules_dir, "rule.md"), "# Rule\n")

            # Skill with SKILL.md and references
            skill_dir = os.path.join(skills_dir, "my-skill")
            refs_dir = os.path.join(skill_dir, "references")
            os.makedirs(refs_dir)
            _write(os.path.join(skill_dir, "SKILL.md"), "# Skill\n")
            _write(os.path.join(refs_dir, "ref.md"), "# Ref\n")

            with (
                patch.object(whs, "REPO_ROOT", tmp),
                patch.object(whs, "SCRIPTS_DIR", scripts_dir),
                patch.object(whs, "SKILLS_DIR", skills_dir),
                patch.object(whs, "HOOKS_DIR", hooks_dir),
                patch.object(whs, "RULES_DIR", rules_dir),
            ):
                inv = whs.inventory_infrastructure()

        self.assertIn("scripts", inv)
        self.assertIn("skills", inv)
        self.assertIn("hooks", inv)
        self.assertIn("rules", inv)
        self.assertGreater(inv["claudemd_tokens"], 0)

    def test_script_without_test_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts_dir = os.path.join(tmp, ".claude", "scripts")
            os.makedirs(scripts_dir)
            _write(os.path.join(tmp, "CLAUDE.md"), "# CLAUDE\n")
            _write(os.path.join(scripts_dir, "orphan_script.py"), "# script\n")

            with (
                patch.object(whs, "REPO_ROOT", tmp),
                patch.object(whs, "SCRIPTS_DIR", scripts_dir),
                patch.object(whs, "SKILLS_DIR", os.path.join(tmp, "nonexistent")),
                patch.object(whs, "HOOKS_DIR", os.path.join(tmp, "nonexistent2")),
                patch.object(whs, "RULES_DIR", os.path.join(tmp, "nonexistent3")),
            ):
                inv = whs.inventory_infrastructure()

        scripts_without_tests = inv["scripts_without_tests"]
        self.assertIn("orphan_script.py", scripts_without_tests)

    def test_skill_with_references_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts_dir = os.path.join(tmp, ".claude", "scripts")
            skills_dir = os.path.join(tmp, ".claude", "skills")
            os.makedirs(scripts_dir)

            skill_dir = os.path.join(skills_dir, "test-skill")
            refs_dir = os.path.join(skill_dir, "references")
            os.makedirs(refs_dir)
            _write(os.path.join(skill_dir, "SKILL.md"), "# Skill\n")
            _write(os.path.join(refs_dir, "ref1.md"), "# R1\n")
            _write(os.path.join(refs_dir, "ref2.md"), "# R2\n")
            _write(os.path.join(tmp, "CLAUDE.md"), "# C\n")

            with (
                patch.object(whs, "REPO_ROOT", tmp),
                patch.object(whs, "SCRIPTS_DIR", scripts_dir),
                patch.object(whs, "SKILLS_DIR", skills_dir),
                patch.object(whs, "HOOKS_DIR", os.path.join(tmp, "nx")),
                patch.object(whs, "RULES_DIR", os.path.join(tmp, "nx2")),
            ):
                inv = whs.inventory_infrastructure()

        skills = inv["skills"]
        self.assertEqual(len(skills), 1)
        self.assertEqual(skills[0]["name"], "test-skill")
        self.assertEqual(skills[0]["reference_files"], 2)


# ---------------------------------------------------------------------------
# parse_daily_log
# ---------------------------------------------------------------------------


class ParseDailyLogTests(unittest.TestCase):
    def test_no_log_returns_zeros(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "daily-log.md")
            with patch.object(whs, "DAILY_LOG", log_path):
                result = whs.parse_daily_log()
        self.assertEqual(result["daily_runs_total"], 0)
        self.assertEqual(result["daily_runs_zero_output"], 0)

    def test_parses_run_entries(self):
        log = (
            "# Daily Log\n\n"
            "## 2026-01-01\n\n"
            "- 3 sources processed\n"
            "- 2 files auto-fixed\n"
            "- 1 link added\n\n"
            "## 2026-01-02\n\n"
            "- no work found\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "daily-log.md")
            _write(log_path, log)
            with patch.object(whs, "DAILY_LOG", log_path):
                result = whs.parse_daily_log()
        self.assertEqual(result["daily_runs_total"], 2)
        self.assertEqual(result["daily_ingest_total"], 3)
        self.assertEqual(result["daily_lint_fixes_total"], 2)
        self.assertEqual(result["daily_crosslinks_total"], 1)
        self.assertEqual(result["daily_runs_zero_output"], 1)

    def test_last_entry_counted_if_no_output(self):
        log = "## 2026-01-01\n\nNo work done here.\n"
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "daily-log.md")
            _write(log_path, log)
            with patch.object(whs, "DAILY_LOG", log_path):
                result = whs.parse_daily_log()
        self.assertEqual(result["daily_runs_zero_output"], 1)

    def test_multiple_sources_lines(self):
        log = (
            "## 2026-01-01\n\n"
            "- 5 sources processed\n"
            "## 2026-01-02\n\n"
            "- 3 sources processed\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "daily-log.md")
            _write(log_path, log)
            with patch.object(whs, "DAILY_LOG", log_path):
                result = whs.parse_daily_log()
        self.assertEqual(result["daily_ingest_total"], 8)


# ---------------------------------------------------------------------------
# run_lint (mocked subprocess)
# ---------------------------------------------------------------------------


class RunLintTests(unittest.TestCase):
    def test_parses_lint_summary(self):
        mock_result = MagicMock()
        mock_result.stdout = "  wiki/foo.md  broken-wikilink  detail  ·fix: x\n"
        mock_result.stderr = "3 errors · 2 warnings · 5 quality"
        with patch("subprocess.run", return_value=mock_result):
            result = whs.run_lint()
        self.assertEqual(result["errors"], 3)
        self.assertEqual(result["warnings"], 2)
        self.assertEqual(result["quality"], 5)

    def test_empty_output_returns_zeros(self):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = whs.run_lint()
        self.assertEqual(result["errors"], 0)

    def test_timeout_returns_empty(self):
        import subprocess

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
            result = whs.run_lint()
        self.assertEqual(result["errors"], 0)

    def test_categories_parsed(self):
        mock_result = MagicMock()
        mock_result.stdout = (
            "  wiki/foo.md  broken-wikilink  detail\n"
            "  wiki/bar.md  orphan  detail\n"
            "  wiki/baz.md  broken-wikilink  detail\n"
        )
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = whs.run_lint()
        self.assertEqual(result["by_category"].get("broken-wikilink", 0), 2)
        self.assertEqual(result["by_category"].get("orphan", 0), 1)


# ---------------------------------------------------------------------------
# count_pending_ingest (mocked subprocess)
# ---------------------------------------------------------------------------


class CountPendingIngestTests(unittest.TestCase):
    def test_parses_count_from_stdout(self):
        mock_result = MagicMock()
        mock_result.stdout = "7\n"
        with patch("subprocess.run", return_value=mock_result):
            count = whs.count_pending_ingest()
        self.assertEqual(count, 7)

    def test_returns_minus_one_on_timeout(self):
        import subprocess

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
            count = whs.count_pending_ingest()
        self.assertEqual(count, -1)

    def test_handles_non_integer_output(self):
        mock_result = MagicMock()
        mock_result.stdout = "not a number\n"
        with patch("subprocess.run", return_value=mock_result):
            count = whs.count_pending_ingest()
        self.assertEqual(count, -1)


# ---------------------------------------------------------------------------
# take_snapshot (mocked sub-calls)
# ---------------------------------------------------------------------------


class TakeSnapshotTests(unittest.TestCase):
    def test_snapshot_has_required_keys(self):
        with (
            patch.object(whs, "count_wiki_files", return_value=(10, 40000, 2)),
            patch.object(
                whs,
                "run_lint",
                return_value={
                    "errors": 1,
                    "warnings": 2,
                    "quality": 3,
                    "by_category": {},
                },
            ),
            patch.object(whs, "count_pending_ingest", return_value=5),
            patch.object(whs, "count_hooks", return_value=3),
            patch.object(whs, "count_script_tests", return_value=8),
            patch.object(
                whs,
                "inventory_infrastructure",
                return_value={
                    "scripts": [],
                    "scripts_without_tests": [],
                    "skills": [],
                    "hooks": [],
                    "rules": [],
                    "claudemd_tokens": 100,
                    "skill_tokens": 200,
                    "infra_tokens": 300,
                },
            ),
            patch.object(
                whs,
                "parse_daily_log",
                return_value={
                    "daily_runs_total": 5,
                    "daily_runs_zero_output": 1,
                    "daily_ingest_total": 10,
                    "daily_lint_fixes_total": 3,
                    "daily_crosslinks_total": 2,
                },
            ),
        ):
            snapshot = whs.take_snapshot("test")

        required_keys = [
            "timestamp",
            "file_count",
            "total_tokens",
            "mean_file_tokens",
            "lint_errors",
            "lint_warnings",
            "lint_quality",
            "lint_total",
            "orphan_count",
            "deadend_count",
            "stub_summaries",
            "pending_ingest",
            "hook_count",
            "script_test_count",
        ]
        for key in required_keys:
            self.assertIn(key, snapshot, f"Missing key: {key}")

    def test_snapshot_calculates_mean(self):
        with (
            patch.object(whs, "count_wiki_files", return_value=(10, 40000, 2)),
            patch.object(
                whs,
                "run_lint",
                return_value={
                    "errors": 0,
                    "warnings": 0,
                    "quality": 0,
                    "by_category": {},
                },
            ),
            patch.object(whs, "count_pending_ingest", return_value=0),
            patch.object(whs, "count_hooks", return_value=0),
            patch.object(whs, "count_script_tests", return_value=0),
            patch.object(
                whs,
                "inventory_infrastructure",
                return_value={
                    "scripts": [],
                    "scripts_without_tests": [],
                    "skills": [],
                    "hooks": [],
                    "rules": [],
                    "claudemd_tokens": 0,
                    "skill_tokens": 0,
                    "infra_tokens": 0,
                },
            ),
            patch.object(
                whs,
                "parse_daily_log",
                return_value={
                    "daily_runs_total": 0,
                    "daily_runs_zero_output": 0,
                    "daily_ingest_total": 0,
                    "daily_lint_fixes_total": 0,
                    "daily_crosslinks_total": 0,
                },
            ),
        ):
            snapshot = whs.take_snapshot()

        # 40000 chars / 4 = 10000 tokens, / 10 files = 1000 mean
        self.assertEqual(snapshot["total_tokens"], 10000)
        self.assertEqual(snapshot["mean_file_tokens"], 1000)


if __name__ == "__main__":
    unittest.main()
