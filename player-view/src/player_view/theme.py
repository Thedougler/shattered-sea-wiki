from nicegui import ui

BACKGROUND = '#111118'
TEXT_COLOR = '#e8e6e3'
ACCENT = '#c9a84c'

DISTANCE_CSS = '''
body {
    background-color: #111118 !important;
    color: #e8e6e3;
    font-family: Georgia, 'Times New Roman', Baskerville, serif;
    font-size: 2.5rem;
    line-height: 1.4;
}
.nicegui-content {
    padding: 0 !important;
}
.q-page {
    background-color: #111118 !important;
}
.teleprompter-text {
    font-size: 3.2rem;
    line-height: 1.5;
    font-family: Georgia, 'Times New Roman', Baskerville, serif;
    color: #e8e6e3;
}
.teleprompter-text .spoken {
    color: #555;
    transition: color 0.3s ease;
}
.chat-message {
    font-size: 1.8rem;
    padding: 0.5rem 1rem;
    margin: 0.3rem 0;
    border-radius: 0.5rem;
}
.chat-speaker {
    font-size: 1.4rem;
    font-weight: bold;
    color: #c9a84c;
}
.status-panel {
    font-size: 1.2rem;
    color: #888;
    font-family: 'SF Mono', 'Fira Code', monospace;
}
'''


def apply_theme():
    ui.add_css(DISTANCE_CSS)
    ui.query('body').style(f'background-color: {BACKGROUND}')
