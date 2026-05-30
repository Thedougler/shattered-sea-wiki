import numpy as np
import pytest

from player_view.services.spatial import SpatialAnalyzer


def _sine(freq, duration, sr=16000, amplitude=0.5):
    t = np.arange(int(sr * duration)) / sr
    return (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def _make_chunk(dm_signal, player_signal, channels=3):
    n = len(dm_signal)
    chunk = np.zeros((n, channels), dtype=np.float32)
    chunk[:, 0] = dm_signal
    chunk[:, 1] = player_signal
    if channels > 2:
        chunk[:, 2] = player_signal
    return chunk


class TestSilenceDetection:
    def test_silence_detected(self):
        analyzer = SpatialAnalyzer()
        chunk = np.zeros((1600, 3), dtype=np.float32)
        result = analyzer.analyze(chunk)
        assert result.is_speech is False

    def test_very_quiet_is_silence(self):
        analyzer = SpatialAnalyzer()
        chunk = np.full((1600, 3), 1e-6, dtype=np.float32)
        result = analyzer.analyze(chunk)
        assert result.is_speech is False


class TestDMRatio:
    def test_dm_louder_gives_high_ratio(self):
        analyzer = SpatialAnalyzer()
        dm = _sine(440, 0.1, amplitude=0.5)
        player = np.random.randn(len(dm)).astype(np.float32) * 0.01
        chunk = _make_chunk(dm, player)
        result = analyzer.analyze(chunk)
        assert result.dm_ratio > 0.7
        assert result.is_speech is True

    def test_player_louder_gives_low_ratio(self):
        analyzer = SpatialAnalyzer()
        dm = np.random.randn(1600).astype(np.float32) * 0.01
        player = _sine(440, 0.1, amplitude=0.5)
        chunk = _make_chunk(dm, player)
        result = analyzer.analyze(chunk)
        assert result.dm_ratio < 0.3

    def test_balanced_gives_mid_ratio(self):
        analyzer = SpatialAnalyzer()
        signal = _sine(440, 0.1, amplitude=0.3)
        chunk = _make_chunk(signal, signal)
        result = analyzer.analyze(chunk)
        assert 0.4 < result.dm_ratio < 0.6

    def test_dm_energy_and_player_energy_populated(self):
        analyzer = SpatialAnalyzer()
        dm = _sine(440, 0.1, amplitude=0.5)
        player = _sine(440, 0.1, amplitude=0.1)
        chunk = _make_chunk(dm, player)
        result = analyzer.analyze(chunk)
        assert result.dm_energy > result.player_energy


class TestBestChannel:
    def test_best_channel_is_dm_when_dm_louder(self):
        analyzer = SpatialAnalyzer()
        dm = _sine(440, 0.1, amplitude=0.5)
        player = np.random.randn(len(dm)).astype(np.float32) * 0.01
        chunk = _make_chunk(dm, player)
        result = analyzer.analyze(chunk)
        np.testing.assert_array_equal(result.best_channel_audio, result.dm_channel_audio)

    def test_best_channel_is_player_when_player_louder(self):
        analyzer = SpatialAnalyzer()
        dm = np.random.randn(1600).astype(np.float32) * 0.01
        player = _sine(440, 0.1, amplitude=0.5)
        chunk = _make_chunk(dm, player)
        result = analyzer.analyze(chunk)
        np.testing.assert_array_equal(result.best_channel_audio, result.player_channel_audio)

    def test_player_channels_downmixed_to_mono(self):
        analyzer = SpatialAnalyzer()
        n = 1600
        chunk = np.zeros((n, 3), dtype=np.float32)
        chunk[:, 1] = 0.4
        chunk[:, 2] = 0.2
        result = analyzer.analyze(chunk)
        expected = (chunk[:, 1] + chunk[:, 2]) / 2.0
        np.testing.assert_array_almost_equal(result.player_channel_audio, expected)

    def test_dm_channel_is_mono(self):
        analyzer = SpatialAnalyzer()
        chunk = np.zeros((1600, 3), dtype=np.float32)
        chunk[:, 0] = 0.5
        result = analyzer.analyze(chunk)
        assert result.dm_channel_audio.ndim == 1
        np.testing.assert_array_almost_equal(result.dm_channel_audio, chunk[:, 0])


class TestConfiguration:
    def test_custom_channel_mapping(self):
        analyzer = SpatialAnalyzer(dm_channels=[2], player_channels=[0, 1])
        chunk = np.zeros((1600, 3), dtype=np.float32)
        chunk[:, 2] = 0.5  # "DM" is now channel 2
        chunk[:, 0] = 0.01
        chunk[:, 1] = 0.01
        result = analyzer.analyze(chunk)
        assert result.dm_ratio > 0.7

    def test_speech_threshold_configurable(self):
        analyzer_sensitive = SpatialAnalyzer(silence_db=-60.0)
        analyzer_strict = SpatialAnalyzer(silence_db=-20.0)
        chunk = np.full((1600, 3), 0.005, dtype=np.float32)
        assert analyzer_sensitive.analyze(chunk).is_speech is True
        assert analyzer_strict.analyze(chunk).is_speech is False


class TestEdgeCases:
    def test_single_sample_doesnt_crash(self):
        analyzer = SpatialAnalyzer()
        chunk = np.ones((1, 3), dtype=np.float32) * 0.3
        result = analyzer.analyze(chunk)
        assert isinstance(result.dm_ratio, float)
        assert not np.isnan(result.dm_ratio)
