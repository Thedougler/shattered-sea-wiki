"""Voice profile management — enrollment, identification, and retraining."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from .capture import SAMPLE_RATE

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 256


@dataclass
class SpeakerMatch:
    name: str
    confidence: float


@dataclass
class VoiceProfile:
    name: str
    embedding: np.ndarray
    sample_count: int = 1
    associated_mics: list[str] | None = None


def _get_encoder():
    """Lazy-load the resemblyzer voice encoder."""
    from resemblyzer import VoiceEncoder

    return VoiceEncoder("cpu")


def extract_embedding(audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Extract a d-vector embedding from audio samples."""
    from resemblyzer import preprocess_wav

    wav = preprocess_wav(audio, source_sr=sample_rate)
    encoder = _get_encoder()
    return encoder.embed_utterance(wav)


def load_profiles(profiles_dir: Path) -> dict[str, VoiceProfile]:
    """Load all voice profiles from a directory."""
    profiles = {}
    if not profiles_dir.exists():
        return profiles

    for npy_path in profiles_dir.glob("*.npy"):
        name = npy_path.stem
        meta_path = npy_path.with_name(f"{name}_meta.yaml")

        embedding = np.load(npy_path)
        meta = {}
        if meta_path.exists():
            with open(meta_path) as f:
                meta = yaml.safe_load(f) or {}

        profiles[name] = VoiceProfile(
            name=meta.get("name", name),
            embedding=embedding,
            sample_count=meta.get("sample_count", 1),
            associated_mics=meta.get("associated_mics"),
        )
        logger.debug("Loaded profile: %s (%d samples)", name, profiles[name].sample_count)

    return profiles


def save_profile(profile: VoiceProfile, profiles_dir: Path) -> None:
    """Save a voice profile to disk."""
    profiles_dir.mkdir(parents=True, exist_ok=True)
    slug = profile.name.lower().replace(" ", "-")

    np.save(profiles_dir / f"{slug}.npy", profile.embedding)

    meta = {
        "name": profile.name,
        "sample_count": profile.sample_count,
    }
    if profile.associated_mics:
        meta["associated_mics"] = profile.associated_mics

    with open(profiles_dir / f"{slug}_meta.yaml", "w") as f:
        yaml.dump(meta, f, default_flow_style=False)

    logger.info("Saved profile: %s", profile.name)


def identify_speaker(
    audio: np.ndarray,
    profiles: dict[str, VoiceProfile],
    source_mic: str | None = None,
    channel_priors: dict[str, str] | None = None,
    channel_boost: float = 0.15,
    threshold: float = 0.7,
    sample_rate: int = SAMPLE_RATE,
) -> SpeakerMatch | None:
    """Identify who is speaking from a segment of audio.

    Returns the best matching speaker if confidence exceeds threshold.
    """
    if not profiles:
        return None

    embedding = extract_embedding(audio, sample_rate)

    best_name = None
    best_score = -1.0

    for slug, profile in profiles.items():
        score = float(
            np.dot(embedding, profile.embedding)
            / (np.linalg.norm(embedding) * np.linalg.norm(profile.embedding))
        )

        # Apply channel prior boost
        if source_mic and channel_priors and profile.associated_mics:
            expected_speaker = channel_priors.get(source_mic)
            if expected_speaker and expected_speaker.lower() == profile.name.lower():
                score += channel_boost

        if score > best_score:
            best_score = score
            best_name = profile.name

    if best_score >= threshold and best_name:
        return SpeakerMatch(name=best_name, confidence=best_score)

    return None


def enroll_from_audio(
    name: str,
    audio: np.ndarray,
    profiles_dir: Path,
    sample_rate: int = SAMPLE_RATE,
    associated_mics: list[str] | None = None,
) -> VoiceProfile:
    """Create a new voice profile from audio samples."""
    embedding = extract_embedding(audio, sample_rate)

    existing = load_profiles(profiles_dir)
    slug = name.lower().replace(" ", "-")

    if slug in existing:
        old = existing[slug]
        blend = 0.3
        embedding = blend * old.embedding + (1 - blend) * embedding
        embedding = embedding / np.linalg.norm(embedding)
        sample_count = old.sample_count + 1
        mics = associated_mics or old.associated_mics
    else:
        sample_count = 1
        mics = associated_mics

    profile = VoiceProfile(
        name=name,
        embedding=embedding,
        sample_count=sample_count,
        associated_mics=mics,
    )
    save_profile(profile, profiles_dir)
    return profile


def enroll_from_file(
    name: str,
    audio_path: Path,
    profiles_dir: Path,
    associated_mics: list[str] | None = None,
) -> VoiceProfile:
    """Enroll a speaker from an audio file."""
    from pydub import AudioSegment

    seg = AudioSegment.from_file(str(audio_path))
    seg = seg.set_channels(1).set_frame_rate(SAMPLE_RATE).set_sample_width(2)
    samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0

    return enroll_from_audio(name, samples, profiles_dir, associated_mics=associated_mics)


def retrain_from_transcript(
    transcript_path: Path,
    audio_dir: Path,
    profiles_dir: Path,
    blend_old: float = 0.3,
) -> dict[str, VoiceProfile]:
    """Retrain voice profiles from a corrected transcript.

    Parses speaker labels and timestamps from the transcript,
    extracts corresponding audio, and updates profiles.
    """
    from pydub import AudioSegment

    text = transcript_path.read_text(encoding="utf-8")

    # Parse frontmatter for audio_file reference
    audio_file = None
    fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if fm_match:
        fm = yaml.safe_load(fm_match.group(1)) or {}
        audio_file = fm.get("audio_file")

    # Find the WAV file
    if audio_file:
        wav_path = audio_dir / audio_file
    else:
        wavs = list(audio_dir.glob("*.wav"))
        if not wavs:
            raise FileNotFoundError(f"No WAV files found in {audio_dir}")
        wav_path = wavs[0]

    if not wav_path.exists():
        raise FileNotFoundError(f"Audio file not found: {wav_path}")

    audio = AudioSegment.from_wav(str(wav_path))
    audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE).set_sample_width(2)

    # Parse transcript lines: [HH:MM:SS] **Speaker:** text
    pattern = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})\]\s+\*\*(.+?)\*\*:")
    speaker_segments: dict[str, list[np.ndarray]] = {}

    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = pattern.match(line.strip())
        if not match:
            continue
        h, m, s, speaker = match.groups()
        start_ms = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000

        # Look ahead for next timestamp to get end time
        end_ms = start_ms + 15000  # default 15s
        for j in range(i + 1, min(i + 10, len(lines))):
            next_match = pattern.match(lines[j].strip())
            if next_match:
                nh, nm, ns = next_match.group(1), next_match.group(2), next_match.group(3)
                end_ms = (int(nh) * 3600 + int(nm) * 60 + int(ns)) * 1000
                break

        segment = audio[start_ms:end_ms]
        samples = np.array(segment.get_array_of_samples(), dtype=np.float32) / 32768.0

        if len(samples) < SAMPLE_RATE * 0.5:  # skip very short segments
            continue

        speaker = speaker.strip()
        if speaker.startswith("UNKNOWN"):
            continue

        if speaker not in speaker_segments:
            speaker_segments[speaker] = []
        speaker_segments[speaker].append(samples)

    existing = load_profiles(profiles_dir)
    updated = {}

    for speaker, segments in speaker_segments.items():
        combined = np.concatenate(segments)
        new_embedding = extract_embedding(combined)
        slug = speaker.lower().replace(" ", "-")

        if slug in existing:
            old = existing[slug]
            blended = blend_old * old.embedding + (1 - blend_old) * new_embedding
            blended = blended / np.linalg.norm(blended)
            profile = VoiceProfile(
                name=speaker,
                embedding=blended,
                sample_count=old.sample_count + len(segments),
                associated_mics=old.associated_mics,
            )
        else:
            profile = VoiceProfile(
                name=speaker,
                embedding=new_embedding,
                sample_count=len(segments),
            )

        save_profile(profile, profiles_dir)
        updated[slug] = profile
        logger.info(
            "Retrained profile: %s (%d segments, %d total samples)",
            speaker,
            len(segments),
            profile.sample_count,
        )

    return updated
