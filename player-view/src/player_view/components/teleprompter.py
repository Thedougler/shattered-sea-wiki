from nicegui import ui


class Teleprompter:
    def __init__(self, script_text: str = ''):
        self.script_words = script_text.split() if script_text else []
        self.finalized_count = 0
        self.draft_count = 0
        self._script_element: ui.html | None = None
        self._raw_element: ui.html | None = None

    def render_script(self, container_style: str = ''):
        outer = ui.column().classes('w-full scroll-hidden').style(container_style)
        with outer:
            self._script_element = ui.html('').classes('teleprompter-text')
            self._refresh_script()
            ui.element('div').style('height: 50vh')
        return outer

    def render_raw_output(self, container_style: str = ''):
        container = ui.column().classes('w-full').style(container_style)
        with container:
            self._raw_element = ui.html('').classes('raw-output')
        return container

    def _refresh_script(self):
        if not self._script_element:
            return
        parts = []
        frontier = self.finalized_count + self.draft_count
        for i, word in enumerate(self.script_words):
            if i < self.finalized_count:
                cls = 'spoken'
            elif i < frontier:
                cls = 'draft'
            elif i == frontier:
                cls = 'current'
            else:
                cls = ''
            parts.append(f'<span id="tw-{i}" class="{cls}">{word} </span>')
        self._script_element.content = ''.join(parts)

        target = min(frontier, len(self.script_words) - 1)
        if target >= 0:
            ui.run_javascript(f'''(() => {{
                const el = document.getElementById("tw-{target}");
                if (!el) return;
                const p = el.closest('.scroll-hidden');
                if (!p) {{ el.scrollIntoView({{behavior:"smooth",block:"center"}}); return; }}
                const y = el.offsetTop - p.clientHeight * 0.35;
                p.scrollTo({{top: Math.max(0, y), behavior: "smooth"}});
            }})()''')

    def update_spoken(self, finalized_count: int, draft_count: int = 0):
        self.finalized_count = min(finalized_count, len(self.script_words))
        remaining = len(self.script_words) - self.finalized_count
        self.draft_count = min(draft_count, remaining)
        self._refresh_script()

    def update_raw(self, finalized: str = '', draft: str = ''):
        if not self._raw_element:
            return
        parts = []
        if finalized:
            parts.append(f'<span class="finalized">{finalized}</span>')
        if draft:
            parts.append(f' <span class="draft-text">{draft}</span>')
        self._raw_element.content = ''.join(parts) or '&nbsp;'

    def reset(self):
        self.finalized_count = 0
        self.draft_count = 0
        self._refresh_script()
        if self._raw_element:
            self._raw_element.content = ''
