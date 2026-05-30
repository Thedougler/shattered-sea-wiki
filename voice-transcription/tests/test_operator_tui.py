"""Tests for operator TUI data helpers (pure functions, no Textual runtime)."""

import unittest

from voice_transcription.app.operator_tui import (
    format_status_line,
    format_script_preview,
    format_elapsed,
)


class FormatElapsedTests(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertEqual(format_elapsed(0), "00:00:00")

    def test_minutes_seconds(self) -> None:
        self.assertEqual(format_elapsed(125), "00:02:05")

    def test_hours(self) -> None:
        self.assertEqual(format_elapsed(3661), "01:01:01")


class FormatStatusLineTests(unittest.TestCase):
    def test_recording(self) -> None:
        line = format_status_line(
            status="recording", matched=50, total=200,
            profiles_loaded=3, llm_enabled=True,
        )
        self.assertIn("Recording", line)
        self.assertIn("50/200", line)
        self.assertIn("3", line)

    def test_idle(self) -> None:
        line = format_status_line(
            status="idle", matched=0, total=100,
            profiles_loaded=0, llm_enabled=False,
        )
        self.assertIn("Idle", line)
        self.assertIn("LLM: off", line)

    def test_extending(self) -> None:
        line = format_status_line(
            status="extending", matched=100, total=200,
            profiles_loaded=2, llm_enabled=True,
        )
        self.assertIn("extending", line.lower())


class FormatScriptPreviewTests(unittest.TestCase):
    def test_shows_context_around_position(self) -> None:
        tokens = [f"word{i}" for i in range(100)]
        preview = format_script_preview(tokens, matched_up_to=50, context=3)
        self.assertIn("word50", preview)
        self.assertIn("word48", preview)
        self.assertIn("word53", preview)

    def test_position_at_start(self) -> None:
        tokens = ["hello", "world", "foo", "bar"]
        preview = format_script_preview(tokens, matched_up_to=0, context=2)
        self.assertIn("hello", preview)

    def test_position_negative(self) -> None:
        tokens = ["hello", "world"]
        preview = format_script_preview(tokens, matched_up_to=-1, context=2)
        self.assertIn("hello", preview)

    def test_empty_tokens(self) -> None:
        preview = format_script_preview([], matched_up_to=-1, context=3)
        self.assertEqual(preview, "")

    def test_marks_current_word(self) -> None:
        tokens = ["one", "two", "three"]
        preview = format_script_preview(tokens, matched_up_to=1, context=3)
        self.assertIn("▶", preview)


if __name__ == "__main__":
    unittest.main()
