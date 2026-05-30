"""CLI entry point for the voice profiler teleprompter."""

from __future__ import annotations

import argparse
import os


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI wiring
    parser = argparse.ArgumentParser(description="Voice-profiler teleprompter.")
    parser.add_argument("--name", required=True, help="Character voice name (e.g. Grigori).")
    parser.add_argument("--player", required=True, help="Physical player performing the voice.")
    parser.add_argument("--script-file", default=None, help="Override teleprompter text file.")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)

    from ..core.profiler_core import load_script
    from ..app.profiler_ui import run_app

    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    assets_dir = os.path.join(project_root, "assets", "teleprompter")
    script_text = load_script(args.script_file, assets_dir)
    run_app(args.name, args.player, script_text, port=args.port)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
