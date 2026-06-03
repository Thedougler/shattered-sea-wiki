"""CLI entry point for shattered-audio."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import Config

app = typer.Typer(name="shattered-audio", help="Session audio processing for Shattered Sea")
console = Console()


@app.command()
def transcribe(
    audio_path: Path = typer.Argument(..., help="Path to audio file"),
    session: int = typer.Option(..., "--session", "-s", help="Session number"),
    vault: Optional[Path] = typer.Option(None, "--vault", help="Vault root directory"),
    speakers: Optional[str] = typer.Option(
        None, "--speakers", help="Comma-separated speaker names (e.g. DM,Nick,Chad)"
    ),
    model: Optional[str] = typer.Option(None, "--model", help="Whisper model to use"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
    skip_diarize: bool = typer.Option(False, "--no-diarize", help="Skip speaker diarization"),
) -> None:
    """Transcribe a session audio file and output wiki-formatted markdown."""
    cfg = Config.load(config_path)

    if not audio_path.exists():
        console.print(f"[red]Audio file not found: {audio_path}[/red]")
        raise typer.Exit(1)

    vault_path = vault or cfg.vault_path
    whisper_model = model or cfg.whisper_model

    console.print(f"[bold]Transcribing session {session}[/bold]")
    console.print(f"  Audio: {audio_path}")
    console.print(f"  Model: {whisper_model}")

    from .transcribe import transcribe as do_transcribe

    with console.status("Transcribing..."):
        segments = do_transcribe(audio_path, model=whisper_model)

    console.print(f"  Segments: {len(segments)}")

    if speakers:
        speaker_names = [s.strip() for s in speakers.split(",")]
        speaker_map = {f"SPEAKER_{i:02d}": name for i, name in enumerate(speaker_names)}
        speaker_map.update(cfg.speaker_map)
    else:
        speaker_map = cfg.speaker_map

    diarization_model = None

    if not skip_diarize:
        try:
            from .diarize import diarize as do_diarize

            console.print("  Running speaker diarization...")
            with console.status("Diarizing..."):
                diar_segments = do_diarize(
                    audio_path,
                    num_speakers=len(speaker_map) if speaker_map else None,
                )

            diarization_model = "pyannote/speaker-diarization-3.1"

            for seg in segments:
                best = None
                best_overlap = 0
                for ds in diar_segments:
                    overlap = min(seg.end, ds.end) - max(seg.start, ds.start)
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best = ds.speaker
                if best:
                    seg.speaker = speaker_map.get(best, best)

        except ImportError:
            console.print("[yellow]pyannote.audio not installed — skipping diarization[/yellow]")
    else:
        console.print("  Diarization: skipped")

    from .formatter import format_wiki_transcript

    output = format_wiki_transcript(
        segments,
        session_number=session,
        model=whisper_model,
        diarization_model=diarization_model,
    )

    session_str = str(session).zfill(3)
    out_dir = vault_path / ".raw" / "sessions" / f"s{session_str}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"s{session_str}-raw.md"

    out_path.write_text(output, encoding="utf-8")
    console.print(f"[green]Wrote transcript to {out_path}[/green]")


@app.command()
def assemble(
    session: int = typer.Argument(..., help="Session number (e.g. 4)"),
    audio_dir: Path = typer.Option(
        Path("audio/sessions"), "--audio-dir", help="Directory containing audio parts"
    ),
) -> None:
    """Assemble transcript CSV parts into a single continuous transcript."""
    from .assemble import assemble as do_assemble
    from .assemble import speaker_distribution, write_assembled_csv

    session_str = str(session).zfill(2)

    try:
        rows = do_assemble(audio_dir, session_str)
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    out_dir = audio_dir / f"session{session_str}"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "assembled.csv"

    write_assembled_csv(rows, out_path)
    console.print(f"[green]Assembled {len(rows)} lines -> {out_path}[/green]")

    dist = speaker_distribution(rows)
    console.print("\nSpeaker distribution:")
    for speaker, count in dist.most_common():
        pct = 100 * count / len(rows)
        console.print(f"  {speaker}: {count} ({pct:.0f}%)")

    unresolved = [s for s in dist if s.startswith("Speaker") or s == "Unknown"]
    if unresolved:
        total = sum(dist[s] for s in unresolved)
        console.print(f"\n[yellow]{total} lines need speaker resolution[/yellow]")


if __name__ == "__main__":
    app()
