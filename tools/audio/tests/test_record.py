"""Tests for the multi-mic ffmpeg recorder (pure logic)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from shattered_audio import record
from shattered_audio.record import (
    RecordMic,
    build_ffmpeg_command,
    build_manifest,
    parse_avfoundation_devices,
    raw_mic_dir,
    select_mics,
    session_dir,
)

# Real `ffmpeg -f avfoundation -list_devices true -i ""` stderr on macOS.
SAMPLE_LISTING = """\
[AVFoundation indev @ 0x850c24140] AVFoundation video devices:
[AVFoundation indev @ 0x850c24140] [0] FaceTime HD Camera
[AVFoundation indev @ 0x850c24140] AVFoundation audio devices:
[AVFoundation indev @ 0x850c24140] [0] MacBook Air Microphone
[AVFoundation indev @ 0x850c24140] [1] EMEET OfficeCore M0 Plus
[in#0 @ 0x850c24000] Error opening input: Input/output error
"""


def test_parse_avfoundation_devices_returns_only_audio():
    devs = parse_avfoundation_devices(SAMPLE_LISTING)
    assert devs == [
        {"index": 0, "name": "MacBook Air Microphone"},
        {"index": 1, "name": "EMEET OfficeCore M0 Plus"},
    ]


def test_parse_avfoundation_devices_empty_when_no_audio_section():
    assert parse_avfoundation_devices("no devices here") == []


def test_select_mics_defaults_to_all():
    devs = parse_avfoundation_devices(SAMPLE_LISTING)
    mics = select_mics(devs)
    assert [m.index for m in mics] == [0, 1]
    assert [m.mic_id for m in mics] == ["mic00", "mic01"]
    assert mics[0].name == "MacBook Air Microphone"


def test_select_mics_by_index_spec_preserves_request_order():
    devs = parse_avfoundation_devices(SAMPLE_LISTING)
    mics = select_mics(devs, indices=[1, 0])
    assert [m.index for m in mics] == [1, 0]
    # mic_id is positional in the selection, not the device index
    assert [m.mic_id for m in mics] == ["mic00", "mic01"]


def test_select_mics_by_name_substring():
    devs = parse_avfoundation_devices(SAMPLE_LISTING)
    mics = select_mics(devs, names=["EMEET"])
    assert [m.index for m in mics] == [1]
    assert mics[0].name == "EMEET OfficeCore M0 Plus"


def test_select_mics_unknown_index_is_skipped():
    devs = parse_avfoundation_devices(SAMPLE_LISTING)
    mics = select_mics(devs, indices=[0, 9])
    assert [m.index for m in mics] == [0]


def test_build_ffmpeg_command_shape():
    out = Path("/tmp/s07/audio/raw/mic-00/part-%03d.m4a")
    cmd = build_ffmpeg_command(device_index=1, out_pattern=out, segment_seconds=900)
    assert cmd[0] == "ffmpeg"
    # avfoundation audio-only input is ":<index>"
    assert "-f" in cmd and "avfoundation" in cmd
    i = cmd.index("-i")
    assert cmd[i + 1] == ":1"
    # mono, 16 kHz, aac, segmented
    assert "-ac" in cmd and cmd[cmd.index("-ac") + 1] == "1"
    assert "-ar" in cmd and cmd[cmd.index("-ar") + 1] == "16000"
    assert "segment" in cmd
    assert cmd[cmd.index("-segment_time") + 1] == "900"
    assert cmd[-1] == str(out)


def test_session_and_raw_dirs_are_zero_padded():
    base = Path("/vault/.raw/sessions")
    assert session_dir(base, 7) == base / "session-07"
    assert session_dir(base, 12) == base / "session-12"
    mic = RecordMic(index=1, name="EMEET", mic_id="mic00")
    assert raw_mic_dir(base, 7, mic) == base / "session-07" / "audio" / "raw" / "mic-00"
    # a higher positional mic id reformats to dash form too
    mic1 = RecordMic(index=3, name="USB", mic_id="mic01")
    assert raw_mic_dir(base, 7, mic1) == base / "session-07" / "audio" / "raw" / "mic-01"


def test_build_manifest_records_mic_mapping():
    mics = [
        RecordMic(index=0, name="MacBook Air Microphone", mic_id="mic00", speaker="DM"),
        RecordMic(index=1, name="EMEET OfficeCore M0 Plus", mic_id="mic01"),
    ]
    m = build_manifest(session=7, mics=mics, segment_seconds=900)
    assert m["session"] == 7
    assert m["segment_seconds"] == 900
    assert m["mics"] == [
        {"mic_id": "mic00", "index": 0, "name": "MacBook Air Microphone", "speaker": "DM"},
        {"mic_id": "mic01", "index": 1, "name": "EMEET OfficeCore M0 Plus", "speaker": None},
    ]


# --- real-capture integration (skips without ffmpeg + a working mic) ---------


def _has_mics() -> bool:
    if shutil.which("ffmpeg") is None:
        return False
    try:
        return len(record.list_avfoundation_devices()) > 0
    except Exception:
        return False


@pytest.mark.skipif(not _has_mics(), reason="no ffmpeg/avfoundation mic available")
def test_record_session_real_capture(tmp_path):
    """A few seconds of real capture should produce finalized, segmented m4a."""
    mics = select_mics(record.list_avfoundation_devices())
    sdir = record.record_session(
        session=99, mics=mics, audio_dir=tmp_path, segment_seconds=2, max_seconds=5.0
    )
    assert (sdir / "audio" / "manifest.json").exists()
    parts = list(sdir.rglob("*.m4a"))
    assert parts, "expected at least one recorded segment"
    # every selected mic produced its own track directory (dash-form, under audio/)
    for mic in mics:
        assert raw_mic_dir(tmp_path, 99, mic).is_dir()
    # segments are non-trivially sized (not empty/truncated)
    assert all(p.stat().st_size > 256 for p in parts)
