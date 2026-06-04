"""Voice profile management — enrollment, identification, and retraining.

v2.0: Hierarchical actor→persona profiles for character voice separation.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

from .capture import SAMPLE_RATE

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 256


# ---------------------------------------------------------------------------
# v1 compat types (still used by legacy load/save paths)
# ---------------------------------------------------------------------------


@dataclass
class VoiceProfile:
    name: str
    embedding: np.ndarray
    sample_count: int = 1
    associated_mics: list[str] | None = None


# ---------------------------------------------------------------------------
# v2 types
# ---------------------------------------------------------------------------


@dataclass
class SpeakerMatch:
    name: str
    confidence: float
    actor: str | None = None
    persona: str | None = None
    tier: str = "low"


@dataclass
class ProsodyStats:
    pitch_mean: float
    pitch_std: float
    pitch_range: float
    energy_mean: float
    speaking_rate: float
    sample_count: int = 1


@dataclass
class PersonaProfile:
    name: str
    embedding: np.ndarray
    prosody: ProsodyStats | None = None
    sample_count: int = 1
    exemplar_embeddings: list[np.ndarray] | None = None


@dataclass
class ActorProfile:
    name: str
    embedding: np.ndarray
    personas: dict[str, PersonaProfile] = field(default_factory=dict)
    prosody: ProsodyStats | None = None
    sample_count: int = 1
    associated_mics: list[str] | None = None
    is_dm: bool = False


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


def extract_prosody(audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> ProsodyStats:
    """Extract prosodic features from audio — pitch, energy, speaking rate."""
    import torch

    energy_rms = float(np.sqrt(np.mean(audio**2)))

    # Pitch via torchaudio
    waveform = torch.from_numpy(audio).unsqueeze(0).float()
    try:
        import torchaudio.functional as F

        pitch = F.detect_pitch_frequency(waveform, sample_rate)
        pitch_vals = pitch[pitch > 50].numpy()  # filter sub-50Hz artifacts
    except Exception:
        pitch_vals = np.array([])

    if len(pitch_vals) > 0:
        p5, p95 = np.percentile(pitch_vals, [5, 95])
        pitch_mean = float(np.mean(pitch_vals))
        pitch_std = float(np.std(pitch_vals))
        pitch_range = float(p95 - p5)
    else:
        pitch_mean = 0.0
        pitch_std = 0.0
        pitch_range = 0.0

    # Speaking rate proxy: peaks in smoothed energy envelope
    frame_len = int(0.02 * sample_rate)  # 20ms frames
    n_frames = len(audio) // frame_len
    if n_frames > 0:
        frames = audio[: n_frames * frame_len].reshape(n_frames, frame_len)
        envelope = np.sqrt(np.mean(frames**2, axis=1))
        if len(envelope) > 3:
            smoothed = np.convolve(envelope, np.ones(3) / 3, mode="same")
            peaks = 0
            for i in range(1, len(smoothed) - 1):
                if smoothed[i] > smoothed[i - 1] and smoothed[i] > smoothed[i + 1]:
                    peaks += 1
            duration_s = len(audio) / sample_rate
            speaking_rate = peaks / duration_s if duration_s > 0 else 0.0
        else:
            speaking_rate = 0.0
    else:
        speaking_rate = 0.0

    return ProsodyStats(
        pitch_mean=pitch_mean,
        pitch_std=pitch_std,
        pitch_range=pitch_range,
        energy_mean=energy_rms,
        speaking_rate=speaking_rate,
    )


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def _prosody_distance(a: ProsodyStats, b: ProsodyStats) -> float:
    """Weighted Euclidean distance between prosody stats, normalized 0-1."""
    weights = np.array([1.0, 0.5, 0.8, 0.3, 0.7])
    va = np.array([a.pitch_mean, a.pitch_std, a.pitch_range, a.energy_mean, a.speaking_rate])
    vb = np.array([b.pitch_mean, b.pitch_std, b.pitch_range, b.energy_mean, b.speaking_rate])
    # Normalize each dimension by the max of the two values to get 0-1 range
    maxes = np.maximum(np.abs(va), np.abs(vb))
    maxes = np.where(maxes == 0, 1.0, maxes)
    diff = np.abs(va - vb) / maxes
    return float(np.sqrt(np.sum(weights * diff**2)) / np.sqrt(np.sum(weights)))


# ---------------------------------------------------------------------------
# v2 load/save — actor subdirectory format with legacy fallback
# ---------------------------------------------------------------------------


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def _load_persona(actor_dir: Path, slug: str) -> PersonaProfile | None:
    npy_path = actor_dir / f"{slug}.npy"
    if not npy_path.exists():
        return None
    embedding = np.load(npy_path)

    prosody_path = actor_dir / f"{slug}_prosody.yaml"
    prosody = None
    if prosody_path.exists():
        with open(prosody_path) as f:
            pd = yaml.safe_load(f) or {}
        prosody = ProsodyStats(**{k: pd[k] for k in ProsodyStats.__dataclass_fields__ if k in pd})

    exemplars_path = actor_dir / f"{slug}_exemplars.npy"
    exemplars = None
    if exemplars_path.exists():
        arr = np.load(exemplars_path)
        exemplars = [arr[i] for i in range(arr.shape[0])]

    meta_path = actor_dir / f"{slug}_meta.yaml"
    meta = {}
    if meta_path.exists():
        with open(meta_path) as f:
            meta = yaml.safe_load(f) or {}

    return PersonaProfile(
        name=meta.get("name", slug),
        embedding=embedding,
        prosody=prosody,
        sample_count=meta.get("sample_count", 1),
        exemplar_embeddings=exemplars,
    )


def load_actor_profiles(profiles_dir: Path) -> dict[str, ActorProfile]:
    """Load all actor profiles, auto-detecting v1 and v2 formats."""
    actors: dict[str, ActorProfile] = {}
    if not profiles_dir.exists():
        return actors

    # v2 format: subdirectories with base.npy + meta.yaml
    for actor_dir in profiles_dir.iterdir():
        if not actor_dir.is_dir():
            continue
        base_path = actor_dir / "base.npy"
        if not base_path.exists():
            continue

        embedding = np.load(base_path)
        meta_path = actor_dir / "meta.yaml"
        meta = {}
        if meta_path.exists():
            with open(meta_path) as f:
                meta = yaml.safe_load(f) or {}

        # Load actor-level prosody
        prosody_path = actor_dir / "base_prosody.yaml"
        prosody = None
        if prosody_path.exists():
            with open(prosody_path) as f:
                pd = yaml.safe_load(f) or {}
            prosody = ProsodyStats(
                **{k: pd[k] for k in ProsodyStats.__dataclass_fields__ if k in pd}
            )

        # Load personas
        personas: dict[str, PersonaProfile] = {}
        for persona_slug in meta.get("personas", []):
            persona = _load_persona(actor_dir, persona_slug)
            if persona:
                personas[persona_slug] = persona

        actor_slug = actor_dir.name
        actors[actor_slug] = ActorProfile(
            name=meta.get("name", actor_slug),
            embedding=embedding,
            personas=personas,
            prosody=prosody,
            sample_count=meta.get("sample_count", 1),
            associated_mics=meta.get("associated_mics"),
            is_dm=meta.get("is_dm", False),
        )
        logger.debug("Loaded actor: %s (%d personas)", actors[actor_slug].name, len(personas))

    # v1 legacy: flat .npy files at profiles root (not inside subdirectories)
    for npy_path in profiles_dir.glob("*.npy"):
        slug = npy_path.stem
        if slug in actors:
            continue
        meta_path = npy_path.with_name(f"{slug}_meta.yaml")
        meta = {}
        if meta_path.exists():
            with open(meta_path) as f:
                meta = yaml.safe_load(f) or {}

        actors[slug] = ActorProfile(
            name=meta.get("name", slug),
            embedding=np.load(npy_path),
            sample_count=meta.get("sample_count", 1),
            associated_mics=meta.get("associated_mics"),
        )
        logger.debug("Loaded legacy profile as actor: %s", slug)

    return actors


def save_actor_profile(actor: ActorProfile, profiles_dir: Path) -> None:
    """Save an actor profile to the v2 subdirectory format."""
    profiles_dir.mkdir(parents=True, exist_ok=True)
    actor_slug = _slug(actor.name)
    actor_dir = profiles_dir / actor_slug
    actor_dir.mkdir(exist_ok=True)

    np.save(actor_dir / "base.npy", actor.embedding)

    if actor.prosody:
        with open(actor_dir / "base_prosody.yaml", "w") as f:
            yaml.dump(
                {
                    "pitch_mean": actor.prosody.pitch_mean,
                    "pitch_std": actor.prosody.pitch_std,
                    "pitch_range": actor.prosody.pitch_range,
                    "energy_mean": actor.prosody.energy_mean,
                    "speaking_rate": actor.prosody.speaking_rate,
                    "sample_count": actor.prosody.sample_count,
                },
                f,
                default_flow_style=False,
            )

    meta = {
        "name": actor.name,
        "sample_count": actor.sample_count,
        "is_dm": actor.is_dm,
        "personas": list(actor.personas.keys()),
    }
    if actor.associated_mics:
        meta["associated_mics"] = actor.associated_mics

    with open(actor_dir / "meta.yaml", "w") as f:
        yaml.dump(meta, f, default_flow_style=False)

    for persona_slug, persona in actor.personas.items():
        np.save(actor_dir / f"{persona_slug}.npy", persona.embedding)

        if persona.prosody:
            with open(actor_dir / f"{persona_slug}_prosody.yaml", "w") as f:
                yaml.dump(
                    {
                        "pitch_mean": persona.prosody.pitch_mean,
                        "pitch_std": persona.prosody.pitch_std,
                        "pitch_range": persona.prosody.pitch_range,
                        "energy_mean": persona.prosody.energy_mean,
                        "speaking_rate": persona.prosody.speaking_rate,
                        "sample_count": persona.prosody.sample_count,
                    },
                    f,
                    default_flow_style=False,
                )

        if persona.exemplar_embeddings:
            stacked = np.stack(persona.exemplar_embeddings)
            np.save(actor_dir / f"{persona_slug}_exemplars.npy", stacked)

        persona_meta = {"name": persona.name, "sample_count": persona.sample_count}
        with open(actor_dir / f"{persona_slug}_meta.yaml", "w") as f:
            yaml.dump(persona_meta, f, default_flow_style=False)

    logger.info("Saved actor: %s (%d personas)", actor.name, len(actor.personas))


def build_persona_lookup(actors: dict[str, ActorProfile]) -> dict[str, str]:
    """Build a persona_name→actor_slug lookup from loaded actors."""
    lookup: dict[str, str] = {}
    for actor_slug, actor in actors.items():
        for persona_slug in actor.personas:
            lookup[persona_slug] = actor_slug
    return lookup


# ---------------------------------------------------------------------------
# v2 identification — two-stage hierarchical
# ---------------------------------------------------------------------------


def identify_speaker_v2(
    audio: np.ndarray,
    actors: dict[str, ActorProfile],
    source_mic: str | None = None,
    channel_priors: dict[str, str] | None = None,
    channel_boost: float = 0.15,
    actor_threshold: float = 0.7,
    persona_threshold: float = 0.6,
    persona_margin: float = 0.05,
    prosody_weight: float = 0.3,
    use_prosody: bool = True,
    sample_rate: int = SAMPLE_RATE,
) -> SpeakerMatch | None:
    """Two-stage speaker identification: actor first, then persona.

    Stage 1 identifies the physical speaker (actor) via d-vector similarity.
    Stage 2 distinguishes character voices (personas) using embeddings + prosody.
    Falls back to actor name when persona can't be distinguished.
    """
    if not actors:
        return None

    embedding = extract_embedding(audio, sample_rate)

    # Stage 1: actor identification
    best_actor_slug = None
    best_actor_score = -1.0

    for slug, actor in actors.items():
        score = _cosine_similarity(embedding, actor.embedding)

        if source_mic and channel_priors:
            expected = channel_priors.get(source_mic)
            if expected and expected.lower() == actor.name.lower():
                score += channel_boost

        if score > best_actor_score:
            best_actor_score = score
            best_actor_slug = slug

    if best_actor_score < actor_threshold or best_actor_slug is None:
        return None

    actor = actors[best_actor_slug]

    # Fast path: no personas registered — return actor name
    if not actor.personas:
        tier = "high" if best_actor_score >= 0.8 else "medium"
        return SpeakerMatch(
            name=actor.name,
            confidence=best_actor_score,
            actor=actor.name,
            persona=None,
            tier=tier,
        )

    # Stage 2: persona disambiguation
    prosody = None
    if use_prosody:
        try:
            prosody = extract_prosody(audio, sample_rate)
        except Exception:
            logger.debug("Prosody extraction failed, using embedding-only for Stage 2")

    # Score each persona
    best_persona_slug = None
    best_persona_score = -1.0
    self_score = _cosine_similarity(embedding, actor.embedding)

    if prosody and actor.prosody:
        pdist = _prosody_distance(prosody, actor.prosody)
        self_score = (1 - prosody_weight) * self_score + prosody_weight * (1 - pdist)

    for p_slug, persona in actor.personas.items():
        if persona.exemplar_embeddings:
            emb_sim = max(_cosine_similarity(embedding, ex) for ex in persona.exemplar_embeddings)
        else:
            emb_sim = _cosine_similarity(embedding, persona.embedding)

        if prosody and persona.prosody:
            pdist = _prosody_distance(prosody, persona.prosody)
            combined = (1 - prosody_weight) * emb_sim + prosody_weight * (1 - pdist)
        else:
            combined = emb_sim

        if combined > best_persona_score:
            best_persona_score = combined
            best_persona_slug = p_slug

    # Decision: does the best persona beat "self" by enough margin?
    if (
        best_persona_slug is not None
        and best_persona_score >= persona_threshold
        and best_persona_score > self_score + persona_margin
    ):
        persona = actor.personas[best_persona_slug]
        tier = "high" if best_persona_score >= 0.7 else "medium"
        return SpeakerMatch(
            name=persona.name,
            confidence=best_persona_score,
            actor=actor.name,
            persona=persona.name,
            tier=tier,
        )

    # Fallback: return actor name
    tier = "high" if best_actor_score >= 0.8 else "medium"
    return SpeakerMatch(
        name=actor.name,
        confidence=best_actor_score,
        actor=actor.name,
        persona=None,
        tier=tier,
    )


# ---------------------------------------------------------------------------
# v2 enrollment
# ---------------------------------------------------------------------------


def enroll_actor(
    name: str,
    audio: np.ndarray,
    profiles_dir: Path,
    sample_rate: int = SAMPLE_RATE,
    associated_mics: list[str] | None = None,
    is_dm: bool = False,
) -> ActorProfile:
    """Create or update an actor-level voice profile."""
    embedding = extract_embedding(audio, sample_rate)
    prosody = extract_prosody(audio, sample_rate)

    actors = load_actor_profiles(profiles_dir)
    slug = _slug(name)

    if slug in actors:
        old = actors[slug]
        blend = 0.3
        embedding = blend * old.embedding + (1 - blend) * embedding
        embedding = embedding / np.linalg.norm(embedding)
        actor = ActorProfile(
            name=name,
            embedding=embedding,
            personas=old.personas,
            prosody=prosody,
            sample_count=old.sample_count + 1,
            associated_mics=associated_mics or old.associated_mics,
            is_dm=is_dm or old.is_dm,
        )
    else:
        actor = ActorProfile(
            name=name,
            embedding=embedding,
            prosody=prosody,
            sample_count=1,
            associated_mics=associated_mics,
            is_dm=is_dm,
        )

    save_actor_profile(actor, profiles_dir)
    return actor


def enroll_persona(
    persona_name: str,
    actor_name: str,
    audio: np.ndarray,
    profiles_dir: Path,
    sample_rate: int = SAMPLE_RATE,
    max_exemplars: int = 8,
) -> ActorProfile:
    """Create or update a persona (character voice) under an actor."""
    actors = load_actor_profiles(profiles_dir)
    actor_slug = _slug(actor_name)

    if actor_slug not in actors:
        raise ValueError(
            f"Actor '{actor_name}' not found. Enroll the actor first with: "
            f'shattered-audio enroll "{actor_name}"'
        )

    actor = actors[actor_slug]
    embedding = extract_embedding(audio, sample_rate)
    prosody = extract_prosody(audio, sample_rate)
    persona_slug = _slug(persona_name)

    if persona_slug in actor.personas:
        old = actor.personas[persona_slug]
        # Update averaged embedding
        blend = 0.3
        avg_embedding = blend * old.embedding + (1 - blend) * embedding
        avg_embedding = avg_embedding / np.linalg.norm(avg_embedding)

        # Add to exemplars
        exemplars = list(old.exemplar_embeddings or [])
        exemplars.append(embedding)
        if len(exemplars) > max_exemplars:
            # Keep most recent exemplars
            exemplars = exemplars[-max_exemplars:]

        actor.personas[persona_slug] = PersonaProfile(
            name=persona_name,
            embedding=avg_embedding,
            prosody=prosody,
            sample_count=old.sample_count + 1,
            exemplar_embeddings=exemplars,
        )
    else:
        actor.personas[persona_slug] = PersonaProfile(
            name=persona_name,
            embedding=embedding,
            prosody=prosody,
            sample_count=1,
            exemplar_embeddings=[embedding],
        )

    save_actor_profile(actor, profiles_dir)
    return actor


# ---------------------------------------------------------------------------
# Speaker map parsing (bridges session-ingest → retrain)
# ---------------------------------------------------------------------------

_SPEAKER_MAP_ROW = re.compile(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(high|medium|low|unknown)\s*\|")


def parse_speaker_map(path: Path) -> dict[str, str]:
    """Read a session-ingest speaker-map.md and return {label: resolved_name}.

    Only includes high and medium confidence resolutions.
    Keys are case-preserved original labels (e.g. "UNKNOWN_3", "Speaker 1").
    """
    label_map: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _SPEAKER_MAP_ROW.match(line.strip())
        if not m:
            continue
        label, resolved, confidence = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if confidence in ("high", "medium") and label.lower() not in ("label", "---"):
            label_map[label] = resolved
    return label_map


# ---------------------------------------------------------------------------
# v2 retraining
# ---------------------------------------------------------------------------


def retrain_from_transcript_v2(
    transcript_path: Path,
    audio_dir: Path,
    profiles_dir: Path,
    blend_old: float = 0.3,
    speaker_map: dict[str, str] | None = None,
) -> dict[str, ActorProfile]:
    """Retrain actor+persona profiles from a corrected transcript.

    Handles both actor labels ("Nick") and persona labels ("Thunk").
    Persona labels are resolved via the actor registry.
    Also parses "Name (as Persona)" format.

    If speaker_map is provided, remaps labels before processing — e.g.
    {"UNKNOWN_3": "Perrin", "Speaker 1": "Crissdalyn"} turns UNKNOWN lines
    into usable training data.
    """
    from pydub import AudioSegment

    text = transcript_path.read_text(encoding="utf-8")

    audio_file = None
    fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if fm_match:
        fm = yaml.safe_load(fm_match.group(1)) or {}
        audio_file = fm.get("audio_file")

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

    pattern = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})\]\s+\*\*(.+?)\*\*:")
    actor_persona_pattern = re.compile(r"(.+?)\s*\(as\s+(.+?)\)")

    # Collect segments per resolved label: (actor_slug, persona_slug | None) → samples
    actors = load_actor_profiles(profiles_dir)
    persona_lookup = build_persona_lookup(actors)

    segments_by_target: dict[tuple[str, str | None], list[np.ndarray]] = {}

    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = pattern.match(line.strip())
        if not match:
            continue
        h, m, s, speaker_raw = match.groups()
        start_ms = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000

        end_ms = start_ms + 15000
        for j in range(i + 1, min(i + 10, len(lines))):
            next_match = pattern.match(lines[j].strip())
            if next_match:
                nh, nm, ns = next_match.group(1), next_match.group(2), next_match.group(3)
                end_ms = (int(nh) * 3600 + int(nm) * 60 + int(ns)) * 1000
                break

        segment = audio[start_ms:end_ms]
        samples = np.array(segment.get_array_of_samples(), dtype=np.float32) / 32768.0

        if len(samples) < SAMPLE_RATE * 0.5:
            continue

        speaker_raw = speaker_raw.strip()
        if speaker_map:
            speaker_raw = speaker_map.get(speaker_raw, speaker_raw)
        if speaker_raw.startswith("UNKNOWN"):
            continue

        # Parse "Nick (as Thunk)" format
        ap_match = actor_persona_pattern.match(speaker_raw)
        if ap_match:
            actor_slug = _slug(ap_match.group(1))
            persona_slug = _slug(ap_match.group(2))
            target = (actor_slug, persona_slug)
        else:
            slug = _slug(speaker_raw)
            if slug in persona_lookup:
                target = (persona_lookup[slug], slug)
            elif slug in actors:
                target = (slug, None)
            else:
                target = (slug, None)

        if target not in segments_by_target:
            segments_by_target[target] = []
        segments_by_target[target].append(samples)

    updated: dict[str, ActorProfile] = {}

    for (actor_slug, persona_slug), sample_list in segments_by_target.items():
        combined = np.concatenate(sample_list)
        new_embedding = extract_embedding(combined)
        new_prosody = extract_prosody(combined)

        if actor_slug in actors:
            actor = actors[actor_slug]
        else:
            actor = ActorProfile(
                name=actor_slug.replace("-", " ").title(),
                embedding=new_embedding,
                prosody=new_prosody,
                sample_count=len(sample_list),
            )

        if persona_slug is None:
            blended = blend_old * actor.embedding + (1 - blend_old) * new_embedding
            blended = blended / np.linalg.norm(blended)
            actor.embedding = blended
            actor.prosody = new_prosody
            actor.sample_count += len(sample_list)
        else:
            if persona_slug in actor.personas:
                old_p = actor.personas[persona_slug]
                blended = blend_old * old_p.embedding + (1 - blend_old) * new_embedding
                blended = blended / np.linalg.norm(blended)
                exemplars = list(old_p.exemplar_embeddings or [])
                exemplars.append(new_embedding)
                if len(exemplars) > 8:
                    exemplars = exemplars[-8:]
                actor.personas[persona_slug] = PersonaProfile(
                    name=old_p.name,
                    embedding=blended,
                    prosody=new_prosody,
                    sample_count=old_p.sample_count + len(sample_list),
                    exemplar_embeddings=exemplars,
                )
            else:
                actor.personas[persona_slug] = PersonaProfile(
                    name=persona_slug.replace("-", " ").title(),
                    embedding=new_embedding,
                    prosody=new_prosody,
                    sample_count=len(sample_list),
                    exemplar_embeddings=[new_embedding],
                )

        save_actor_profile(actor, profiles_dir)
        updated[actor_slug] = actor
        label = f"{actor.name}/{persona_slug}" if persona_slug else actor.name
        logger.info("Retrained: %s (%d segments)", label, len(sample_list))

    return updated


# ---------------------------------------------------------------------------
# v1 functions preserved for backwards compatibility
# ---------------------------------------------------------------------------


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
