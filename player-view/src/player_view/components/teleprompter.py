from nicegui import ui


class Teleprompter:
    def __init__(self, script_text: str = ''):
        self.script_words = script_text.split() if script_text else []
        self.spoken_count = 0
        self._script_element: ui.html | None = None
        self._raw_element: ui.label | None = None

    def render_script(self):
        container = ui.column().classes('w-full p-8')
        with container:
            self._script_element = ui.html('').classes('teleprompter-text')
            self._refresh_script()
        return container

    def render_raw_output(self):
        self._raw_element = ui.label('').classes('teleprompter-text w-full p-8')
        return self._raw_element

    def _refresh_script(self):
        if not self._script_element:
            return
        parts = []
        for i, word in enumerate(self.script_words):
            cls = 'spoken' if i < self.spoken_count else ''
            parts.append(f'<span class="{cls}">{word} </span>')
        self._script_element.content = ''.join(parts)

    def update_spoken(self, count: int):
        self.spoken_count = min(count, len(self.script_words))
        self._refresh_script()

    def update_raw(self, text: str):
        if self._raw_element:
            self._raw_element.text = text

    def reset(self):
        self.spoken_count = 0
        self._refresh_script()
        if self._raw_element:
            self._raw_element.text = ''
