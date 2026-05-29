#!/usr/bin/env python3
"""CLI entry point for live session transcription.

Thin wrapper over ``run_loop.main`` so the documented command line
(``transcribe_session.py --session N --speakers M``) matches the file name. All
orchestration lives in ``run_loop`` (unit-tested with fakes); the real model/mic
wiring lives in ``adapters.build_live_deps``.
"""

from __future__ import annotations

from run_loop import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
