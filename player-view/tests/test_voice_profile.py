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


class TestSpatialSignature:
    def test_spatial_signature_none_by_default(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Test', player='Test', embedding=emb)
        assert profile.spatial_signature is None
        assert profile.spatial_sample_count == 0

    def test_spatial_signature_serialization(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(
            character='Test', player='Test', embedding=emb,
            spatial_signature=0.75, spatial_sample_count=5,
        )
        d = profile.to_dict()
        restored = VoiceProfile.from_dict(d)
        assert restored.spatial_signature == pytest.approx(0.75)
        assert restored.spatial_sample_count == 5

    def test_spatial_signature_backward_compat(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='Old', player='Old', embedding=emb)
        d = profile.to_dict()
        del d['spatial_signature']
        del d['spatial_sample_count']
        restored = VoiceProfile.from_dict(d)
        assert restored.spatial_signature is None
        assert restored.spatial_sample_count == 0

    def test_update_spatial_signature_averaging(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(
            character='Spatial', player='Test', embedding=emb,
            spatial_signature=0.8, spatial_sample_count=2,
        )
        profile.update_spatial(0.4)
        assert profile.spatial_sample_count == 3
        expected = (0.8 * 2 + 0.4) / 3
        assert profile.spatial_signature == pytest.approx(expected)

    def test_update_spatial_from_none(self):
        emb = np.random.randn(192).astype(np.float32)
        profile = VoiceProfile(character='New', player='Test', embedding=emb)
        profile.update_spatial(0.6)
        assert profile.spatial_signature == pytest.approx(0.6)
        assert profile.spatial_sample_count == 1
