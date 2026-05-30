import re
from html import escape

from nicegui import ui


def _normalize(word: str) -> str:
    return re.sub(r"[^a-z0-9']", '', word.lower())


class Teleprompter:
    LOOKAHEAD = 5

    def __init__(self, script_text: str = ''):
        self._script_words: list[str] = script_text.split() if script_text else []
        self._cursor = 0
        self._insertions: dict[int, list[str]] = {}
        self._prev_finalized_count = 0
        self._script_element: ui.html | None = None
        self._raw_element: ui.html | None = None

    def render_script(self, container_style: str = ''):
        outer = ui.column().classes('w-full scroll-hidden').style(container_style)
        with outer:
            self._script_element = ui.html('').classes('teleprompter-text')
            self._refresh()
            ui.element('div').style('height: 50vh')
        return outer

    def render_raw_output(self, container_style: str = ''):
        container = ui.column().classes('w-full').style(container_style)
        with container:
            self._raw_element = ui.html('').classes('raw-output')
        return container

    def update_from_asr(self, finalized_text: str, draft_text: str):
        finalized_words = finalized_text.split() if finalized_text else []

        for word in finalized_words[self._prev_finalized_count:]:
            idx = self._match_word(word, self._cursor)
            if idx >= 0:
                self._cursor = idx + 1
            else:
                self._insertions.setdefault(self._cursor, []).append(word)

        self._prev_finalized_count = len(finalized_words)

        draft_words = draft_text.split() if draft_text else []
        draft_cursor = self._cursor
        draft_ins: dict[int, list[str]] = {}
        for word in draft_words:
            idx = self._match_word(word, draft_cursor)
            if idx >= 0:
                draft_cursor = idx + 1
            else:
                draft_ins.setdefault(draft_cursor, []).append(word)

        self._refresh(draft_cursor, draft_ins)

    def update_raw(self, finalized: str = '', draft: str = ''):
        if not self._raw_element:
            return
        parts = []
        if finalized:
            parts.append(f'<span class="finalized">{escape(finalized)}</span>')
        if draft:
            parts.append(f' <span class="draft-text">{escape(draft)}</span>')
        self._raw_element.content = ''.join(parts) or '&nbsp;'

    @property
    def word_count(self) -> int:
        return len(self._script_words)

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def progress(self) -> float:
        return self._cursor / max(1, len(self._script_words))

    def append_words(self, text: str) -> int:
        new_words = text.split()
        self._script_words.extend(new_words)
        self._refresh()
        return len(new_words)

    def set_script(self, text: str):
        self._script_words = text.split() if text else []
        self._cursor = 0
        self._insertions = {}
        self._prev_finalized_count = 0
        self._refresh()

    def reset(self):
        self._cursor = 0
        self._insertions = {}
        self._prev_finalized_count = 0
        self._refresh()
        if self._raw_element:
            self._raw_element.content = ''

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

    def _refresh(self, draft_cursor: int = -1, draft_ins: dict | None = None):
        if not self._script_element:
            return

        if draft_cursor < 0:
            draft_cursor = self._cursor
        if draft_ins is None:
            draft_ins = {}

        parts: list[str] = []
        cursor_id_set = False

        for i, word in enumerate(self._script_words):
            for off in self._insertions.get(i, []):
                parts.append(f'<span class="offscript">({escape(off)}) </span>')
            for off in draft_ins.get(i, []):
                parts.append(
                    f'<span class="offscript draft">({escape(off)}) </span>'
                )

            if i < self._cursor:
                cls = 'spoken'
            elif i < draft_cursor:
                cls = 'draft'
            elif i == draft_cursor and not cursor_id_set:
                cls = 'current'
                parts.append(
                    f'<span id="tw-cursor" class="{cls}">{escape(word)} </span>'
                )
                cursor_id_set = True
                continue
            else:
                cls = ''
            parts.append(f'<span class="{cls}">{escape(word)} </span>')

        end = len(self._script_words)
        for off in self._insertions.get(end, []):
            parts.append(f'<span class="offscript">({escape(off)}) </span>')
        for off in draft_ins.get(end, []):
            parts.append(
                f'<span class="offscript draft">({escape(off)}) </span>'
            )

        self._script_element.content = ''.join(parts)

        if cursor_id_set:
            ui.run_javascript('''(() => {
                const el = document.getElementById("tw-cursor");
                if (!el) return;
                const p = el.closest('.scroll-hidden');
                if (!p) { el.scrollIntoView({behavior:"smooth",block:"center"}); return; }
                const y = el.offsetTop - p.clientHeight * 0.35;
                p.scrollTo({top: Math.max(0, y), behavior: "smooth"});
            })()''')
