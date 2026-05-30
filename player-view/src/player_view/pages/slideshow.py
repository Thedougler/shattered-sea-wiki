import random
from pathlib import Path

from nicegui import app, ui
from pydantic import BaseModel

from player_view.theme import apply_theme
from player_view.models.state import SlideshowState

_state = SlideshowState()

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}


class FolderPayload(BaseModel):
    path: str
    interval_s: float = 10.0


@app.post('/api/slideshow/folder')
def set_folder(payload: FolderPayload):
    folder = Path(payload.path)
    if not folder.is_dir():
        return {'ok': False, 'error': 'not a directory'}
    images = [str(p) for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
    random.shuffle(images)
    _state.images = images
    _state.current_index = 0
    _state.interval_s = payload.interval_s
    return {'ok': True, 'count': len(images)}


def _scan_default_folder():
    candidates = [
        Path(__file__).resolve().parent.parent.parent.parent / 'assets' / 'slideshow',
    ]
    for folder in candidates:
        if folder.is_dir():
            images = [str(p) for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
            if images:
                random.shuffle(images)
                _state.images = images
                return


@ui.page('/slideshow')
def slideshow_page():
    apply_theme()

    if not _state.images:
        _scan_default_folder()

    img = None

    with ui.column().classes('w-full h-screen items-center justify-center'):
        if _state.images:
            img = ui.image(_state.images[0]).classes('max-w-full max-h-screen object-contain')
        else:
            img = ui.image('').classes('max-w-full max-h-screen object-contain')
            ui.label('No images loaded').classes('text-2xl').style('color: #888')

    def advance():
        if not _state.images:
            return
        _state.current_index = (_state.current_index + 1) % len(_state.images)
        img.source = _state.images[_state.current_index]

    ui.timer(_state.interval_s, advance)
