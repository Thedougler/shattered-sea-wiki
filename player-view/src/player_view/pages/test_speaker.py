from nicegui import ui

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.components.teleprompter import Teleprompter
from player_view import services


@ui.page('/test-speaker')
def test_speaker_page():
    apply_theme()
    teleprompter = Teleprompter()
    recording = {'active': False}

    with operator_header('Test Speaker'):
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP & MATCH', on_click=lambda: stop(), color='green').props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')
        ui.separator().props('vertical').classes('self-stretch')
        ranking_label = ui.label('').style('color: #ccc; white-space: nowrap')

    teleprompter.render_raw_output()

    def poll_asr():
        if not recording['active']:
            return
        result = services.asr.latest_result
        if result.text:
            teleprompter.update_raw(result.text)

    ui.timer(0.2, poll_asr)

    def start():
        recording['active'] = True
        status_label.text = 'recording...'
        status_label.style('color: #f44336')
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)
        ranking_label.text = ''
        teleprompter.reset()

        def on_chunk(chunk):
            services.asr.feed_audio(chunk)

        services.asr.start_streaming()
        services.audio.start(on_chunk=on_chunk)

    def stop():
        recording['active'] = False
        audio = services.audio.stop()
        services.asr.stop_streaming()
        stop_btn.set_visibility(False)

        status_label.text = 'matching...'
        status_label.style('color: #888')
        ui.timer(0.1, lambda: _match_profiles(audio), once=True)

    def _match_profiles(audio):
        embedding = services.diarization.extract_embedding(audio)
        all_profiles = services.profiles.load_all()

        if not all_profiles:
            status_label.text = 'no profiles'
            status_label.style('color: #ff9800')
            record_btn.set_visibility(True)
            return

        ranked = services.diarization.rank_against(
            embedding,
            [(p.character, p.embedding) for p in all_profiles],
        )

        parts = []
        for name, similarity in ranked[:5]:
            pct = int(similarity * 100)
            parts.append(f'{name} {pct}%')
        ranking_label.text = ' | '.join(parts)

        status_label.text = 'done'
        status_label.style('color: #4caf50')
        record_btn.set_visibility(True)
