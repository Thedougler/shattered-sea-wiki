#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest

import check_ingest


def write(path: str, content: bytes) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(content)


class CheckIngestTests(unittest.TestCase):
    def test_classifies_raw_duplicates_as_safe_to_prune(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            inbox_source = os.path.join(inbox, "Source.md")
            raw_source = os.path.join(raw, "reference", "Source.md")
            write(inbox_source, b"same source")
            write(raw_source, b"same source")

            result = check_ingest.classify_inbox(inbox, raw, "sha256")

            self.assertEqual(result.pending, [])
            self.assertEqual([d.path for d in result.raw_duplicates], [inbox_source])
            self.assertEqual(result.raw_duplicates[0].duplicate_of, raw_source)

    def test_keeps_one_canonical_inbox_copy_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            canonical = os.path.join(inbox, "Calveno.md")
            copy = os.path.join(inbox, "Calveno copy.md")
            numbered_copy = os.path.join(inbox, "Calveno (1).md")
            write(canonical, b"same source")
            write(copy, b"same source")
            write(numbered_copy, b"same source")

            result = check_ingest.classify_inbox(inbox, raw, "sha256")

            self.assertEqual(result.pending, [canonical])
            self.assertEqual(
                sorted(d.path for d in result.inbox_duplicates),
                sorted([copy, numbered_copy]),
            )
            self.assertTrue(
                all(d.duplicate_of == canonical for d in result.inbox_duplicates)
            )

    def test_main_prunes_exact_duplicates_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            canonical = os.path.join(inbox, "Calveno.md")
            copy = os.path.join(inbox, "Calveno copy.md")
            archived = os.path.join(inbox, "Already Archived.md")
            raw_archived = os.path.join(raw, "reference", "Already Archived.md")
            write(canonical, b"pending source")
            write(copy, b"pending source")
            write(archived, b"archived source")
            write(raw_archived, b"archived source")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = check_ingest.main(["--inbox", inbox, "--raw", raw])

            self.assertEqual(code, 0)
            self.assertEqual(stdout.getvalue().strip(), canonical)
            self.assertTrue(os.path.exists(canonical))
            self.assertFalse(os.path.exists(copy))
            self.assertFalse(os.path.exists(archived))
            self.assertIn("pruned", stderr.getvalue())

    def test_limit_truncates_printed_list_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            for name in ("A.md", "B.md", "C.md"):
                write(os.path.join(inbox, name), name.encode())

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = check_ingest.main(
                    ["--inbox", inbox, "--raw", raw, "--limit", "2"]
                )

            self.assertEqual(code, 0)
            printed = [line for line in stdout.getvalue().splitlines() if line.strip()]
            self.assertEqual(len(printed), 2)
            self.assertTrue(printed[0].endswith("A.md"))
            self.assertTrue(printed[1].endswith("B.md"))
            self.assertIn("showing 2 of 3", stderr.getvalue())

    def test_no_dedupe_reports_without_removing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = os.path.join(tmp, "Inbox")
            raw = os.path.join(tmp, ".raw")
            canonical = os.path.join(inbox, "Calveno.md")
            copy = os.path.join(inbox, "Calveno copy.md")
            write(canonical, b"pending source")
            write(copy, b"pending source")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = check_ingest.main(
                    ["--inbox", inbox, "--raw", raw, "--no-dedupe"]
                )

            self.assertEqual(code, 0)
            self.assertEqual(stdout.getvalue().strip(), canonical)
            self.assertTrue(os.path.exists(copy))
            self.assertIn("exact duplicate", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
