"""Accurate (cold) transcription pass — full model + diarization, replaces hot output."""

from __future__ import annotations

import logging
from pathlib import Path

from .chunker import Chunk
from .profiles import VoiceProfile, identify_speaker

logger = logging.getLogger(__name__)


def format_timestamp(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


class ColdPass:
    """Runs accurate transcription + diarization on completed chunks."""

    def __init__(
        self,
        output_dir: Path,
        session_number: int,
        model: str = "mlx-community/whisper-large-v3-mlx",
        profiles: dict[str, VoiceProfile] | None = None,
        channel_priors: dict[str, str] | None = None,
        channel_boost: float = 0.15,
        speaker_threshold: float = 0.7,
        skip_diarize: bool = False,
    ):
        self.output_dir = output_dir
        self.session_number = session_number
        self.model = model
        self.profiles = profiles or {}
        self.channel_priors = channel_priors
        self.channel_boost = channel_boost
        self.speaker_threshold = speaker_threshold
        self.skip_diarize = skip_diarize

    async def process_chunk(self, chunk: Chunk) -> Path:
        """Run full transcription + diarization on a chunk. Returns output path."""
        import asyncio

        return await asyncio.to_thread(self._process_sync, chunk)

    def _process_sync(self, chunk: Chunk) -> Path:
        if not chunk.wav_path or not chunk.wav_path.exists():
            raise FileNotFoundError(f"Chunk WAV not found: {chunk.wav_path}")

        # Full-accuracy transcription
        from .transcribe import transcribe

        segments = transcribe(chunk.wav_path, model=self.model)

        # Diarization
        diarization_model = None
        diar_segments = []
        if not self.skip_diarize:
            try:
                from .diarize import diarize

                diar_segments = diarize(chunk.wav_path)
                diarization_model = "pyannote/speaker-diarization-3.1"
            except (ImportError, RuntimeError) as e:
                logger.warning("Diarization unavailable: %s", e)

        # Speaker identification: voice profiles take precedence, diarization fills gaps
        speaker_confidences: dict[str, list[float]] = {}

        for seg in segments:
            # Try voice profile match first using the audio from the utterance
            # that best overlaps this segment
            best_utterance = None
            best_overlap = 0.0
            for utt in chunk.utterances:
                # Adjust utterance times relative to chunk start
                utt_start_rel = utt.start - chunk.start_time
                utt_end_rel = utt.end - chunk.start_time
                overlap = min(seg.end, utt_end_rel) - max(seg.start, utt_start_rel)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_utterance = utt

            if best_utterance and self.profiles:
                match = identify_speaker(
                    best_utterance.audio,
                    self.profiles,
                    source_mic=best_utterance.source_mic_id,
                    channel_priors=self.channel_priors,
                    channel_boost=self.channel_boost,
                    threshold=self.speaker_threshold,
                )
                if match:
                    seg.speaker = match.name
                    if match.name not in speaker_confidences:
                        speaker_confidences[match.name] = []
                    speaker_confidences[match.name].append(match.confidence)

            # Fall back to diarization label if no profile match
            if not seg.speaker and diar_segments:
                best_diar = None
                best_diar_overlap = 0.0
                for ds in diar_segments:
                    overlap = min(seg.end, ds.end) - max(seg.start, ds.start)
                    if overlap > best_diar_overlap:
                        best_diar_overlap = overlap
                        best_diar = ds.speaker
                if best_diar:
                    seg.speaker = best_diar

        # Compute average confidence per speaker
        avg_confidence = {
            name: round(sum(scores) / len(scores), 2)
            for name, scores in speaker_confidences.items()
        }

        # Format output
        speakers_detected = sorted(set(s.speaker for s in segments if s.speaker))
        time_range_str = f"{format_timestamp(chunk.start_time)}-{format_timestamp(chunk.end_time)}"

        session_str = str(self.session_number).zfill(2)
        chunk_str = str(chunk.chunk_number).zfill(3)

        lines = [
            "---",
            "type: raw",
            "subtype: raw-session-chunk",
            f"session_number: {self.session_number}",
            f"chunk: {chunk.chunk_number}",
            f'time_range: "{time_range_str}"',
            f'audio_file: "s{session_str}-chunk-{chunk_str}.wav"',
            f"speakers_detected: {speakers_detected}",
        ]

        if avg_confidence:
            lines.append(f"speaker_confidence: {avg_confidence}")

        lines.append(f'model: "{self.model}"')

        if diarization_model:
            lines.append(f'diarization_model: "{diarization_model}"')

        lines.extend(
            [
                "ingest_status: pending",
                "---",
                "",
                f"# Session {self.session_number} — Chunk {chunk.chunk_number}"
                f" ({format_timestamp(chunk.start_time)} - {format_timestamp(chunk.end_time)})",
                "",
            ]
        )

        for seg in segments:
            # Offset timestamps relative to session start
            abs_start = seg.start + chunk.start_time
            speaker = seg.speaker or "Unknown"
            ts = format_timestamp(abs_start)
            lines.append(f"[{ts}] **{speaker}:** {seg.text}")
            lines.append("")

        out_name = f"s{session_str}-chunk-{chunk_str}.md"
        out_path = self.output_dir / out_name
        out_path.write_text("\n".join(lines), encoding="utf-8")

        logger.info("Cold pass complete: %s (%d segments)", out_name, len(segments))
        return out_path
