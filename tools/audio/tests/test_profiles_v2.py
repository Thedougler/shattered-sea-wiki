"""Tests for v2 actor/persona voice profiles — data model, save/load, identification."""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from shattered_audio.profiles import (
    ActorProfile,
    PersonaProfile,
    ProsodyStats,
    SpeakerMatch,
    VoiceProfile,
    _cosine_similarity,
    _prosody_distance,
    _slug,
    build_persona_lookup,
    identify_speaker_v2,
    load_actor_profiles,
    save_actor_profile,
    save_profile,
)


def _random_embedding(seed: int = 0) -> np.ndarray:
    rng = np.random.RandomState(seed)
    v = rng.randn(256).astype(np.float32)
    return v / np.linalg.norm(v)


def _make_prosody(**overrides) -> ProsodyStats:
    defaults = dict(
        pitch_mean=150.0,
        pitch_std=30.0,
        pitch_range=100.0,
        energy_mean=0.05,
        speaking_rate=4.0,
    )
    defaults.update(overrides)
    return ProsodyStats(**defaults)


# ---------------------------------------------------------------------------
# Data model basics
# ---------------------------------------------------------------------------


class TestSlug:
    def test_simple(self):
        assert _slug("Nick") == "nick"

    def test_spaces(self):
        assert _slug("Jean Claude") == "jean-claude"


class TestCosine:
    def test_identical(self):
        v = _random_embedding(1)
        assert _cosine_similarity(v, v) == pytest.approx(1.0, abs=1e-5)

    def test_orthogonal(self):
        a = np.zeros(256, dtype=np.float32)
        b = np.zeros(256, dtype=np.float32)
        a[0] = 1.0
        b[1] = 1.0
        assert _cosine_similarity(a, b) == pytest.approx(0.0, abs=1e-5)

    def test_zero_vector(self):
        v = _random_embedding(1)
        z = np.zeros(256, dtype=np.float32)
        assert _cosine_similarity(v, z) == 0.0


class TestProsodyDistance:
    def test_identical(self):
        p = _make_prosody()
        assert _prosody_distance(p, p) == pytest.approx(0.0, abs=1e-5)

    def test_different(self):
        a = _make_prosody(pitch_mean=100.0)
        b = _make_prosody(pitch_mean=200.0)
        d = _prosody_distance(a, b)
        assert 0.0 < d < 1.0


# ---------------------------------------------------------------------------
# Save / load round-trip
# ---------------------------------------------------------------------------


class TestSaveLoadActorProfile:
    def test_round_trip_actor_only(self, tmp_path: Path):
        emb = _random_embedding(42)
        actor = ActorProfile(
            name="Nick",
            embedding=emb,
            prosody=_make_prosody(),
            sample_count=3,
            associated_mics=["mic_0"],
            is_dm=True,
        )
        save_actor_profile(actor, tmp_path)
        loaded = load_actor_profiles(tmp_path)

        assert "nick" in loaded
        a = loaded["nick"]
        assert a.name == "Nick"
        assert a.sample_count == 3
        assert a.is_dm is True
        assert a.associated_mics == ["mic_0"]
        assert np.allclose(a.embedding, emb, atol=1e-5)
        assert a.prosody is not None
        assert a.prosody.pitch_mean == pytest.approx(150.0)
        assert len(a.personas) == 0

    def test_round_trip_with_personas(self, tmp_path: Path):
        thunk_emb = _random_embedding(10)
        grigori_emb = _random_embedding(20)
        actor = ActorProfile(
            name="Nick",
            embedding=_random_embedding(1),
            prosody=_make_prosody(),
            is_dm=True,
            personas={
                "thunk": PersonaProfile(
                    name="Thunk",
                    embedding=thunk_emb,
                    prosody=_make_prosody(pitch_mean=80.0, speaking_rate=2.0),
                    sample_count=2,
                    exemplar_embeddings=[_random_embedding(11), _random_embedding(12)],
                ),
                "grigori": PersonaProfile(
                    name="Grigori",
                    embedding=grigori_emb,
                    prosody=_make_prosody(pitch_mean=200.0, speaking_rate=6.0),
                    sample_count=1,
                ),
            },
        )
        save_actor_profile(actor, tmp_path)
        loaded = load_actor_profiles(tmp_path)

        a = loaded["nick"]
        assert len(a.personas) == 2
        assert "thunk" in a.personas
        assert "grigori" in a.personas

        t = a.personas["thunk"]
        assert t.name == "Thunk"
        assert t.sample_count == 2
        assert t.prosody.pitch_mean == pytest.approx(80.0)
        assert t.exemplar_embeddings is not None
        assert len(t.exemplar_embeddings) == 2

        g = a.personas["grigori"]
        assert g.name == "Grigori"
        assert g.exemplar_embeddings is None

    def test_legacy_flat_profiles_loaded(self, tmp_path: Path):
        """Old v1 flat profiles should load as actors with no personas."""
        emb = _random_embedding(99)
        profile = VoiceProfile(name="Chad", embedding=emb, sample_count=2)
        save_profile(profile, tmp_path)

        actors = load_actor_profiles(tmp_path)
        assert "chad" in actors
        a = actors["chad"]
        assert a.name == "Chad"
        assert a.sample_count == 2
        assert len(a.personas) == 0

    def test_mixed_v1_v2(self, tmp_path: Path):
        """v2 actor dirs and v1 flat files coexist."""
        actor = ActorProfile(name="Nick", embedding=_random_embedding(1), is_dm=True)
        save_actor_profile(actor, tmp_path)

        flat = VoiceProfile(name="Chad", embedding=_random_embedding(2))
        save_profile(flat, tmp_path)

        actors = load_actor_profiles(tmp_path)
        assert "nick" in actors
        assert "chad" in actors
        assert actors["nick"].is_dm is True
        assert len(actors["chad"].personas) == 0


# ---------------------------------------------------------------------------
# Persona lookup
# ---------------------------------------------------------------------------


class TestPersonaLookup:
    def test_builds_lookup(self):
        actors = {
            "nick": ActorProfile(
                name="Nick",
                embedding=_random_embedding(1),
                personas={
                    "thunk": PersonaProfile(name="Thunk", embedding=_random_embedding(10)),
                    "grigori": PersonaProfile(name="Grigori", embedding=_random_embedding(20)),
                },
            ),
            "alex": ActorProfile(
                name="Alex",
                embedding=_random_embedding(2),
                personas={
                    "delmar": PersonaProfile(name="Delmar", embedding=_random_embedding(30)),
                },
            ),
        }
        lookup = build_persona_lookup(actors)
        assert lookup == {"thunk": "nick", "grigori": "nick", "delmar": "alex"}


# ---------------------------------------------------------------------------
# Identification
# ---------------------------------------------------------------------------


class TestIdentifySpeakerV2:
    @patch("shattered_audio.profiles.extract_embedding")
    def test_no_actors_returns_none(self, mock_embed):
        audio = np.zeros(16000, dtype=np.float32)
        assert identify_speaker_v2(audio, {}) is None

    @patch("shattered_audio.profiles.extract_embedding")
    def test_actor_only_match(self, mock_embed):
        """When actor has no personas, returns actor name."""
        emb = _random_embedding(1)
        mock_embed.return_value = emb

        actors = {
            "nick": ActorProfile(name="Nick", embedding=emb, sample_count=1),
        }
        audio = np.zeros(16000, dtype=np.float32)
        result = identify_speaker_v2(audio, actors, actor_threshold=0.5, use_prosody=False)

        assert result is not None
        assert result.name == "Nick"
        assert result.actor == "Nick"
        assert result.persona is None

    @patch("shattered_audio.profiles.extract_embedding")
    def test_below_threshold_returns_none(self, mock_embed):
        mock_embed.return_value = _random_embedding(1)
        actors = {
            "nick": ActorProfile(name="Nick", embedding=_random_embedding(99)),
        }
        audio = np.zeros(16000, dtype=np.float32)
        result = identify_speaker_v2(audio, actors, actor_threshold=0.99, use_prosody=False)
        assert result is None

    @patch("shattered_audio.profiles.extract_prosody")
    @patch("shattered_audio.profiles.extract_embedding")
    def test_persona_match_with_prosody(self, mock_embed, mock_prosody):
        """When persona embedding + prosody clearly different from actor base, returns persona."""
        actor_emb = _random_embedding(1)
        # Thunk embedding is distinct from actor base
        thunk_emb = _random_embedding(50)
        # Utterance is close to thunk
        mock_embed.return_value = thunk_emb
        mock_prosody.return_value = _make_prosody(pitch_mean=80.0, speaking_rate=2.0)

        actors = {
            "nick": ActorProfile(
                name="Nick",
                embedding=actor_emb,
                prosody=_make_prosody(pitch_mean=150.0, speaking_rate=4.0),
                personas={
                    "thunk": PersonaProfile(
                        name="Thunk",
                        embedding=thunk_emb,
                        prosody=_make_prosody(pitch_mean=80.0, speaking_rate=2.0),
                        exemplar_embeddings=[thunk_emb],
                    ),
                },
            ),
        }
        audio = np.zeros(16000, dtype=np.float32)
        result = identify_speaker_v2(
            audio,
            actors,
            actor_threshold=-1.0,
            persona_threshold=0.3,
            persona_margin=0.01,
            prosody_weight=0.3,
            use_prosody=True,
        )

        assert result is not None
        assert result.name == "Thunk"
        assert result.actor == "Nick"
        assert result.persona == "Thunk"

    @patch("shattered_audio.profiles.extract_embedding")
    def test_persona_fallback_to_actor(self, mock_embed):
        """When persona can't be distinguished, falls back to actor name."""
        emb = _random_embedding(1)
        mock_embed.return_value = emb

        actors = {
            "nick": ActorProfile(
                name="Nick",
                embedding=emb,
                personas={
                    "thunk": PersonaProfile(
                        name="Thunk",
                        embedding=emb,
                        exemplar_embeddings=[emb],
                    ),
                },
            ),
        }
        audio = np.zeros(16000, dtype=np.float32)
        result = identify_speaker_v2(
            audio,
            actors,
            actor_threshold=0.5,
            persona_threshold=0.6,
            persona_margin=0.05,
            use_prosody=False,
        )

        assert result is not None
        assert result.name == "Nick"
        assert result.actor == "Nick"
        assert result.persona is None

    @patch("shattered_audio.profiles.extract_embedding")
    def test_channel_prior_boost(self, mock_embed):
        """Channel priors should boost the correct actor."""
        nick_emb = _random_embedding(1)
        alex_emb = _random_embedding(2)
        # Utterance embedding is equidistant from both
        mid = (nick_emb + alex_emb) / 2
        mid = mid / np.linalg.norm(mid)
        mock_embed.return_value = mid

        actors = {
            "nick": ActorProfile(name="Nick", embedding=nick_emb),
            "alex": ActorProfile(name="Alex", embedding=alex_emb),
        }
        audio = np.zeros(16000, dtype=np.float32)

        result = identify_speaker_v2(
            audio,
            actors,
            source_mic="mic_0",
            channel_priors={"mic_0": "Nick"},
            channel_boost=0.15,
            actor_threshold=0.0,
            use_prosody=False,
        )

        assert result is not None
        assert result.name == "Nick"

    @patch("shattered_audio.profiles.extract_embedding")
    def test_speaker_match_tier(self, mock_embed):
        emb = _random_embedding(1)
        mock_embed.return_value = emb

        actors = {"nick": ActorProfile(name="Nick", embedding=emb)}
        audio = np.zeros(16000, dtype=np.float32)
        result = identify_speaker_v2(audio, actors, actor_threshold=0.5, use_prosody=False)

        assert result is not None
        assert result.tier in ("high", "medium", "low")
        assert result.confidence >= 0.5


# ---------------------------------------------------------------------------
# SpeakerMatch backwards compat
# ---------------------------------------------------------------------------


class TestSpeakerMatchCompat:
    def test_v1_fields_still_work(self):
        m = SpeakerMatch(name="Nick", confidence=0.85)
        assert m.name == "Nick"
        assert m.confidence == 0.85
        assert m.actor is None
        assert m.persona is None
        assert m.tier == "low"

    def test_v2_fields(self):
        m = SpeakerMatch(name="Thunk", confidence=0.72, actor="Nick", persona="Thunk", tier="high")
        assert m.actor == "Nick"
        assert m.persona == "Thunk"
