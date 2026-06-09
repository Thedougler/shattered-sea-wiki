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
        Path(".raw/sessions"), "--audio-dir", help="Directory containing session packets"
    ),
) -> None:
    """Assemble transcript CSV parts into a single continuous transcript."""
    from .assemble import assemble as do_assemble
    from .assemble import speaker_distribution, write_assembled_csv
    from .record import session_dir as _session_dir

    session_str = str(session).zfill(2)
    sdir = _session_dir(audio_dir, session)
    parts_dir = sdir / "transcripts" / "raw"

    try:
        rows = do_assemble(parts_dir, session_str)
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    out_dir = sdir / "transcripts" / "assembled"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"session-{session_str}-assembled.csv"

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
def delete(
    name: str = typer.Argument(..., help="Actor or persona name to delete"),
    actor: Optional[str] = typer.Option(
        None,
        "--actor",
        "-a",
        help="Delete only this persona under the named actor (omit to delete the whole actor)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Delete a voice profile — actor (and all their personas) or a single persona."""
    import shutil

    from .profiles import load_actor_profiles, save_actor_profile

    cfg = Config.load(config_path)
    actors = load_actor_profiles(cfg.profiles_dir)

    if actor:
        actor_slug = actor.lower().replace(" ", "-")
        if actor_slug not in actors:
            console.print(f"[red]Actor '{actor}' not found[/red]")
            raise typer.Exit(1)
        persona_slug = name.lower().replace(" ", "-")
        act = actors[actor_slug]
        if persona_slug not in act.personas:
            console.print(f"[red]Persona '{name}' not found under actor '{actor}'[/red]")
            raise typer.Exit(1)

        if not yes and not typer.confirm(f"Delete persona '{name}' from actor '{actor}'?"):
            raise typer.Exit(0)

        actor_dir = cfg.profiles_dir / actor_slug
        for suffix in (".npy", "_prosody.yaml", "_exemplars.npy", "_meta.yaml"):
            p = actor_dir / f"{persona_slug}{suffix}"
            if p.exists():
                p.unlink()
        del act.personas[persona_slug]
        save_actor_profile(act, cfg.profiles_dir)
        console.print(f"[green]Deleted persona '{name}' from actor '{actor}'[/green]")

    else:
        actor_slug = name.lower().replace(" ", "-")
        if actor_slug not in actors:
            console.print(f"[red]Actor '{name}' not found[/red]")
            raise typer.Exit(1)
        act = actors[actor_slug]
        persona_names = [p.name for p in act.personas.values()]

        if not yes:
            desc = f"actor '{name}'"
            if persona_names:
                desc += f" and {len(persona_names)} persona(s): {', '.join(persona_names)}"
            if not typer.confirm(f"Delete {desc}?"):
                raise typer.Exit(0)

        shutil.rmtree(cfg.profiles_dir / actor_slug)
        console.print(f"[green]Deleted actor '{name}'[/green]")


@app.command()
def retrain(
    transcript: Path = typer.Argument(..., help="Path to corrected transcript markdown"),
    audio_dir: Optional[Path] = typer.Option(
        None, "--audio-dir", help="Directory containing chunk WAV files"
    ),
    speaker_map_path: Optional[Path] = typer.Option(
        None, "--speaker-map", help="speaker-map.md from session-ingest (remaps UNKNOWN labels)"
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

    label_map = None
    if speaker_map_path:
        if not speaker_map_path.exists():
            console.print(f"[red]Speaker map not found: {speaker_map_path}[/red]")
            raise typer.Exit(1)
        from .profiles import parse_speaker_map

        label_map = parse_speaker_map(speaker_map_path)
        console.print(f"  Speaker map: {len(label_map)} resolutions from {speaker_map_path}")
        for orig, resolved in label_map.items():
            console.print(f"    {orig} → {resolved}")

    console.print(f"[bold]Retraining profiles from {transcript}[/bold]")
    console.print(f"  Audio dir: {wav_dir}")
    console.print(f"  Blend: {1 - blend:.0%} old + {blend:.0%} new")

    if legacy:
        if label_map:
            console.print("[yellow]--speaker-map is ignored with --legacy[/yellow]")
        from .profiles import retrain_from_transcript

        updated = retrain_from_transcript(
            transcript, wav_dir, cfg.profiles_dir, blend_old=1 - blend
        )
        for slug, profile in updated.items():
            console.print(f"  [green]{profile.name}[/green]: {profile.sample_count} samples")
    else:
        from .profiles import retrain_from_transcript_v2

        updated = retrain_from_transcript_v2(
            transcript,
            wav_dir,
            cfg.profiles_dir,
            blend_old=1 - blend,
            speaker_map=label_map,
        )
        for slug, actor in updated.items():
            console.print(f"  [green]{actor.name}[/green]: {actor.sample_count} samples")
            for p_slug, persona in actor.personas.items():
                console.print(f"    [cyan]{persona.name}[/cyan]: {persona.sample_count} samples")

    if not updated:
        console.print("[yellow]No profiles updated (no labeled speakers found)[/yellow]")


@app.command(name="transcribe-session")
def transcribe_session_cmd(
    session: int = typer.Option(..., "--session", "-s", help="Session number"),
    audio_dir: Path = typer.Option(
        Path(".raw/sessions"), "--audio-dir", help="Where session audio is stored"
    ),
    no_profiles: bool = typer.Option(
        False, "--no-profiles", help="Label purely by mic; skip voice-profile identification"
    ),
    save_profile: Optional[str] = typer.Option(
        None, "--save-profile", help="Enroll/refresh a voice profile with this speaker's name"
    ),
    from_mic: Optional[str] = typer.Option(
        None, "--from-mic", help="Mic id to harvest the --save-profile voice from (e.g. mic01)"
    ),
    as_actor: Optional[str] = typer.Option(
        None, "--actor", help="Save --save-profile as a character voice (persona) under this actor"
    ),
    model: Optional[str] = typer.Option(None, "--model", help="Whisper model to use"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Transcribe a recorded session into per-part speaker CSVs.

    Reads the per-mic m4a tracks under ``.raw/sessions/session-NN/audio/`` and
    writes ``transcripts/raw/session-NN-part-MM.csv`` for each part — the format
    session-ingest and ``assemble`` consume. Voice profiles are loaded
    automatically; the mic each voice came from is a strong speaker prior.
    """
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    from . import session_transcribe as st
    from .record import session_dir as _session_dir

    cfg = Config.load(config_path)
    whisper_model = model or cfg.whisper_model

    sdir = _session_dir(audio_dir, session)
    if not sdir.exists():
        console.print(f"[red]No recording found at {sdir}[/red]")
        raise typer.Exit(1)

    if save_profile:
        _save_profile_from_session(
            sdir, save_profile, from_mic, as_actor, cfg, console
        )

    console.print(f"[bold]Transcribing session {session}[/bold]")
    console.print(f"  Audio: {sdir}")
    console.print(f"  Model: {whisper_model}")
    console.print(f"  Voice profiles: {'off' if no_profiles else 'auto-load'}")

    written = st.transcribe_session(
        session,
        audio_dir=audio_dir,
        use_profiles=not no_profiles,
        profiles_dir=cfg.profiles_dir,
        model=whisper_model,
        channel_boost=cfg.channel_boost,
        actor_threshold=cfg.actor_threshold,
        persona_threshold=cfg.persona_threshold,
        persona_margin=cfg.persona_margin,
        prosody_weight=cfg.prosody_weight,
        log=lambda m: console.print(f"  {m}", style="dim"),
    )
    out_dir = sdir / "transcripts" / "raw"
    console.print(f"[green]Wrote {len(written)} part CSV(s) to {out_dir}/[/green]")
    console.print(
        f"[dim]Next: shattered-audio assemble {session}  →  then the session-ingest skill[/dim]"
    )


def _save_profile_from_session(sdir, name, from_mic, as_actor, cfg, console) -> None:
    """Harvest a mic's audio from a recorded session and enroll a voice profile."""
    import numpy as np

    from .session_transcribe import _load_samples, discover_tracks

    tracks = discover_tracks(sdir)
    if not tracks:
        console.print("[red]No mic tracks to harvest a profile from[/red]")
        raise typer.Exit(1)

    if from_mic:
        track = next((t for t in tracks if t.mic_id == from_mic), None)
        if track is None:
            console.print(f"[red]Mic '{from_mic}' not found in this session[/red]")
            raise typer.Exit(1)
    elif len(tracks) == 1:
        track = tracks[0]
    else:
        mics = ", ".join(t.mic_id for t in tracks)
        console.print(f"[red]Multiple mics ({mics}) — pass --from-mic to pick one[/red]")
        raise typer.Exit(1)

    if not track.parts:
        console.print(f"[red]Mic '{track.mic_id}' has no audio[/red]")
        raise typer.Exit(1)

    # Concatenate up to ~60s of this mic's audio for a clean enrollment sample.
    chunks, total = [], 0
    for part in track.parts:
        s = _load_samples(part)
        chunks.append(s)
        total += len(s)
        if total >= 60 * 16000:
            break
    samples = np.concatenate(chunks)[: 120 * 16000]

    if as_actor:
        from .profiles import enroll_persona

        console.print(f"[bold]Saving persona '{name}' under actor '{as_actor}'[/bold]")
        enroll_persona(name, as_actor, samples, cfg.profiles_dir, max_exemplars=cfg.max_exemplars)
    else:
        from .profiles import enroll_actor

        console.print(f"[bold]Saving voice profile '{name}' (from {track.mic_id})[/bold]")
        enroll_actor(name, samples, cfg.profiles_dir)
    console.print(f"[green]Saved profile '{name}'[/green]")


@app.command()
def record(
    session: int = typer.Option(..., "--session", "-s", help="Session number"),
    mics: Optional[str] = typer.Option(
        None, "--mics", help="Comma-separated avfoundation device indices (default: all)"
    ),
    segment_minutes: int = typer.Option(
        15, "--segment-minutes", help="Length of each audio chunk in minutes"
    ),
    audio_dir: Path = typer.Option(
        Path(".raw/sessions"), "--audio-dir", help="Where session audio is stored"
    ),
    max_seconds: Optional[float] = typer.Option(
        None, "--max-seconds", help="Auto-stop after N seconds (for testing); default: run until stopped"
    ),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Record a session from all mics — one isolated track per mic, chunked to m4a.

    Fires up one ffmpeg process per microphone and keeps recording until you
    stop it (Ctrl+C, or the controlling agent sends SIGTERM). Built for 4+ hour
    sessions: each chunk is flushed to disk as it finishes.
    """
    import logging

    from . import record as rec

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    cfg = Config.load(config_path)

    devs = rec.list_avfoundation_devices()
    if not devs:
        console.print("[red]No avfoundation audio input devices found[/red]")
        console.print("[dim]Is ffmpeg installed and does the terminal have mic permission?[/dim]")
        raise typer.Exit(1)

    indices = [int(x) for x in mics.split(",")] if mics else None
    names = cfg.mic_names if (not indices and cfg.mic_names) else None
    selected = rec.select_mics(devs, indices=indices, names=names)
    if not selected:
        console.print("[red]No microphones selected[/red]")
        raise typer.Exit(1)

    # Apply mic→speaker priors from config so the manifest carries them forward.
    for mic in selected:
        prior = cfg.channel_priors.get(mic.mic_id)
        if prior:
            mic.speaker = prior

    console.print(f"[bold]Recording session {session}[/bold]")
    console.print(f"  Output: {rec.session_dir(audio_dir, session)}/")
    console.print(f"  Chunk length: {segment_minutes} min")
    for mic in selected:
        tag = f" → {mic.speaker}" if mic.speaker else ""
        console.print(f"  [cyan]{mic.mic_id}[/cyan] [{mic.index}] {mic.name}{tag}")
    console.print("\n[dim]Recording… press Ctrl+C (or stop the agent) to end the session.[/dim]\n")

    sdir = rec.record_session(
        session=session,
        mics=selected,
        audio_dir=audio_dir,
        segment_seconds=segment_minutes * 60,
        max_seconds=max_seconds,
    )

    parts = sorted(sdir.rglob("*.m4a"))
    console.print(f"\n[green]Stopped. {len(parts)} chunk(s) written under {sdir}[/green]")
    console.print(f"[dim]Next: shattered-audio transcribe-session --session {session}[/dim]")


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


@app.command()
def watch(
    config_path: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
    threshold: float = typer.Option(
        0.015, "--threshold", help="RMS energy threshold for speech detection"
    ),
    min_blocks: int = typer.Option(
        4, "--min-blocks", help="Minimum 100ms blocks to count as an utterance (default: 400ms)"
    ),
    silence_blocks: int = typer.Option(
        8, "--silence", help="100ms silent blocks to end utterance (default: 800ms)"
    ),
    history: int = typer.Option(12, "--history", help="Identification rows to show in TUI"),
    mic: Optional[int] = typer.Option(
        None,
        "--mic",
        help="Device index to listen on (default: system default). Use 'devices' to list.",
    ),
) -> None:
    """Live speaker-identification TUI — listens on mic and prints who is speaking. Ctrl+C to stop.

    No audio is recorded or saved. Needs the live extras (sounddevice); if
    missing, run the editable install with the all extras in tools/audio/.
    """
    import queue as _queue
    import threading
    import time as _time

    import numpy as np

    cfg = Config.load(config_path)

    from .profiles import identify_speaker_v2, load_actor_profiles

    actors = load_actor_profiles(cfg.profiles_dir)
    if not actors:
        console.print(
            "[yellow]No voice profiles enrolled — use 'shattered-audio enroll' first.[/yellow]"
        )
        raise typer.Exit(1)

    try:
        import sounddevice as sd
    except ImportError:
        console.print(
            r"[red]sounddevice not installed. Run: pip install -e '.\[all]' in tools/audio/[/red]"
        )
        raise typer.Exit(1)

    console.print("[bold]Voice Watch[/bold] — speak to identify\n")
    for slug, actor in sorted(actors.items()):
        dm_tag = " [dim](DM)[/dim]" if actor.is_dm else ""
        personas = [p.name for p in actor.personas.values()]
        p_str = ("  →  " + ", ".join(f"[cyan]{p}[/cyan]" for p in personas)) if personas else ""
        console.print(f"  [bold]{actor.name}[/bold]{dm_tag}{p_str}")
    console.print("\n[dim]Ctrl+C to stop[/dim]\n")

    SAMPLE_RATE_W = 16000
    BLOCK_SIZE_W = 1600  # 100ms per block

    rows: list[tuple[str, str, str]] = []  # (timestamp, who_markup, conf_markup)

    from rich.live import Live
    from rich.table import Table

    def make_table() -> Table:
        t = Table("Time", "Speaker", "Confidence", box=None, padding=(0, 2))
        display = rows[-history:] if rows else [("—", "[dim]listening…[/dim]", "")]
        for ts, who, conf in display:
            t.add_row(ts, who, conf)
        return t

    audio_q: _queue.Queue = _queue.Queue()
    stopped = threading.Event()

    def audio_callback(indata, frames, _time_info, _status) -> None:
        audio_q.put(indata[:, 0].copy())

    def identify_loop() -> None:
        buf: list[np.ndarray] = []
        in_speech = False
        silent_count = 0

        while not stopped.is_set():
            try:
                block = audio_q.get(timeout=0.2)
            except _queue.Empty:
                continue

            rms = float(np.sqrt(np.mean(block**2)))

            if rms >= threshold:
                in_speech = True
                silent_count = 0
                buf.append(block)
            elif in_speech:
                buf.append(block)
                silent_count += 1
                if silent_count >= silence_blocks:
                    if len(buf) >= min_blocks:
                        utterance = np.concatenate(buf)
                        try:
                            match = identify_speaker_v2(
                                utterance,
                                actors,
                                channel_priors=cfg.channel_priors,
                                channel_boost=cfg.channel_boost,
                                actor_threshold=cfg.actor_threshold,
                                persona_threshold=cfg.persona_threshold,
                                persona_margin=cfg.persona_margin,
                                prosody_weight=cfg.prosody_weight,
                            )
                        except Exception:
                            match = None

                        ts = _time.strftime("%H:%M:%S")
                        if match:
                            if match.persona:
                                who = f"[bold]{match.actor}[/bold] → [cyan]{match.persona}[/cyan]"
                            else:
                                who = f"[bold]{match.name}[/bold]"
                            color = "green" if match.tier == "high" else "yellow"
                            conf_str = f"[{color}]{match.confidence:.2f}[/{color}]"
                        else:
                            who = "[dim]unknown[/dim]"
                            conf_str = ""
                        rows.append((ts, who, conf_str))
                    buf = []
                    in_speech = False
                    silent_count = 0

    with Live(make_table(), refresh_per_second=4, console=console) as live:
        id_thread = threading.Thread(target=identify_loop, daemon=True)
        id_thread.start()
        try:
            with sd.InputStream(
                samplerate=SAMPLE_RATE_W,
                channels=1,
                dtype="float32",
                blocksize=BLOCK_SIZE_W,
                callback=audio_callback,
                device=mic,
            ):
                while True:
                    _time.sleep(0.1)
                    live.update(make_table())
        except KeyboardInterrupt:
            pass
        finally:
            stopped.set()
            id_thread.join(timeout=2.0)

    console.print("\n[green]Done[/green]")


@app.command()
def laughs(
    audio: list[Path] = typer.Argument(..., help="Audio part files (sorted by name)"),
    top: int = typer.Option(25, "--top", help="How many bursts to print"),
    json_out: Optional[Path] = typer.Option(None, "--json", help="Write ranked results as JSON"),
    threshold: float = typer.Option(0.10, "--threshold", help="Laughter prob threshold"),
    min_len: float = typer.Option(0.5, "--min-len", help="Drop bursts shorter than this (s)"),
    merge_gap: float = typer.Option(1.5, "--merge-gap", help="Merge bursts closer than this (s)"),
    smooth: float = typer.Option(0.5, "--smooth", help="Smoothing window (s)"),
    chunk: float = typer.Option(240.0, "--chunk", help="Inference chunk length (s)"),
    device: str = typer.Option("cpu", "--device", help="cpu or cuda"),
    clips: Optional[Path] = typer.Option(None, "--clips", help="Extract top-N clips into this dir"),
    clip_pad: float = typer.Option(4.0, "--clip-pad", help="Lead-in/out around each clip (s)"),
    context_out: Optional[Path] = typer.Option(
        None, "--context-out", help="Write markdown report of biggest laughs with preceding transcript"
    ),
    context_top: int = typer.Option(
        10, "--context-top", help="How many of the biggest laughs to include in the report"
    ),
    context_seconds: float = typer.Option(
        60.0, "--context-seconds", help="Seconds of transcript before each laugh"
    ),
) -> None:
    """Rank the biggest laughs in session audio (highlight finder)."""
    from .laughs import ScanConfig, bursts_to_dicts, extract_clips, render_table
    from .laughs import render_context_report
    from .laughs import scan as scan_laughs

    missing = [p for p in audio if not p.exists()]
    if missing:
        console.print(f"[red]Audio file(s) not found: {', '.join(str(m) for m in missing)}[/red]")
        raise typer.Exit(1)

    cfg = ScanConfig(
        threshold=threshold,
        min_len=min_len,
        merge_gap=merge_gap,
        smooth_seconds=smooth,
        chunk_seconds=chunk,
        device=device,
    )
    paths = sorted(audio, key=lambda p: p.name)
    bursts = scan_laughs(paths, cfg, log=lambda m: console.print(m, style="dim"))

    if json_out:
        import json as _json

        json_out.write_text(_json.dumps(bursts_to_dicts(bursts), indent=2))
        console.print(f"[green]Wrote {len(bursts)} bursts to {json_out}[/green]")

    if clips:
        console.print(f"Extracting top {top} clips to {clips} ...")
        extract_clips(
            bursts, paths, clips, top, clip_pad, log=lambda m: console.print(m, style="dim")
        )

    if context_out:
        console.print(f"Writing transcript-context report to {context_out} ...")
        report = render_context_report(
            bursts, paths, context_top, context_seconds, log=lambda m: console.print(m, style="dim")
        )
        context_out.write_text(report)
        console.print(f"[green]Wrote {context_out}[/green]")

    print(render_table(bursts, top))


if __name__ == "__main__":
    app()
