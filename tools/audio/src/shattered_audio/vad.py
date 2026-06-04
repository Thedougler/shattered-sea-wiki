"""Voice Activity Detection and utterance segmentation using Silero VAD."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

import numpy as np

from .capture import SAMPLE_RATE

logger = logging.getLogger(__name__)

UTTERANCE_GAP = 0.5  # seconds of silence to end an utterance
MIN_UTTERANCE = 0.3  # minimum utterance length in seconds
VAD_WINDOW = 512  # Silero VAD expects 512 samples at 16kHz (32ms)


@dataclass
class Utterance:
    start: float
    end: float
    audio: np.ndarray  # best-mic mono audio for this utterance
    source_mic_id: str  # mic with highest energy
    all_mic_audio: dict[str, np.ndarray] = field(default_factory=dict)


class VoiceActivityDetector:
    """Segments audio frames into utterances using Silero VAD."""

    def __init__(self, sample_rate: int = SAMPLE_RATE):
        self.sample_rate = sample_rate
        self._model = None
        self._mic_buffers: dict[str, list[np.ndarray]] = {}
        self._mic_speech_active: dict[str, bool] = {}
        self._silence_samples: dict[str, int] = {}
        self._utterance_start: float | None = None
        self._gap_samples = int(UTTERANCE_GAP * sample_rate)
        self._min_samples = int(MIN_UTTERANCE * sample_rate)
        self._vad_buffer: dict[str, np.ndarray] = {}

    def _load_model(self):
        if self._model is not None:
            return
        import torch

        self._model, _ = torch.hub.load("snakers4/silero-vad", "silero_vad", trust_repo=True)
        self._model.eval()

    def _is_speech(self, samples: np.ndarray) -> bool:
        """Run Silero VAD on a chunk of audio."""
        import torch

        tensor = torch.from_numpy(samples).float()
        if len(tensor) < VAD_WINDOW:
            return False
        # Silero expects exactly 512 samples at 16kHz
        chunks = [
            tensor[i : i + VAD_WINDOW] for i in range(0, len(tensor) - VAD_WINDOW + 1, VAD_WINDOW)
        ]
        if not chunks:
            return False
        speech_count = 0
        for chunk in chunks:
            prob = self._model(chunk, self.sample_rate).item()
            if prob > 0.5:
                speech_count += 1
        return speech_count > len(chunks) * 0.3

    def _select_best_mic(self, mic_audio: dict[str, np.ndarray]) -> str:
        """Select the mic with highest RMS energy."""
        best_mic = None
        best_rms = -1.0
        for mic_id, audio in mic_audio.items():
            if len(audio) == 0:
                continue
            rms = float(np.sqrt(np.mean(audio**2)))
            if rms > best_rms:
                best_rms = rms
                best_mic = mic_id
        return best_mic or next(iter(mic_audio))

    async def process_frames(self, frame_iter, utterance_callback) -> None:
        """Process audio frames and emit utterances via callback.

        frame_iter: async iterator of AudioFrame
        utterance_callback: async callable(Utterance)
        """
        self._load_model()

        async for frame in frame_iter:
            mic_id = frame.mic_id

            if mic_id not in self._mic_buffers:
                self._mic_buffers[mic_id] = []
                self._mic_speech_active[mic_id] = False
                self._silence_samples[mic_id] = 0
                self._vad_buffer[mic_id] = np.array([], dtype=np.float32)

            self._vad_buffer[mic_id] = np.concatenate([self._vad_buffer[mic_id], frame.samples])

            # Run VAD when we have enough samples
            if len(self._vad_buffer[mic_id]) < VAD_WINDOW:
                continue

            is_speech = self._is_speech(self._vad_buffer[mic_id])
            self._vad_buffer[mic_id] = np.array([], dtype=np.float32)

            if is_speech:
                self._silence_samples[mic_id] = 0
                self._mic_buffers[mic_id].append(frame.samples)

                if self._utterance_start is None:
                    self._utterance_start = frame.timestamp

                self._mic_speech_active[mic_id] = True
            else:
                self._silence_samples[mic_id] += len(frame.samples)
                if self._mic_speech_active[mic_id]:
                    self._mic_buffers[mic_id].append(frame.samples)

                if self._silence_samples[mic_id] >= self._gap_samples:
                    self._mic_speech_active[mic_id] = False

            any_active = any(self._mic_speech_active.values())
            all_silent = all(
                self._silence_samples.get(m, 0) >= self._gap_samples for m in self._mic_buffers
            )

            if not any_active and all_silent and self._utterance_start is not None:
                mic_audio = {}
                for mid, chunks in self._mic_buffers.items():
                    if chunks:
                        mic_audio[mid] = np.concatenate(chunks)

                if mic_audio:
                    best_mic = self._select_best_mic(mic_audio)
                    best_audio = mic_audio[best_mic]

                    if len(best_audio) >= self._min_samples:
                        utterance = Utterance(
                            start=self._utterance_start,
                            end=frame.timestamp,
                            audio=best_audio,
                            source_mic_id=best_mic,
                            all_mic_audio=mic_audio,
                        )
                        await utterance_callback(utterance)

                for mid in self._mic_buffers:
                    self._mic_buffers[mid] = []
                    self._silence_samples[mid] = 0
                self._utterance_start = None

            # yield control periodically
            await asyncio.sleep(0)

    def flush(self) -> Utterance | None:
        """Flush any remaining buffered audio as a final utterance."""
        if self._utterance_start is None:
            return None

        mic_audio = {}
        for mid, chunks in self._mic_buffers.items():
            if chunks:
                mic_audio[mid] = np.concatenate(chunks)

        if not mic_audio:
            return None

        best_mic = self._select_best_mic(mic_audio)
        best_audio = mic_audio[best_mic]

        if len(best_audio) < self._min_samples:
            return None

        end_time = self._utterance_start + len(best_audio) / self.sample_rate
        utterance = Utterance(
            start=self._utterance_start,
            end=end_time,
            audio=best_audio,
            source_mic_id=best_mic,
            all_mic_audio=mic_audio,
        )

        for mid in self._mic_buffers:
            self._mic_buffers[mid] = []
            self._silence_samples[mid] = 0
        self._utterance_start = None

        return utterance
