import re
import time
from html import escape

from nicegui import ui


def _normalize(word: str) -> str:
    return re.sub(r"[^a-z0-9']", "", word.lower())


class Teleprompter:
    LOOKAHEAD = 5
    TARGET_WPM = 130

    def __init__(self, script_text: str = ""):
        self._script_words: list[str] = script_text.split() if script_text else []
        self._matched_pos = 0
        self._display_cursor = 0
        self._word_debt = 0.0
        self._prev_finalized = 0
        self._last_tick = 0.0
        self._script_element: ui.html | None = None
        self._raw_element: ui.html | None = None

    def render_script(self, container_style: str = ""):
        outer = ui.column().classes("w-full scroll-hidden").style(container_style)
        with outer:
            self._script_element = ui.html("").classes("teleprompter-text")
            self._refresh()
            ui.element("div").style("height: 50vh")
        return outer

    def render_raw_output(self, container_style: str = ""):
        container = ui.column().classes("w-full").style(container_style)
        with container:
            self._raw_element = ui.html("").classes("raw-output")
        return container

    def update_from_asr(self, finalized_text: str, draft_text: str):
        finalized = finalized_text.split() if finalized_text else []

        for word in finalized[self._prev_finalized :]:
            idx = self._match_word(word, self._matched_pos)
            if idx >= 0:
                self._matched_pos = idx + 1
        self._prev_finalized = len(finalized)

        now = time.time()
        target = self._matched_pos

        if self._last_tick > 0 and self._display_cursor < target:
            dt = min(now - self._last_tick, 1.0)
            self._word_debt += self.TARGET_WPM / 60 * dt
            advance = min(int(self._word_debt), target - self._display_cursor)
            if advance > 0:
                self._display_cursor += advance
                self._word_debt -= advance
        elif self._last_tick == 0 and target > 0:
            self._display_cursor = target

        if self._display_cursor >= target:
            self._word_debt = 0.0

        self._last_tick = now
        self._refresh()

    def update_raw(self, finalized: str = "", draft: str = ""):
        if not self._raw_element:
            return
        parts = []
        if finalized:
            parts.append(f'<span class="finalized">{escape(finalized)}</span>')
        if draft:
            parts.append(f' <span class="draft-text">{escape(draft)}</span>')
        self._raw_element.content = "".join(parts) or "&nbsp;"

    @property
    def word_count(self) -> int:
        return len(self._script_words)

    @property
    def cursor(self) -> int:
        return self._matched_pos

    @property
    def progress(self) -> float:
        return self._matched_pos / max(1, len(self._script_words))

    def append_words(self, text: str) -> int:
        new_words = text.split()
        self._script_words.extend(new_words)
        self._refresh()
        return len(new_words)

    def set_script(self, text: str):
        self._script_words = text.split() if text else []
        self._matched_pos = 0
        self._display_cursor = 0
        self._word_debt = 0.0
        self._prev_finalized = 0
        self._last_tick = 0.0
        self._refresh()

    def reset(self):
        self._matched_pos = 0
        self._display_cursor = 0
        self._word_debt = 0.0
        self._prev_finalized = 0
        self._last_tick = 0.0
        self._refresh()
        if self._raw_element:
            self._raw_element.content = ""

    def _match_word(self, asr_word: str, start: int) -> int:
        norm = _normalize(asr_word)
        if not norm:
            return -1
        end = min(start + self.LOOKAHEAD, len(self._script_words))
        for i in range(start, end):
            script_norm = _normalize(self._script_words[i])
            if not script_norm:
                continue
            if norm == script_norm:
                return i
            if len(norm) >= 3 and (
                script_norm.startswith(norm) or norm.startswith(script_norm)
            ):
                return i
        return -1

    def _refresh(self):
        if not self._script_element:
            return

        parts: list[str] = []
        cursor_set = False

        for i, word in enumerate(self._script_words):
            if i < self._display_cursor:
                cls = "spoken"
            elif i == self._display_cursor and not cursor_set:
                cls = "current"
                parts.append(
                    f'<span id="tw-cursor" class="{cls}">{escape(word)} </span>'
                )
                cursor_set = True
                continue
            else:
                cls = ""
            parts.append(f'<span class="{cls}">{escape(word)} </span>')

        self._script_element.content = "".join(parts)

        if cursor_set:
            ui.run_javascript("""(() => {
                const el = document.getElementById("tw-cursor");
                if (!el) return;
                const p = el.closest('.scroll-hidden');
                if (!p) { el.scrollIntoView({behavior:"smooth",block:"center"}); return; }
                const y = el.offsetTop - p.clientHeight * 0.35;
                p.scrollTo({top: Math.max(0, y), behavior: "smooth"});
            })()""")
