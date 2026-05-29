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
from profiles import ProfileStore, VoiceProfile

DEFAULT_SCRIPT_NAME = "default-script.md"


@dataclass(frozen=True)
class EnrollmentResult:
    profile: VoiceProfile
    similarity_to_existing: dict[str, float]


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
) -> EnrollmentResult:
    embedding = vecmath.normalize(embedder.embed(audio, sample_rate))
    profile = VoiceProfile(
        name=name,
        player=player,
        embedding=embedding,
        sample_rate=sample_rate,
        model_id=model_id,
        seconds=len(audio) / sample_rate if sample_rate else 0.0,
        created_utc=now_utc,
    )
    similarity = {
        other.name: vecmath.cosine_similarity(embedding, other.embedding)
        for other in existing
    }
    return EnrollmentResult(profile=profile, similarity_to_existing=similarity)


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
) -> str:
    """Build and persist a profile; returns the written path."""
    store = ProfileStore(profiles_dir)
    result = build_profile(
        name=name, player=player, audio=audio, sample_rate=sample_rate,
        embedder=embedder, existing=store.load_all(), model_id=model_id, now_utc=now_utc,
    )
    return store.save(result.profile)
