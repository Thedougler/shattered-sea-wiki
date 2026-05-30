from nicegui import run, ui

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.components.teleprompter import Teleprompter
from player_view import services

MATCH_WINDOW_S = 4
MATCH_INTERVAL_S = 1.5
MIN_AUDIO_S = 1.5


@ui.page('/test-speaker')
def test_speaker_page():
    apply_theme()
    teleprompter = Teleprompter()
    state = {'recording': False, 'matching': False}

    with operator_header('Test Speaker'):
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP', on_click=lambda: stop()).props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')

    content_height = 'height: calc(100vh - 100px - 90px);'
    with ui.column().classes('w-full scroll-hidden').style(content_height):
        teleprompter.render_raw_output()
        results_container = ui.column().classes('w-full px-8 gap-3')

    with ui.row().classes('status-strip'):
        rec_dot = ui.html('<div class="rec-dot"></div>')
        rec_lbl = ui.html('<span class="rec-label">READY</span>')
        ui.html(
            '<div class="vu-meter">'
            '<div id="vu-fill" class="vu-fill"></div>'
            '</div>'
        )

    def poll_asr():
        if not state['recording']:
            return
        services.asr.process_pending()
        result = services.asr.latest_result
        teleprompter.update_raw(
            result.finalized_text or '',
            result.draft_text or '',
        )

    def poll_vu():
        if not state['recording']:
            return
        pct = int(services.audio.rms_level * 100)
        ui.run_javascript(
            f'document.getElementById("vu-fill").style.width="{pct}%"'
        )

    async def poll_match():
        if not state['recording'] or state['matching']:
            return
        buf = services.audio.get_buffer_copy()
        min_samples = int(MIN_AUDIO_S * services.audio.SAMPLE_RATE)
        if len(buf) < min_samples:
            return
        window_samples = int(MATCH_WINDOW_S * services.audio.SAMPLE_RATE)
        window = buf[-window_samples:]

        all_profiles = services.profiles.load_all()
        if not all_profiles:
            status_label.text = 'no profiles saved'
            status_label.style('color: #ff9800')
            return

        state['matching'] = True
        try:
            embedding = await run.io_bound(
                services.diarization.extract_embedding, window
            )
            ranked = services.diarization.rank_against(
                embedding,
                [(p.character, p.embedding) for p in all_profiles],
            )
            results_container.clear()
            with results_container:
                for name, sim in ranked[:5]:
                    pct = int(sim * 100)
                    color = '#4caf50' if pct > 70 else '#ff9800' if pct > 40 else '#f44336'
                    with ui.row().classes('match-result items-center w-full'):
                        ui.label(name).classes('match-name')
                        with ui.element('div').classes('match-bar-container'):
                            ui.element('div').classes('match-bar').style(
                                f'width: {pct}%; background: {color}'
                            )
                        ui.label(f'{pct}%').classes('match-pct').style(f'color: {color}')

            if ranked:
                status_label.text = f'best: {ranked[0][0]}'
                status_label.style('color: #4caf50')
        finally:
            state['matching'] = False

    ui.timer(0.2, poll_asr)
    ui.timer(0.1, poll_vu)
    ui.timer(MATCH_INTERVAL_S, poll_match)

    def start():
        state['recording'] = True
        state['matching'] = False
        status_label.text = 'listening...'
        status_label.style('color: #f44336')
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)
        results_container.clear()
        teleprompter.reset()

        rec_dot.content = '<div class="rec-dot active"></div>'
        rec_lbl.content = '<span class="rec-label active">REC</span>'

        services.asr.start_streaming()
        services.audio.start(on_chunk=lambda c: services.asr.feed_audio(c))

    def stop():
        state['recording'] = False
        services.audio.stop()
        services.asr.stop_streaming()
        stop_btn.set_visibility(False)
        record_btn.set_visibility(True)

        rec_dot.content = '<div class="rec-dot"></div>'
        rec_lbl.content = '<span class="rec-label">READY</span>'
        ui.run_javascript('document.getElementById("vu-fill").style.width="0%"')

        status_label.text = 'ready'
        status_label.style('color: #888')
