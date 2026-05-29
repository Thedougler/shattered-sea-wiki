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


class FinalizedSessionsTests(unittest.TestCase):
    def test_pairs_finalized_transcripts_with_live_audio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, "sessions")
            live = os.path.join(sessions, ".live")
            os.makedirs(os.path.join(live, "session-03", "audio"))
            os.makedirs(os.path.join(live, "session-04", "audio"))
            open(os.path.join(sessions, "session-03-transcript.md"), "w").close()
            open(os.path.join(sessions, "session-04-transcript.md"), "w").close()
            pairs = session_paths.finalized_sessions(sessions)
            self.assertEqual(
                [(p[0], os.path.basename(os.path.dirname(p[2]))) for p in pairs],
                [(3, "session-03"), (4, "session-04")],
            )
            self.assertTrue(pairs[0][1].endswith("session-03-transcript.md"))

    def test_skips_finalized_without_audio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, "sessions")
            os.makedirs(sessions)
            open(os.path.join(sessions, "session-07-transcript.md"), "w").close()
            self.assertEqual(session_paths.finalized_sessions(sessions), [])

    def test_empty_when_no_sessions_dir(self) -> None:
        self.assertEqual(session_paths.finalized_sessions(os.path.join("no", "dir")), [])


class SessionPathsForTests(unittest.TestCase):
    def test_composes_subpaths(self) -> None:
        sp = session_paths.session_paths_for("/live", 4)
        self.assertEqual(sp.session_number, 4)
        self.assertEqual(sp.root, "/live/session-04")
        self.assertEqual(sp.audio_dir, "/live/session-04/audio")
        self.assertTrue(sp.transcript_md.endswith("session-04/live_transcript.md"))


if __name__ == "__main__":
    unittest.main()
