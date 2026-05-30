from nicegui import ui

from player_view.theme import apply_theme
from player_view import services


class Teleprompter:
    def __init__(self, script_text: str = ''):
        self.script_words = script_text.split() if script_text else []
        self.spoken_count = 0
        self._word_spans: list[ui.html] = []
        self._container = None
        self._raw_output = None
        self._recording = False

    def render_script(self):
        self._container = ui.column().classes('w-full p-8')
        with self._container:
            text_div = ui.html('').classes('teleprompter-text')
            self._update_script_html(text_div)
        return self._container

    def render_raw_output(self):
        self._raw_output = ui.label('').classes('teleprompter-text w-full p-8')
        return self._raw_output

    def _update_script_html(self, element: ui.html):
        parts = []
        for i, word in enumerate(self.script_words):
            cls = 'spoken' if i < self.spoken_count else ''
            parts.append(f'<span class="{cls}">{word} </span>')
        element.content = ''.join(parts)
        self._script_element = element

    def mark_spoken(self, count: int):
        self.spoken_count = min(count, len(self.script_words))
        if hasattr(self, '_script_element'):
            self._update_script_html(self._script_element)

    def set_raw_text(self, text: str):
        if self._raw_output:
            self._raw_output.text = text

    def start_recording(self, on_asr_result=None):
        if self._recording:
            return
        self._recording = True

        def on_chunk(chunk):
            services.asr.feed_audio(chunk)

        def on_result(result):
            if on_asr_result:
                on_asr_result(result)

        services.asr.start_streaming(on_result=on_result)
        services.audio.start(on_chunk=on_chunk)

    def stop_recording(self):
        if not self._recording:
            return None
        self._recording = False
        audio = services.audio.stop()
        asr_result = services.asr.stop_streaming()
        return audio, asr_result
