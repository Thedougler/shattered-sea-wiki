"""Tests for the wiki transcript formatter."""

from shattered_audio.formatter import format_wiki_transcript
from shattered_audio.transcribe import Segment


def test_basic_format():
    segments = [
        Segment(start=0.0, end=5.0, text="Hello everyone", speaker="DM"),
        Segment(start=5.0, end=10.0, text="Hi there", speaker="Nick"),
    ]
    output = format_wiki_transcript(
        segments,
        session_number=5,
        session_date="2026-06-01",
    )
    assert "type: raw" in output
    assert "session_number: 5" in output
    assert "**DM:** Hello everyone" in output
    assert "**Nick:** Hi there" in output


def test_frontmatter_fields():
    segments = [Segment(start=0.0, end=1.0, text="test", speaker="DM")]
    output = format_wiki_transcript(
        segments,
        session_number=10,
        session_date="2026-06-01",
        model="whisper-large-v3",
        diarization_model="pyannote/speaker-diarization-3.1",
        speaker_confidence=0.85,
    )
    assert 'diarization_model: "pyannote/speaker-diarization-3.1"' in output
    assert "speaker_confidence: 0.85" in output
    assert "ingest_status: pending" in output
