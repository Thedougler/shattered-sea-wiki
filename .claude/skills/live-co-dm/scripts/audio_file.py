#!/usr/bin/env python3
"""Write mono float samples to a 16-bit PCM WAV using the stdlib ``wave`` module.

No numpy/soundfile needed for output, so chunk audio can be saved (and the loop
unit-tested) with the standard library alone. Samples are clamped to [-1, 1].
"""

from __future__ import annotations

import os
import struct
import wave


def write_wav(path: str, samples: list[float], sample_rate: int) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    frames = bytearray()
    for x in samples:
        clamped = -1.0 if x < -1.0 else (1.0 if x > 1.0 else x)
        frames += struct.pack("<h", int(clamped * 32767))
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(bytes(frames))


def read_wav(path: str) -> tuple[list[float], int]:
    """Read a mono 16-bit PCM WAV into float samples in [-1, 1] plus its rate."""
    with wave.open(path, "rb") as wf:
        sample_rate = wf.getframerate()
        n = wf.getnframes()
        raw = wf.readframes(n)
    if not raw:
        return [], sample_rate
    ints = struct.unpack(f"<{len(raw) // 2}h", raw)
    return [x / 32767.0 for x in ints], sample_rate
