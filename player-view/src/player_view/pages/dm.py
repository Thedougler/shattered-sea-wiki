import random
import sounddevice as sd
from pathlib import Path

from nicegui import events, ui

from player_view import services
from player_view.models.voice_profile import VoiceProfile
from player_view.services.audio import AudioService
from player_view.services.spatial import SpatialAnalyzer
from player_view.services.session_transcriber import SessionTranscriber
from player_view.pages import slideshow as slideshow_page
from player_view.pages import session as session_page
from player_view.pages import map_view as map_page

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / 'assets'
MAPS_DIR = ASSETS_DIR / 'maps'
SLIDESHOW_DIR = ASSETS_DIR / 'slideshow'
AVATARS_DIR = ASSETS_DIR / 'avatars'
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}

for _d in (MAPS_DIR, SLIDESHOW_DIR, AVATARS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

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
.nav-pill {
    color: #c9a84c !important;
    text-decoration: none !important;
    padding: 5px 14px;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    font-size: 0.82rem;
    transition: all 0.15s ease;
    white-space: nowrap;
    display: inline-block;
}
.nav-pill:hover {
    background: rgba(201, 168, 76, 0.1);
    border-color: #c9a84c;
}
.map-thumb {
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    overflow: hidden;
    transition: border-color 0.15s;
}
.map-thumb:hover {
    border-color: #c9a84c;
}
.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.status-dot.green { background: #4caf50; }
.status-dot.amber { background: #ff9800; }
.status-dot.red { background: #f44336; }
.status-dot.gray { background: #555; }
.status-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: #aaa;
    white-space: nowrap;
}
'''


def _find_avatar(character: str) -> str | None:
    safe = character.lower().replace(' ', '_')
    for ext in IMAGE_EXTS:
        if (AVATARS_DIR / f'{safe}{ext}').exists():
            return f'/assets/avatars/{safe}{ext}'
    return None


@ui.page('/dm')
def dm_page():
    ui.add_css(DM_CSS)
    ui.query('body').style('background: #1a1a2e')

    with ui.column().classes('w-full max-w-6xl mx-auto p-4 gap-4'):
        ui.label('DM Control Panel').style(
            'color: #c9a84c; font-size: 1.6rem; font-weight: bold; text-align: center'
        )

        _build_nav_bar()
        _build_status_bar()

        with ui.row().classes('w-full gap-4'):
            _build_upload_hub()

        with ui.row().classes('w-full gap-4'):
            _build_save_speaker_card()
            _build_test_speaker_card()

        _build_profiles_card()

        with ui.row().classes('w-full gap-4'):
            _build_session_card()

        with ui.row().classes('w-full gap-4'):
            _build_slideshow_card()
            _build_map_card()


def _build_nav_bar():
    with ui.card().classes('dm-card w-full').style('padding: 10px 16px'):
        nav_row = ui.row().classes('gap-2 flex-wrap items-center')

        def refresh():
            nav_row.clear()
            with nav_row:
                ui.label('PLAYER VIEWS').classes('dm-section-label').style('margin-right: 4px')

                pages = [
                    ('Session', '/session'),
                    ('Slideshow', '/slideshow'),
                    ('Save Speaker', '/save-speaker'),
                    ('Test Speaker', '/test-speaker'),
                ]
                for label, path in pages:
                    ui.link(label, path, new_tab=True).classes('nav-pill')

                map_page._discover_maps()
                map_names = sorted(map_page._maps.keys())
                if map_names:
                    ui.separator().props('vertical').classes('self-stretch').style('margin: 0 4px')
                    for name in map_names:
                        ui.link(f'Map: {name}', f'/map/{name}', new_tab=True).classes('nav-pill')

        refresh()
        ui.timer(10, refresh)


def _build_status_bar():
    with ui.card().classes('dm-card w-full').style('padding: 8px 16px'):
        status_row = ui.row().classes('gap-4 flex-wrap items-center')

        def refresh():
            status_row.clear()
            with status_row:
                ui.label('STATUS').classes('dm-section-label').style('margin-right: 4px')

                profile_count = len(services.profiles.load_all()) if services.profiles else 0
                p_cls = 'green' if profile_count > 0 else 'gray'
                with ui.element('div').classes('status-item'):
                    ui.element('span').classes(f'status-dot {p_cls}')
                    ui.label(f'{profile_count} profiles')

                sess_status = services.session_state.status if services.session_state else 'idle'
                s_cls = 'green' if sess_status == 'recording' else 'gray'
                with ui.element('div').classes('status-item'):
                    ui.element('span').classes(f'status-dot {s_cls}')
                    ui.label(f'Session: {sess_status}')

                slide_count = len(slideshow_page._state.images)
                sl_cls = 'green' if slide_count > 0 else 'gray'
                with ui.element('div').classes('status-item'):
                    ui.element('span').classes(f'status-dot {sl_cls}')
                    ui.label(f'{slide_count} slides')

                map_count = len(map_page._maps)
                m_cls = 'green' if map_count > 0 else 'gray'
                with ui.element('div').classes('status-item'):
                    ui.element('span').classes(f'status-dot {m_cls}')
                    ui.label(f'{map_count} maps')

                llm_ok = services.llm and services.llm.available
                l_cls = 'green' if llm_ok else 'amber'
                l_txt = 'LLM ready' if llm_ok else 'LLM: no key'
                with ui.element('div').classes('status-item'):
                    ui.element('span').classes(f'status-dot {l_cls}')
                    ui.label(l_txt)

        refresh()
        ui.timer(2, refresh)


def _build_upload_hub():
    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Upload Images</h3>')

        with ui.row().classes('gap-2 items-end w-full'):
            dest_select = ui.select(
                options=['Maps', 'Slideshow', 'Avatar'],
                value='Maps',
                label='Destination',
            ).props('dense outlined dark').classes('w-36')

            char_select = ui.select(
                options=[],
                label='Character',
            ).props('dense outlined dark').classes('w-36')
            char_select.set_visibility(False)

        def on_dest_change():
            is_avatar = dest_select.value == 'Avatar'
            char_select.set_visibility(is_avatar)
            if is_avatar:
                all_profiles = services.profiles.load_all() if services.profiles else []
                char_select.options = [p.character for p in sorted(all_profiles, key=lambda x: x.character)]
                char_select.update()

        dest_select.on_value_change(lambda _: on_dest_change())

        info_lbl = ui.label('').style('color: #888; font-size: 0.8rem')

        def on_upload(e: events.UploadEventArguments):
            dest = dest_select.value
            if dest == 'Maps':
                fpath = MAPS_DIR / e.name
                fpath.write_bytes(e.content.read())
                name = fpath.stem.lower().replace(' ', '-')
                map_page._maps[name] = f'/assets/maps/{e.name}'
                info_lbl.text = f'Map "{name}" added'
            elif dest == 'Slideshow':
                fpath = SLIDESHOW_DIR / e.name
                fpath.write_bytes(e.content.read())
                path_str = str(fpath)
                if path_str not in slideshow_page._state.images:
                    slideshow_page._state.images.append(path_str)
                info_lbl.text = f'Slide added — {len(slideshow_page._state.images)} total'
            elif dest == 'Avatar':
                character = char_select.value
                if not character:
                    info_lbl.text = 'select a character first'
                    e.sender.run_method('reset')
                    return
                ext = Path(e.name).suffix.lower()
                safe = character.lower().replace(' ', '_')
                for old_ext in IMAGE_EXTS:
                    old = AVATARS_DIR / f'{safe}{old_ext}'
                    if old.exists():
                        old.unlink()
                (AVATARS_DIR / f'{safe}{ext}').write_bytes(e.content.read())
                info_lbl.text = f'Avatar saved for {character}'
            e.sender.run_method('reset')

        ui.upload(
            on_upload=on_upload,
            auto_upload=True,
            multiple=True,
            label='Drop images or click to browse',
        ).props(
            'accept=".png,.jpg,.jpeg,.gif,.webp,.svg" flat bordered dark color=amber'
        ).classes('w-full')


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
        profiles_row = ui.row().classes('w-full gap-3 flex-wrap')

        def _show_avatar_upload(character):
            with ui.dialog() as dlg, ui.card().style(
                'background: #16213e; min-width: 300px; border: 1px solid #2a2a4a'
            ):
                ui.label(f'Avatar — {character}').style(
                    'color: #c9a84c; font-weight: bold; font-size: 1rem'
                )
                current = _find_avatar(character)
                if current:
                    ui.image(current).style(
                        'width: 80px; height: 80px; border-radius: 50%; '
                        'object-fit: cover; margin: 8px auto; display: block'
                    )

                def on_upload(e: events.UploadEventArguments):
                    ext = Path(e.name).suffix.lower()
                    safe = character.lower().replace(' ', '_')
                    for old_ext in IMAGE_EXTS:
                        old = AVATARS_DIR / f'{safe}{old_ext}'
                        if old.exists():
                            old.unlink()
                    dest = AVATARS_DIR / f'{safe}{ext}'
                    dest.write_bytes(e.content.read())
                    ui.notify(f'Avatar saved for {character}', type='positive')
                    dlg.close()
                    refresh_profiles()

                ui.upload(
                    on_upload=on_upload,
                    auto_upload=True,
                    label='Drop image or click to browse',
                ).props(
                    'accept=".png,.jpg,.jpeg,.gif,.webp,.svg" flat bordered dark color=amber'
                ).classes('w-full')

            dlg.open()

        def refresh_profiles():
            profiles_row.clear()
            all_profiles = services.profiles.load_all() if services.profiles else []
            if not all_profiles:
                with profiles_row:
                    ui.label('No profiles saved').style('color: #666')
                return
            with profiles_row:
                for p in sorted(all_profiles, key=lambda x: x.character):
                    avatar_url = _find_avatar(p.character)
                    with ui.card().classes('p-2').style(
                        'background: #1a1a3e; border: 1px solid #333'
                    ):
                        with ui.row().classes('items-center gap-2'):
                            if avatar_url:
                                ui.image(avatar_url).style(
                                    'width: 32px; height: 32px; border-radius: 50%; '
                                    'object-fit: cover'
                                )
                            else:
                                with ui.element('div').style(
                                    'width: 32px; height: 32px; border-radius: 50%; '
                                    'background: #2a2a4a; display: flex; '
                                    'align-items: center; justify-content: center; '
                                    'color: #666; font-size: 0.9rem'
                                ):
                                    ui.label(p.character[0].upper())

                            ui.label(p.character).style('color: #e0e0e0')
                            ui.label(f'({p.sample_count}x)').style(
                                'color: #888; font-size: 0.75rem'
                            )
                            ui.button(
                                icon='photo_camera',
                                on_click=lambda _, n=p.character: _show_avatar_upload(n),
                            ).props('flat dense size=xs').style('color: #666')
                            ui.button(
                                icon='delete', color='red',
                                on_click=lambda _, n=p.character: _delete(n),
                            ).props('flat dense size=xs')

        def _delete(name):
            services.profiles.delete(name)
            refresh_profiles()

        ui.timer(2, refresh_profiles)
        refresh_profiles()


def _get_input_devices():
    devices = sd.query_devices()
    result = {}
    for i, d in enumerate(devices):
        if d['max_input_channels'] > 0:
            label = f"{d['name']} ({d['max_input_channels']}ch)"
            result[i] = label
    return result


def _build_session_card():
    state = {'active': False, 'session_audio': None}

    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Session Transcribe</h3>')

        input_devices = _get_input_devices()
        device_select = ui.select(
            options=input_devices,
            label='Input device',
        ).props('dense outlined dark').classes('w-full')
        for dev_id, label in input_devices.items():
            if 'aggregate' in label.lower():
                device_select.value = dev_id
                break

        with ui.row().classes('gap-2 items-center'):
            dm_ch = ui.input('DM ch', value='0').props('dense outlined dark').classes('w-16')
            player_ch = ui.input('Player ch', value='1,2').props('dense outlined dark').classes('w-20')

        with ui.row().classes('gap-2 items-center'):
            start_btn = ui.button('Start Session', color='green').props('dense')
            stop_btn = ui.button('Stop Session', color='red').props('dense')
            stop_btn.set_visibility(False)

        status_lbl = ui.label('idle').style('color: #888; font-size: 0.8rem')
        ratio_lbl = ui.label('').style('color: #666; font-size: 0.8rem')

        def start():
            dev = device_select.value
            if dev is None:
                status_lbl.text = 'select a device'
                status_lbl.style('color: #ff9800')
                return

            dm_channels = [int(x.strip()) for x in dm_ch.value.split(',')]
            player_channels = [int(x.strip()) for x in player_ch.value.split(',')]
            total_channels = max(max(dm_channels), max(player_channels)) + 1

            spatial = SpatialAnalyzer(
                dm_channels=dm_channels,
                player_channels=player_channels,
            )
            session_audio = AudioService(device=dev, channels=total_channels)

            services.session_state.messages.clear()
            services.session_state.chunk_count = 0
            services.session_state.speaker_count = 0
            services.session_state.status = 'recording'

            session_page._state = services.session_state

            transcriber = SessionTranscriber(
                asr=services.asr,
                spatial=spatial,
                diarization=services.diarization,
                profiles=services.profiles,
                session_state=services.session_state,
            )

            services.asr.start_streaming()
            session_audio.start(on_chunk=lambda c: transcriber.process_chunk(c))

            state['active'] = True
            state['session_audio'] = session_audio
            state['transcriber'] = transcriber
            start_btn.set_visibility(False)
            stop_btn.set_visibility(True)
            status_lbl.text = 'recording...'
            status_lbl.style('color: #4caf50')

        def stop():
            if state.get('session_audio'):
                state['session_audio'].stop()
            services.asr.stop_streaming()
            if state.get('transcriber'):
                state['transcriber'].flush()
            services.session_state.status = 'idle'
            state['active'] = False
            stop_btn.set_visibility(False)
            start_btn.set_visibility(True)
            status_lbl.text = 'stopped'
            status_lbl.style('color: #888')
            ratio_lbl.text = ''

        start_btn.on_click(start)
        stop_btn.on_click(stop)

        def poll():
            s = services.session_state
            if s is None:
                return
            msgs = len(s.messages)
            status_lbl.text = (
                f'{s.status} | {msgs} msgs | {s.speaker_count} spk | '
                f'{s.chunk_count} chunks'
            )
            if state['active'] and state.get('session_audio'):
                levels = state['session_audio'].channel_rms_levels
                if len(levels) >= 2:
                    ratio_lbl.text = f'DM: {levels[0]:.0%} | Player: {max(levels[1:]):.0%}'

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

        preview_img = ui.image('').style(
            'max-width: 160px; max-height: 100px; object-fit: contain; '
            'border-radius: 4px; border: 1px solid #2a2a4a'
        )
        preview_img.set_visibility(False)

        def on_upload(e: events.UploadEventArguments):
            dest = SLIDESHOW_DIR / e.name
            dest.write_bytes(e.content.read())
            path_str = str(dest)
            if path_str not in slideshow_page._state.images:
                slideshow_page._state.images.append(path_str)
            info_lbl.text = f'uploaded {e.name} — {len(slideshow_page._state.images)} total'
            e.sender.run_method('reset')

        ui.upload(
            on_upload=on_upload,
            auto_upload=True,
            multiple=True,
            label='Drop images or click to browse',
        ).props(
            'accept=".png,.jpg,.jpeg,.gif,.webp,.svg" flat bordered dark color=amber'
        ).classes('w-full')

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
                preview_img.source = s.images[s.current_index]
                preview_img.set_visibility(True)
            else:
                info_lbl.text = 'no images loaded'
                preview_img.set_visibility(False)

        ui.timer(1, poll)


def _build_map_card():
    with ui.card().classes('dm-card flex-1'):
        ui.html('<h3>Maps</h3>')

        with ui.row().classes('gap-2 items-end w-full'):
            name_in = ui.input('Map name').props('dense outlined dark').classes('w-28')
            path_in = ui.input('Image path or URL').props('dense outlined dark').classes('flex-grow')
            ui.button('Set', on_click=lambda: _set_map()).props('dense')

        def on_upload(e: events.UploadEventArguments):
            dest = MAPS_DIR / e.name
            dest.write_bytes(e.content.read())
            name = dest.stem.lower().replace(' ', '-')
            map_page._maps[name] = f'/assets/maps/{e.name}'
            ui.notify(f'Map "{name}" added', type='positive')
            e.sender.run_method('reset')
            _refresh()

        ui.upload(
            on_upload=on_upload,
            auto_upload=True,
            multiple=True,
            label='Drop map images or click to browse',
        ).props(
            'accept=".png,.jpg,.jpeg,.gif,.webp,.svg" flat bordered dark color=amber'
        ).classes('w-full')

        thumbs_row = ui.row().classes('gap-2 flex-wrap w-full')
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
            thumbs_row.clear()
            names = sorted(map_page._maps.keys())
            if names:
                with thumbs_row:
                    for name in names:
                        src = map_page._maps[name]
                        with ui.column().classes('items-center gap-1 map-thumb').style(
                            'padding: 4px'
                        ):
                            ui.image(src).style(
                                'width: 80px; height: 60px; object-fit: cover; '
                                'border-radius: 4px'
                            )
                            ui.label(name).style('color: #888; font-size: 0.7rem')
                maps_lbl.text = f'{len(names)} maps'
            else:
                maps_lbl.text = 'no maps configured'

        _refresh()
