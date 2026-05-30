import base64

import numpy as np
import pytest

from player_view.models.voice_profile import VoiceProfile, ProfileStore


class TestVoiceProfile:
    def test_roundtrip_serialization(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Delmar Fisk', player='Nick', embedding=emb)
        d = profile.to_dict()
        restored = VoiceProfile.from_dict(d)
        assert restored.character == 'Delmar Fisk'
        assert restored.player == 'Nick'
        np.testing.assert_array_almost_equal(restored.embedding, emb)
        assert restored.sample_count == 1

    def test_embedding_shape_preserved(self):
        emb = np.random.randn(256).astype(np.float64)
        profile = VoiceProfile(character='Test', player='Test', embedding=emb)
        restored = VoiceProfile.from_dict(profile.to_dict())
        assert restored.embedding.shape == emb.shape
        assert restored.embedding.dtype == emb.dtype


class TestProfileStore:
    def test_save_and_load(self, profile_store):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Perrin', player='Player1', embedding=emb)
        profile_store.save(profile)

        loaded = profile_store.load('Perrin')
        assert loaded is not None
        assert loaded.character == 'Perrin'
        np.testing.assert_array_almost_equal(loaded.embedding, emb)

    def test_load_nonexistent(self, profile_store):
        assert profile_store.load('Nobody') is None

    def test_load_all(self, profile_store):
        for name in ['Alpha', 'Beta', 'Gamma']:
            emb = np.random.randn(192).astype(np.float32)
            profile_store.save(VoiceProfile(character=name, player='test', embedding=emb))
        all_profiles = profile_store.load_all()
        assert len(all_profiles) == 3
        names = {p.character for p in all_profiles}
        assert names == {'Alpha', 'Beta', 'Gamma'}

    def test_delete(self, profile_store):
        emb = np.random.randn(192).astype(np.float32)
        profile_store.save(VoiceProfile(character='ToDelete', player='test', embedding=emb))
        assert profile_store.delete('ToDelete') is True
        assert profile_store.load('ToDelete') is None
        assert profile_store.delete('ToDelete') is False

    def test_update_embedding(self, profile_store):
        emb1 = np.ones(192, dtype=np.float32)
        profile_store.save(VoiceProfile(character='Updater', player='test', embedding=emb1))

        emb2 = np.ones(192, dtype=np.float32) * 3.0
        profile_store.update_embedding('Updater', emb2)

        loaded = profile_store.load('Updater')
        assert loaded.sample_count == 2
        expected = (emb1 * 1 + emb2) / 2
        np.testing.assert_array_almost_equal(loaded.embedding, expected)

    def test_update_nonexistent_raises(self, profile_store):
        with pytest.raises(ValueError):
            profile_store.update_embedding('Ghost', np.zeros(192))


class TestSpatialFingerprint:
    def test_fingerprint_none_by_default(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Test', player='Test', embedding=emb)
        assert profile.spatial_fingerprint is None
        assert profile.spatial_m2 is None
        assert profile.spatial_sample_count == 0

    def test_fingerprint_serialization_roundtrip(self):
        emb = np.random.randn(192).astype(np.float32)
        fp = np.array([0.65, 0.18, 0.17], dtype=np.float32)
        m2 = np.array([0.01, 0.005, 0.004], dtype=np.float32)
        profile = VoiceProfile(
            character='Test', player='Test', embedding=emb,
            spatial_fingerprint=fp, spatial_m2=m2, spatial_sample_count=10,
        )
        d = profile.to_dict()
        restored = VoiceProfile.from_dict(d)
        np.testing.assert_array_almost_equal(restored.spatial_fingerprint, fp)
        np.testing.assert_array_almost_equal(restored.spatial_m2, m2)
        assert restored.spatial_sample_count == 10

    def test_no_spatial_fields_backward_compat(self):
        emb = np.random.randn(192).astype(np.float32)
        d = {
            'character': 'Old', 'player': 'Old',
            'embedding': base64.b64encode(emb.tobytes()).decode(),
            'embedding_shape': [192], 'embedding_dtype': 'float32',
        }
        restored = VoiceProfile.from_dict(d)
        assert restored.spatial_fingerprint is None
        assert restored.spatial_m2 is None
        assert restored.spatial_sample_count == 0

    def test_scalar_spatial_signature_migrated_to_fingerprint(self):
        emb = np.random.randn(192).astype(np.float32)
        d = {
            'character': 'Legacy', 'player': 'Legacy',
            'embedding': base64.b64encode(emb.tobytes()).decode(),
            'embedding_shape': [192], 'embedding_dtype': 'float32',
            'spatial_signature': 0.7, 'spatial_sample_count': 3,
        }
        restored = VoiceProfile.from_dict(d)
        assert restored.spatial_fingerprint is not None
        assert restored.spatial_fingerprint[0] == pytest.approx(0.7)
        assert restored.spatial_fingerprint.sum() == pytest.approx(1.0)
        assert restored.spatial_sample_count == 3

    def test_update_spatial_first_sample(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='New', player='Test', embedding=emb)
        fp = np.array([0.6, 0.2, 0.2])
        profile.update_spatial(fp)
        np.testing.assert_array_almost_equal(profile.spatial_fingerprint, fp)
        assert profile.spatial_sample_count == 1
        np.testing.assert_array_almost_equal(profile.spatial_m2, [0, 0, 0])

    def test_update_spatial_running_average(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Avg', player='Test', embedding=emb)
        profile.update_spatial(np.array([0.8, 0.1, 0.1]))
        profile.update_spatial(np.array([0.6, 0.2, 0.2]))
        assert profile.spatial_sample_count == 2
        np.testing.assert_array_almost_equal(
            profile.spatial_fingerprint, [0.7, 0.15, 0.15]
        )

    def test_update_spatial_variance_tracks_spread(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Var', player='Test', embedding=emb)
        for fp in [
            np.array([0.8, 0.1, 0.1]),
            np.array([0.8, 0.1, 0.1]),
            np.array([0.8, 0.1, 0.1]),
        ]:
            profile.update_spatial(fp)
        assert profile.spatial_consistency > 0.9

    def test_low_consistency_when_position_varies(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Var', player='Test', embedding=emb)
        for fp in [
            np.array([0.8, 0.1, 0.1]),
            np.array([0.1, 0.1, 0.8]),
            np.array([0.1, 0.8, 0.1]),
        ]:
            profile.update_spatial(fp)
        assert profile.spatial_consistency < 0.5

    def test_consistency_none_with_no_samples(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Empty', player='Test', embedding=emb)
        assert profile.spatial_consistency is None
