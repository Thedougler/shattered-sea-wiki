#!/usr/bin/env python3
"""Voice-profiler teleprompter (NiceGUI shell).

Opens a browser teleprompter that auto-scrolls a funny, phonetically-rich script
for one character voice. While the reader performs it, audio is captured from the
local mic (server-side ``sounddevice``); on Stop the capture is turned into a
saved voice profile via ``profiler_core.enroll``.

This module is a thin presentation/capture shell — all real logic lives in the
unit-tested ``profiler_core``. NiceGUI + sounddevice are imported lazily so the
pure test suite never needs them. Best-practice notes:
  - The teleprompter view uses a large, high-contrast, centered column with a CSS
    auto-scroll the reader can pause; a quiet room and a decent mic give the
    cleanest embedding (see references/setup.md).
  - Capture runs on a background thread into a bounded buffer; the UI only starts
    and stops it.

Usage:
    python3 voice_profiler.py --name "Grigori" --player "Dave" [--script-file X] [--port 8080]
"""

from __future__ import annotations

import argparse
import datetime
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SKILL_DIR, "assets", "teleprompter")
PROFILES_DIR = os.path.join(SKILL_DIR, "profiles")
# .claude/skills/live-co-dm -> repo root -> wiki/sessions (corrected transcripts + .live audio).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SKILL_DIR)))
SESSIONS_DIR = os.path.join(REPO_ROOT, "wiki", "sessions")


def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_app(name: str, player: str, script_text: str, *, sample_rate: int = 16000,
            port: int = 8080) -> None:  # pragma: no cover - UI wiring
    import threading

    import numpy as np
    import sounddevice as sd
    from nicegui import app, ui

    from adapters import PYANNOTE_EMBED, PyannoteEmbedder
    from profiler_core import enroll

    captured: list[np.ndarray] = []
    state = {"recording": False, "stream": None}

    def _start() -> None:
        captured.clear()

        def callback(indata, frames, time_info, status):
            if state["recording"]:
                captured.append(indata[:, 0].copy())

        stream = sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32",
                                callback=callback)
        stream.start()
        state["stream"] = stream
        state["recording"] = True
        status_label.set_text("● Recording — read the script aloud at a natural pace.")

    def _stop() -> None:
        state["recording"] = False
        if state["stream"] is not None:
            state["stream"].stop()
            state["stream"].close()
            state["stream"] = None
        if not captured:
            status_label.set_text("No audio captured. Try again.")
            return
        audio = np.concatenate(captured).astype("float32")
        threading.Thread(target=_save, args=(audio,), daemon=True).start()

    def _save(audio) -> None:
        result = enroll(
            name=name, player=player, audio=[float(x) for x in audio],
            sample_rate=sample_rate, embedder=PyannoteEmbedder(), profiles_dir=PROFILES_DIR,
            model_id=PYANNOTE_EMBED, now_utc=_now_utc(), sessions_dir=SESSIONS_DIR,
        )
        p = result.profile
        note = ""
        if p.enhanced_spans:
            note = (f" — enhanced with {p.enhanced_spans} corrected span(s) "
                    f"from session(s) {p.enhanced_sessions}")
        if result.rejected:
            note += f"; {result.rejected} outlier span(s) rejected"
        status_label.set_text(f"Saved profile for {name} ({player}){note}")

    @ui.page("/")
    def index() -> None:
        ui.label(f"Voice Profile — {name} ({player})").classes("text-2xl font-bold")
        with ui.column().classes("w-full items-center"):
            scroller = ui.column().classes(
                "teleprompter w-2/3 h-96 overflow-hidden text-3xl leading-relaxed text-center"
            )
            with scroller:
                for para in script_text.split("\n\n"):
                    ui.label(para).classes("mb-8")
            ui.add_head_html(
                "<style>.teleprompter{animation:scroll 90s linear forwards}"
                "@keyframes scroll{from{transform:translateY(40%)}to{transform:translateY(-100%)}}</style>"
            )
        with ui.row():
            ui.button("Start", on_click=_start).props("color=primary")
            ui.button("Stop & Save", on_click=_stop).props("color=negative")
        global status_label
        status_label = ui.label("Ready. Click Start, then read aloud.").classes("text-lg")

    ui.run(port=port, title=f"Voice Profile — {name}", reload=False)


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI wiring
    parser = argparse.ArgumentParser(description="Voice-profiler teleprompter.")
    parser.add_argument("--name", required=True, help="Character voice name (e.g. Grigori).")
    parser.add_argument("--player", required=True, help="Physical player performing the voice.")
    parser.add_argument("--script-file", default=None, help="Override teleprompter text file.")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    from profiler_core import load_script

    script_text = load_script(args.script_file, ASSETS_DIR)
    run_app(args.name, args.player, script_text, port=args.port)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
