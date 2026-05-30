"""Tests for teleprompter UI rendering helpers (pure functions, no NiceGUI)."""

import unittest

from voice_transcription.app.teleprompter_ui import render_paragraphs, TELEPROMPTER_CSS


class RenderParagraphsTests(unittest.TestCase):
    def test_single_paragraph(self) -> None:
        html = render_paragraphs("hello world")
        self.assertIn('id="word-0"', html)
        self.assertIn('id="word-1"', html)
        self.assertIn("hello", html)
        self.assertIn("world", html)

    def test_multiple_paragraphs(self) -> None:
        html = render_paragraphs("first para\n\nsecond para")
        self.assertIn("<p", html)
        self.assertEqual(html.count("<p"), 2)
        self.assertIn('id="word-0"', html)
        self.assertIn('id="word-3"', html)

    def test_empty_text(self) -> None:
        html = render_paragraphs("")
        self.assertEqual(html.strip(), "")

    def test_word_ids_are_sequential(self) -> None:
        html = render_paragraphs("a b c\n\nd e")
        for i in range(5):
            self.assertIn(f'id="word-{i}"', html)

    def test_word_span_class(self) -> None:
        html = render_paragraphs("hello")
        self.assertIn('class="word-span"', html)


class CSSTests(unittest.TestCase):
    def test_css_has_dark_background(self) -> None:
        self.assertIn("background", TELEPROMPTER_CSS.lower())

    def test_css_has_large_font(self) -> None:
        self.assertIn("font-size", TELEPROMPTER_CSS.lower())

    def test_css_has_read_class(self) -> None:
        self.assertIn(".read", TELEPROMPTER_CSS)


if __name__ == "__main__":
    unittest.main()
