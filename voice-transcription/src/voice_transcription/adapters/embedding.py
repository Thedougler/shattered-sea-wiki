"""Speaker embedding via pyannote."""

from __future__ import annotations

from . import PYANNOTE_EMBED


class PyannoteEmbedder:
    """Speaker embedding for a single audio span (enrollment + per-segment ID)."""

    def __init__(self, model_id: str = PYANNOTE_EMBED, device: str = "mps",
                 auth_token: str | None = None) -> None:
        import torch  # lazy
        from pyannote.audio import Model  # lazy
        from pyannote.audio.pipelines.speaker_verification import (  # lazy
            PretrainedSpeakerEmbedding,
        )

        self._inference = PretrainedSpeakerEmbedding(
            Model.from_pretrained(model_id, use_auth_token=auth_token),
            device=torch.device(device),
        )

    def embed(self, samples: list[float], sample_rate: int) -> list[float]:
        import torch  # lazy

        waveform = torch.tensor([samples], dtype=torch.float32).unsqueeze(0)
        vec = self._inference(waveform)
        return [float(x) for x in vec.reshape(-1)]
