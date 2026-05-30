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

    character_input = None
    player_input = None
    status_label = None

    with ui.column().classes('w-full items-center gap-4 p-4'):
        ui.label('Save Voice Profile').classes('text-3xl').style('color: #c9a84c')

        with ui.row().classes('gap-4'):
            character_input = ui.input('Character Name').classes('text-xl')
            player_input = ui.input('Player Name').classes('text-xl')

        teleprompter.render_script()
        status_label = ui.label('Press Record to begin').classes('text-xl').style('color: #888')

        with ui.row().classes('gap-4'):
            record_btn = ui.button('Record', on_click=lambda: _start())
            stop_btn = ui.button('Stop & Save', on_click=lambda: _stop())
            stop_btn.set_visibility(False)

    word_count = {'value': 0}

    def _on_asr(result):
        word_count['value'] = len(result.text.split())
        teleprompter.mark_spoken(word_count['value'])

    def _start():
        status_label.text = 'Recording... read the text aloud'
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)
        teleprompter.start_recording(on_asr_result=_on_asr)

    def _stop():
        result = teleprompter.stop_recording()
        if result is None:
            return
        audio, asr_result = result
        stop_btn.set_visibility(False)

        character = character_input.value.strip()
        player = player_input.value.strip()
        if not character:
            status_label.text = 'Error: character name required'
            record_btn.set_visibility(True)
            return

        status_label.text = 'Extracting voice embedding...'

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
        teleprompter.mark_spoken(0)
        word_count['value'] = 0
