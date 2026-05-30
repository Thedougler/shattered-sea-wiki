"""Assemble runtime dependencies for live capture CLI."""

from __future__ import annotations


def build_live_deps(args):  # pragma: no cover - wiring only
    """Assemble LoopDeps for the live CLI from parsed args. Returns (deps, banner)."""
    import os

    from ..core.profiles import ProfileStore
    from ..core.run_loop import LoopDeps
    from ..core.session_paths import next_session_number, session_paths_for
    from ..core.silence_chunker import ChunkerConfig, SilenceChunker
    from ..core.speaker_id import SpeakerIdentifier
    from ..core.transcript_writer import TranscriptWriter
    from .audio import SoundDeviceSource
    from .asr import ParakeetTranscriber
    from .diarization import PyannoteDiarizer
    from .embedding import PyannoteEmbedder

    sample_rate = 16000
    sessions_dir = os.path.join(args.wiki, "sessions")
    live_dir = os.path.join(sessions_dir, ".live")
    n = args.session or next_session_number(sessions_dir, live_dir)
    paths = session_paths_for(live_dir, n)
    os.makedirs(paths.audio_dir, exist_ok=True)

    profiles_dir = args.profiles_dir or os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "profiles",
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
        f"voice-transcription: session {n:02d} | {len(enrolled)} profile(s) | "
        f"speakers={args.speakers or 'auto'} | transcript -> {paths.transcript_md}"
    )
    return deps, banner
