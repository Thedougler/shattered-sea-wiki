"""Voice-profiler teleprompter (NiceGUI shell).

Opens a browser teleprompter with per-word spans. While the reader performs the
script, audio is captured server-side and streamed to Parakeet for real-time ASR.
Recognized words are matched against the script via ScriptTracker, greying out
words as they are spoken. On Stop & Save the captured audio is enrolled as a voice
profile.

Bug fixes over the original:
  - Stop & Save uses ``run.io_bound`` so UI feedback works (was a raw daemon thread)
  - Errors surface in the UI and terminal (were silently swallowed)
  - Process exits cleanly after save (was hanging uvicorn)
"""

from __future__ import annotations

import datetime
import os
import queue
import signal
import sys

_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
PROFILES_DIR = os.path.join(_PROJECT_ROOT, "profiles")
SESSIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(_PROJECT_ROOT)), "wiki", "sessions"
)


def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_enroll_status(name: str, player: str, result) -> str:
    """Format enrollment result for display. Pure helper — unit-testable."""
    p = result.profile
    note = ""
    if p.enhanced_spans:
        note = (f" — enhanced with {p.enhanced_spans} corrected span(s) "
                f"from session(s) {p.enhanced_sessions}")
    if result.rejected:
        note += f"; {result.rejected} outlier span(s) rejected"
    return f"Saved profile for {name} ({player}){note}"


def run_app(name: str, player: str, script_text: str, *, sample_rate: int = 16000,
            port: int = 8080) -> None:  # pragma: no cover - UI wiring
    import numpy as np
    import sounddevice as sd
    from nicegui import app, run, ui

    from ..adapters import PYANNOTE_EMBED
    from ..adapters.embedding import PyannoteEmbedder
    from ..core.profiler_core import enroll
    from ..core.script_tracker import ScriptTracker

    captured: list[np.ndarray] = []
    audio_queue: queue.Queue[np.ndarray] = queue.Queue()
    state: dict = {"recording": False, "stream": None, "tracker": None,
                   "streamer": None, "poll_timer": None, "scroll_timer": None}

    def _cleanup_stream() -> None:
        state["recording"] = False
        if state["stream"] is not None:
            try:
                state["stream"].stop()
                state["stream"].close()
            except Exception:
                pass
            state["stream"] = None
        if state["streamer"] is not None:
            try:
                state["streamer"].close()
            except Exception:
                pass
            state["streamer"] = None

    def _start() -> None:
        captured.clear()
        while not audio_queue.empty():
            try:
                audio_queue.get_nowait()
            except queue.Empty:
                break

        tracker = ScriptTracker(script_text)
        state["tracker"] = tracker

        streamer = None
        try:
            from ..adapters.asr import StreamingParakeetAdapter
            status_label.set_text("Loading ASR model...")
            streamer = StreamingParakeetAdapter()
            state["streamer"] = streamer
        except Exception as exc:
            sys.stderr.write(f"ASR model load failed (grey-out disabled): {exc}\n")
            status_label.set_text("Recording (grey-out unavailable — ASR load failed)")

        def callback(indata, frames, time_info, sd_status):
            if state["recording"]:
                chunk = indata[:, 0].copy()
                captured.append(chunk)
                audio_queue.put(chunk)

        stream = sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32",
                                callback=callback)
        stream.start()
        state["stream"] = stream
        state["recording"] = True

        if streamer:
            status_label.set_text("Recording — read the script aloud at a natural pace.")

        def _poll_asr() -> None:
            if not state["recording"] or state["streamer"] is None:
                return
            chunks_fed = 0
            while not audio_queue.empty() and chunks_fed < 50:
                try:
                    chunk = audio_queue.get_nowait()
                    state["streamer"].add_audio([float(x) for x in chunk])
                    chunks_fed += 1
                except queue.Empty:
                    break
                except Exception:
                    break
            try:
                words = state["streamer"].finalized_words()
                if words and state["tracker"] is not None:
                    s = state["tracker"].advance(words)
                    if s.matched_up_to >= 0:
                        ui.run_javascript(f'''
                            for (let i = 0; i <= {s.matched_up_to}; i++) {{
                                const el = document.getElementById("word-" + i);
                                if (el) el.classList.add("read");
                            }}
                        ''')
            except Exception:
                pass

        def _auto_scroll() -> None:
            if state["tracker"] is None:
                return
            s = state["tracker"].state
            if s.matched_up_to >= 0:
                ui.run_javascript(f'''
                    const el = document.getElementById("word-{s.matched_up_to}");
                    if (el) el.scrollIntoView({{behavior: "smooth", block: "center"}});
                ''')

        state["poll_timer"] = ui.timer(0.3, _poll_asr)
        state["scroll_timer"] = ui.timer(0.5, _auto_scroll)

    async def _stop() -> None:
        if state["poll_timer"] is not None:
            state["poll_timer"].active = False
        if state["scroll_timer"] is not None:
            state["scroll_timer"].active = False
        _cleanup_stream()

        if not captured:
            status_label.set_text("No audio captured. Try again.")
            return

        status_label.set_text("Saving profile...")
        audio = np.concatenate(captured).astype("float32")

        def _save_sync():
            return enroll(
                name=name, player=player, audio=[float(x) for x in audio],
                sample_rate=sample_rate, embedder=PyannoteEmbedder(),
                profiles_dir=PROFILES_DIR, model_id=PYANNOTE_EMBED,
                now_utc=_now_utc(), sessions_dir=SESSIONS_DIR,
            )

        try:
            result = await run.io_bound(_save_sync)
            msg = format_enroll_status(name, player, result)
            status_label.set_text(msg)
            ui.notify(msg, type="positive")
            sys.stderr.write(msg + "\n")
            ui.timer(2.0, app.shutdown, once=True)
        except Exception as exc:
            err = f"Save failed: {exc}"
            status_label.set_text(err)
            ui.notify(err, type="negative")
            sys.stderr.write(err + "\n")

    @ui.page("/")
    def index() -> None:
        nonlocal status_label
        ui.label(f"Voice Profile — {name} ({player})").classes("text-2xl font-bold")
        ui.add_head_html("""<style>
            .teleprompter { overflow-y: auto; scroll-behavior: smooth; }
            .word-span { transition: color 0.3s; }
            .word-span.read { color: #9ca3af; }
        </style>""")
        with ui.column().classes("w-full items-center"):
            with ui.column().classes(
                "teleprompter w-2/3 overflow-y-auto text-3xl leading-relaxed text-center"
            ).style("height: 60vh"):
                tokens = script_text.split() if script_text.strip() else []
                paragraphs = script_text.split("\n\n") if script_text.strip() else []
                word_idx = 0
                for para in paragraphs:
                    with ui.element("p").classes("mb-8"):
                        para_words = para.split()
                        for i, word in enumerate(para_words):
                            ui.html(
                                f'<span id="word-{word_idx}" class="word-span">{word}</span>'
                            ).classes("inline")
                            if i < len(para_words) - 1:
                                ui.html('<span>&nbsp;</span>').classes("inline")
                            word_idx += 1
        with ui.row():
            ui.button("Start", on_click=_start).props("color=primary")
            ui.button("Stop & Save", on_click=_stop).props("color=negative")
        status_label = ui.label("Ready. Click Start, then read aloud.").classes("text-lg")

    status_label = None

    def _sigint_handler(sig, frame):
        sys.stderr.write("\nInterrupted — cleaning up.\n")
        _cleanup_stream()
        app.shutdown()

    signal.signal(signal.SIGINT, _sigint_handler)
    signal.signal(signal.SIGTERM, _sigint_handler)

    ui.run(port=port, title=f"Voice Profile — {name}", reload=False)
