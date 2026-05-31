#!/usr/bin/env python3
"""Tests for wiki_health_snapshot.py — validates the measurement infrastructure."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", ".."))
SNAPSHOT_SCRIPT = os.path.join(SCRIPTS_DIR, "wiki_health_snapshot.py")


class TestSnapshotOutput(unittest.TestCase):
    """Verify the snapshot script produces valid, complete output."""

    def test_produces_valid_json(self):
        proc = subprocess.run(
            [sys.executable, SNAPSHOT_SCRIPT],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=REPO_ROOT,
        )
        self.assertEqual(proc.returncode, 0, f"Script failed: {proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIsInstance(data, dict)

    def test_required_keys_present(self):
        proc = subprocess.run(
            [sys.executable, SNAPSHOT_SCRIPT],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=REPO_ROOT,
        )
        data = json.loads(proc.stdout)
        required = [
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
        for key in required:
            self.assertIn(key, data, f"Missing required key: {key}")

    def test_file_count_is_positive(self):
        proc = subprocess.run(
            [sys.executable, SNAPSHOT_SCRIPT],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=REPO_ROOT,
        )
        data = json.loads(proc.stdout)
        self.assertGreater(data["file_count"], 0)

    def test_lint_total_is_sum(self):
        proc = subprocess.run(
            [sys.executable, SNAPSHOT_SCRIPT],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=REPO_ROOT,
        )
        data = json.loads(proc.stdout)
        expected = data["lint_errors"] + data["lint_warnings"] + data["lint_quality"]
        self.assertEqual(data["lint_total"], expected)


class TestSaveAndHistory(unittest.TestCase):
    """Verify snapshot persistence and retrieval."""

    def test_save_creates_jsonl(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "test-snapshots.jsonl")
            env = os.environ.copy()
            # We can't easily override the log path, so test via the module
            import importlib.util

            spec = importlib.util.spec_from_file_location("whs", SNAPSHOT_SCRIPT)
            mod = importlib.util.module_from_spec(spec)
            old_log = None
            try:
                spec.loader.exec_module(mod)
                old_log = mod.SNAPSHOT_LOG
                mod.SNAPSHOT_LOG = log_path

                snapshot = {
                    "timestamp": "2026-01-01T00:00:00",
                    "lint_total": 42,
                    "file_count": 100,
                }
                mod.save_snapshot(snapshot)
                mod.save_snapshot(snapshot)

                loaded = mod.load_snapshots()
                self.assertEqual(len(loaded), 2)
                self.assertEqual(loaded[0]["lint_total"], 42)
            finally:
                if old_log:
                    mod.SNAPSHOT_LOG = old_log


class TestDiff(unittest.TestCase):
    """Verify snapshot comparison logic."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("whs", SNAPSHOT_SCRIPT)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_diff_detects_improvement(self):
        a = {"lint_total": 100, "lint_errors": 5, "orphan_count": 20, "file_count": 500}
        b = {"lint_total": 80, "lint_errors": 3, "orphan_count": 18, "file_count": 500}
        deltas = self.mod.diff_snapshots(a, b)
        self.assertEqual(deltas["lint_total"]["delta"], -20)
        self.assertEqual(deltas["lint_errors"]["delta"], -2)
        self.assertNotIn("file_count", deltas)  # unchanged

    def test_diff_empty_when_identical(self):
        a = {"lint_total": 50, "file_count": 500}
        deltas = self.mod.diff_snapshots(a, a)
        self.assertEqual(len(deltas), 0)


if __name__ == "__main__":
    unittest.main()
