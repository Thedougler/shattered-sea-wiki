#!/usr/bin/env python3
"""Tests for transcript_writer: durable incremental markdown append."""

from __future__ import annotations

import os
import tempfile
import unittest

from transcript_writer import TranscriptWriter


class TranscriptWriterTests(unittest.TestCase):
    def test_write_header_then_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "t.md")
            w = TranscriptWriter(path)
            w.write_header(4, "2026-05-29T18:00:00Z")
            with open(path) as fh:
                self.assertIn("Session 04", fh.read())

    def test_append_accumulates_blocks_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "t.md")
            w = TranscriptWriter(path)
            w.append_line("**A** [00:01]: one")
            w.append_line("**B** [00:02]: two")
            with open(path) as fh:
                body = fh.read()
            self.assertEqual(body, "**A** [00:01]: one\n**B** [00:02]: two\n")

    def test_append_is_durable_before_close(self) -> None:
        # A reader opening the file mid-session must see flushed content.
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "t.md")
            w = TranscriptWriter(path)
            w.append_line("**A** [00:01]: mid-session")
            with open(path) as fh:
                self.assertIn("mid-session", fh.read())

    def test_creates_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "nested", "deep", "t.md")
            w = TranscriptWriter(path)
            w.append_line("hello")
            self.assertTrue(os.path.exists(path))

    def test_append_block_normalizes_trailing_newline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "t.md")
            w = TranscriptWriter(path)
            w.append_line("line-with-newline\n")
            with open(path) as fh:
                self.assertEqual(fh.read(), "line-with-newline\n")


if __name__ == "__main__":
    unittest.main()
