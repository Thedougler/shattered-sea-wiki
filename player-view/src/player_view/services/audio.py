import asyncio
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
        self._lock = threading.Lock()
        self._on_chunk = None

    @property
    def recording(self) -> bool:
        return self._stream is not None and self._stream.active

    def start(self, on_chunk=None):
        self._on_chunk = on_chunk
        with self._lock:
            self._buffer = []
        self._stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            blocksize=self.chunk_size,
            dtype='float32',
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        with self._lock:
            audio = np.concatenate(self._buffer) if self._buffer else np.zeros(0, dtype=np.float32)
            self._buffer = []
        return audio

    def _callback(self, indata, frames, time_info, status):
        chunk = indata[:, 0].copy()
        with self._lock:
            self._buffer.append(chunk)
        if self._on_chunk:
            self._on_chunk(chunk)
