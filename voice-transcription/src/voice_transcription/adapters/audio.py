"""Mono microphone capture via sounddevice."""

from __future__ import annotations

from typing import Iterator


class SoundDeviceSource:
    """Mono microphone capture via ``sounddevice``, yielded as float frames."""

    def __init__(self, sample_rate: int = 16000, frame_ms: int = 30, device=None) -> None:
        import sounddevice as sd  # lazy

        self.sample_rate = sample_rate
        self._blocksize = int(sample_rate * frame_ms / 1000)
        self._stream = sd.InputStream(
            samplerate=sample_rate, channels=1, dtype="float32",
            blocksize=self._blocksize, device=device,
        )
        self._stream.start()

    def frames(self) -> Iterator[list[float]]:
        while True:
            data, _ = self._stream.read(self._blocksize)
            yield [float(x) for x in data[:, 0]]

    def close(self) -> None:
        self._stream.stop()
        self._stream.close()
