import time
import numpy as np
import pytest

from player_view.services.audio import AudioService
from player_view.services.asr import ASRService
from player_view.services.diarization import DiarizationService


class TestAudioService:
    def test_not_recording_initially(self):
        svc = AudioService()
        assert not svc.recording

    def test_record_and_stop(self):
        svc = AudioService(chunk_duration=0.5)
        chunks = []
        svc.start(on_chunk=lambda c: chunks.append(c))
        assert svc.recording
        time.sleep(1.5)
        audio = svc.stop()
        assert not svc.recording
        assert len(audio) > 0
        assert len(chunks) >= 2

    def test_stop_without_start_returns_empty(self):
        svc = AudioService()
        audio = svc.stop()
        assert len(audio) == 0


class TestASRService:
    @pytest.fixture(scope='class')
    def asr(self):
        svc = ASRService()
        svc.init()
        return svc

    def test_model_loaded(self, asr):
        assert asr.model is not None
        assert asr.sample_rate == 16000

    def test_streaming_with_silence(self, asr):
        silence = np.zeros(16000, dtype=np.float32)
        results = []
        asr.start_streaming(on_result=lambda r: results.append(r))
        asr.feed_audio(silence)
        asr.feed_audio(silence)
        final = asr.stop_streaming()
        assert final is not None

    def test_streaming_with_speech(self, asr):
        svc = AudioService(chunk_duration=0.5)
        chunks = []
        svc.start(on_chunk=lambda c: chunks.append(c))
        time.sleep(3)
        audio = svc.stop()

        results = []
        asr.start_streaming(on_result=lambda r: results.append(r))
        chunk_size = 8000
        for i in range(0, len(audio), chunk_size):
            asr.feed_audio(audio[i:i + chunk_size])
        final = asr.stop_streaming()
        assert final is not None


class TestDiarizationService:
    @pytest.fixture(scope='class')
    def diarization(self):
        svc = DiarizationService()
        svc.init()
        return svc

    def test_model_loaded(self, diarization):
        assert diarization._embedding_model is not None

    def test_extract_embedding(self, diarization):
        audio = np.random.randn(16000 * 3).astype(np.float32)
        embedding = diarization.extract_embedding(audio)
        assert embedding.ndim == 1
        assert len(embedding) > 0

    def test_compare_same_embedding(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        sim = diarization.compare(emb, emb)
        assert sim > 0.99

    def test_compare_different_embeddings(self, diarization):
        emb_a = np.random.randn(192).astype(np.float32)
        emb_b = np.random.randn(192).astype(np.float32)
        sim = diarization.compare(emb_a, emb_b)
        assert -1.0 <= sim <= 1.0

    def test_rank_against(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('Alice', np.random.randn(192).astype(np.float32)),
            ('Bob', target * 1.0),
            ('Charlie', np.random.randn(192).astype(np.float32)),
        ]
        ranked = diarization.rank_against(target, profiles)
        assert ranked[0][0] == 'Bob'
        assert ranked[0][1] > 0.99
