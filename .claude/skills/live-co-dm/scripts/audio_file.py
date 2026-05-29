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
