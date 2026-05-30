import random
from pathlib import Path

from nicegui import ui

from player_view import services
from player_view.models.voice_profile import VoiceProfile
from player_view.pages import slideshow as slideshow_page
from player_view.pages import session as session_page
from player_view.pages import map_view as map_page

DM_CSS = '''
body {
    background: #1a1a2e !important;
    color: #e0e0e0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.9rem;
}
.dm-card {
    background: #16213e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 16px;
}
.dm-card h3 {
    color: #c9a84c;
    margin: 0 0 12px 0;
    font-size: 1.1rem;
}
.dm-section-label {
    color: #888;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
'''


@ui.page('/dm')
def dm_page():
    ui.add_css(DM_CSS)
    ui.query('body').style('background: #1a1a2e')

    with ui.column().classes('w-full max-w-4xl mx-auto p-4 gap-4'):
        ui.label('DM Control Panel').style(
            'color: #c9a84c; font-size: 1.6rem; font-weight: bold; text-align: center'
        )

        with ui.row().classes('w-full gap-4'):
            _build_save_speaker_card()
            _build_test_speaker_card()

        _build_profiles_card()

        with ui.row().classes('w-full gap-4'):
            _build_session_card()

        with ui.row().classes('w-full gap-4'):
            _build_slideshow_card()
            _build_map_card()


def _build_save_speaker_card():
    recording = {'active': False}

    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Save Speaker</h3>')
        name_input = ui.input('Name').props('dense outlined dark').classes('w-full')

        with ui.row().classes('gap-2 items-center'):
            rec_btn = ui.button('REC', color='red').props('dense')
            stop_btn = ui.button('STOP & SAVE', color='green').props('dense')
            stop_btn.set_visibility(False)
            status = ui.label('ready').style('color: #888; font-size: 0.8rem')

        asr_preview = ui.label('').style(
            'color: #666; font-size: 0.8rem; font-style: italic; '
            'max-height: 60px; overflow: hidden'
        )

        def poll():
            if not recording['active']:
                return
            result = services.asr.latest_result
            if result.text:
                asr_preview.text = result.text[-200:]

        ui.timer(0.3, poll)

        def start():
            recording['active'] = True
            status.text = 'recording...'
            status.style('color: #f44336')
            rec_btn.set_visibility(False)
            stop_btn.set_visibility(True)
            asr_preview.text = ''

            services.asr.start_streaming()
            services.audio.start(on_chunk=lambda c: services.asr.feed_audio(c))

        def stop():
            recording['active'] = False
            audio = services.audio.stop()
            services.asr.stop_streaming()
            stop_btn.set_visibility(False)

            name = name_input.value.strip()
            if not name:
                status.text = 'need name'
                status.style('color: #ff9800')
                rec_btn.set_visibility(True)
                return

            status.text = 'extracting...'
            status.style('color: #888')
            ui.timer(0.1, lambda: _save(name, audio), once=True)

        def _save(name, audio):
            embedding = services.diarization.extract_embedding(audio)
            existing = services.profiles.load(name)
            if existing:
                services.profiles.update_embedding(name, embedding)
                status.text = f'updated {name} (#{existing.sample_count + 1})'
            else:
                profile = VoiceProfile(character=name, player='', embedding=embedding)
                services.profiles.save(profile)
                status.text = f'saved {name}'
            status.style('color: #4caf50')
            rec_btn.set_visibility(True)

        rec_btn.on_click(start)
        stop_btn.on_click(stop)


def _build_test_speaker_card():
    recording = {'active': False}

    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Test Speaker</h3>')

        with ui.row().classes('gap-2 items-center'):
            rec_btn = ui.button('REC', color='red').props('dense')
            stop_btn = ui.button('STOP & MATCH', color='green').props('dense')
            stop_btn.set_visibility(False)
            status = ui.label('ready').style('color: #888; font-size: 0.8rem')

        asr_preview = ui.label('').style(
            'color: #666; font-size: 0.8rem; font-style: italic; '
            'max-height: 40px; overflow: hidden'
        )
        results_col = ui.column().classes('w-full gap-1')

        def poll():
            if not recording['active']:
                return
            result = services.asr.latest_result
            if result.text:
                asr_preview.text = result.text[-200:]

        ui.timer(0.3, poll)

        def start():
            recording['active'] = True
            status.text = 'recording...'
            status.style('color: #f44336')
            rec_btn.set_visibility(False)
            stop_btn.set_visibility(True)
            asr_preview.text = ''
            results_col.clear()

            services.asr.start_streaming()
            services.audio.start(on_chunk=lambda c: services.asr.feed_audio(c))

        def stop():
            recording['active'] = False
            audio = services.audio.stop()
            services.asr.stop_streaming()
            stop_btn.set_visibility(False)

            status.text = 'matching...'
            status.style('color: #888')
            ui.timer(0.1, lambda: _match(audio), once=True)

        def _match(audio):
            embedding = services.diarization.extract_embedding(audio)
            all_profiles = services.profiles.load_all()
            if not all_profiles:
                status.text = 'no profiles saved'
                status.style('color: #ff9800')
                rec_btn.set_visibility(True)
                return

            ranked = services.diarization.rank_against(
                embedding,
                [(p.character, p.embedding) for p in all_profiles],
            )
            results_col.clear()
            with results_col:
                for name, sim in ranked[:5]:
                    pct = int(sim * 100)
                    color = '#4caf50' if pct > 70 else '#ff9800' if pct > 40 else '#f44336'
                    with ui.row().classes('items-center gap-2'):
                        ui.label(name).style('min-width: 120px; color: #ccc')
                        ui.linear_progress(value=sim).classes('w-32').props(f'color="{color}"')
                        ui.label(f'{pct}%').style(f'color: {color}; font-size: 0.8rem')

            status.text = 'done'
            status.style('color: #4caf50')
            rec_btn.set_visibility(True)

        rec_btn.on_click(start)
        stop_btn.on_click(stop)


def _build_profiles_card():
    with ui.card().classes('dm-card w-full'):
        ui.html('<h3>Voice Profiles</h3>')
        profiles_row = ui.row().classes('w-full gap-2 flex-wrap')

        def refresh_profiles():
            profiles_row.clear()
            all_profiles = services.profiles.load_all() if services.profiles else []
            if not all_profiles:
                with profiles_row:
                    ui.label('No profiles saved').style('color: #666')
                return
            with profiles_row:
                for p in sorted(all_profiles, key=lambda x: x.character):
                    with ui.card().classes('p-2').style(
                        'background: #1a1a3e; border: 1px solid #333'
                    ):
                        with ui.row().classes('items-center gap-2'):
                            ui.label(p.character).style('color: #e0e0e0')
                            ui.label(f'({p.sample_count}x)').style(
                                'color: #888; font-size: 0.75rem'
                            )
                            ui.button(
                                icon='delete', color='red',
                                on_click=lambda _, n=p.character: _delete(n),
                            ).props('flat dense size=xs')

        def _delete(name):
            services.profiles.delete(name)
            refresh_profiles()

        ui.timer(2, refresh_profiles)
        refresh_profiles()


def _build_session_card():
    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Session Transcribe</h3>')
        status_lbl = ui.label('').style('color: #888; font-size: 0.8rem')

        def poll():
            s = session_page._state
            mins, secs = divmod(int(s.session_length_s), 60)
            status_lbl.text = (
                f'{s.status} | {len(s.messages)} msgs | '
                f'{s.speaker_count} spk | {mins}:{secs:02d}'
            )

        ui.timer(1, poll)


def _build_slideshow_card():
    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Slideshow</h3>')

        with ui.row().classes('gap-2 items-end w-full'):
            folder_in = ui.input('Image folder path').props('dense outlined dark').classes('flex-grow')
            ui.button('Set', on_click=lambda: _set_folder()).props('dense')

        with ui.row().classes('gap-2 items-center'):
            interval_num = ui.number('Interval (s)', value=10, min=1, max=120).props(
                'dense outlined dark'
            ).classes('w-28')
            ui.button('Prev', on_click=lambda: _prev()).props('dense flat')
            ui.button('Next', on_click=lambda: _next()).props('dense flat')

        info_lbl = ui.label('').style('color: #888; font-size: 0.8rem')

        def _set_folder():
            folder = Path(folder_in.value.strip())
            if not folder.is_dir():
                info_lbl.text = 'not a valid directory'
                return
            exts = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
            images = [str(p) for p in folder.iterdir() if p.suffix.lower() in exts]
            random.shuffle(images)
            slideshow_page._state.images = images
            slideshow_page._state.current_index = 0
            slideshow_page._state.interval_s = interval_num.value or 10
            info_lbl.text = f'loaded {len(images)} images'

        def _next():
            s = slideshow_page._state
            if s.images:
                s.current_index = (s.current_index + 1) % len(s.images)

        def _prev():
            s = slideshow_page._state
            if s.images:
                s.current_index = (s.current_index - 1) % len(s.images)

        def poll():
            s = slideshow_page._state
            if s.images:
                info_lbl.text = f'{s.current_index + 1}/{len(s.images)} images'
            else:
                info_lbl.text = 'no images loaded'

        ui.timer(1, poll)


def _build_map_card():
    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Maps</h3>')

        with ui.row().classes('gap-2 items-end w-full'):
            name_in = ui.input('Map name').props('dense outlined dark').classes('w-28')
            path_in = ui.input('Image path or URL').props('dense outlined dark').classes('flex-grow')
            ui.button('Set', on_click=lambda: _set_map()).props('dense')

        maps_lbl = ui.label('').style('color: #888; font-size: 0.8rem')

        def _set_map():
            name = name_in.value.strip().lower().replace(' ', '-')
            path = path_in.value.strip()
            if name and path:
                map_page._maps[name] = path
                _refresh()
                name_in.value = ''
                path_in.value = ''

        def _refresh():
            map_page._discover_maps()
            names = sorted(map_page._maps.keys())
            if names:
                maps_lbl.text = f'available: {", ".join(names)}'
            else:
                maps_lbl.text = 'no maps configured'

        _refresh()
