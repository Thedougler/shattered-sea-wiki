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
            ('Alice', np.random.randn(192).astype(np.float32), None, None, 0),
            ('Bob', target * 1.0, None, None, 0),
            ('Charlie', np.random.randn(192).astype(np.float32), None, None, 0),
        ]
        fp = np.array([0.5, 0.25, 0.25])
        ranked = diarization.rank_against_with_spatial(target, fp, profiles)
        original = diarization.rank_against(
            target, [(n, e) for n, e, *_ in profiles]
        )
        assert [r[0] for r in ranked] == [r[0] for r in original]

    def test_spatial_boost_breaks_tie(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        emb_norm = emb / np.linalg.norm(emb)
        near_dm = np.array([0.7, 0.15, 0.15])
        far_dm = np.array([0.1, 0.45, 0.45])
        profiles = [
            ('Near DM', emb_norm.copy(), near_dm, None, 10),
            ('Far from DM', emb_norm.copy(), far_dm, None, 10),
        ]
        current = np.array([0.72, 0.14, 0.14])
        ranked = diarization.rank_against_with_spatial(
            emb_norm, current, profiles, base_weight=0.3,
        )
        assert ranked[0][0] == 'Near DM'

    def test_embedding_still_dominant(self, diarization):
        good_emb = np.random.randn(192).astype(np.float32)
        bad_emb = np.random.randn(192).astype(np.float32)
        current = np.array([0.7, 0.15, 0.15])
        profiles = [
            ('Bad embed, good spatial', bad_emb, current.copy(), None, 10),
            ('Good embed, bad spatial', good_emb * 1.0, np.array([0.1, 0.45, 0.45]), None, 10),
        ]
        ranked = diarization.rank_against_with_spatial(
            good_emb, current, profiles, base_weight=0.3,
        )
        assert ranked[0][0] == 'Good embed, bad spatial'

    def test_spatial_ignored_when_profile_has_none(self, diarization):
        target = np.random.randn(192).astype(np.float32)
        profiles = [
            ('No spatial', target * 1.0, None, None, 0),
            ('Has spatial', np.random.randn(192).astype(np.float32),
             np.array([0.5, 0.25, 0.25]), None, 10),
        ]
        ranked = diarization.rank_against_with_spatial(
            target, np.array([0.5, 0.25, 0.25]), profiles, base_weight=0.3,
        )
        assert ranked[0][0] == 'No spatial'


class TestAdaptiveWeight:
    @pytest.fixture(scope='class')
    def diarization(self):
        svc = DiarizationService()
        svc.init()
        return svc

    def test_few_samples_low_weight(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        emb_norm = emb / np.linalg.norm(emb)
        fp = np.array([0.7, 0.15, 0.15])
        profiles_few = [
            ('A', emb_norm.copy(), fp.copy(), None, 1),
            ('B', emb_norm.copy(), np.array([0.1, 0.45, 0.45]), None, 1),
        ]
        profiles_many = [
            ('A', emb_norm.copy(), fp.copy(), None, 20),
            ('B', emb_norm.copy(), np.array([0.1, 0.45, 0.45]), None, 20),
        ]
        current = np.array([0.72, 0.14, 0.14])
        r_few = diarization.rank_against_with_spatial(emb_norm, current, profiles_few, base_weight=0.3)
        r_many = diarization.rank_against_with_spatial(emb_norm, current, profiles_many, base_weight=0.3)
        score_diff_few = abs(r_few[0][1] - r_few[1][1])
        score_diff_many = abs(r_many[0][1] - r_many[1][1])
        assert score_diff_many > score_diff_few

    def test_high_consistency_increases_spatial_influence(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        emb_norm = emb / np.linalg.norm(emb)
        fp = np.array([0.7, 0.15, 0.15])
        low_var = np.array([0.001, 0.001, 0.001])
        high_var = np.array([0.1, 0.1, 0.1])
        profiles_consistent = [
            ('A', emb_norm.copy(), fp.copy(), low_var, 20),
            ('B', emb_norm.copy(), np.array([0.1, 0.45, 0.45]), low_var, 20),
        ]
        profiles_noisy = [
            ('A', emb_norm.copy(), fp.copy(), high_var, 20),
            ('B', emb_norm.copy(), np.array([0.1, 0.45, 0.45]), high_var, 20),
        ]
        current = np.array([0.72, 0.14, 0.14])
        r_consistent = diarization.rank_against_with_spatial(emb_norm, current, profiles_consistent, base_weight=0.3)
        r_noisy = diarization.rank_against_with_spatial(emb_norm, current, profiles_noisy, base_weight=0.3)
        diff_consistent = abs(r_consistent[0][1] - r_consistent[1][1])
        diff_noisy = abs(r_noisy[0][1] - r_noisy[1][1])
        assert diff_consistent > diff_noisy


class TestChannelReliability:
    @pytest.fixture(scope='class')
    def diarization(self):
        svc = DiarizationService()
        svc.init()
        return svc

    def test_channel_weights_applied(self, diarization):
        emb = np.random.randn(192).astype(np.float32)
        emb_norm = emb / np.linalg.norm(emb)
        profiles = [
            ('Left', emb_norm.copy(), np.array([0.3, 0.5, 0.2]), None, 10),
            ('Right', emb_norm.copy(), np.array([0.3, 0.2, 0.5]), None, 10),
        ]
        current = np.array([0.3, 0.5, 0.2])
        ranked = diarization.rank_against_with_spatial(
            emb_norm, current, profiles, base_weight=0.3,
            channel_weights=np.array([0.5, 1.0, 1.0]),
        )
        assert ranked[0][0] == 'Left'
