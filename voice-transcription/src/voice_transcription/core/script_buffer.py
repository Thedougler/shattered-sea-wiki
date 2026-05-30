"""Thread-safe growing script text manager for the teleprompter."""

from __future__ import annotations

import threading


class ScriptBuffer:
    def __init__(self, seed_text: str) -> None:
        self._lock = threading.Lock()
        self._text = seed_text
        self._tokens = seed_text.split() if seed_text.strip() else []

    @property
    def full_text(self) -> str:
        with self._lock:
            return self._text

    @property
    def token_count(self) -> int:
        with self._lock:
            return len(self._tokens)

    def extend(self, new_text: str) -> None:
        with self._lock:
            if self._text.strip():
                self._text += "\n\n" + new_text
            else:
                self._text = new_text
            self._tokens.extend(new_text.split())

    def needs_extension(self, matched_up_to: int, lookahead: int = 200) -> bool:
        with self._lock:
            total = len(self._tokens)
            if total == 0:
                return True
            remaining = total - (matched_up_to + 1)
            return remaining < lookahead
