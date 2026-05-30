from nicegui import ui

from player_view.theme import apply_theme
from player_view.components.teleprompter import Teleprompter
from player_view import services


@ui.page('/test-speaker')
def test_speaker_page():
    apply_theme()
    teleprompter = Teleprompter()

    ranking_column = None
    status_label = None

    with ui.column().classes('w-full items-center gap-4 p-4'):
        ui.label('Test Voice Profile').classes('text-3xl').style('color: #c9a84c')

        with ui.row().classes('w-full gap-8 p-4'):
            with ui.column().classes('w-2/3'):
                ui.label('Raw ASR Output').classes('text-xl').style('color: #888')
                teleprompter.render_raw_output()

            with ui.column().classes('w-1/3'):
                ui.label('Profile Match').classes('text-xl').style('color: #888')
                ranking_column = ui.column().classes('w-full gap-2')

        status_label = ui.label('Press Record to begin').classes('text-xl').style('color: #888')

        with ui.row().classes('gap-4'):
            record_btn = ui.button('Record', on_click=lambda: _start())
            stop_btn = ui.button('Stop & Match', on_click=lambda: _stop())
            stop_btn.set_visibility(False)

    def _on_asr(result):
        teleprompter.set_raw_text(result.text)

    def _start():
        status_label.text = 'Recording... speak naturally'
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)
        ranking_column.clear()
        teleprompter.start_recording(on_asr_result=_on_asr)

    def _stop():
        result = teleprompter.stop_recording()
        if result is None:
            return
        audio, asr_result = result
        stop_btn.set_visibility(False)

        status_label.text = 'Extracting embedding and matching...'

        embedding = services.diarization.extract_embedding(audio)
        all_profiles = services.profiles.load_all()

        if not all_profiles:
            status_label.text = 'No saved profiles to compare against'
            record_btn.set_visibility(True)
            return

        ranked = services.diarization.rank_against(
            embedding,
            [(p.character, p.embedding) for p in all_profiles],
        )

        ranking_column.clear()
        with ranking_column:
            for name, similarity in ranked:
                pct = similarity * 100
                color = '#4caf50' if pct > 70 else '#ff9800' if pct > 40 else '#f44336'
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{name}').classes('text-xl').style('color: #e8e6e3; min-width: 200px')
                    ui.linear_progress(value=similarity).classes('w-48').props(f'color="{color}"')
                    ui.label(f'{pct:.0f}%').classes('text-lg').style(f'color: {color}')

        status_label.text = 'Done'
        record_btn.set_visibility(True)
