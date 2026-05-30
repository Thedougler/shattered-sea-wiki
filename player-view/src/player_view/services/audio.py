import math
import threading

import numpy as np
import sounddevice as sd


class AudioService:
    SAMPLE_RATE = 16000
    CHANNELS = 1

    def __init__(self, chunk_duration: float = 1.0):
        self.chunk_duration = chunk_duration
        self.chunk_size = int(self.SAMPLE_RATE * chunk_duration)
        self._stream: sd.InputStream | None = None
        self._buffer: list[np.ndarray] = []
        self._chunk_acc: list[np.ndarray] = []
        self._chunk_acc_samples: int = 0
        self._lock = threading.Lock()
        self._on_chunk = None
        self._rms_level: float = 0.0

    @property
    def recording(self) -> bool:
        return self._stream is not None and self._stream.active

    @property
    def rms_level(self) -> float:
        return self._rms_level

    def get_buffer_copy(self) -> np.ndarray:
        with self._lock:
            if self._buffer:
                return np.concatenate(self._buffer)
            return np.zeros(0, dtype=np.float32)

    def start(self, on_chunk=None):
        self._on_chunk = on_chunk
        self._rms_level = 0.0
        self._chunk_acc = []
        self._chunk_acc_samples = 0
        with self._lock:
            self._buffer = []
        self._stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            dtype='float32',
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._rms_level = 0.0
        self._chunk_acc = []
        self._chunk_acc_samples = 0
        with self._lock:
            audio = np.concatenate(self._buffer) if self._buffer else np.zeros(0, dtype=np.float32)
            self._buffer = []
        return audio

    def _callback(self, indata, frames, time_info, status):
        chunk = indata[:, 0].copy()

        rms = float(np.sqrt(np.mean(chunk ** 2)))
        db = 20 * math.log10(max(rms, 1e-10))
        self._rms_level = max(0.0, min(1.0, (db + 60) / 50))

        with self._lock:
            self._buffer.append(chunk)

        self._chunk_acc.append(chunk)
        self._chunk_acc_samples += len(chunk)
        if self._chunk_acc_samples >= self.chunk_size:
            full_chunk = np.concatenate(self._chunk_acc)
            self._chunk_acc = []
            self._chunk_acc_samples = 0
            if self._on_chunk:
                self._on_chunk(full_chunk)
