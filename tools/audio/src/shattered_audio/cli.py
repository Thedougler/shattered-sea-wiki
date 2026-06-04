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


@app.command()
def live(
    session: int = typer.Option(..., "--session", "-s", help="Session number"),
    speakers: Optional[str] = typer.Option(
        None, "--speakers", help="Comma-separated speaker names"
    ),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Start a live recording and transcription session."""
    import asyncio

    cfg = Config.load(config_path)
    speaker_list = [s.strip() for s in speakers.split(",")] if speakers else None

    console.print(f"[bold]Starting live session {session}[/bold]")
    console.print(f"  Output: {cfg.inbox_path}/")
    console.print(f"  Fast model: {cfg.whisper_model_fast}")
    console.print(f"  Accurate model: {cfg.whisper_model}")

    from .profiles import load_actor_profiles, load_profiles

    actors = load_actor_profiles(cfg.profiles_dir)
    if actors:
        for slug, actor in actors.items():
            personas = [p.name for p in actor.personas.values()]
            dm_tag = " (DM)" if actor.is_dm else ""
            if personas:
                console.print(f"  Voice: {actor.name}{dm_tag} + personas: {', '.join(personas)}")
            else:
                console.print(f"  Voice: {actor.name}{dm_tag}")
    else:
        profiles = load_profiles(cfg.profiles_dir)
        if profiles:
            console.print(f"  Voice profiles: {', '.join(p.name for p in profiles.values())}")
        else:
            console.print("  [yellow]No voice profiles loaded[/yellow]")

    console.print("\n[dim]Press Ctrl+C to stop recording[/dim]\n")

    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

    from .live_session import run_live_session

    try:
        asyncio.run(run_live_session(session, cfg, speaker_list))
    except KeyboardInterrupt:
        pass

    console.print("\n[green]Session stopped[/green]")


@app.command()
def enroll(
    name: str = typer.Argument(..., help="Speaker or character name"),
    audio_file: Optional[Path] = typer.Argument(None, help="Audio file for enrollment"),
    record: Optional[int] = typer.Option(
        None, "--record", "-r", help="Record N seconds from default mic instead of using a file"
    ),
    actor: Optional[str] = typer.Option(
        None, "--actor", "-a", help="Enroll as a character voice (persona) under this actor"
    ),
    dm: bool = typer.Option(False, "--dm", help="Mark this actor as the DM"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Enroll a voice profile — actor (default) or character persona (--actor)."""
    cfg = Config.load(config_path)

    if record:
        import sounddevice as sd

        console.print(f"[bold]Recording {record}s for '{name}'...[/bold]")
        audio = sd.rec(
            int(record * 16000),
            samplerate=16000,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        samples = audio[:, 0]
    elif audio_file:
        if not audio_file.exists():
            console.print(f"[red]File not found: {audio_file}[/red]")
            raise typer.Exit(1)

        from pydub import AudioSegment

        seg = AudioSegment.from_file(str(audio_file))
        seg = seg.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        import numpy as np

        samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0
    else:
        console.print("[red]Provide an audio file or use --record N[/red]")
        raise typer.Exit(1)

    if actor:
        from .profiles import enroll_persona

        console.print(f"[bold]Enrolling persona '{name}' under actor '{actor}'[/bold]")
        try:
            result = enroll_persona(
                name, actor, samples, cfg.profiles_dir, max_exemplars=cfg.max_exemplars
            )
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)
        persona = result.personas.get(name.lower().replace(" ", "-"))
        count = persona.sample_count if persona else 1
        console.print(
            f"[green]Enrolled persona '{name}' under '{actor}' ({count} sample(s))[/green]"
        )
    else:
        from .profiles import enroll_actor

        console.print(f"[bold]Enrolling actor '{name}'[/bold]")
        result = enroll_actor(name, samples, cfg.profiles_dir, is_dm=dm)
        dm_tag = " (DM)" if result.is_dm else ""
        console.print(
            f"[green]Enrolled '{result.name}'{dm_tag} ({result.sample_count} sample(s))[/green]"
        )


@app.command()
def profiles(
    actor_name: Optional[str] = typer.Argument(None, help="Show detail for a specific actor"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """List all voice profiles — actors and their character personas."""
    cfg = Config.load(config_path)

    from .profiles import load_actor_profiles

    actors = load_actor_profiles(cfg.profiles_dir)

    if not actors:
        console.print("[yellow]No voice profiles found[/yellow]")
        console.print(f"[dim]Profiles dir: {cfg.profiles_dir}[/dim]")
        raise typer.Exit(0)

    if actor_name:
        slug = actor_name.lower().replace(" ", "-")
        if slug not in actors:
            console.print(f"[red]Actor '{actor_name}' not found[/red]")
            raise typer.Exit(1)
        actor = actors[slug]
        dm_tag = " (DM)" if actor.is_dm else ""
        mic_info = f", mics: {actor.associated_mics}" if actor.associated_mics else ""
        console.print(f"[bold]{actor.name}{dm_tag}[/bold] — {actor.sample_count} samples{mic_info}")
        if actor.prosody:
            p = actor.prosody
            console.print(
                f"  Prosody: pitch={p.pitch_mean:.0f}Hz (std={p.pitch_std:.0f}), "
                f"range={p.pitch_range:.0f}Hz, rate={p.speaking_rate:.1f}/s"
            )
        if actor.personas:
            for p_slug, persona in actor.personas.items():
                exemplar_count = (
                    len(persona.exemplar_embeddings) if persona.exemplar_embeddings else 0
                )
                console.print(
                    f"  [cyan]{persona.name}[/cyan] — {persona.sample_count} samples, "
                    f"{exemplar_count} exemplars"
                )
                if persona.prosody:
                    pp = persona.prosody
                    console.print(
                        f"    Prosody: pitch={pp.pitch_mean:.0f}Hz (std={pp.pitch_std:.0f}), "
                        f"range={pp.pitch_range:.0f}Hz, rate={pp.speaking_rate:.1f}/s"
                    )
        else:
            console.print("  [dim](no character voices)[/dim]")
        return

    console.print("[bold]Voice Profiles[/bold]\n")
    for slug, actor in sorted(actors.items()):
        dm_tag = " (DM)" if actor.is_dm else ""
        mic_info = f", mic: {', '.join(actor.associated_mics)}" if actor.associated_mics else ""
        console.print(
            f"  [bold]{actor.name}{dm_tag}[/bold] — {actor.sample_count} samples{mic_info}"
        )
        if actor.personas:
            items = list(actor.personas.items())
            for i, (p_slug, persona) in enumerate(items):
                prefix = "└──" if i == len(items) - 1 else "├──"
                console.print(
                    f"    {prefix} [cyan]{persona.name}[/cyan] — {persona.sample_count} samples"
                )
        else:
            console.print("    [dim](no character voices)[/dim]")


@app.command()
def retrain(
    transcript: Path = typer.Argument(..., help="Path to corrected transcript markdown"),
    audio_dir: Optional[Path] = typer.Option(
        None, "--audio-dir", help="Directory containing chunk WAV files"
    ),
    blend: float = typer.Option(
        0.7, "--blend", help="Weight for new data (0-1, higher = more new)"
    ),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
    legacy: bool = typer.Option(False, "--legacy", help="Use v1 flat profile retraining"),
) -> None:
    """Retrain voice profiles from a corrected transcript."""
    cfg = Config.load(config_path)

    if not transcript.exists():
        console.print(f"[red]Transcript not found: {transcript}[/red]")
        raise typer.Exit(1)

    wav_dir = audio_dir or transcript.parent

    console.print(f"[bold]Retraining profiles from {transcript}[/bold]")
    console.print(f"  Audio dir: {wav_dir}")
    console.print(f"  Blend: {1 - blend:.0%} old + {blend:.0%} new")

    if legacy:
        from .profiles import retrain_from_transcript

        updated = retrain_from_transcript(
            transcript, wav_dir, cfg.profiles_dir, blend_old=1 - blend
        )
        for slug, profile in updated.items():
            console.print(f"  [green]{profile.name}[/green]: {profile.sample_count} samples")
    else:
        from .profiles import retrain_from_transcript_v2

        updated = retrain_from_transcript_v2(
            transcript, wav_dir, cfg.profiles_dir, blend_old=1 - blend
        )
        for slug, actor in updated.items():
            console.print(f"  [green]{actor.name}[/green]: {actor.sample_count} samples")
            for p_slug, persona in actor.personas.items():
                console.print(f"    [cyan]{persona.name}[/cyan]: {persona.sample_count} samples")

    if not updated:
        console.print("[yellow]No profiles updated (no labeled speakers found)[/yellow]")


@app.command()
def devices() -> None:
    """List available audio input devices."""
    from .capture import list_devices

    devs = list_devices()
    if not devs:
        console.print("[yellow]No audio input devices found[/yellow]")
        raise typer.Exit(1)

    console.print("[bold]Audio Input Devices[/bold]\n")
    for dev in devs:
        default = " [green](default)[/green]" if dev["is_default"] else ""
        console.print(f"  [{dev['id']}] {dev['name']}{default}")
        console.print(f"      Channels: {dev['channels']}  Sample rate: {dev['sample_rate']}")


if __name__ == "__main__":
    app()
