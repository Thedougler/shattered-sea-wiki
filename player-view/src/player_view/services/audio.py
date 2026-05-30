import math
import threading

import numpy as np
import sounddevice as sd


class AudioService:
    SAMPLE_RATE = 16000

    def __init__(
        self,
        chunk_duration: float = 1.0,
        device: int | str | None = None,
        channels: int = 1,
    ):
        self.chunk_duration = chunk_duration
        self.chunk_size = int(self.SAMPLE_RATE * chunk_duration)
        self.device = device
        self.channels = channels
        self._stream: sd.InputStream | None = None
        self._buffer: list[np.ndarray] = []
        self._chunk_acc: list[np.ndarray] = []
        self._chunk_acc_samples: int = 0
        self._lock = threading.Lock()
        self._on_chunk = None
        self._rms_level: float = 0.0
        self._rms_levels: list[float] = [0.0] * channels

    @property
    def recording(self) -> bool:
        return self._stream is not None and self._stream.active

    @property
    def rms_level(self) -> float:
        return self._rms_level

    @property
    def channel_rms_levels(self) -> list[float]:
        return list(self._rms_levels)

    def get_buffer_copy(self) -> np.ndarray:
        with self._lock:
            if self._buffer:
                return np.concatenate(self._buffer)
            if self.channels == 1:
                return np.zeros(0, dtype=np.float32)
            return np.zeros((0, self.channels), dtype=np.float32)

    def start(self, on_chunk=None):
        self._on_chunk = on_chunk
        self._rms_level = 0.0
        self._chunk_acc = []
        self._chunk_acc_samples = 0
        with self._lock:
            self._buffer = []
        self._rms_levels = [0.0] * self.channels
        self._stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.channels,
            dtype="float32",
            callback=self._callback,
            device=self.device,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._rms_level = 0.0
        self._rms_levels = [0.0] * self.channels
        self._chunk_acc = []
        self._chunk_acc_samples = 0
        with self._lock:
            if self._buffer:
                audio = np.concatenate(self._buffer)
            elif self.channels == 1:
                audio = np.zeros(0, dtype=np.float32)
            else:
                audio = np.zeros((0, self.channels), dtype=np.float32)
            self._buffer = []
        return audio

    def _callback(self, indata, frames, time_info, status):
        if self.channels == 1:
            chunk = indata[:, 0].copy()
        else:
            chunk = indata.copy()

        levels = []
        for ch in range(self.channels):
            col = indata[:, ch]
            rms = float(np.sqrt(np.mean(col**2)))
            db = 20 * math.log10(max(rms, 1e-10))
            levels.append(max(0.0, min(1.0, (db + 60) / 50)))
        self._rms_levels = levels
        self._rms_level = max(levels)

        with self._lock:
            self._buffer.append(chunk)

        self._chunk_acc.append(chunk)
        self._chunk_acc_samples += frames
        if self._chunk_acc_samples >= self.chunk_size:
            full_chunk = np.concatenate(self._chunk_acc)
            self._chunk_acc = []
            self._chunk_acc_samples = 0
            if self._on_chunk:
                self._on_chunk(full_chunk)
