#!/usr/bin/env python3
"""Thin, intentionally-untested adapters around the real ML/audio libraries.

Each class converts at the boundary (numpy/torch <-> plain float lists) and
forwards a single call to the underlying library. There is no branching logic to
unit-test here; testing these would only test mocks of the libraries. They are
verified by the opt-in integration test (``RUN_ML_TESTS=1``) and manual smoke
runs documented in ``references/setup.md``. All heavy imports are lazy so the
pure test suite never needs the ML stack installed.

Runtime target: Apple Silicon — Parakeet via ``parakeet-mlx`` (MLX), pyannote /
diart on MPS or CPU.
"""

from __future__ import annotations

from typing import Iterator

from attribute import SpeakerTurn, Word

PARAKEET_MODEL = "mlx-community/parakeet-tdt-0.6b-v3"
PYANNOTE_DIARIZE = "pyannote/speaker-diarization-3.1"
PYANNOTE_EMBED = "pyannote/embedding"


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


def build_live_deps(args):  # pragma: no cover - wiring only
    """Assemble LoopDeps for the live CLI from parsed args. Returns (deps, banner)."""
    import os

    from profiles import ProfileStore
    from run_loop import LoopDeps
    from session_paths import next_session_number, session_paths_for
    from silence_chunker import ChunkerConfig, SilenceChunker
    from speaker_id import SpeakerIdentifier
    from transcript_writer import TranscriptWriter

    sample_rate = 16000
    sessions_dir = os.path.join(args.wiki, "sessions")
    live_dir = os.path.join(sessions_dir, ".live")
    n = args.session or next_session_number(sessions_dir, live_dir)
    paths = session_paths_for(live_dir, n)
    os.makedirs(paths.audio_dir, exist_ok=True)

    profiles_dir = args.profiles_dir or os.path.join(
        os.path.dirname(__file__), os.pardir, "profiles"
    )
    enrolled = ProfileStore(profiles_dir).load_all()
    auth = os.environ.get("HF_TOKEN")

    writer = TranscriptWriter(paths.transcript_md)
    deps = LoopDeps(
        source=SoundDeviceSource(sample_rate=sample_rate),
        chunker=SilenceChunker(ChunkerConfig(sample_rate=sample_rate)),
        diarizer=PyannoteDiarizer(num_speakers=args.speakers, auth_token=auth),
        transcriber=ParakeetTranscriber(),
        embedder=PyannoteEmbedder(auth_token=auth),
        identifier=SpeakerIdentifier(enrolled, threshold=args.threshold),
        writer=writer,
        audio_dir=paths.audio_dir,
        sample_rate=sample_rate,
        on_status=lambda m: None,
    )
    banner = (
        f"live-co-dm: session {n:02d} | {len(enrolled)} profile(s) | "
        f"speakers={args.speakers or 'auto'} | transcript -> {paths.transcript_md}"
    )
    return deps, banner
