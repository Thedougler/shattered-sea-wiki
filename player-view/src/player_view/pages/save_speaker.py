import time as _time

from nicegui import run, ui

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.components.teleprompter import Teleprompter
from player_view import services
from player_view.models.voice_profile import VoiceProfile

_script_cache: dict[str, dict] = {}


def _build_script(name: str) -> str:
    who = f"I'm {name} and I'm" if name else "I'm"
    return (
        f"{who} about to read whatever nonsense appears on this screen "
        "without laughing, breaking character, or questioning my life choices. "
        "Thirty seconds is the minimum but honestly the longer I go the more "
        "the machine learns my voice so here we go. "
        "Picture a grizzled old sea captain who just discovered his parrot "
        "has been ordering supplies behind his back. "
        "Six hundred silver spoons shipped south on a single shallow sloop. "
        "Now that same captain, whispering, confessing he actually "
        "respects the parrot's initiative. "
        "Alright, still going, this is going well, the machine is listening."
    )


def _get_cached_script(name: str) -> tuple[str, int]:
    key = name.lower().strip() if name else ''
    if key in _script_cache:
        return _script_cache[key]['script'], _script_cache[key]['level']
    base = _build_script(name)
    return base, 1


def _cache_script(name: str, script: str, level: int):
    key = name.lower().strip() if name else ''
    _script_cache[key] = {'script': script, 'level': level}


@ui.page('/save-speaker')
def save_speaker_page():
    apply_theme()
    teleprompter = Teleprompter(script_text=_build_script(''))
    state = {
        'recording': False, 'matching': False, 'last_match': 0.0,
        'level': 1, 'high_level': 1,
        'chunk_start': 0,
        'chunk_size': teleprompter.word_count,
        'generating': False,
    }

    with operator_header('Save Speaker'):
        def _on_name_change(e):
            if not state['recording']:
                cached_script, _ = _get_cached_script(e.value.strip())
                teleprompter.set_script(cached_script)
                state['chunk_size'] = len(_build_script(e.value.strip()).split())

        name_input = ui.input('Name', on_change=_on_name_change).props('dense').classes('w-36')
        record_btn = ui.button('REC', on_click=lambda: start(), color='red').props('dense')
        stop_btn = ui.button('STOP & SAVE', on_click=lambda: stop(), color='green').props('dense')
        stop_btn.set_visibility(False)
        status_label = ui.label('ready').style('color: #888')

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
        ui.element('div').style('flex: 1')
        level_badge = ui.html('<span class="level-badge">LVL 1</span>')

    async def _generate_next_chunk():
        chunk_start = state['chunk_start']
        chunk_end = chunk_start + state['chunk_size']
        next_level = state['level'] + 1

        if next_level > state['high_level']:
            previous_chunk = ' '.join(teleprompter.script_words[chunk_start:chunk_end])
            name = name_input.value.strip()
            new_text = await services.llm.generate_script(next_level, previous_chunk)
            new_count = teleprompter.append_words(new_text)
            state['high_level'] = next_level
            full_script = ' '.join(teleprompter.script_words)
            _cache_script(name, full_script, next_level)
        else:
            new_count = teleprompter.word_count - chunk_end

        state['chunk_start'] = chunk_end
        state['chunk_size'] = new_count
        state['level'] = next_level
        state['generating'] = False

        level_badge.content = f'<span class="level-badge">LVL {next_level}</span>'
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
        name = name_input.value.strip()
        cached_script, cached_level = _get_cached_script(name)
        teleprompter.set_script(cached_script)
        base_size = len(_build_script(name).split())

        state['recording'] = True
        state['last_match'] = 0.0
        state['level'] = 1
        state['high_level'] = cached_level
        state['chunk_start'] = 0
        state['chunk_size'] = base_size
        state['generating'] = False
        level_badge.content = '<span class="level-badge">LVL 1</span>'

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
            cached_script, _ = _get_cached_script(name)
            teleprompter.set_script(cached_script)
            state['level'] = 1
            state['chunk_start'] = 0
            state['chunk_size'] = len(_build_script(name).split())
            state['generating'] = False
            level_badge.content = '<span class="level-badge">LVL 1</span>'

        ui.timer(0.1, save, once=True)
