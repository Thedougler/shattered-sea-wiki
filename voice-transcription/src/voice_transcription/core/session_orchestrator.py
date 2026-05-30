"""Coordinates recording state, script tracking, and LLM-driven script extension."""

from __future__ import annotations

import sys
from typing import Any

from .script_buffer import ScriptBuffer
from .script_tracker import ScriptTracker


class SessionOrchestrator:
    def __init__(
        self,
        *,
        script_buffer: ScriptBuffer,
        script_tracker: ScriptTracker,
        script_generator: Any | None = None,
        extension_lookahead: int = 200,
    ) -> None:
        self._buffer = script_buffer
        self._tracker = script_tracker
        self._generator = script_generator
        self._lookahead = extension_lookahead
        self._recording = False
        self._extending = False

    @property
    def is_recording(self) -> bool:
        return self._recording

    @property
    def status(self) -> str:
        if self._extending:
            return "extending"
        return "recording" if self._recording else "idle"

    def start(self) -> None:
        self._recording = True

    def stop(self) -> None:
        self._recording = False

    async def extend_if_needed(self) -> None:
        if self._generator is None:
            return
        state = self._tracker.state
        if not self._buffer.needs_extension(state.matched_up_to, self._lookahead):
            return
        self._extending = True
        try:
            new_text = await self._generator.generate(self._buffer.full_text)
            self._buffer.extend(new_text)
            self._tracker.extend_script(new_text)
        except Exception as exc:
            sys.stderr.write(f"Script extension failed: {exc}\n")
        finally:
            self._extending = False

    def snapshot(self) -> dict[str, Any]:
        state = self._tracker.state
        return {
            "matched_up_to": state.matched_up_to,
            "total_tokens": state.total_tokens,
            "status": self.status,
            "full_text": self._buffer.full_text,
            "is_recording": self._recording,
        }
