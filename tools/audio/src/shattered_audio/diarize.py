"""Speaker diarization via pyannote on MPS backend."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SpeakerSegment:
    start: float
    end: float
    speaker: str


def diarize(
    audio_path: Path,
    *,
    num_speakers: int | None = None,
    hf_token: str | None = None,
) -> list[SpeakerSegment]:
    """Run speaker diarization on an audio file.

    Requires pyannote.audio and a HuggingFace token with model access.
    """
    import os

    from pyannote.audio import Pipeline

    token = hf_token or os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "HF_TOKEN required for pyannote diarization. Set HF_TOKEN env var or pass --hf-token."
        )

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=token,
    )

    import torch

    if torch.backends.mps.is_available():
        pipeline.to(torch.device("mps"))

    params = {}
    if num_speakers is not None:
        params["num_speakers"] = num_speakers

    diarization = pipeline(str(audio_path), **params)

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append(
            SpeakerSegment(
                start=turn.start,
                end=turn.end,
                speaker=speaker,
            )
        )

    return segments
