"""Track reading progress through a known teleprompter script via ASR word matching.

Pure logic — no ML, no audio. Given a script text and incrementally-arriving
recognized words, advances a monotonic pointer through the script tokens.
The NiceGUI UI uses this to grey out words as they are spoken and recognized.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PUNCT = re.compile(r"[.,!?;:\"'‘’“”—–\-\(\)]")
LOOKAHEAD_WINDOW = 10


@dataclass(frozen=True)
class TrackerState:
    matched_up_to: int
    total_tokens: int


def _normalize(word: str) -> str:
    return _PUNCT.sub("", word).lower()


class ScriptTracker:
    def __init__(self, script_text: str) -> None:
        self._raw_tokens: list[str] = script_text.split() if script_text.strip() else []
        self._norm_tokens: list[str] = [_normalize(w) for w in self._raw_tokens]
        self._matched_up_to: int = -1

    @property
    def raw_tokens(self) -> list[str]:
        return list(self._raw_tokens)

    @property
    def norm_tokens(self) -> list[str]:
        return list(self._norm_tokens)

    @property
    def state(self) -> TrackerState:
        return TrackerState(
            matched_up_to=self._matched_up_to,
            total_tokens=len(self._raw_tokens),
        )

    def extend_script(self, new_text: str) -> None:
        if not new_text.strip():
            return
        new_raw = new_text.split()
        self._raw_tokens.extend(new_raw)
        self._norm_tokens.extend(_normalize(w) for w in new_raw)

    def advance(self, recognized_words: list[str]) -> TrackerState:
        for word in recognized_words:
            norm = _normalize(word)
            if not norm:
                continue
            search_start = self._matched_up_to + 1
            search_end = min(search_start + LOOKAHEAD_WINDOW, len(self._norm_tokens))
            for i in range(search_start, search_end):
                if self._norm_tokens[i] == norm:
                    self._matched_up_to = i
                    break
        return self.state
