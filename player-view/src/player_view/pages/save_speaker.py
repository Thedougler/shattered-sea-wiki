from nicegui import ui

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.components.teleprompter import Teleprompter
from player_view import services
from player_view.models.voice_profile import VoiceProfile

DEFAULT_SCRIPT = (
    'The quick brown fox jumps over the lazy dog. '
    'She sells seashells by the seashore. '
    'How vexingly quick daft zebras jump. '
    'The five boxing wizards jump quickly. '
    'Pack my box with five dozen liquor jugs. '
    'Amazingly few discotheques provide jukeboxes. '
    'The old sailor watched the horizon, his weathered hands gripping the wheel '
    'as the storm clouds gathered in the distance. He had seen worse, far worse, '
    'but something about this particular squall set his teeth on edge. '
    'The sea had a memory, and tonight it was angry.'
)


@ui.page('/save-speaker')
def save_speaker_page():
    apply_theme()
    teleprompter = Teleprompter(script_text=DEFAULT_SCRIPT)
    recording = {'active': False}

    with operator_header('Save Speaker'):
        name_input = ui.input('Name').props('dense').classes('w-36')
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP & SAVE', on_click=lambda: stop(), color='green').props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')

    teleprompter.render_script()

    def poll_asr():
        if not recording['active']:
            return
        result = services.asr.latest_result
        if result.text:
            word_count = len(result.text.split())
            teleprompter.update_spoken(word_count)

    ui.timer(0.2, poll_asr)

    def start():
        recording['active'] = True
        status_label.text = 'recording...'
        status_label.style('color: #f44336')
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)

        def on_chunk(chunk):
            services.asr.feed_audio(chunk)

        services.asr.start_streaming()
        services.audio.start(on_chunk=on_chunk)

    def stop():
        recording['active'] = False
        audio = services.audio.stop()
        services.asr.stop_streaming()
        stop_btn.set_visibility(False)

        name = name_input.value.strip()
        if not name:
            status_label.text = 'need name'
            status_label.style('color: #ff9800')
            record_btn.set_visibility(True)
            return

        status_label.text = 'extracting embedding...'
        status_label.style('color: #888')
        ui.timer(0.1, lambda: _save_profile(name, audio), once=True)

    def _save_profile(name, audio):
        embedding = services.diarization.extract_embedding(audio)
        existing = services.profiles.load(name)
        if existing:
            services.profiles.update_embedding(name, embedding)
            status_label.text = f'updated {name} (#{existing.sample_count + 1})'
        else:
            profile = VoiceProfile(character=name, player='', embedding=embedding)
            services.profiles.save(profile)
            status_label.text = f'saved {name}'

        status_label.style('color: #4caf50')
        record_btn.set_visibility(True)
        teleprompter.reset()
