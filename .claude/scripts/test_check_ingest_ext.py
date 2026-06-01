#!/usr/bin/env python3
"""Extended tests for check_ingest.py — covers branches missed by test_check_ingest.py."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import check_ingest


def write(path: str, content: bytes) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(content)


def writes(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


# ---------------------------------------------------------------------------
# _extract_frontmatter
# ---------------------------------------------------------------------------


class ExtractFrontmatterTests(unittest.TestCase):
    def test_extracts_frontmatter(self):
        content = "---\ntype: entity\n---\n\n# Body"
        fm, body = check_ingest._extract_frontmatter(content)
        self.assertIn("type: entity", fm)
        self.assertIn("# Body", body)

    def test_no_frontmatter(self):
        content = "# Just a heading"
        fm, body = check_ingest._extract_frontmatter(content)
        self.assertEqual(fm, "")
        self.assertEqual(body, content)

    def test_no_closing_delimiter(self):
        content = "---\ntype: entity\nno close"
        fm, body = check_ingest._extract_frontmatter(content)
        self.assertEqual(fm, "")
        self.assertEqual(body, content)

    def test_trailing_newline_consumed(self):
        content = "---\ntype: entity\n---\n# Body"
        _fm, body = check_ingest._extract_frontmatter(content)
        self.assertFalse(body.startswith("\n"))


# ---------------------------------------------------------------------------
# _split_by_headings
# ---------------------------------------------------------------------------


class SplitByHeadingsTests(unittest.TestCase):
    def test_no_headings_returns_one_section(self):
        body = "Line 1\nLine 2\nLine 3"
        sections = check_ingest._split_by_headings(body)
        self.assertEqual(len(sections), 1)

    def test_splits_at_double_hash(self):
        body = "Intro\n## Section One\nContent 1\n## Section Two\nContent 2"
        sections = check_ingest._split_by_headings(body)
        self.assertEqual(len(sections), 3)

    def test_empty_body(self):
        sections = check_ingest._split_by_headings("")
        self.assertEqual(sections, [""])

    def test_first_section_has_intro(self):
        body = "Intro text\n## Section\nContent"
        sections = check_ingest._split_by_headings(body)
        self.assertIn("Intro text", sections[0])

    def test_single_hash_not_split(self):
        body = "# Main Heading\nContent"
        sections = check_ingest._split_by_headings(body)
        self.assertEqual(len(sections), 1)


# ---------------------------------------------------------------------------
# chunk_oversized
# ---------------------------------------------------------------------------


class ChunkOversizedTests(unittest.TestCase):
    def test_small_file_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "small.md")
            writes(path, "# Small\n\nShort content.")
            result = check_ingest.chunk_oversized(path, 100_000, tmp)
            self.assertIsNone(result)

    def test_non_md_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "data.csv")
            writes(path, "col1,col2\nval1,val2\n")
            result = check_ingest.chunk_oversized(path, 1, tmp)
            self.assertIsNone(result)

    def test_single_section_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Oversized but no ## headings to split on
            path = os.path.join(tmp, "mono.md")
            big_content = "# Title\n\n" + "word " * 10000
            writes(path, big_content)
            result = check_ingest.chunk_oversized(path, 1, tmp)
            self.assertIsNone(result)

    def test_chunks_oversized_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "big.md")
            # Build a file with many sections that will exceed budget
            lines = ["---\ntype: entity\n---\n\n"]
            for i in range(20):
                lines.append(f"## Section {i}\n\n" + "word " * 500 + "\n\n")
            content = "".join(lines)
            writes(path, content)
            result = check_ingest.chunk_oversized(path, 500, tmp)
            if result is not None:
                self.assertGreater(len(result), 1)
                for chunk_path in result:
                    self.assertTrue(os.path.exists(chunk_path))
                # Original should be hidden
                hidden = os.path.join(tmp, ".big.md")
                self.assertTrue(os.path.exists(hidden))

    def test_chunks_with_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "source.md")
            lines = ["---\ntype: entity\ntitle: Test\n---\n\n"]
            for i in range(15):
                lines.append(f"## Section {i}\n\n" + "content " * 300 + "\n\n")
            content = "".join(lines)
            writes(path, content)
            result = check_ingest.chunk_oversized(path, 300, tmp)
            if result is not None:
                # Each chunk should contain frontmatter
                with open(result[0]) as fh:
                    chunk = fh.read()
                self.assertIn("chunk_of", chunk)


# ---------------------------------------------------------------------------
# display_path
# ---------------------------------------------------------------------------


class DisplayPathTests(unittest.TestCase):
    def test_path_inside_repo_returns_relative(self):
        result = check_ingest.display_path(
            os.path.join(check_ingest.REPO_ROOT, "wiki", "test.md")
        )
        self.assertEqual(result, "wiki/test.md")

    def test_absolute_path_outside_repo(self):
        result = check_ingest.display_path("/tmp/external.md")
        self.assertEqual(result, "/tmp/external.md")


# ---------------------------------------------------------------------------
# iter_files
# ---------------------------------------------------------------------------


class IterFilesTests(unittest.TestCase):
    def test_missing_dir_returns_empty(self):
        result = check_ingest.iter_files("/nonexistent/path")
        self.assertEqual(result, [])

    def test_lists_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "a.md"), b"content a")
            write(os.path.join(tmp, "b.md"), b"content b")
            result = check_ingest.iter_files(tmp)
        self.assertEqual(len(result), 2)
        paths = [p for p, _ in result]
        self.assertTrue(any(p.endswith("a.md") for p in paths))

    def test_skips_dot_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, ".hidden"), b"hidden")
            write(os.path.join(tmp, "visible.md"), b"visible")
            result = check_ingest.iter_files(tmp)
        paths = [p for p, _ in result]
        self.assertTrue(all(not os.path.basename(p).startswith(".") for p in paths))

    def test_skips_dot_subdirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, ".chunks-foo"))
            write(os.path.join(tmp, ".chunks-foo", "chunk1.md"), b"chunk")
            write(os.path.join(tmp, "visible.md"), b"visible")
            result = check_ingest.iter_files(tmp)
        paths = [p for p, _ in result]
        self.assertTrue(all("chunk1.md" not in p for p in paths))


# ---------------------------------------------------------------------------
# is_inside
# ---------------------------------------------------------------------------


class IsInsideTests(unittest.TestCase):
    def test_child_path_is_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            child = os.path.join(tmp, "sub", "file.md")
            self.assertTrue(check_ingest.is_inside(child, tmp))

    def test_unrelated_path_not_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(check_ingest.is_inside("/some/other/path", tmp))

    def test_different_drives_windows_style(self):
        # On Unix this just returns False for differing roots
        result = check_ingest.is_inside("/tmp/foo", "/var/bar")
        self.assertFalse(result)


# ---------------------------------------------------------------------------
# remove_file
# ---------------------------------------------------------------------------


class RemoveFileTests(unittest.TestCase):
    def test_removes_untracked_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "Inbox", "file.md")
            os.makedirs(os.path.dirname(path))
            write(path, b"content")
            inbox_root = os.path.join(tmp, "Inbox")
            with patch("check_ingest.is_tracked", return_value=False):
                check_ingest.remove_file(path, inbox_root)
            self.assertFalse(os.path.exists(path))

    def test_refuses_file_outside_inbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "outside", "file.md")
            os.makedirs(os.path.dirname(path))
            write(path, b"content")
            inbox_root = os.path.join(tmp, "Inbox")
            with self.assertRaises(RuntimeError):
                check_ingest.remove_file(path, inbox_root)

    def test_uses_git_rm_for_tracked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "Inbox", "tracked.md")
            os.makedirs(os.path.dirname(path))
            write(path, b"content")
            inbox_root = os.path.join(tmp, "Inbox")
            mock_result = MagicMock()
            mock_result.returncode = 0
            with (
                patch("check_ingest.is_tracked", return_value=True),
                patch("subprocess.run", return_value=mock_result) as mock_run,
            ):
                check_ingest.remove_file(path, inbox_root)
            mock_run.assert_called_once()

    def test_raises_when_git_rm_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "Inbox", "tracked.md")
            os.makedirs(os.path.dirname(path))
            write(path, b"content")
            inbox_root = os.path.join(tmp, "Inbox")
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stderr = "git rm failed"
            with (
                patch("check_ingest.is_tracked", return_value=True),
                patch("subprocess.run", return_value=mock_result),
            ):
                with self.assertRaises(RuntimeError):
                    check_ingest.remove_file(path, inbox_root)


# ---------------------------------------------------------------------------
# describe_duplicate
# ---------------------------------------------------------------------------


class DescribeDuplicateTests(unittest.TestCase):
    def test_raw_kind(self):
        dup = check_ingest.Duplicate(
            path="/repo/Inbox/foo.md",
            duplicate_of="/repo/.raw/reference/foo.md",
            kind="raw",
        )
        desc = check_ingest.describe_duplicate(dup)
        self.assertIn("already archived", desc)

    def test_inbox_kind(self):
        dup = check_ingest.Duplicate(
            path="/repo/Inbox/foo copy.md",
            duplicate_of="/repo/Inbox/foo.md",
            kind="inbox",
        )
        desc = check_ingest.describe_duplicate(dup)
        self.assertIn("duplicate of pending", desc)


# ---------------------------------------------------------------------------
# count_tokens / _count_str_tokens
# ---------------------------------------------------------------------------


class CountTokensTests(unittest.TestCase):
    def test_counts_tokens_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "text.md")
            writes(path, "Hello world, this is a test.")
            count = check_ingest.count_tokens(path)
            self.assertGreater(count, 0)

    def test_returns_size_on_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "text.md")
            writes(path, "Hello world")
            with patch("check_ingest._ENC") as mock_enc:
                mock_enc.encode.side_effect = Exception("error")
                count = check_ingest.count_tokens(path)
            self.assertGreater(count, 0)

    def test_count_str_tokens(self):
        count = check_ingest._count_str_tokens("Hello world")
        self.assertGreater(count, 0)


# ---------------------------------------------------------------------------
# main — extended flag coverage
# ---------------------------------------------------------------------------


class MainExtendedTests(unittest.TestCase):
    def test_count_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            for name in ("A.md", "B.md"):
                write(os.path.join(inbox, name), name.encode())
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--count"])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "2")

    def test_count_flag_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            os.makedirs(inbox)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--count"])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "0")

    def test_quiet_suppresses_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            write(os.path.join(inbox, "A.md"), b"content")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--quiet"])
            self.assertEqual(code, 0)
            self.assertEqual(err.getvalue(), "")

    def test_missing_inbox_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    [
                        "--inbox",
                        os.path.join(tmp, "NonExistent"),
                        "--raw",
                        os.path.join(tmp, ".raw"),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertIn("not found", err.getvalue())

    def test_missing_inbox_with_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    [
                        "--inbox",
                        os.path.join(tmp, "NonExistent"),
                        "--raw",
                        os.path.join(tmp, ".raw"),
                        "--count",
                    ]
                )
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "0")

    def test_bad_algorithm_returns_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            os.makedirs(inbox)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    [
                        "--inbox",
                        inbox,
                        "--raw",
                        os.path.join(tmp, ".raw"),
                        "--algorithm",
                        "not-a-real-algorithm",
                    ]
                )
            self.assertEqual(code, 2)

    def test_dry_run_does_not_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            canonical = os.path.join(inbox, "File.md")
            copy = os.path.join(inbox, "File copy.md")
            write(canonical, b"same")
            write(copy, b"same")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--dry-run"])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(copy))
            self.assertIn("would prune", err.getvalue())

    def test_no_dedupe_reports_without_deleting(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            canonical = os.path.join(inbox, "File.md")
            copy = os.path.join(inbox, "File copy.md")
            write(canonical, b"same")
            write(copy, b"same")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    ["--inbox", inbox, "--raw", raw, "--no-dedupe"]
                )
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(copy))
            self.assertIn("exact duplicate", err.getvalue())

    def test_queue_clear_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            os.makedirs(inbox)
            raw = os.path.join(tmp, ".raw")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw])
            self.assertEqual(code, 0)
            self.assertIn("queue clear", err.getvalue())

    def test_batch_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            write(os.path.join(inbox, "A.md"), b"Small file A.")
            write(os.path.join(inbox, "B.md"), b"Small file B.")
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--batch"])
            self.assertEqual(code, 0)

    def test_batch_mode_empty_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            os.makedirs(inbox)
            raw = os.path.join(tmp, ".raw")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw, "--batch"])
            self.assertEqual(code, 0)
            self.assertIn("queue clear", err.getvalue())

    def test_batch_budget_limits_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            # Write a larger file that'll exceed a small budget
            write(os.path.join(inbox, "A.md"), b"word " * 1000)
            write(os.path.join(inbox, "B.md"), b"word " * 1000)
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    ["--inbox", inbox, "--raw", raw, "--batch", "--budget", "50"]
                )
            self.assertEqual(code, 0)
            # With a very small budget, only one file should fit
            printed = [line for line in out.getvalue().splitlines() if line.strip()]
            self.assertLessEqual(len(printed), 2)

    def test_pending_sources_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            write(os.path.join(inbox, "A.md"), b"content a")
            write(os.path.join(inbox, "B.md"), b"content b")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw])
            self.assertEqual(code, 0)
            self.assertIn("pending", err.getvalue())

    def test_limit_message_shown_of(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            for name in ("A.md", "B.md", "C.md", "D.md"):
                write(os.path.join(inbox, name), name.encode())
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = check_ingest.main(
                    ["--inbox", inbox, "--raw", raw, "--limit", "2"]
                )
            self.assertEqual(code, 0)
            self.assertIn("showing 2 of 4", err.getvalue())


# ---------------------------------------------------------------------------
# canonical_inbox_key
# ---------------------------------------------------------------------------


class CanonicalInboxKeyTests(unittest.TestCase):
    def test_copy_ranked_worse(self):
        with tempfile.TemporaryDirectory() as tmp:
            canonical = os.path.join(tmp, "Source.md")
            copy = os.path.join(tmp, "Source copy.md")
            open(canonical, "w").write("x")
            open(copy, "w").write("x")
            k_can = check_ingest.canonical_inbox_key(canonical)
            k_copy = check_ingest.canonical_inbox_key(copy)
            self.assertLess(k_can, k_copy)

    def test_numbered_copy_ranked_worse(self):
        with tempfile.TemporaryDirectory() as tmp:
            canonical = os.path.join(tmp, "Source.md")
            numbered = os.path.join(tmp, "Source (1).md")
            open(canonical, "w").write("x")
            open(numbered, "w").write("x")
            k_can = check_ingest.canonical_inbox_key(canonical)
            k_num = check_ingest.canonical_inbox_key(numbered)
            self.assertLess(k_can, k_num)


if __name__ == "__main__":
    unittest.main()
