from nicegui import ui

from player_view.theme import apply_theme
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

    with ui.column().classes('w-full items-center gap-4 p-4'):
        ui.label('Save Voice Profile').classes('text-3xl').style('color: #c9a84c')

        with ui.row().classes('gap-4'):
            character_input = ui.input('Character Name').classes('text-xl')
            player_input = ui.input('Player Name').classes('text-xl')

        teleprompter.render_script()
        status_label = ui.label('Press Record to begin').classes('text-xl').style('color: #888')

        with ui.row().classes('gap-4'):
            record_btn = ui.button('Record', on_click=lambda: start())
            stop_btn = ui.button('Stop & Save', on_click=lambda: stop())
            stop_btn.set_visibility(False)

    def poll_asr():
        if not recording['active']:
            return
        result = services.asr.latest_result
        if result.text:
            word_count = len(result.text.split())
            teleprompter.update_spoken(word_count)

    timer = ui.timer(0.2, poll_asr)

    def start():
        recording['active'] = True
        status_label.text = 'Recording... read the text aloud'
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)

        def on_chunk(chunk):
            services.asr.feed_audio(chunk)

        services.asr.start_streaming()
        services.audio.start(on_chunk=on_chunk)

    def stop():
        recording['active'] = False
        audio = services.audio.stop()
        asr_result = services.asr.stop_streaming()
        stop_btn.set_visibility(False)

        character = character_input.value.strip()
        player = player_input.value.strip()
        if not character:
            status_label.text = 'Error: character name required'
            record_btn.set_visibility(True)
            return

        status_label.text = 'Extracting voice embedding...'
        ui.timer(0.1, lambda: _save_profile(character, player, audio), once=True)

    def _save_profile(character, player, audio):
        embedding = services.diarization.extract_embedding(audio)
        existing = services.profiles.load(character)
        if existing:
            services.profiles.update_embedding(character, embedding)
            status_label.text = f'Updated profile for {character} (sample #{existing.sample_count + 1})'
        else:
            profile = VoiceProfile(
                character=character,
                player=player or 'unknown',
                embedding=embedding,
            )
            services.profiles.save(profile)
            status_label.text = f'Saved new profile for {character}'

        record_btn.set_visibility(True)
        teleprompter.reset()
