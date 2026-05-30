"""Profiler TUI — terminal control panel for voice profile enrollment.

Shows profile name/player, recording status, script progress, and enrollment
results. Keybindings: S=Start, V=Stop & Save, Q=Quit. Designed to pair with
the read-only teleprompter WebUI on a separate screen.
"""

from __future__ import annotations

import datetime
import queue
import sys
import time
from typing import TYPE_CHECKING

from .operator_tui import format_elapsed, format_script_preview

if TYPE_CHECKING:
    from ..core.session_orchestrator import SessionOrchestrator


def format_profiler_status(
    *,
    name: str,
    player: str,
    status: str,
    matched: int,
    total: int,
    save_result: str | None,
) -> str:
    status_label = {
        "recording": "Recording",
        "idle": "Idle",
        "saving": "Saving profile...",
    }.get(status, status.capitalize())
    line = (
        f"Profile: {name} ({player})  |  "
        f"STATUS: {status_label}  |  "
        f"Script: {matched}/{total} tokens"
    )
    if save_result:
        line += f"\n{save_result}"
    return line


def run_profiler_tui(  # pragma: no cover - TUI wiring
    orchestrator: SessionOrchestrator,
    *,
    name: str,
    player: str,
    sample_rate: int = 16000,
    profiles_dir: str,
    sessions_dir: str,
) -> None:
    from textual.app import App, ComposeResult
    from textual.containers import Vertical
    from textual.widgets import Footer, Header, Static

    import numpy as np
    import sounddevice as sd

    class ProfilerApp(App):
        BINDINGS = [
            ("s", "start_recording", "Start"),
            ("v", "save_profile", "Stop & Save"),
            ("q", "quit", "Quit"),
        ]
        CSS = """
        #status { height: 5; padding: 0 1; }
        #script { height: 1fr; padding: 0 1; border-top: solid green; }
        """

        def __init__(self) -> None:
            super().__init__()
            self._start_time: float | None = None
            self._save_result: str | None = None
            self._captured: list[np.ndarray] = []
            self._audio_queue: queue.Queue[np.ndarray] = queue.Queue()
            self._stream: sd.InputStream | None = None
            self._streamer = None

        def compose(self) -> ComposeResult:
            yield Header()
            with Vertical():
                yield Static("Initializing...", id="status")
                yield Static("Script preview loading...", id="script")
            yield Footer()

        def on_mount(self) -> None:
            self.title = f"Voice Profile — {name}"
            self.set_interval(0.5, self._refresh_display)
            self.set_interval(0.3, self._poll_asr)

        def _refresh_display(self) -> None:
            snap = orchestrator.snapshot()
            elapsed = ""
            if self._start_time is not None:
                elapsed = f"  {format_elapsed(int(time.time() - self._start_time))}"

            status_widget = self.query_one("#status", Static)
            status_widget.update(
                format_profiler_status(
                    name=name, player=player,
                    status=snap["status"],
                    matched=snap["matched_up_to"],
                    total=snap["total_tokens"],
                    save_result=self._save_result,
                ) + elapsed
            )

            tokens = snap["full_text"].split() if snap["full_text"].strip() else []
            script_widget = self.query_one("#script", Static)
            script_widget.update(
                "--- Script ---\n"
                + format_script_preview(tokens, snap["matched_up_to"], context=8)
            )

        def _poll_asr(self) -> None:
            if not orchestrator.is_recording or self._streamer is None:
                return
            chunks_fed = 0
            while not self._audio_queue.empty() and chunks_fed < 50:
                try:
                    chunk = self._audio_queue.get_nowait()
                    self._streamer.add_audio([float(x) for x in chunk])
                    chunks_fed += 1
                except queue.Empty:
                    break
                except Exception:
                    break
            try:
                words = self._streamer.finalized_words()
                if words:
                    orchestrator._tracker.advance(words)
            except Exception:
                pass

        def _cleanup_stream(self) -> None:
            orchestrator.stop()
            if self._stream is not None:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception:
                    pass
                self._stream = None
            if self._streamer is not None:
                try:
                    self._streamer.close()
                except Exception:
                    pass
                self._streamer = None

        def action_start_recording(self) -> None:
            if orchestrator.is_recording:
                return
            self._captured.clear()
            while not self._audio_queue.empty():
                try:
                    self._audio_queue.get_nowait()
                except queue.Empty:
                    break

            self._save_result = None

            try:
                from ..adapters.asr import StreamingParakeetAdapter
                self._streamer = StreamingParakeetAdapter()
            except Exception as exc:
                sys.stderr.write(f"ASR load failed (grey-out disabled): {exc}\n")

            def callback(indata, frames, time_info, sd_status):
                if orchestrator.is_recording:
                    chunk = indata[:, 0].copy()
                    self._captured.append(chunk)
                    self._audio_queue.put(chunk)

            self._stream = sd.InputStream(
                samplerate=sample_rate, channels=1, dtype="float32",
                callback=callback,
            )
            self._stream.start()
            orchestrator.start()
            self._start_time = time.time()

        def action_save_profile(self) -> None:
            if not orchestrator.is_recording and not self._captured:
                return
            self._cleanup_stream()

            if not self._captured:
                self._save_result = "No audio captured."
                return

            self._save_result = "Saving..."
            audio = np.concatenate(self._captured).astype("float32")

            def _do_save():
                from ..adapters import PYANNOTE_EMBED
                from ..adapters.embedding import PyannoteEmbedder
                from ..core.profiler_core import enroll, format_enroll_status

                now_utc = datetime.datetime.now(
                    datetime.timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                result = enroll(
                    name=name, player=player,
                    audio=[float(x) for x in audio],
                    sample_rate=sample_rate,
                    embedder=PyannoteEmbedder(),
                    profiles_dir=profiles_dir,
                    model_id=PYANNOTE_EMBED,
                    now_utc=now_utc,
                    sessions_dir=sessions_dir,
                )
                return format_enroll_status(name, player, result)

            try:
                msg = _do_save()
                self._save_result = msg
                sys.stderr.write(msg + "\n")
            except Exception as exc:
                self._save_result = f"Save failed: {exc}"
                sys.stderr.write(self._save_result + "\n")

    app = ProfilerApp()
    app.run()
