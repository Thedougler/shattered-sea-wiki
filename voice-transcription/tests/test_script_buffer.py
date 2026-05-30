"""Tests for ScriptBuffer — the growing script text manager."""

import unittest

from voice_transcription.core.script_buffer import ScriptBuffer


class ScriptBufferTests(unittest.TestCase):
    def test_initial_text(self) -> None:
        buf = ScriptBuffer("Hello world")
        self.assertEqual(buf.full_text, "Hello world")

    def test_token_count(self) -> None:
        buf = ScriptBuffer("one two three")
        self.assertEqual(buf.token_count, 3)

    def test_extend_appends_text(self) -> None:
        buf = ScriptBuffer("Hello world")
        buf.extend("New paragraph here")
        self.assertIn("New paragraph here", buf.full_text)
        self.assertEqual(buf.token_count, 5)

    def test_extend_adds_paragraph_break(self) -> None:
        buf = ScriptBuffer("First paragraph.")
        buf.extend("Second paragraph.")
        self.assertIn("\n\n", buf.full_text)

    def test_needs_extension_far_from_end(self) -> None:
        text = " ".join(f"word{i}" for i in range(500))
        buf = ScriptBuffer(text)
        self.assertFalse(buf.needs_extension(matched_up_to=10))

    def test_needs_extension_near_end(self) -> None:
        text = " ".join(f"word{i}" for i in range(500))
        buf = ScriptBuffer(text)
        self.assertTrue(buf.needs_extension(matched_up_to=400))

    def test_needs_extension_custom_lookahead(self) -> None:
        text = " ".join(f"word{i}" for i in range(100))
        buf = ScriptBuffer(text)
        self.assertFalse(buf.needs_extension(matched_up_to=50, lookahead=40))
        self.assertTrue(buf.needs_extension(matched_up_to=50, lookahead=60))

    def test_needs_extension_negative_matched_short_script(self) -> None:
        buf = ScriptBuffer("Hello world")
        self.assertTrue(buf.needs_extension(matched_up_to=-1))

    def test_needs_extension_negative_matched_long_script(self) -> None:
        text = " ".join(f"word{i}" for i in range(500))
        buf = ScriptBuffer(text)
        self.assertFalse(buf.needs_extension(matched_up_to=-1))

    def test_empty_seed(self) -> None:
        buf = ScriptBuffer("")
        self.assertEqual(buf.token_count, 0)
        self.assertTrue(buf.needs_extension(matched_up_to=-1))

    def test_multiple_extends(self) -> None:
        buf = ScriptBuffer("Start")
        buf.extend("Middle")
        buf.extend("End")
        self.assertEqual(buf.token_count, 3)
        self.assertIn("Start", buf.full_text)
        self.assertIn("End", buf.full_text)


if __name__ == "__main__":
    unittest.main()
