import time

from nicegui import app, ui
from pydantic import BaseModel

from player_view.theme import apply_theme
from player_view.components.header import operator_header
from player_view.models.state import ChatMessage, SessionState

_state = SessionState()

_SPEAKER_COLORS: dict[str, str] = {}
_PALETTE = [
    '#e74c3c', '#3498db', '#2ecc71', '#e67e22', '#9b59b6',
    '#1abc9c', '#f39c12', '#e91e63', '#00bcd4', '#8bc34a',
]


def _speaker_color(name: str) -> str:
    if name not in _SPEAKER_COLORS:
        _SPEAKER_COLORS[name] = _PALETTE[len(_SPEAKER_COLORS) % len(_PALETTE)]
    return _SPEAKER_COLORS[name]


class MessagePayload(BaseModel):
    speaker: str
    text: str


class StatusPayload(BaseModel):
    status: str | None = None
    session_length_s: float | None = None
    chunk_count: int | None = None
    speaker_count: int | None = None


@app.post('/api/session/message')
def push_message(payload: MessagePayload):
    msg = ChatMessage(speaker=payload.speaker, text=payload.text, timestamp=time.time())
    _state.messages.append(msg)
    return {'ok': True, 'count': len(_state.messages)}


@app.post('/api/session/status')
def push_status(payload: StatusPayload):
    if payload.status is not None:
        _state.status = payload.status
    if payload.session_length_s is not None:
        _state.session_length_s = payload.session_length_s
    if payload.chunk_count is not None:
        _state.chunk_count = payload.chunk_count
    if payload.speaker_count is not None:
        _state.speaker_count = payload.speaker_count
    return {'ok': True}


@ui.page('/session')
def session_page():
    apply_theme()

    with operator_header('Session'):
        status_lbl = ui.label('idle').style('color: #888')
        length_lbl = ui.label('0:00').style('color: #888')
        chunks_lbl = ui.label('0 chunks').style('color: #888')
        speakers_lbl = ui.label('0 spk').style('color: #888')

    VISIBLE_MESSAGES = 30

    message_container = ui.column().classes(
        'w-full p-4 gap-1 session-messages scroll-hidden'
    ).style('height: calc(100vh - 100px);')

    rendered = {'count': 0}

    def refresh():
        status_lbl.text = _state.status or 'idle'
        mins, secs = divmod(int(_state.session_length_s), 60)
        hrs, mins = divmod(mins, 60)
        length_lbl.text = f'{hrs}:{mins:02d}:{secs:02d}' if hrs else f'{mins}:{secs:02d}'
        chunks_lbl.text = f'{_state.chunk_count} chunks'
        speakers_lbl.text = f'{_state.speaker_count} spk'

        total = len(_state.messages)
        if total == rendered['count']:
            return

        tail = _state.messages[-VISIBLE_MESSAGES:]
        message_container.clear()
        with message_container:
            for msg in tail:
                color = _speaker_color(msg.speaker)
                with ui.column().classes('chat-message chat-message-new').style(
                    f'border-left-color: {color}'
                ):
                    ui.label(msg.speaker).classes('chat-speaker').style(f'color: {color}')
                    ui.label(msg.text).classes('chat-text')
        rendered['count'] = total
        ui.run_javascript('''
            const c = document.querySelector('.session-messages');
            if (c) c.scrollTo({top: c.scrollHeight, behavior: 'smooth'});
        ''')

    ui.timer(0.5, refresh)
