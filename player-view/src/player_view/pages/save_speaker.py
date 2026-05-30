import time as _time

from nicegui import run, ui

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
    state = {'recording': False, 'matching': False, 'last_match': 0.0}

    with operator_header('Save Speaker'):
        name_input = ui.input('Name').props('dense').classes('w-36')
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP & SAVE', on_click=lambda: stop(), color='green').props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')

    teleprompter.render_script(
        container_style='height: calc(100vh - 100px - 90px);'
    )

    with ui.row().classes('status-strip'):
        rec_dot = ui.html('<div class="rec-dot"></div>')
        rec_lbl = ui.html('<span class="rec-label">READY</span>')
        ui.html(
            '<div class="vu-meter">'
            '<div id="vu-fill" class="vu-fill"></div>'
            '</div>'
        )
        match_lbl = ui.label('').classes('voice-match')

    def poll_asr():
        if not state['recording']:
            return
        result = services.asr.latest_result
        finalized = len(result.finalized_text.split()) if result.finalized_text else 0
        draft = len(result.draft_text.split()) if result.draft_text else 0
        teleprompter.update_spoken(finalized, draft)

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
        now = _time.time()
        if now - state['last_match'] < 5:
            return
        audio_snapshot = services.audio.get_buffer_copy()
        if len(audio_snapshot) < 3 * services.audio.SAMPLE_RATE:
            return

        all_profiles = services.profiles.load_all()
        if not all_profiles:
            return

        state['matching'] = True
        state['last_match'] = now
        try:
            embedding = await run.io_bound(
                services.diarization.extract_embedding, audio_snapshot
            )
            ranked = services.diarization.rank_against(
                embedding,
                [(p.character, p.embedding) for p in all_profiles],
            )
            if ranked:
                best_name, best_sim = ranked[0]
                pct = int(best_sim * 100)
                match_lbl.text = f'{best_name} ({pct}%)'
                color = '#4caf50' if pct > 70 else '#ff9800' if pct > 40 else '#666'
                match_lbl.style(f'color: {color}')
        finally:
            state['matching'] = False

    ui.timer(0.2, poll_asr)
    ui.timer(0.1, poll_vu)
    ui.timer(2.0, poll_match)

    def start():
        state['recording'] = True
        state['last_match'] = 0.0
        status_label.text = 'recording...'
        status_label.style('color: #f44336')
        record_btn.set_visibility(False)
        stop_btn.set_visibility(True)

        rec_dot.content = '<div class="rec-dot active"></div>'
        rec_lbl.content = '<span class="rec-label active">REC</span>'
        match_lbl.text = ''

        services.asr.start_streaming()
        services.audio.start(on_chunk=lambda c: services.asr.feed_audio(c))

    def stop():
        state['recording'] = False
        audio = services.audio.stop()
        services.asr.stop_streaming()
        stop_btn.set_visibility(False)

        rec_dot.content = '<div class="rec-dot"></div>'
        rec_lbl.content = '<span class="rec-label">READY</span>'
        ui.run_javascript('document.getElementById("vu-fill").style.width="0%"')
        match_lbl.text = ''

        name = name_input.value.strip()
        if not name:
            status_label.text = 'need name'
            status_label.style('color: #ff9800')
            record_btn.set_visibility(True)
            return

        status_label.text = 'extracting embedding...'
        status_label.style('color: #888')

        async def save():
            embedding = await run.io_bound(
                services.diarization.extract_embedding, audio
            )
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

        ui.timer(0.1, save, once=True)
