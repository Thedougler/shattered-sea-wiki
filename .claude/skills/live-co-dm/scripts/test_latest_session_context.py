#!/usr/bin/env python3
"""Tests for latest_session_context: the co-DM fast context loader.

Finds the newest live transcript + canonical session note + hot.md and prints a
compact bundle so the agent can answer mid-session without the full wiki startup.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest

import latest_session_context as lsc


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


class FindLiveTests(unittest.TestCase):
    def test_returns_highest_numbered_live_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            live = os.path.join(tmp, ".live")
            write(os.path.join(live, "session-02", "live_transcript.md"), "two")
            write(os.path.join(live, "session-05", "live_transcript.md"), "five")
            found = lsc.find_latest_live(live)
            self.assertEqual(found[0], 5)
            self.assertTrue(found[1].endswith("session-05/live_transcript.md"))

    def test_none_when_no_live_dir(self) -> None:
        self.assertIsNone(lsc.find_latest_live(os.path.join("no", "such")))


class FindCanonicalTests(unittest.TestCase):
    def test_finds_session_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "session-03.md"), "x")
            self.assertTrue(lsc.find_canonical(tmp, 3).endswith("session-03.md"))

    def test_none_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(lsc.find_canonical(tmp, 9))


class TailTests(unittest.TestCase):
    def test_returns_last_n_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "t.md")
            write(p, "\n".join(f"line{i}" for i in range(10)))
            tail = lsc.tail_lines(p, 3)
            self.assertEqual(tail.splitlines(), ["line7", "line8", "line9"])

    def test_short_file_returns_all(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "t.md")
            write(p, "only")
            self.assertEqual(lsc.tail_lines(p, 50), "only")


class BundleTests(unittest.TestCase):
    def _wiki(self, tmp: str) -> str:
        wiki = os.path.join(tmp, "wiki")
        write(os.path.join(wiki, "hot.md"), "# hot\nfaction clocks here")
        write(os.path.join(wiki, "sessions", "session-03.md"), "canonical three")
        write(os.path.join(wiki, "sessions", ".live", "session-04", "live_transcript.md"),
              "\n".join(f"**Delmar** [00:0{i}]: line {i}" for i in range(5)))
        return wiki

    def test_bundle_includes_live_tail_and_hot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._wiki(tmp)
            bundle = lsc.build_bundle(wiki, tail=3)
            self.assertIn("LIVE TRANSCRIPT", bundle)
            self.assertIn("line 4", bundle)
            self.assertIn("faction clocks", bundle)
            self.assertIn("SKIP", bundle)  # reminds agent to skip maintenance

    def test_bundle_graceful_without_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = os.path.join(tmp, "wiki")
            write(os.path.join(wiki, "hot.md"), "# hot")
            bundle = lsc.build_bundle(wiki, tail=3)
            self.assertIn("no live transcript", bundle.lower())

    def test_main_prints_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = self._wiki(tmp)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = lsc.main(["--wiki", wiki, "--tail", "2"])
            self.assertEqual(code, 0)
            self.assertIn("LIVE TRANSCRIPT", out.getvalue())


if __name__ == "__main__":
    unittest.main()
