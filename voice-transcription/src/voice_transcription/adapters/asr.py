"""Parakeet v3 ASR adapters (MLX) — batch and streaming."""

from __future__ import annotations

from ..core.attribute import Word
from . import PARAKEET_MODEL


class ParakeetTranscriber:
    """Parakeet v3 ASR (MLX). Returns word-level timestamped tokens."""

    def __init__(self, model_id: str = PARAKEET_MODEL) -> None:
        from parakeet_mlx import from_pretrained  # lazy

        self._model = from_pretrained(model_id)

    def transcribe(self, samples: list[float], sample_rate: int) -> list[Word]:
        import mlx.core as mx  # lazy

        result = self._model.transcribe(mx.array(samples, dtype=mx.float32))
        words: list[Word] = []
        for sentence in getattr(result, "sentences", []):
            for tok in getattr(sentence, "tokens", []):
                words.append(Word(text=tok.text.strip(), start=float(tok.start), end=float(tok.end)))
        return [w for w in words if w.text]


class StreamingParakeetAdapter:
    """Real-time streaming transcription via parakeet-mlx transcribe_stream."""

    def __init__(self, model_id: str = PARAKEET_MODEL) -> None:
        from parakeet_mlx import from_pretrained  # lazy

        self._model = from_pretrained(model_id)
        self._streamer = self._model.transcribe_stream(
            context_size=(256, 256), depth=2, keep_original_attention=False,
        ).__enter__()

    def add_audio(self, chunk: list[float]) -> None:
        import mlx.core as mx  # lazy

        self._streamer.add_audio(mx.array(chunk, dtype=mx.float32))

    def finalized_words(self) -> list[str]:
        return [t.text.strip() for t in self._streamer.finalized_tokens if t.text.strip()]

    def close(self) -> None:
        self._streamer.__exit__(None, None, None)
