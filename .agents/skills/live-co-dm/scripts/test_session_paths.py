#!/usr/bin/env python3
"""Tests for session_paths: pure numbering + path composition for live sessions."""

from __future__ import annotations

import os
import tempfile
import unittest

import session_paths


class ChunkFilenameTests(unittest.TestCase):
    def test_zero_pads_index_and_formats_elapsed(self) -> None:
        self.assertEqual(session_paths.chunk_audio_filename(7, 723_000), "0007_00h12m03s.wav")

    def test_handles_hours(self) -> None:
        self.assertEqual(session_paths.chunk_audio_filename(1, 3_725_000), "0001_01h02m05s.wav")


class NextSessionNumberTests(unittest.TestCase):
    def test_empty_dirs_start_at_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, "sessions")
            live = os.path.join(tmp, "live")
            self.assertEqual(session_paths.next_session_number(sessions, live), 1)

    def test_counts_canonical_session_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, "sessions")
            os.makedirs(sessions)
            for name in ("session-01.md", "session-03.md", "session-03-recap.md"):
                open(os.path.join(sessions, name), "w").close()
            self.assertEqual(session_paths.next_session_number(sessions, tmp), 4)

    def test_takes_max_of_canonical_and_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, "sessions")
            live = os.path.join(tmp, "live")
            os.makedirs(sessions)
            os.makedirs(os.path.join(live, "session-05"))
            open(os.path.join(sessions, "session-02.md"), "w").close()
            self.assertEqual(session_paths.next_session_number(sessions, live), 6)


class SessionPathsForTests(unittest.TestCase):
    def test_composes_subpaths(self) -> None:
        sp = session_paths.session_paths_for("/live", 4)
        self.assertEqual(sp.session_number, 4)
        self.assertEqual(sp.root, "/live/session-04")
        self.assertEqual(sp.audio_dir, "/live/session-04/audio")
        self.assertTrue(sp.transcript_md.endswith("session-04/live_transcript.md"))


if __name__ == "__main__":
    unittest.main()
