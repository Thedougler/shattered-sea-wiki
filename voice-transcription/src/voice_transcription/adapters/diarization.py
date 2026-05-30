"""Overlap-aware diarization via pyannote."""

from __future__ import annotations

from ..core.attribute import SpeakerTurn
from . import PYANNOTE_DIARIZE


class PyannoteDiarizer:
    """Overlap-aware diarization. ``num_speakers`` sharply improves crosstalk."""

    def __init__(self, model_id: str = PYANNOTE_DIARIZE, num_speakers: int | None = None,
                 device: str = "mps", auth_token: str | None = None) -> None:
        import torch  # lazy
        from pyannote.audio import Pipeline  # lazy

        self._pipeline = Pipeline.from_pretrained(model_id, use_auth_token=auth_token)
        self._pipeline.to(torch.device(device))
        self._num_speakers = num_speakers

    def diarize(self, samples: list[float], sample_rate: int) -> list[SpeakerTurn]:
        import torch  # lazy

        waveform = torch.tensor([samples], dtype=torch.float32)
        kwargs = {"num_speakers": self._num_speakers} if self._num_speakers else {}
        annotation = self._pipeline({"waveform": waveform, "sample_rate": sample_rate}, **kwargs)
        return [
            SpeakerTurn(speaker=str(label), start=float(seg.start), end=float(seg.end))
            for seg, _, label in annotation.itertracks(yield_label=True)
        ]
