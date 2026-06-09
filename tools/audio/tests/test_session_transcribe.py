"""Tests for the per-mic → per-part-CSV session transcription logic."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess

import pytest

from shattered_audio.session_transcribe import (
    Utterance,
    discover_tracks,
    fmt_timestamp,
    group_parts_by_index,
    merge_part_utterances,
    resolve_speaker,
    write_part_csv,
)


def _make_session(tmp_path, manifest, layout):
    """layout: {mic_id: [part_filenames]} — create empty m4a placeholders.

    Builds the new packet layout: capture artifacts live under ``<sdir>/audio/``
    (``audio/manifest.json`` + ``audio/raw/<mic_id>/``).
    """
    sdir = tmp_path / "session-07"
    audio = sdir / "audio"
    (audio / "raw").mkdir(parents=True)
    (audio / "manifest.json").write_text(json.dumps(manifest))
    for mic_id, parts in layout.items():
        d = audio / "raw" / mic_id
        d.mkdir(parents=True)
        for p in parts:
            (d / p).write_bytes(b"\x00")
    return sdir


def test_fmt_timestamp_is_mm_ss():
    assert fmt_timestamp(0) == "00:00"
    assert fmt_timestamp(5) == "00:05"
    assert fmt_timestamp(65) == "01:05"
    assert fmt_timestamp(900) == "15:00"


def test_discover_tracks_reads_manifest_and_orders_parts(tmp_path):
    manifest = {
        "session": 7,
        "segment_seconds": 900,
        "mics": [
            {"mic_id": "mic00", "index": 0, "name": "Built-in", "speaker": "DM"},
            {"mic_id": "mic01", "index": 1, "name": "USB", "speaker": "Nick"},
        ],
    }
    sdir = _make_session(
        tmp_path,
        manifest,
        {"mic-00": ["part-001.m4a", "part-000.m4a"], "mic-01": ["part-000.m4a"]},
    )
    tracks = discover_tracks(sdir)
    # mic_id stays in positional manifest form; on-disk dirs are dash-form
    assert [t.mic_id for t in tracks] == ["mic00", "mic01"]
    assert tracks[0].speaker == "DM"
    # parts sorted by name regardless of creation order
    assert [p.name for p in tracks[0].parts] == ["part-000.m4a", "part-001.m4a"]


def test_discover_tracks_without_manifest_treats_loose_parts_as_one_mic(tmp_path):
    sdir = tmp_path / "session-09"
    parts_dir = sdir / "audio" / "parts"
    parts_dir.mkdir(parents=True)
    (parts_dir / "session-09-part-00.m4a").write_bytes(b"\x00")
    tracks = discover_tracks(sdir)
    assert len(tracks) == 1
    assert tracks[0].speaker is None
    assert [p.name for p in tracks[0].parts] == ["session-09-part-00.m4a"]


def test_group_parts_by_index_aligns_mics_on_the_same_window(tmp_path):
    manifest = {
        "session": 7,
        "segment_seconds": 900,
        "mics": [
            {"mic_id": "mic00", "index": 0, "name": "a", "speaker": "DM"},
            {"mic_id": "mic01", "index": 1, "name": "b", "speaker": "Nick"},
        ],
    }
    sdir = _make_session(
        tmp_path,
        manifest,
        {"mic-00": ["part-000.m4a", "part-001.m4a"], "mic-01": ["part-000.m4a"]},
    )
    tracks = discover_tracks(sdir)
    groups = group_parts_by_index(tracks)
    # part 0 has both mics; part 1 has only mic00
    assert sorted(groups.keys()) == [0, 1]
    assert {t.mic_id for t, _ in groups[0]} == {"mic00", "mic01"}
    assert {t.mic_id for t, _ in groups[1]} == {"mic00"}


def test_resolve_speaker_prefers_match_then_prior_then_label():
    # identified persona/actor wins
    assert resolve_speaker("Thunk", prior="DM", mic_id="mic00") == "Thunk"
    # no match → mic's speaker prior from the manifest
    assert resolve_speaker(None, prior="Nick", mic_id="mic01") == "Nick"
    # no match, no prior → a stable mic-based label (so it's resolvable later)
    assert resolve_speaker(None, prior=None, mic_id="mic01") == "Speaker mic01"


def test_merge_part_utterances_sorts_and_numbers():
    utts = [
        Utterance(start=3.0, end=4.0, speaker="Nick", text="second"),
        Utterance(start=0.0, end=1.0, speaker="DM", text="first"),
        Utterance(start=3.0, end=3.5, speaker="DM", text="tie-break by speaker"),
    ]
    rows = merge_part_utterances(utts)
    assert [r["ID"] for r in rows] == [1, 2, 3]
    assert [r["Text"] for r in rows] == ["first", "tie-break by speaker", "second"]
    assert rows[0] == {
        "ID": 1,
        "Start": "00:00",
        "End": "00:01",
        "Speaker": "DM",
        "Text": "first",
    }


def test_merge_drops_empty_text():
    utts = [
        Utterance(start=0.0, end=1.0, speaker="DM", text="  "),
        Utterance(start=1.0, end=2.0, speaker="DM", text="real"),
    ]
    rows = merge_part_utterances(utts)
    assert [r["Text"] for r in rows] == ["real"]


def test_write_part_csv_matches_session_ingest_schema(tmp_path):
    rows = [
        {"ID": 1, "Start": "00:00", "End": "00:01", "Speaker": "DM", "Text": 'He said "hi"'},
    ]
    out = tmp_path / "session-07-part-00.csv"
    write_part_csv(rows, out)
    with open(out, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["ID", "Start", "End", "Speaker", "Text"]
        got = list(reader)
    assert got[0]["Text"] == 'He said "hi"'
    assert got[0]["Speaker"] == "DM"


# --- real whisper end-to-end (skips without mlx_whisper + macOS `say`) --------


def _can_e2e() -> bool:
    if shutil.which("say") is None or shutil.which("ffmpeg") is None:
        return False
    try:
        import mlx_whisper  # noqa: F401

        return True
    except Exception:
        return False


@pytest.mark.skipif(not _can_e2e(), reason="needs macOS `say` + ffmpeg + mlx_whisper")
def test_transcribe_session_real_whisper(tmp_path):
    """Synthesize speech, record it as a session part, transcribe to CSV."""
    from shattered_audio.session_transcribe import transcribe_session

    sdir = tmp_path / "session-42"
    mic_dir = sdir / "audio" / "raw" / "mic-00"
    mic_dir.mkdir(parents=True)
    (sdir / "audio" / "manifest.json").write_text(
        json.dumps(
            {
                "session": 42,
                "segment_seconds": 900,
                "mics": [{"mic_id": "mic00", "index": 0, "name": "test", "speaker": "DM"}],
            }
        )
    )
    aiff = tmp_path / "line.aiff"
    subprocess.run(
        ["say", "-o", str(aiff), "The dragon guards the bridge."], check=True
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(aiff),
         "-ac", "1", "-ar", "16000", "-c:a", "aac", str(mic_dir / "part-000.m4a")],
        check=True,
    )

    transcribe_session(42, audio_dir=tmp_path, use_profiles=False)

    csv_path = sdir / "transcripts" / "raw" / "session-42-part-00.csv"
    assert csv_path.exists(), "expected a per-part CSV"
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows, "transcript should not be empty"
    assert all(r["Speaker"] == "DM" for r in rows)  # mic prior applied
    joined = " ".join(r["Text"] for r in rows).lower()
    assert "dragon" in joined or "bridge" in joined
