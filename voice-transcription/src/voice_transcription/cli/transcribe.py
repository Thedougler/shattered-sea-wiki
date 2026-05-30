"""CLI entry point for live session transcription — TUI + teleprompter WebUI.

Delegates to the operator CLI (``voice_transcription.cli.operator:main``),
which provides the Textual TUI control panel and read-only teleprompter WebUI.
"""

from __future__ import annotations

from .operator import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
