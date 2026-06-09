"""Transcribe a multi-mic session recording into per-part speaker CSVs.

Consumes what :mod:`shattered_audio.record` produces — one isolated m4a track
per microphone, chunked into time-aligned parts — and emits the per-part CSVs
that the ``session-ingest`` skill and ``shattered-audio assemble`` already
consume::

    .raw/sessions/session-07/transcripts/raw/session-07-part-00.csv  (ID,Start,End,Speaker,Text)
    .raw/sessions/session-07/transcripts/raw/session-07-part-01.csv
    ...

Because every mic is recorded with the same ``segment_time``, part index *MM*
covers the same wall-clock window across all mics. We transcribe each mic's
chunk for that window, label every utterance by which mic it came from (the mic
is a strong speaker prior — the DM's mic is the DM), refine the label with voice
profiles when available, then merge all mics into one time-ordered CSV for the
part.

Speaker attribution degrades gracefully:

1. **Voice profiles** (default, when enrolled) — :func:`identify_speaker_v2`
   turns a mic's audio into an actor or character-voice name.
2. **Mic prior** — the ``speaker`` recorded in the manifest for that mic.
3. **Stable label** — ``"Speaker mic01"`` so ``session-ingest`` can resolve it.

pyannote diarization is layered in only when ``HF_TOKEN`` is set; it splits
turns *within* a single mic (useful when two people share one mic). Without it,
each mic chunk is treated as one speaker stream — which is exactly right for the
common one-person-per-mic setup.
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

PART_CSV_FIELDS = ["ID", "Start", "End", "Speaker", "Text"]


@dataclass
class MicTrack:
    mic_id: str
    speaker: str | None
    parts: list[Path] = field(default_factory=list)


@dataclass
class Utterance:
    start: float
    end: float
    speaker: str
    text: str


def fmt_timestamp(seconds: float) -> str:
    """Format part-relative seconds as ``MM:SS`` (parts are <= ~15 min)."""
    total = int(round(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def _part_index(path: Path) -> int:
    """Extract the trailing integer from ``part003.m4a`` → 3."""
    digits = "".join(ch for ch in path.stem if ch.isdigit())
    return int(digits) if digits else 0


def discover_tracks(session_dir: Path) -> list[MicTrack]:
    """Find mic tracks for a session, honoring manifest.json if present.

    ``session_dir`` is the session packet root (``.raw/sessions/session-NN/``).
    Capture artifacts live under its ``audio/`` subdir: ``audio/manifest.json``,
    per-mic raw tracks under ``audio/raw/mic-XX/``, and any pre-split
    transcribe-ready parts under ``audio/parts/``.
    """
    audio = session_dir / "audio"
    manifest_path = audio / "manifest.json"
    raw = audio / "raw"

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        tracks: list[MicTrack] = []
        for m in manifest.get("mics", []):
            mic_id = m["mic_id"]
            # The manifest keeps the positional id (mic00); on disk the raw dir
            # is dash-form (mic-00), matching record.raw_mic_dir.
            digits = "".join(ch for ch in mic_id if ch.isdigit())
            mic_dir_name = f"mic-{int(digits):02d}" if digits else mic_id
            parts = sorted((raw / mic_dir_name).glob("*.m4a"), key=lambda p: p.name)
            tracks.append(MicTrack(mic_id=mic_id, speaker=m.get("speaker"), parts=parts))
        return tracks

    # No manifest: treat per-mic subdirs if present, else loose parts as one mic.
    if raw.is_dir():
        tracks = []
        for mic_dir in sorted(p for p in raw.iterdir() if p.is_dir()):
            parts = sorted(mic_dir.glob("*.m4a"), key=lambda p: p.name)
            if parts:
                tracks.append(MicTrack(mic_id=mic_dir.name, speaker=None, parts=parts))
        if tracks:
            return tracks

    loose = sorted((audio / "parts").glob("*.m4a"), key=lambda p: p.name)
    if loose:
        return [MicTrack(mic_id="mic00", speaker=None, parts=loose)]
    return []


def group_parts_by_index(tracks: list[MicTrack]) -> dict[int, list[tuple[MicTrack, Path]]]:
    """Group (track, part) pairs by part index so aligned windows transcribe together."""
    groups: dict[int, list[tuple[MicTrack, Path]]] = {}
    for track in tracks:
        for part in track.parts:
            groups.setdefault(_part_index(part), []).append((track, part))
    return groups


def resolve_speaker(match: str | None, prior: str | None, mic_id: str) -> str:
    """Pick the best available speaker label for an utterance."""
    if match:
        return match
    if prior:
        return prior
    return f"Speaker {mic_id}"


def merge_part_utterances(utterances: list[Utterance]) -> list[dict]:
    """Sort utterances across mics into one numbered, timestamped CSV row list."""
    kept = [u for u in utterances if u.text.strip()]
    kept.sort(key=lambda u: (u.start, u.speaker))
    rows = []
    for i, u in enumerate(kept, start=1):
        rows.append(
            {
                "ID": i,
                "Start": fmt_timestamp(u.start),
                "End": fmt_timestamp(u.end),
                "Speaker": u.speaker,
                "Text": u.text.strip(),
            }
        )
    return rows


def write_part_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PART_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Audio + model glue (kept behind small functions so tests can stay light)
# ---------------------------------------------------------------------------


def _load_samples(path: Path, sample_rate: int = 16000):
    """Load an audio file as mono float32 at ``sample_rate`` (resemblyzer-ready)."""
    import numpy as np
    from pydub import AudioSegment

    seg = AudioSegment.from_file(str(path)).set_channels(1).set_frame_rate(sample_rate)
    seg = seg.set_sample_width(2)
    return np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0


def _transcribe_part(path: Path, model: str) -> list[Utterance]:
    from .transcribe import transcribe as do_transcribe

    segments = do_transcribe(path, model=model)
    return [Utterance(start=s.start, end=s.end, speaker="", text=s.text) for s in segments]


def transcribe_session(
    session: int,
    audio_dir: Path,
    *,
    use_profiles: bool = True,
    profiles_dir: Path | None = None,
    model: str = "mlx-community/whisper-large-v3-mlx",
    channel_boost: float = 0.15,
    actor_threshold: float = 0.7,
    persona_threshold: float = 0.6,
    persona_margin: float = 0.05,
    prosody_weight: float = 0.3,
    log=None,
) -> list[Path]:
    """Transcribe every part of a recorded session to per-part speaker CSVs.

    Returns the list of CSV paths written. Voice profiles are loaded and applied
    by default; pass ``use_profiles=False`` to label purely by mic prior.
    """
    log = log or logger.info
    from .record import session_dir as _session_dir

    sdir = _session_dir(audio_dir, session)
    tracks = discover_tracks(sdir)
    if not tracks:
        raise FileNotFoundError(f"No mic tracks found under {sdir}")

    actors = {}
    if use_profiles:
        try:
            from .profiles import load_actor_profiles

            pdir = profiles_dir or (Path.home() / ".config" / "shattered-audio" / "profiles")
            actors = load_actor_profiles(pdir)
            if actors:
                log(f"Loaded {len(actors)} voice profile(s): {', '.join(a.name for a in actors.values())}")
            else:
                log("No voice profiles enrolled — labeling by mic prior")
        except Exception as e:  # resemblyzer / torch missing, etc.
            log(f"Voice profiles unavailable ({e}) — labeling by mic prior")
            actors = {}

    channel_priors = {t.mic_id: t.speaker for t in tracks if t.speaker}

    def identify(samples, mic_id: str) -> str | None:
        if not actors:
            return None
        try:
            from .profiles import identify_speaker_v2

            match = identify_speaker_v2(
                samples,
                actors,
                source_mic=mic_id,
                channel_priors=channel_priors,
                channel_boost=channel_boost,
                actor_threshold=actor_threshold,
                persona_threshold=persona_threshold,
                persona_margin=persona_margin,
                prosody_weight=prosody_weight,
            )
            return match.name if match else None
        except Exception:
            logger.debug("identify_speaker_v2 failed", exc_info=True)
            return None

    groups = group_parts_by_index(tracks)
    written: list[Path] = []

    for part_index in sorted(groups):
        members = groups[part_index]
        utterances: list[Utterance] = []
        for track, part_path in members:
            log(f"Transcribing part {part_index:02d} · {track.mic_id} ({part_path.name})")
            samples = None
            for utt in _transcribe_part(part_path, model):
                match = None
                if actors:
                    if samples is None:
                        samples = _load_samples(part_path)
                    seg_audio = _slice(samples, utt.start, utt.end)
                    if seg_audio is not None and len(seg_audio) > 0:
                        match = identify(seg_audio, track.mic_id)
                utt.speaker = resolve_speaker(match, track.speaker, track.mic_id)
                utterances.append(utt)

        rows = merge_part_utterances(utterances)
        out = (
            sdir
            / "transcripts"
            / "raw"
            / f"session-{session:02d}-part-{part_index:02d}.csv"
        )
        write_part_csv(rows, out)
        written.append(out)
        log(f"Wrote {len(rows)} line(s) → {out.name}")

    return written


def _slice(samples, start: float, end: float, sample_rate: int = 16000):
    """Slice [start, end] seconds out of a mono sample array."""
    a = max(0, int(start * sample_rate))
    b = min(len(samples), int(end * sample_rate))
    if b <= a:
        return None
    return samples[a:b]
