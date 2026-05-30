"""CLI entry point for the voice profiler — TUI + teleprompter WebUI."""

from __future__ import annotations

import argparse
import os
import sys
import threading
import time
import webbrowser


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI wiring
    parser = argparse.ArgumentParser(description="Voice-profiler: TUI + teleprompter.")
    parser.add_argument("--name", required=True, help="Character voice name (e.g. Grigori).")
    parser.add_argument("--player", required=True, help="Physical player performing the voice.")
    parser.add_argument("--script-file", default=None, help="Override teleprompter text file.")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)

    from ..core.profiler_core import load_script
    from ..core.script_buffer import ScriptBuffer
    from ..core.script_tracker import ScriptTracker
    from ..core.session_orchestrator import SessionOrchestrator

    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    assets_dir = os.path.join(project_root, "assets", "teleprompter")
    profiles_dir = os.path.join(project_root, "profiles")
    sessions_dir = os.path.join(
        os.path.dirname(os.path.dirname(project_root)), "wiki", "sessions"
    )

    script_text = load_script(args.script_file, assets_dir)

    buf = ScriptBuffer(script_text)
    tracker = ScriptTracker(script_text)
    orchestrator = SessionOrchestrator(
        script_buffer=buf,
        script_tracker=tracker,
    )

    from ..app.teleprompter_ui import run_teleprompter

    webui_thread = threading.Thread(
        target=run_teleprompter,
        args=(orchestrator,),
        kwargs={"port": args.port},
        daemon=True,
    )
    webui_thread.start()
    url = f"http://localhost:{args.port}"
    sys.stderr.write(f"Teleprompter WebUI: {url}\n")

    def _open_browser():
        time.sleep(1.5)
        webbrowser.open(url)

    threading.Thread(target=_open_browser, daemon=True).start()

    from ..app.profiler_tui import run_profiler_tui

    run_profiler_tui(
        orchestrator,
        name=args.name,
        player=args.player,
        profiles_dir=profiles_dir,
        sessions_dir=sessions_dir,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
