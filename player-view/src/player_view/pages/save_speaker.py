import time as _time

from nicegui import run, ui

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.components.teleprompter import Teleprompter
from player_view import services
from player_view.models.voice_profile import VoiceProfile

DEFAULT_SCRIPT = (
    'Welcome, brave voice actor, to the enchanted voice chamber. '
    'Right now your dulcet tones are being captured by ancient microphone magic. '
    'Just speak naturally and read along. Thirty seconds is the minimum, '
    'but the longer you go, the better your voice print becomes. '
    'She sells seashells by the shimmering shore. '
    'Try a deep gravelly pirate voice: Arrr, the kraken devours ships at dawn! '
    'Now go high and nasal: Excuse me, I ordered the quinoa frittata. '
    'Excellent. Keep going, the machine is learning your beautiful, unique, '
    'completely unreplicable voice. Red leather yellow leather, '
    'red leather yellow leather. You are doing fantastically.'
)


@ui.page('/save-speaker')
def save_speaker_page():
    apply_theme()
    teleprompter = Teleprompter(script_text=DEFAULT_SCRIPT)
    state = {
        'recording': False, 'matching': False, 'last_match': 0.0,
        'level': 1,
        'chunk_start': 0,
        'chunk_size': teleprompter.word_count,
        'generating': False,
    }

    with operator_header('Save Speaker'):
        name_input = ui.input('Name').props('dense').classes('w-36')
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP & SAVE', on_click=lambda: stop(), color='green').props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')

    level_badge = ui.html('<div class="level-badge">LVL 1</div>')

    scroll = teleprompter.render_script(
        container_style='height: calc(100vh - 100px - 90px);'
    )
    scroll.classes('teleprompter-mask')

    with ui.row().classes('status-strip'):
        rec_dot = ui.html('<div class="rec-dot"></div>')
        rec_lbl = ui.html('<span class="rec-label">READY</span>')
        ui.html(
            '<div class="vu-meter">'
            '<div id="vu-fill" class="vu-fill"></div>'
            '</div>'
        )
        match_lbl = ui.label('').classes('voice-match')

    async def _generate_next_chunk():
        chunk_start = state['chunk_start']
        chunk_end = chunk_start + state['chunk_size']
        previous_chunk = ' '.join(teleprompter.script_words[chunk_start:chunk_end])
        next_level = state['level'] + 1

        new_text = await services.llm.generate_script(next_level, previous_chunk)
        new_count = teleprompter.append_words(new_text)

        state['chunk_start'] = chunk_end
        state['chunk_size'] = new_count
        state['level'] = next_level
        state['generating'] = False

        level_badge.content = f'<div class="level-badge">LVL {next_level}</div>'
        ui.run_javascript('''
            const b = document.querySelector('.level-badge');
            if (b) { b.classList.add('level-up');
            setTimeout(() => b.classList.remove('level-up'), 600); }
        ''')

    def poll_asr():
        if not state['recording']:
            return
        result = services.asr.latest_result
        finalized = len(result.finalized_text.split()) if result.finalized_text else 0
        draft = len(result.draft_text.split()) if result.draft_text else 0
        teleprompter.update_spoken(finalized, draft)

        threshold = state['chunk_start'] + int(state['chunk_size'] * 0.5)
        if finalized >= threshold and not state['generating']:
            state['generating'] = True
            ui.timer(0, _generate_next_chunk, once=True)

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
            state['level'] = 1
            state['chunk_start'] = 0
            state['chunk_size'] = teleprompter.word_count
            state['generating'] = False
            level_badge.content = '<div class="level-badge">LVL 1</div>'

        ui.timer(0.1, save, once=True)
