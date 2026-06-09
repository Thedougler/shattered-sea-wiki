#!/usr/bin/env python3
"""Tests for assemble_transcript.py."""

from __future__ import annotations

import contextlib
import csv
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Import the module — needs RAW_DIR/INBOX_DIR patched or we just import functions.
import assemble_transcript as at

# ---------------------------------------------------------------------------
# Test helpers — build the new per-session packet layout under a tmp root
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def patched_dirs(tmp):
    """Patch RAW_DIR, INBOX_DIR (and REPO_ROOT) onto a tmp root."""
    raw = Path(tmp) / ".raw" / "sessions"
    inbox = Path(tmp) / "Inbox" / "sessions"
    with (
        patch("assemble_transcript.RAW_DIR", raw),
        patch("assemble_transcript.INBOX_DIR", inbox),
        patch("assemble_transcript.REPO_ROOT", Path(tmp)),
    ):
        yield raw, inbox


def _write_part_csv(path: str, rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Start", "End", "Speaker", "Text"])
        writer.writeheader()
        writer.writerows(rows)


def _write_part(tmp, session: str, part: str, rows: list[dict]) -> Path:
    """Write a raw part CSV to .raw/sessions/session-NN/transcripts/raw/."""
    path = (
        Path(tmp)
        / ".raw"
        / "sessions"
        / f"session-{session}"
        / "transcripts"
        / "raw"
        / f"session-{session}-part-{part}.csv"
    )
    _write_part_csv(str(path), rows)
    return path


# ---------------------------------------------------------------------------
# Pure functions
# ---------------------------------------------------------------------------


class ParseTimestampTests(unittest.TestCase):
    def test_mm_ss(self):
        self.assertEqual(at.parse_timestamp("1:30"), 90)

    def test_hh_mm_ss(self):
        self.assertEqual(at.parse_timestamp("1:01:01"), 3661)

    def test_zero(self):
        self.assertEqual(at.parse_timestamp("0:00"), 0)

    def test_padding(self):
        self.assertEqual(at.parse_timestamp("0:05"), 5)

    def test_unknown_format(self):
        self.assertEqual(at.parse_timestamp("bad"), 0)


class FormatTimestampTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(at.format_timestamp(0), "0:00:00")

    def test_one_minute(self):
        self.assertEqual(at.format_timestamp(60), "0:01:00")

    def test_one_hour(self):
        self.assertEqual(at.format_timestamp(3600), "1:00:00")

    def test_mixed(self):
        self.assertEqual(at.format_timestamp(3661), "1:01:01")

    def test_seconds_only(self):
        self.assertEqual(at.format_timestamp(45), "0:00:45")


# ---------------------------------------------------------------------------
# Path helpers — verify the new dash-form layout
# ---------------------------------------------------------------------------


class PathHelperTests(unittest.TestCase):
    def test_raw_parts_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                p = at.get_raw_parts_dir("07")
            self.assertTrue(
                str(p).endswith(".raw/sessions/session-07/transcripts/raw"),
                str(p),
            )

    def test_assembled_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                p = at.get_assembled_path("07")
            self.assertTrue(
                str(p).endswith(
                    ".raw/sessions/session-07/transcripts/assembled/"
                    "session-07-assembled.csv"
                ),
                str(p),
            )

    def test_resolved_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                p = at.get_resolved_path("07")
            self.assertTrue(
                str(p).endswith(
                    ".raw/sessions/session-07/transcripts/corrected/"
                    "session-07-resolved.csv"
                ),
                str(p),
            )

    def test_speaker_map_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                p = at.get_speaker_map_path("07")
            self.assertTrue(
                str(p).endswith(
                    "Inbox/sessions/session-07/processing/speaker-map.md"
                ),
                str(p),
            )


class ParseSpeakerMapTests(unittest.TestCase):
    def _write_map(self, tmp, content):
        p = Path(tmp) / "speaker-map.md"
        p.write_text(content)
        return p

    def test_parses_table(self):
        content = (
            "# Speaker Map\n\n"
            "| Label | Resolved To | Confidence |\n"
            "|---|---|---|\n"
            "| Speaker A | Nick | high |\n"
            "| Speaker B | Jane | medium |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write_map(tmp, content)
            mapping = at.parse_speaker_map(p)
        self.assertEqual(mapping["Speaker A"], "Nick")
        self.assertEqual(mapping["Speaker B"], "Jane")

    def test_skips_unknown_confidence(self):
        content = (
            "# Speaker Map\n\n"
            "| Label | Resolved To | Confidence |\n"
            "|---|---|---|\n"
            "| Speaker X | Unknown | unknown |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write_map(tmp, content)
            mapping = at.parse_speaker_map(p)
        self.assertNotIn("Speaker X", mapping)

    def test_low_confidence_prefixed(self):
        content = (
            "# Speaker Map\n\n"
            "| Label | Resolved To | Confidence |\n"
            "|---|---|---|\n"
            "| Speaker C | Dave | low |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write_map(tmp, content)
            mapping = at.parse_speaker_map(p)
        self.assertEqual(mapping["Speaker C"], "?Dave")

    def test_stops_at_non_table_line(self):
        content = (
            "# Speaker Map\n\n"
            "| Label | Resolved To | Confidence |\n"
            "|---|---|---|\n"
            "| Speaker A | Nick | high |\n"
            "\n"
            "Some prose that shouldn't be parsed as a table row.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write_map(tmp, content)
            mapping = at.parse_speaker_map(p)
        self.assertIn("Speaker A", mapping)

    def test_empty_map(self):
        content = "# Speaker Map\n\nNo table here.\n"
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write_map(tmp, content)
            mapping = at.parse_speaker_map(p)
        self.assertEqual(mapping, {})


# ---------------------------------------------------------------------------
# cmd_assemble
# ---------------------------------------------------------------------------


class CmdAssembleTests(unittest.TestCase):
    def test_assembles_single_part(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "01",
                "00",
                [
                    {"Start": "0:00", "End": "0:05", "Speaker": "Nick", "Text": "Hello"},
                    {"Start": "0:06", "End": "0:10", "Speaker": "Jane", "Text": "World"},
                ],
            )
            with patched_dirs(tmp):
                at.cmd_assemble("01")
                out_path = at.get_assembled_path("01")
            self.assertTrue(out_path.exists())
            with open(out_path, newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)

    def test_assembles_two_parts_continuous_timestamps(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "02",
                "00",
                [{"Start": "0:00", "End": "0:10", "Speaker": "A", "Text": "One"}],
            )
            _write_part(
                tmp,
                "02",
                "01",
                [{"Start": "0:00", "End": "0:05", "Speaker": "B", "Text": "Two"}],
            )
            with patched_dirs(tmp):
                at.cmd_assemble("02")
                out_path = at.get_assembled_path("02")
            with open(out_path, newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)
            # Second part's start should be offset
            start_2 = at.parse_timestamp(rows[1]["Start"])
            self.assertGreater(start_2, 0)

    def test_no_parts_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp), self.assertRaises(SystemExit):
                at.cmd_assemble("99")

    def test_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "03",
                "00",
                [{"Start": "0:00", "End": "0:05", "Speaker": "Nick", "Text": "Test"}],
            )
            with patched_dirs(tmp):
                at.cmd_assemble("03")
                manifest = at.get_assembled_path("03").parent / "parts.txt"
            self.assertTrue(manifest.exists())
            self.assertIn("session-03-part-00.csv", manifest.read_text())

    def test_unresolved_speakers_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "04",
                "00",
                [{"Start": "0:00", "End": "0:05", "Speaker": "Speaker 1", "Text": "Hi"}],
            )
            with patched_dirs(tmp):
                at.cmd_assemble("04")


# ---------------------------------------------------------------------------
# cmd_status
# ---------------------------------------------------------------------------


class CmdStatusTests(unittest.TestCase):
    def test_status_no_parts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("01")
            output = out.getvalue()
            self.assertIn("0", output)
            self.assertIn("not started", output)

    def test_status_with_assembled(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "01",
                "00",
                [{"Start": "0:00", "End": "0:05", "Speaker": "A", "Text": "Text"}],
            )
            with patched_dirs(tmp):
                assembled = at.get_assembled_path("01")
                assembled.parent.mkdir(parents=True, exist_ok=True)
                with open(assembled, "w", newline="") as f:
                    w = csv.DictWriter(
                        f,
                        fieldnames=["ID", "Start", "End", "Speaker", "Text", "Source"],
                    )
                    w.writeheader()
                    w.writerow(
                        {
                            "ID": 1,
                            "Start": "0:00:00",
                            "End": "0:00:05",
                            "Speaker": "A",
                            "Text": "Text",
                            "Source": "part00",
                        }
                    )
                (assembled.parent / "parts.txt").write_text(
                    "session-01-part-00.csv\n"
                )
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("01")
            self.assertIn("assembled.csv", out.getvalue())

    def test_status_shows_pass3_when_extracts_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                processing = at.get_inbox_processing_dir("05")
                processing.mkdir(parents=True, exist_ok=True)
                (processing / "extracts.md").write_text("# Extracts\n")
                (processing / "progress.txt").write_text("chunk 1\nchunk 2\n")
                (processing / "flags.md").write_text("- [ ] unresolved\n- [x] done\n")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("05")
            self.assertIn("Pass 3", out.getvalue())
            self.assertIn("2 chunk", out.getvalue())

    def test_status_pass3_no_output_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                processing = at.get_inbox_processing_dir("06")
                processing.mkdir(parents=True, exist_ok=True)
                (processing / "progress.txt").write_text("chunk 1\n")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("06")
            self.assertIn("progress.txt", out.getvalue())

    def test_status_with_speaker_map_no_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                speaker_map = at.get_speaker_map_path("07")
                speaker_map.parent.mkdir(parents=True, exist_ok=True)
                speaker_map.write_text("# Map\n")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("07")
            self.assertIn("map written", out.getvalue())

    def test_status_stale_assembled(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_part(
                tmp,
                "08",
                "00",
                [{"Start": "0:00", "End": "0:05", "Speaker": "A", "Text": "T"}],
            )
            _write_part(
                tmp,
                "08",
                "01",
                [{"Start": "0:00", "End": "0:05", "Speaker": "B", "Text": "U"}],
            )
            with patched_dirs(tmp):
                assembled = at.get_assembled_path("08")
                assembled.parent.mkdir(parents=True, exist_ok=True)
                with open(assembled, "w", newline="") as f:
                    w = csv.DictWriter(
                        f,
                        fieldnames=["ID", "Start", "End", "Speaker", "Text", "Source"],
                    )
                    w.writeheader()
                # Manifest only knows about part-00 — part-01 is new
                (assembled.parent / "parts.txt").write_text(
                    "session-08-part-00.csv\n"
                )
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("08")
            self.assertIn("STALE", out.getvalue())

    def test_status_pass4_session_note_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki_sessions = Path(tmp) / "wiki" / "sessions"
            wiki_sessions.mkdir(parents=True)
            (wiki_sessions / "session-09.md").write_text("# Session 09\n")
            with patched_dirs(tmp):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("09")
            self.assertIn("session note exists", out.getvalue())

    def test_status_pass4_ready_when_extracts_and_recap(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                processing = at.get_inbox_processing_dir("10")
                processing.mkdir(parents=True, exist_ok=True)
                (processing / "extracts.md").write_text("# E\n")
                (processing / "recap.md").write_text("# R\n")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    at.cmd_status("10")
            self.assertIn("ready", out.getvalue())


# ---------------------------------------------------------------------------
# cmd_resolve
# ---------------------------------------------------------------------------


class CmdResolveTests(unittest.TestCase):
    def _make_assembled(self, session, rows):
        path = at.get_assembled_path(session)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(
                f, fieldnames=["ID", "Start", "End", "Speaker", "Text", "Source"]
            )
            w.writeheader()
            w.writerows(rows)
        return path

    def _make_map(self, session, content):
        p = at.get_speaker_map_path(session)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def test_resolves_speakers(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                self._make_assembled(
                    "01",
                    [
                        {
                            "ID": 1,
                            "Start": "0:00:00",
                            "End": "0:00:05",
                            "Speaker": "Speaker A",
                            "Text": "Hello",
                            "Source": "p0",
                        },
                        {
                            "ID": 2,
                            "Start": "0:00:06",
                            "End": "0:00:10",
                            "Speaker": "Speaker B",
                            "Text": "World",
                            "Source": "p0",
                        },
                    ],
                )
                self._make_map(
                    "01",
                    "| Label | Resolved To | Confidence |\n"
                    "|---|---|---|\n"
                    "| Speaker A | Nick | high |\n",
                )
                at.cmd_resolve("01")
                resolved = at.get_resolved_path("01")
            self.assertTrue(resolved.exists())
            with open(resolved, newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["Speaker"], "Nick")
            self.assertEqual(rows[1]["Speaker"], "Speaker B")

    def test_no_assembled_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp), self.assertRaises(SystemExit):
                at.cmd_resolve("02")

    def test_no_speaker_map_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                self._make_assembled(
                    "03",
                    [
                        {
                            "ID": 1,
                            "Start": "0:00:00",
                            "End": "0:00:05",
                            "Speaker": "A",
                            "Text": "T",
                            "Source": "p",
                        }
                    ],
                )
                with self.assertRaises(SystemExit):
                    at.cmd_resolve("03")

    def test_empty_map_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patched_dirs(tmp):
                self._make_assembled(
                    "04",
                    [
                        {
                            "ID": 1,
                            "Start": "0:00:00",
                            "End": "0:00:05",
                            "Speaker": "A",
                            "Text": "T",
                            "Source": "p",
                        }
                    ],
                )
                self._make_map("04", "# No table\n")
                with self.assertRaises(SystemExit):
                    at.cmd_resolve("04")


if __name__ == "__main__":
    unittest.main()
