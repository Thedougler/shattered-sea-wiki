import numpy as np
import pytest

from player_view.services.diarization import DiarizationService


class TestSpatialAwareRanking:
    @pytest.fixture(scope='class')
    def diarization(self):
        svc = DiarizationService()
        svc.init()
        return svc

    def test_rank_without_spatial_matches_original(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('Alice', np.random.randn(192).astype(np.float32), None),
            ('Bob', target * 1.0, None),
            ('Charlie', np.random.randn(192).astype(np.float32), None),
        ]
        ranked = diarization.rank_against_with_spatial(target, 0.5, profiles)
        original = diarization.rank_against(
            target, [(n, e) for n, e, _ in profiles]
        )
        assert [r[0] for r in ranked] == [r[0] for r in original]

    def test_spatial_boost_breaks_tie(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        emb_norm = emb / np.linalg.norm(emb)
        profiles = [
            ('Near DM', emb_norm.copy(), 0.8),
            ('Far from DM', emb_norm.copy(), 0.2),
        ]
        ranked = diarization.rank_against_with_spatial(
            emb_norm, 0.75, profiles, spatial_weight=0.3,
        )
        assert ranked[0][0] == 'Near DM'

    def test_embedding_still_dominant(self, diarization):
        good_emb = np.random.randn(192).astype(np.float32)
        bad_emb = np.random.randn(192).astype(np.float32)
        profiles = [
            ('Bad embed, good spatial', bad_emb, 0.75),
            ('Good embed, bad spatial', good_emb * 1.0, 0.1),
        ]
        ranked = diarization.rank_against_with_spatial(
            good_emb, 0.75, profiles, spatial_weight=0.2,
        )
        assert ranked[0][0] == 'Good embed, bad spatial'

    def test_spatial_weight_zero_is_pure_embedding(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('A', np.random.randn(192).astype(np.float32), 0.9),
            ('B', target * 1.0, 0.1),
        ]
        ranked = diarization.rank_against_with_spatial(
            target, 0.9, profiles, spatial_weight=0.0,
        )
        assert ranked[0][0] == 'B'

    def test_spatial_ignored_when_profile_has_none(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('No spatial', target * 1.0, None),
            ('Has spatial', np.random.randn(192).astype(np.float32), 0.5),
        ]
        ranked = diarization.rank_against_with_spatial(
            target, 0.5, profiles, spatial_weight=0.3,
        )
        assert ranked[0][0] == 'No spatial'

    def test_returns_combined_score(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('A', target * 1.0, 0.5),
        ]
        ranked = diarization.rank_against_with_spatial(
            target, 0.5, profiles, spatial_weight=0.2,
        )
        name, score = ranked[0]
        assert 0.0 <= score <= 1.0
