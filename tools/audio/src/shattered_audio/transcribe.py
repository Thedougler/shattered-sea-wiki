"""Whisper-based audio transcription via MLX on Apple Silicon."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: str | None = None


def transcribe(
    audio_path: Path,
    *,
    model: str = "mlx-community/whisper-large-v3-mlx",
) -> list[Segment]:
    """Transcribe an audio file using mlx-whisper.

    Returns a list of timed segments with text.
    """
    import mlx_whisper

    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=model,
        verbose=False,
    )

    segments = []
    for seg in result.get("segments", []):
        segments.append(
            Segment(
                start=seg["start"],
                end=seg["end"],
                text=seg["text"].strip(),
            )
        )

    return segments
