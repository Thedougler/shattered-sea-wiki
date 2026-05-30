"""Tests for ScriptTracker — live grey-out progress tracking."""

from __future__ import annotations

import unittest

from voice_transcription.core.script_tracker import ScriptTracker


class TokenizeTests(unittest.TestCase):
    def test_splits_on_whitespace(self) -> None:
        t = ScriptTracker("hello world")
        self.assertEqual(t.raw_tokens, ["hello", "world"])

    def test_normalizes_lowercase_and_strips_punctuation(self) -> None:
        t = ScriptTracker('Hello, World! "Quoted"')
        self.assertEqual(t.norm_tokens, ["hello", "world", "quoted"])

    def test_preserves_raw_form(self) -> None:
        t = ScriptTracker('Hello, World! "Quoted"')
        self.assertEqual(t.raw_tokens, ["Hello,", "World!", '"Quoted"'])


class EmptyScriptTests(unittest.TestCase):
    def test_empty_script(self) -> None:
        t = ScriptTracker("")
        state = t.advance(["hello"])
        self.assertEqual(state.matched_up_to, -1)
        self.assertEqual(state.total_tokens, 0)


class ExactMatchTests(unittest.TestCase):
    def test_exact_match_sequence(self) -> None:
        t = ScriptTracker("one two three four")
        state = t.advance(["one", "two", "three"])
        self.assertEqual(state.matched_up_to, 2)
        self.assertEqual(state.total_tokens, 4)

    def test_advance_incremental(self) -> None:
        t = ScriptTracker("one two three four")
        t.advance(["one"])
        state = t.advance(["two", "three"])
        self.assertEqual(state.matched_up_to, 2)


class CaseInsensitiveTests(unittest.TestCase):
    def test_case_insensitive(self) -> None:
        t = ScriptTracker("hello world")
        state = t.advance(["HELLO", "WORLD"])
        self.assertEqual(state.matched_up_to, 1)


class PunctuationTests(unittest.TestCase):
    def test_punctuation_stripped_from_script(self) -> None:
        t = ScriptTracker("Hello! World.")
        state = t.advance(["hello", "world"])
        self.assertEqual(state.matched_up_to, 1)

    def test_punctuation_stripped_from_recognized(self) -> None:
        t = ScriptTracker("hello world")
        state = t.advance(["hello,", "world!"])
        self.assertEqual(state.matched_up_to, 1)


class NoiseToleranceTests(unittest.TestCase):
    def test_asr_noise_skipped(self) -> None:
        t = ScriptTracker("one two three")
        state = t.advance(["zzz", "xxx", "one"])
        self.assertEqual(state.matched_up_to, 0)

    def test_garbage_between_matches(self) -> None:
        t = ScriptTracker("one two three")
        state = t.advance(["one", "zzz", "two"])
        self.assertEqual(state.matched_up_to, 1)


class SkippedWordTests(unittest.TestCase):
    def test_skipped_word(self) -> None:
        t = ScriptTracker("one two three four")
        state = t.advance(["one", "three"])
        self.assertEqual(state.matched_up_to, 2)


class MonotonicTests(unittest.TestCase):
    def test_monotonic(self) -> None:
        t = ScriptTracker("one two three four")
        t.advance(["one", "two", "three"])
        state = t.advance(["one", "two"])
        self.assertEqual(state.matched_up_to, 2)


class RepeatedWordTests(unittest.TestCase):
    def test_repeated_word_advances_to_next(self) -> None:
        t = ScriptTracker("the cat the dog the fish")
        t.advance(["the", "cat"])
        state = t.advance(["the", "dog"])
        self.assertEqual(state.matched_up_to, 3)

    def test_repeated_word_first_occurrence(self) -> None:
        t = ScriptTracker("the cat the dog")
        state = t.advance(["the"])
        self.assertEqual(state.matched_up_to, 0)


class PartialMatchTests(unittest.TestCase):
    def test_partial_match_rejected(self) -> None:
        t = ScriptTracker("the cat")
        state = t.advance(["th"])
        self.assertEqual(state.matched_up_to, -1)


class WindowLimitTests(unittest.TestCase):
    def test_window_limit(self) -> None:
        words = [f"w{i}" for i in range(20)]
        t = ScriptTracker(" ".join(words))
        state = t.advance(["w15"])
        self.assertEqual(state.matched_up_to, -1)

    def test_within_window(self) -> None:
        words = [f"w{i}" for i in range(20)]
        t = ScriptTracker(" ".join(words))
        state = t.advance(["w5"])
        self.assertEqual(state.matched_up_to, 5)


class FullScriptTests(unittest.TestCase):
    def test_full_script_read(self) -> None:
        script = "Right then roll the recorder breathe from the belly"
        t = ScriptTracker(script)
        words = script.lower().split()
        state = t.advance(words)
        self.assertEqual(state.matched_up_to, len(words) - 1)

    def test_state_property(self) -> None:
        t = ScriptTracker("hello world")
        t.advance(["hello"])
        state = t.state
        self.assertEqual(state.matched_up_to, 0)
        self.assertEqual(state.total_tokens, 2)


class EmDashTests(unittest.TestCase):
    def test_em_dash_stripped(self) -> None:
        t = ScriptTracker("word—another")
        self.assertEqual(t.norm_tokens, ["wordanother"])

    def test_quoted_words(self) -> None:
        t = ScriptTracker('"hello" \'world\'')
        self.assertEqual(t.norm_tokens, ["hello", "world"])


if __name__ == "__main__":
    unittest.main()
