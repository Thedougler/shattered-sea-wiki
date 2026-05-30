import numpy as np
import pytest

from player_view.services.audio import AudioService


class TestMultichannelBackwardCompat:
    def test_default_is_mono(self):
        svc = AudioService()
        assert svc.channels == 1
        assert svc.device is None

    def test_mono_callback_stores_1d(self):
        svc = AudioService()
        indata = np.random.randn(512, 1).astype(np.float32)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        svc._callback(indata, 512, None, None)
        assert svc._buffer[0].ndim == 1

    def test_mono_on_chunk_shape(self):
        svc = AudioService(chunk_duration=0.1)
        chunks = []
        svc._on_chunk = lambda c: chunks.append(c)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        samples = int(svc.SAMPLE_RATE * 0.1)
        indata = np.random.randn(samples, 1).astype(np.float32)
        svc._callback(indata, samples, None, None)
        assert len(chunks) == 1
        assert chunks[0].ndim == 1


class TestMultichannelConfig:
    def test_accepts_device_and_channels(self):
        svc = AudioService(device=4, channels=3)
        assert svc.device == 4
        assert svc.channels == 3

    def test_multichannel_callback_stores_2d(self):
        svc = AudioService(device=4, channels=3)
        indata = np.random.randn(512, 3).astype(np.float32)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        svc._callback(indata, 512, None, None)
        assert svc._buffer[0].ndim == 2
        assert svc._buffer[0].shape == (512, 3)

    def test_multichannel_get_buffer_copy_shape(self):
        svc = AudioService(device=4, channels=3)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        for _ in range(3):
            indata = np.random.randn(512, 3).astype(np.float32)
            svc._callback(indata, 512, None, None)
        buf = svc.get_buffer_copy()
        assert buf.shape == (512 * 3, 3)

    def test_multichannel_on_chunk_shape(self):
        svc = AudioService(device=4, channels=3, chunk_duration=0.1)
        chunks = []
        svc._on_chunk = lambda c: chunks.append(c)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        samples = int(svc.SAMPLE_RATE * 0.1)
        indata = np.random.randn(samples, 3).astype(np.float32)
        svc._callback(indata, samples, None, None)
        assert len(chunks) == 1
        assert chunks[0].ndim == 2
        assert chunks[0].shape[1] == 3


class TestChannelRMS:
    def test_channel_rms_levels_per_channel(self):
        svc = AudioService(device=4, channels=3)
        indata = np.zeros((512, 3), dtype=np.float32)
        indata[:, 0] = 0.5
        indata[:, 1] = 0.01
        indata[:, 2] = 0.01
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        svc._callback(indata, 512, None, None)
        levels = svc.channel_rms_levels
        assert len(levels) == 3
        assert levels[0] > levels[1]
        assert levels[0] > levels[2]

    def test_rms_level_returns_max_across_channels(self):
        svc = AudioService(device=4, channels=3)
        indata = np.zeros((512, 3), dtype=np.float32)
        indata[:, 0] = 0.5
        indata[:, 1] = 0.01
        indata[:, 2] = 0.01
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        svc._callback(indata, 512, None, None)
        assert svc.rms_level == max(svc.channel_rms_levels)

    def test_mono_channel_rms_levels_single_element(self):
        svc = AudioService()
        indata = np.full((512, 1), 0.3, dtype=np.float32)
        svc._buffer = []
        svc._chunk_acc = []
        svc._chunk_acc_samples = 0
        svc._callback(indata, 512, None, None)
        levels = svc.channel_rms_levels
        assert len(levels) == 1
