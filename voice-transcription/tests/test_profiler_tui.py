"""Tests for profiler TUI pure helpers."""

import unittest

from voice_transcription.app.profiler_tui import format_profiler_status


class FormatProfilerStatusTests(unittest.TestCase):
    def test_idle(self) -> None:
        line = format_profiler_status(
            name="Grigori", player="Dave", status="idle",
            matched=0, total=100, save_result=None,
        )
        self.assertIn("Grigori", line)
        self.assertIn("Dave", line)
        self.assertIn("Idle", line)

    def test_recording(self) -> None:
        line = format_profiler_status(
            name="Grigori", player="Dave", status="recording",
            matched=30, total=100, save_result=None,
        )
        self.assertIn("Recording", line)
        self.assertIn("30/100", line)

    def test_with_save_result(self) -> None:
        line = format_profiler_status(
            name="Grigori", player="Dave", status="idle",
            matched=100, total=100,
            save_result="Saved profile for Grigori (Dave)",
        )
        self.assertIn("Saved profile", line)

    def test_saving(self) -> None:
        line = format_profiler_status(
            name="Grigori", player="Dave", status="saving",
            matched=100, total=100, save_result=None,
        )
        self.assertIn("Saving", line)


if __name__ == "__main__":
    unittest.main()
