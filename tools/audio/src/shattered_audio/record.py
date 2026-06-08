"""Multi-microphone session recorder built on ffmpeg + avfoundation.

One ffmpeg process per microphone, each writing a segmented (chunked) AAC/m4a
track. Recording each mic to its own track keeps the DM and players physically
isolated, which the transcribe step exploits for far better speaker separation
than a single mixed feed.

Why ffmpeg instead of a long-running Python audio loop: a 4+ hour D&D session
needs a recorder that does not drift, leak, or die. ffmpeg's segment muxer is
battle-tested for exactly this — it flushes each chunk to disk as it goes, so a
crash at hour 3 still leaves you hours 0-3 of finalized audio.

Output layout (under ``audio/sessions/``)::

    session07/
      manifest.json
      raw/
        mic00/ part000.m4a part001.m4a ...
        mic01/ part000.m4a part001.m4a ...

The pure helpers here (device parsing, command building, mic selection, path
layout, manifest) are unit-tested; :func:`record_session` does the process
orchestration and is exercised by a short real-capture integration test.
"""

from __future__ import annotations

import json
import logging
import re
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
DEFAULT_BITRATE = "64k"
DEFAULT_SEGMENT_MINUTES = 15

# Matches `[AVFoundation indev @ 0x...] [1] EMEET OfficeCore M0 Plus`
_DEVICE_LINE = re.compile(r"\[AVFoundation indev[^\]]*\]\s*\[(\d+)\]\s*(.+?)\s*$")
_AUDIO_HEADER = re.compile(r"AVFoundation audio devices:")
_VIDEO_HEADER = re.compile(r"AVFoundation video devices:")


@dataclass
class RecordMic:
    """A microphone selected for recording.

    ``index`` is the avfoundation audio-device index (what ffmpeg's ``-i``
    needs). ``mic_id`` is positional within the selection (mic00, mic01, ...)
    and is what shows up in the output path and manifest.
    """

    index: int
    name: str
    mic_id: str
    speaker: str | None = None


def parse_avfoundation_devices(stderr: str) -> list[dict]:
    """Parse audio input devices from ffmpeg's ``-list_devices`` stderr.

    ffmpeg prints video devices and audio devices under separate headers, each
    using ``[N]`` indices that restart at 0. We only want the audio block.
    """
    devices: list[dict] = []
    in_audio = False
    for line in stderr.splitlines():
        if _AUDIO_HEADER.search(line):
            in_audio = True
            continue
        if _VIDEO_HEADER.search(line):
            in_audio = False
            continue
        if not in_audio:
            continue
        m = _DEVICE_LINE.search(line)
        if m:
            devices.append({"index": int(m.group(1)), "name": m.group(2)})
    return devices


def list_avfoundation_devices(ffmpeg: str = "ffmpeg") -> list[dict]:
    """Query the OS for avfoundation audio input devices."""
    proc = subprocess.run(
        [ffmpeg, "-hide_banner", "-f", "avfoundation", "-list_devices", "true", "-i", ""],
        capture_output=True,
        text=True,
    )
    # ffmpeg exits non-zero after listing (it has no real input) — that's normal.
    return parse_avfoundation_devices(proc.stderr)


def select_mics(
    devices: list[dict],
    indices: list[int] | None = None,
    names: list[str] | None = None,
) -> list[RecordMic]:
    """Choose which devices to record.

    Priority: explicit ``indices`` → ``names`` substring match → all devices.
    Unknown indices and unmatched names are skipped (a warning, not a crash).
    """
    by_index = {d["index"]: d for d in devices}

    chosen: list[dict] = []
    if indices is not None:
        for idx in indices:
            if idx in by_index:
                chosen.append(by_index[idx])
            else:
                logger.warning("Requested mic index %s not found — skipping", idx)
    elif names:
        for name in names:
            name_lower = name.lower()
            match = next(
                (d for d in devices if name_lower in d["name"].lower() and d not in chosen),
                None,
            )
            if match:
                chosen.append(match)
            else:
                logger.warning("No mic matching %r — skipping", name)
    else:
        chosen = list(devices)

    return [
        RecordMic(index=d["index"], name=d["name"], mic_id=f"mic{i:02d}")
        for i, d in enumerate(chosen)
    ]


def session_dir(audio_dir: Path, session: int) -> Path:
    return audio_dir / f"session{session:02d}"


def raw_mic_dir(audio_dir: Path, session: int, mic: RecordMic) -> Path:
    return session_dir(audio_dir, session) / "raw" / mic.mic_id


def build_ffmpeg_command(
    device_index: int,
    out_pattern: Path,
    segment_seconds: int,
    sample_rate: int = SAMPLE_RATE,
    bitrate: str = DEFAULT_BITRATE,
    ffmpeg: str = "ffmpeg",
) -> list[str]:
    """Build the ffmpeg argv for one mic: avfoundation in → segmented m4a out.

    - ``-i :N`` selects avfoundation *audio* device N (the leading colon means
      "no video, audio index N").
    - downmix to mono 16 kHz — whisper's native rate, and tiny on disk.
    - segment muxer with ``reset_timestamps`` so each chunk starts at t=0,
      which is exactly what the per-part CSV timeline expects.
    """
    return [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "warning",
        "-f",
        "avfoundation",
        "-i",
        f":{device_index}",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-c:a",
        "aac",
        "-b:a",
        bitrate,
        "-f",
        "segment",
        "-segment_time",
        str(segment_seconds),
        "-reset_timestamps",
        "1",
        str(out_pattern),
    ]


def build_manifest(
    session: int,
    mics: list[RecordMic],
    segment_seconds: int,
    started_at: str | None = None,
) -> dict:
    """Serializable description of the recording for the transcribe step."""
    return {
        "session": session,
        "segment_seconds": segment_seconds,
        "sample_rate": SAMPLE_RATE,
        "started_at": started_at,
        "mics": [
            {"mic_id": m.mic_id, "index": m.index, "name": m.name, "speaker": m.speaker}
            for m in mics
        ],
    }


def _spawn(mic: RecordMic, out_pattern: Path, segment_seconds: int, ffmpeg: str) -> subprocess.Popen:
    out_pattern.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_ffmpeg_command(mic.index, out_pattern, segment_seconds, ffmpeg=ffmpeg)
    logger.info("Recording %s (avfoundation :%s) → %s", mic.mic_id, mic.index, out_pattern.parent)
    # stdin=PIPE lets us send 'q' for a clean ffmpeg shutdown that finalizes the
    # current segment's moov atom (a hard kill can leave a truncated m4a).
    return subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


def _stop(proc: subprocess.Popen) -> None:
    """Ask ffmpeg to stop gracefully, then escalate if it ignores us."""
    if proc.poll() is not None:
        return
    try:
        if proc.stdin:
            proc.stdin.write(b"q")
            proc.stdin.flush()
    except (BrokenPipeError, OSError):
        pass
    try:
        proc.wait(timeout=5)
        return
    except subprocess.TimeoutExpired:
        pass
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def record_session(
    session: int,
    mics: list[RecordMic],
    audio_dir: Path,
    segment_seconds: int,
    *,
    max_seconds: float | None = None,
    ffmpeg: str = "ffmpeg",
    on_ready=None,
) -> Path:
    """Record all ``mics`` until interrupted (or ``max_seconds`` elapses).

    Returns the session directory. Writes ``manifest.json`` up front so the
    transcribe step can run even if recording is cut short. Stops cleanly on
    SIGINT/SIGTERM so the controlling agent can end the session on command.
    """
    sdir = session_dir(audio_dir, session)
    sdir.mkdir(parents=True, exist_ok=True)

    started_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    manifest = build_manifest(session, mics, segment_seconds, started_at=started_at)
    (sdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    procs: list[tuple[RecordMic, subprocess.Popen]] = []
    for mic in mics:
        out_pattern = raw_mic_dir(audio_dir, session, mic) / "part%03d.m4a"
        procs.append((mic, _spawn(mic, out_pattern, segment_seconds, ffmpeg)))

    stop_event = threading.Event()

    def _handle(signum, _frame):
        logger.info("Received signal %s — stopping recording", signum)
        stop_event.set()

    prev_int = signal.getsignal(signal.SIGINT)
    prev_term = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, _handle)
    signal.signal(signal.SIGTERM, _handle)

    if on_ready:
        on_ready(procs)

    start = time.monotonic()
    try:
        while not stop_event.is_set():
            # Bail out if every recorder died (bad device, disk full, ...).
            if all(p.poll() is not None for _, p in procs):
                logger.error("All ffmpeg recorders exited unexpectedly")
                break
            if max_seconds is not None and time.monotonic() - start >= max_seconds:
                break
            time.sleep(0.25)
    finally:
        signal.signal(signal.SIGINT, prev_int)
        signal.signal(signal.SIGTERM, prev_term)
        for mic, proc in procs:
            _stop(proc)
            if proc.returncode not in (0, None):
                err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
                if err.strip():
                    logger.warning("%s ffmpeg stderr: %s", mic.mic_id, err.strip()[-500:])

    return sdir
