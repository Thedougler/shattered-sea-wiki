import time

from nicegui import app, ui
from pydantic import BaseModel

from player_view.theme import apply_theme
from player_view.models.state import ChatMessage, SessionState

_state = SessionState()


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

    message_container = None
    status_labels = {}

    with ui.column().classes('w-full h-screen'):
        with ui.row().classes('w-full p-4 gap-8').style('border-bottom: 1px solid #333'):
            status_labels['status'] = ui.label('idle').classes('status-panel')
            status_labels['length'] = ui.label('0:00').classes('status-panel')
            status_labels['chunks'] = ui.label('0 chunks').classes('status-panel')
            status_labels['speakers'] = ui.label('0 speakers').classes('status-panel')

        message_container = ui.column().classes(
            'w-full flex-grow overflow-y-auto p-4 gap-1'
        )

    last_count = {'value': 0}

    def refresh():
        if _state.status:
            status_labels['status'].text = _state.status
        mins, secs = divmod(int(_state.session_length_s), 60)
        hrs, mins = divmod(mins, 60)
        status_labels['length'].text = f'{hrs}:{mins:02d}:{secs:02d}' if hrs else f'{mins}:{secs:02d}'
        status_labels['chunks'].text = f'{_state.chunk_count} chunks'
        status_labels['speakers'].text = f'{_state.speaker_count} speakers'

        current_count = len(_state.messages)
        if current_count > last_count['value']:
            with message_container:
                for msg in _state.messages[last_count['value']:]:
                    with ui.column().classes('chat-message').style('background: #1a1a2e'):
                        ui.label(msg.speaker).classes('chat-speaker')
                        ui.label(msg.text).style('color: #e8e6e3')
            last_count['value'] = current_count
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

    ui.timer(0.5, refresh)
