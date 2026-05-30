"""Operator TUI — terminal control panel for voice recording sessions.

Shows status dashboard, script preview around current position, live transcript
tail, and keybindings (S=start, P=pause, Q=quit). Drives the recording pipeline
and launches the teleprompter WebUI in a background thread.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.session_orchestrator import SessionOrchestrator


def format_elapsed(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def format_status_line(
    *,
    status: str,
    matched: int,
    total: int,
    profiles_loaded: int,
    llm_enabled: bool,
) -> str:
    status_label = {"recording": "Recording", "idle": "Idle", "extending": "Extending script..."}.get(
        status, status.capitalize()
    )
    llm_label = "LLM: on" if llm_enabled else "LLM: off"
    return (
        f"STATUS: {status_label}  |  "
        f"Script: {matched}/{total} tokens  |  "
        f"Profiles: {profiles_loaded}  |  "
        f"{llm_label}"
    )


def format_script_preview(
    tokens: list[str], matched_up_to: int, context: int = 5,
) -> str:
    if not tokens:
        return ""
    start = max(0, matched_up_to - context)
    end = min(len(tokens), matched_up_to + context + 1)
    parts: list[str] = []
    if start > 0:
        parts.append("...")
    for i in range(start, end):
        if i == matched_up_to + 1:
            parts.append(f"▶ {tokens[i]}")
        else:
            parts.append(tokens[i])
    if end < len(tokens):
        parts.append("...")
    return " ".join(parts)


def run_operator_tui(orchestrator: SessionOrchestrator, *, port: int = 8080) -> None:  # pragma: no cover
    from textual.app import App, ComposeResult
    from textual.containers import Vertical
    from textual.widgets import Footer, Header, Static

    class OperatorApp(App):
        BINDINGS = [
            ("s", "start_recording", "Start"),
            ("p", "pause_recording", "Pause"),
            ("q", "quit", "Quit"),
        ]
        CSS = """
        #status { height: 3; padding: 0 1; }
        #script { height: 1fr; padding: 0 1; border-top: solid green; }
        #transcript { height: 1fr; padding: 0 1; border-top: solid cyan; }
        """

        def __init__(self) -> None:
            super().__init__()
            self._start_time: float | None = None
            self._transcript_lines: list[str] = []

        def compose(self) -> ComposeResult:
            yield Header()
            with Vertical():
                yield Static("Initializing...", id="status")
                yield Static("Script preview loading...", id="script")
                yield Static("Transcript will appear here...", id="transcript")
            yield Footer()

        def on_mount(self) -> None:
            self.title = "Voice Transcription"
            self.set_interval(0.5, self._refresh_display)

        def _refresh_display(self) -> None:
            snap = orchestrator.snapshot()
            elapsed = ""
            if self._start_time is not None:
                elapsed = f"  {format_elapsed(int(time.time() - self._start_time))}"

            status_widget = self.query_one("#status", Static)
            status_widget.update(
                format_status_line(
                    status=snap["status"],
                    matched=snap["matched_up_to"],
                    total=snap["total_tokens"],
                    profiles_loaded=0,
                    llm_enabled=orchestrator._generator is not None,
                )
                + elapsed
            )

            tokens = snap["full_text"].split() if snap["full_text"].strip() else []
            script_widget = self.query_one("#script", Static)
            script_widget.update(
                "--- Script ---\n"
                + format_script_preview(tokens, snap["matched_up_to"], context=8)
            )

            if self._transcript_lines:
                transcript_widget = self.query_one("#transcript", Static)
                tail = self._transcript_lines[-10:]
                transcript_widget.update("--- Transcript ---\n" + "\n".join(tail))

        def action_start_recording(self) -> None:
            orchestrator.start()
            self._start_time = time.time()

        def action_pause_recording(self) -> None:
            orchestrator.stop()

        def add_transcript_line(self, line: str) -> None:
            self._transcript_lines.append(line)

    app = OperatorApp()
    app.run()
