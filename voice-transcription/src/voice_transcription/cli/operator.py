"""CLI entry point for the combined operator TUI + teleprompter WebUI."""

from __future__ import annotations

import argparse
import os
import sys
import threading


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI wiring
    parser = argparse.ArgumentParser(
        description="Voice session: operator TUI + teleprompter WebUI.",
    )
    parser.add_argument("--port", type=int, default=8080, help="WebUI port (default: 8080).")
    parser.add_argument("--script-file", default=None, help="Override teleprompter script file.")
    parser.add_argument("--session", type=int, default=None, help="Session number.")
    parser.add_argument("--speakers", type=int, default=None, help="Known physical speaker count.")
    parser.add_argument("--wiki", default="wiki", help="Wiki root directory.")
    parser.add_argument("--profiles-dir", default=None, help="Voice profiles directory.")
    args = parser.parse_args(argv)

    from ..core.config import load_llm_config
    from ..core.llm_client import OpenRouterClient
    from ..core.profiler_core import load_script
    from ..core.script_buffer import ScriptBuffer
    from ..core.script_tracker import ScriptTracker
    from ..core.session_orchestrator import SessionOrchestrator

    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    assets_dir = os.path.join(project_root, "assets", "teleprompter")

    env = {**os.environ}
    env_file = os.path.join(os.path.dirname(project_root), ".env")
    if os.path.isfile(env_file):
        with open(env_file) as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    env.setdefault(key.strip(), val.strip())

    script_text = load_script(args.script_file, assets_dir)

    llm_config = load_llm_config(env)
    generator = OpenRouterClient(llm_config) if llm_config.enabled else None

    buf = ScriptBuffer(script_text)
    tracker = ScriptTracker(script_text)
    orchestrator = SessionOrchestrator(
        script_buffer=buf,
        script_tracker=tracker,
        script_generator=generator,
    )

    from ..app.teleprompter_ui import run_teleprompter

    webui_thread = threading.Thread(
        target=run_teleprompter,
        args=(orchestrator,),
        kwargs={"port": args.port},
        daemon=True,
    )
    webui_thread.start()
    sys.stderr.write(f"Teleprompter WebUI: http://localhost:{args.port}\n")

    from ..app.operator_tui import run_operator_tui

    run_operator_tui(orchestrator, port=args.port)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
