import numpy as np
import pytest
from player_view.models.state import SessionState
from player_view.models.voice_profile import ProfileStore, VoiceProfile
from player_view.services.asr import ASRResult
from player_view.services.session_transcriber import SessionTranscriber
from player_view.services.spatial import SpatialAnalyzer


def _make_chunk(dm_amp, player_amp, samples=1600):
    chunk = np.zeros((samples, 3), dtype=np.float32)
    t = np.arange(samples) / 16000
    chunk[:, 0] = dm_amp * np.sin(2 * np.pi * 440 * t)
    chunk[:, 1] = player_amp * np.sin(2 * np.pi * 440 * t)
    chunk[:, 2] = player_amp * np.sin(2 * np.pi * 440 * t)
    return chunk


class FakeASR:
    def __init__(self, results: list[str]):
        self._results = list(results)
        self._call_count = 0
        self.latest_result = ASRResult()
        self._fed_chunks = []

    def start_streaming(self, on_result=None):
        self._call_count = 0
        self.latest_result = ASRResult()

    def feed_audio(self, chunk):
        self._fed_chunks.append(chunk)
        if self._call_count < len(self._results):
            text = " ".join(self._results[: self._call_count + 1])
            self.latest_result = ASRResult(
                text=text,
                finalized_text=text,
                draft_text="",
            )
        self._call_count += 1

    def stop_streaming(self):
        return self.latest_result


class FakeDiarization:
    def __init__(self, rankings: list[list[tuple[str, float]]]):
        self._rankings = list(rankings)
        self._call_count = 0
        self._embeddings_from = []

    def extract_embedding(self, audio):
        self._embeddings_from.append(audio)
        return np.random.randn(192).astype(np.float32)

    def rank_against_with_spatial(
        self, embedding, fingerprint, profiles, base_weight=0.2, **kwargs
    ):
        if self._call_count < len(self._rankings):
            result = self._rankings[self._call_count]
        else:
            result = self._rankings[-1]
        self._call_count += 1
        return result


@pytest.fixture
def profile_store(tmp_path):
    store = ProfileStore(tmp_path / "profiles")
    emb = np.random.randn(192).astype(np.float32)
    store.save(VoiceProfile(character="Perrin", player="P1", embedding=emb))
    store.save(VoiceProfile(character="Delmar", player="P2", embedding=emb))
    return store


class TestSilence:
    def test_silence_produces_no_messages(self, profile_store):
        state = SessionState()
        asr = FakeASR([])
        diar = FakeDiarization([])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        silent_chunk = np.zeros((1600, 3), dtype=np.float32)
        transcriber.process_chunk(silent_chunk)
        transcriber.process_chunk(silent_chunk)
        assert len(state.messages) == 0


class TestAttribution:
    def test_speech_gets_transcribed_and_attributed(self, profile_store):
        state = SessionState()
        asr = FakeASR(["hello", "there"])
        diar = FakeDiarization([[("Perrin", 0.85)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        chunk = _make_chunk(0.01, 0.5)
        transcriber.process_chunk(chunk)
        transcriber.flush()
        assert len(state.messages) == 1
        assert state.messages[0].speaker == "Perrin"
        assert "hello" in state.messages[0].text

    def test_best_channel_fed_to_asr(self, profile_store):
        state = SessionState()
        asr = FakeASR(["word"])
        diar = FakeDiarization([[("Perrin", 0.9)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        chunk = _make_chunk(0.01, 0.5)  # player louder
        transcriber.process_chunk(chunk)
        fed = asr._fed_chunks[0]
        assert fed.ndim == 1

    def test_best_channel_used_for_embedding(self, profile_store):
        state = SessionState()
        asr = FakeASR(["word"])
        diar = FakeDiarization([[("Delmar", 0.9)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        chunk = _make_chunk(0.5, 0.01)  # DM louder
        transcriber.process_chunk(chunk)
        emb_audio = diar._embeddings_from[0]
        assert emb_audio.ndim == 1


class TestTurnMerging:
    def test_consecutive_same_speaker_merged(self, profile_store):
        state = SessionState()
        asr = FakeASR(["word1", "word2", "word3"])
        diar = FakeDiarization([[("Delmar", 0.9)]] * 3)
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        for _ in range(3):
            transcriber.process_chunk(_make_chunk(0.5, 0.01))
        transcriber.flush()
        assert len(state.messages) == 1
        assert state.messages[0].speaker == "Delmar"

    def test_speaker_change_flushes_previous(self, profile_store):
        state = SessionState()
        asr = FakeASR(["hello", "world", "goodbye"])
        rankings = [
            [("Delmar", 0.9)],
            [("Delmar", 0.9)],
            [("Perrin", 0.85)],
        ]
        diar = FakeDiarization(rankings)
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        transcriber.process_chunk(_make_chunk(0.5, 0.01))
        transcriber.process_chunk(_make_chunk(0.5, 0.01))
        transcriber.process_chunk(_make_chunk(0.01, 0.5))
        transcriber.flush()
        assert len(state.messages) == 2
        assert state.messages[0].speaker == "Delmar"
        assert state.messages[1].speaker == "Perrin"


class TestSpatialIntegration:
    def test_uses_spatial_aware_ranking(self, profile_store):
        state = SessionState()
        asr = FakeASR(["word"])
        called_with = {}

        class TrackingDiarization(FakeDiarization):
            def rank_against_with_spatial(
                self, embedding, fingerprint, profiles, base_weight=0.2, **kwargs
            ):
                called_with["fingerprint"] = fingerprint
                called_with["base_weight"] = base_weight
                return super().rank_against_with_spatial(
                    embedding, fingerprint, profiles, base_weight
                )

        diar = TrackingDiarization([[("Perrin", 0.9)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        transcriber.process_chunk(_make_chunk(0.01, 0.5))
        assert "fingerprint" in called_with
        assert called_with["fingerprint"][0] < 0.3  # DM channel quiet

    def test_spatial_fingerprint_updated_on_identification(self, tmp_path):
        store = ProfileStore(tmp_path / "profiles")
        emb = np.random.randn(192).astype(np.float32)
        store.save(VoiceProfile(character="Perrin", player="P1", embedding=emb))
        state = SessionState()
        asr = FakeASR(["word"])
        diar = FakeDiarization([[("Perrin", 0.9)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=store,
            session_state=state,
        )
        transcriber.process_chunk(_make_chunk(0.01, 0.5))
        transcriber.flush()
        updated = store.load("Perrin")
        assert updated.spatial_fingerprint is not None
        assert len(updated.spatial_fingerprint) == 3
        assert updated.spatial_sample_count == 1


class TestSessionStatus:
    def test_chunk_count_updated(self, profile_store):
        state = SessionState()
        asr = FakeASR(["word"])
        diar = FakeDiarization([[("Perrin", 0.9)]])
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        transcriber.process_chunk(_make_chunk(0.01, 0.5))
        assert state.chunk_count == 1

    def test_speaker_count_updated(self, profile_store):
        state = SessionState()
        asr = FakeASR(["hello", "world"])
        rankings = [
            [("Delmar", 0.9)],
            [("Perrin", 0.85)],
        ]
        diar = FakeDiarization(rankings)
        spatial = SpatialAnalyzer()
        transcriber = SessionTranscriber(
            asr=asr,
            spatial=spatial,
            diarization=diar,
            profiles=profile_store,
            session_state=state,
        )
        transcriber.process_chunk(_make_chunk(0.5, 0.01))
        transcriber.process_chunk(_make_chunk(0.01, 0.5))
        assert state.speaker_count == 2
