#!/usr/bin/env python3
"""Testable core of the voice profiler — no NiceGUI, no microphone.

Given captured audio for one character voice, build a normalized speaker profile
with metadata, report how close it is to already-enrolled voices (so the UI can
warn "this sounds like Nona"), and save it. The NiceGUI teleprompter shell in
``voice_profiler.py`` only handles presentation + capture and then calls
``enroll``.

A long, phonetically-rich read (the bundled teleprompter targets ~60–90s) yields
a stronger, more separable embedding — which is what makes the noisy, multi-voice
sessions tractable downstream.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import vecmath
from boundaries import Embedder
from profile_enhance import aggregate_embedding
from profile_harvest import harvest_embeddings
from profiles import ProfileStore, VoiceProfile
from session_paths import finalized_sessions

DEFAULT_SCRIPT_NAME = "default-script.md"

# Enhancement defaults. The teleprompter anchor is weighted heavily so the
# deliberate clean read stays the backbone; harvested spans only refine it.
DEFAULT_ANCHOR_WEIGHT = 3.0
DEFAULT_REJECT_BELOW = 0.45
DEFAULT_MIN_SPAN_SECONDS = 1.5
DEFAULT_MAX_SPAN_SECONDS = 30.0


@dataclass(frozen=True)
class EnrollmentResult:
    profile: VoiceProfile
    similarity_to_existing: dict[str, float]
    rejected: int = 0


def load_script(script_file: str | None, assets_dir: str) -> str:
    """Return teleprompter text: an explicit ``--script-file`` else the bundled default."""
    if script_file is not None:
        if not os.path.isfile(script_file):
            raise FileNotFoundError(f"teleprompter script not found: {script_file}")
        path = script_file
    else:
        path = os.path.join(assets_dir, DEFAULT_SCRIPT_NAME)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def build_profile(
    *,
    name: str,
    player: str,
    audio: list[float],
    sample_rate: int,
    embedder: Embedder,
    existing: list[VoiceProfile],
    model_id: str,
    now_utc: str,
    harvested: list[list[float]] | None = None,
    harvested_sessions: list[int] | None = None,
    reject_below: float = DEFAULT_REJECT_BELOW,
    anchor_weight: float = DEFAULT_ANCHOR_WEIGHT,
) -> EnrollmentResult:
    """Build a profile from the teleprompter read, optionally enhanced by harvest.

    The clean teleprompter read is the **anchor**. Any ``harvested`` embeddings
    from corrected sessions are folded in via ``aggregate_embedding`` — outliers
    (mis-attributions that slipped through) are rejected against the anchor, so
    correction can only sharpen, never poison, a profile.
    """
    anchor = embedder.embed(audio, sample_rate)
    agg = aggregate_embedding(
        anchor, harvested or [], reject_below=reject_below, anchor_weight=anchor_weight,
    )
    profile = VoiceProfile(
        name=name,
        player=player,
        embedding=agg.embedding,
        sample_rate=sample_rate,
        model_id=model_id,
        seconds=len(audio) / sample_rate if sample_rate else 0.0,
        created_utc=now_utc,
        enhanced_spans=agg.used,
        enhanced_sessions=list(harvested_sessions or []) if agg.used else [],
    )
    similarity = {
        other.name: vecmath.cosine_similarity(agg.embedding, other.embedding)
        for other in existing
    }
    return EnrollmentResult(
        profile=profile, similarity_to_existing=similarity, rejected=agg.rejected,
    )


def enroll(
    *,
    name: str,
    player: str,
    audio: list[float],
    sample_rate: int,
    embedder: Embedder,
    profiles_dir: str,
    model_id: str,
    now_utc: str,
    sessions_dir: str | None = None,
) -> EnrollmentResult:
    """Build and persist a profile; returns the EnrollmentResult.

    If ``sessions_dir`` is given, corrected finalized transcripts there (with
    surviving live audio) are harvested for this character and folded into the
    profile — so re-saving a profile after the session is corrected automatically
    picks up the corrections.
    """
    store = ProfileStore(profiles_dir)
    harvested: list[list[float]] = []
    sessions: list[int] = []
    if sessions_dir is not None:
        pairs = finalized_sessions(sessions_dir)
        if pairs:
            harvested = harvest_embeddings(
                transcript_paths=[p[1] for p in pairs],
                audio_dirs=[p[2] for p in pairs],
                character=name,
                embedder=embedder,
                min_seconds=DEFAULT_MIN_SPAN_SECONDS,
                max_span_s=DEFAULT_MAX_SPAN_SECONDS,
            )
            sessions = [p[0] for p in pairs]
    result = build_profile(
        name=name, player=player, audio=audio, sample_rate=sample_rate,
        embedder=embedder, existing=store.load_all(), model_id=model_id, now_utc=now_utc,
        harvested=harvested, harvested_sessions=sessions,
    )
    store.save(result.profile)
    return result
