"""Tests for profiler_ui pure helpers (format_enroll_status)."""

from __future__ import annotations

import unittest

from voice_transcription.core.profiler_core import EnrollmentResult
from voice_transcription.core.profiles import VoiceProfile
from voice_transcription.app.profiler_ui import format_enroll_status


def _profile(**overrides) -> VoiceProfile:
    defaults = dict(
        name="Grigori", player="Dave", embedding=[1.0, 0.0],
        sample_rate=16000, model_id="test", seconds=60.0,
        created_utc="2025-01-01T00:00:00Z", enhanced_spans=0,
        enhanced_sessions=[],
    )
    defaults.update(overrides)
    return VoiceProfile(**defaults)


def _result(**overrides) -> EnrollmentResult:
    return EnrollmentResult(
        profile=overrides.pop("profile", _profile(**{k: v for k, v in overrides.items()
                                                       if k in VoiceProfile.__dataclass_fields__})),
        similarity_to_existing={},
        rejected=overrides.get("rejected", 0),
    )


class FormatEnrollStatusTests(unittest.TestCase):
    def test_basic(self) -> None:
        result = _result()
        msg = format_enroll_status("Grigori", "Dave", result)
        self.assertEqual(msg, "Saved profile for Grigori (Dave)")

    def test_enhanced(self) -> None:
        result = _result(profile=_profile(enhanced_spans=3, enhanced_sessions=[1, 5]))
        msg = format_enroll_status("Grigori", "Dave", result)
        self.assertIn("enhanced with 3 corrected span(s)", msg)
        self.assertIn("[1, 5]", msg)

    def test_rejected(self) -> None:
        result = EnrollmentResult(
            profile=_profile(), similarity_to_existing={}, rejected=2,
        )
        msg = format_enroll_status("Grigori", "Dave", result)
        self.assertIn("2 outlier span(s) rejected", msg)

    def test_enhanced_and_rejected(self) -> None:
        result = EnrollmentResult(
            profile=_profile(enhanced_spans=3, enhanced_sessions=[1, 5]),
            similarity_to_existing={}, rejected=2,
        )
        msg = format_enroll_status("Grigori", "Dave", result)
        self.assertIn("enhanced with 3", msg)
        self.assertIn("2 outlier", msg)


if __name__ == "__main__":
    unittest.main()
