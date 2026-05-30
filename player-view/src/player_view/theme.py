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
    overflow: hidden;
}
.nicegui-content {
    padding: 0 !important;
}
.q-page {
    background-color: #111118 !important;
}

/* --- Scroll container (hidden scrollbar) --- */
.scroll-hidden {
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
}
.scroll-hidden::-webkit-scrollbar {
    display: none;
}

/* --- Teleprompter word states --- */
.teleprompter-text {
    font-size: 3.2rem;
    line-height: 1.6;
    font-family: Georgia, 'Times New Roman', Baskerville, serif;
    color: #e8e6e3;
    padding: 2rem;
}
.teleprompter-text .spoken {
    color: #3a3a3a;
    transition: color 0.4s ease;
}
.teleprompter-text .draft {
    color: #777;
    font-style: italic;
    transition: color 0.3s ease;
}
.teleprompter-text .current {
    color: #c9a84c;
    text-shadow: 0 0 20px rgba(201, 168, 76, 0.3);
}

/* --- Status strip (fixed bottom bar) --- */
.status-strip {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 72px;
    background: linear-gradient(180deg, #0f0f1a 0%, #0a0a12 100%);
    border-top: 1px solid #2a2a3a;
    display: flex;
    align-items: center;
    padding: 0 2rem;
    gap: 1.5rem;
    z-index: 200;
    font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
    font-size: 1.1rem;
    color: #888;
}

/* --- Recording indicator --- */
.rec-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #333;
    flex-shrink: 0;
    transition: background 0.3s;
}
.rec-dot.active {
    background: #f44336;
    animation: pulse-rec 1.5s ease-in-out infinite;
}
@keyframes pulse-rec {
    0%, 100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.6); }
    50% { box-shadow: 0 0 0 8px rgba(244, 67, 54, 0); }
}
.rec-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: #555;
    letter-spacing: 0.05em;
    transition: color 0.3s;
}
.rec-label.active {
    color: #f44336;
}

/* --- VU meter --- */
.vu-meter {
    width: 180px;
    height: 14px;
    background: #1a1a2e;
    border-radius: 3px;
    overflow: hidden;
    border: 1px solid #2a2a3a;
    flex-shrink: 0;
}
.vu-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #4caf50 0%, #8bc34a 40%, #ffeb3b 70%, #f44336 100%);
    transition: width 0.08s linear;
    border-radius: 3px;
}

/* --- Voice match label --- */
.voice-match {
    font-size: 1.1rem;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* --- Match results (test-speaker, large for distance) --- */
.match-result {
    padding: 0.6rem 1.5rem;
    margin: 0.3rem 0;
}
.match-name {
    font-size: 2rem;
    color: #e8e6e3;
    font-family: Georgia, serif;
    min-width: 180px;
}
.match-bar-container {
    flex: 1;
    height: 20px;
    background: #1a1a2e;
    border-radius: 4px;
    overflow: hidden;
    margin: 0 1rem;
    border: 1px solid #2a2a3a;
}
.match-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}
.match-pct {
    font-size: 1.8rem;
    font-family: 'SF Mono', monospace;
    min-width: 80px;
    text-align: right;
}

/* --- Raw ASR output --- */
.raw-output {
    font-size: 2.8rem;
    line-height: 1.5;
    font-family: Georgia, serif;
    padding: 2rem;
    color: #e8e6e3;
}
.raw-output .finalized {
    color: #e8e6e3;
}
.raw-output .draft-text {
    color: #777;
    font-style: italic;
}

/* --- Chat messages --- */
.chat-message {
    font-size: 1.8rem;
    padding: 0.7rem 1.2rem;
    margin: 0.3rem 0;
    border-radius: 0.5rem;
    border-left: 4px solid #333;
    background: #1a1a2e;
}
.chat-speaker {
    font-size: 1.2rem;
    font-weight: bold;
    font-family: 'SF Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.chat-text {
    color: #e8e6e3;
    line-height: 1.4;
}
@keyframes msg-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.chat-message-new {
    animation: msg-in 0.3s ease-out;
}

/* --- Status panel (header labels) --- */
.status-panel {
    font-size: 1.2rem;
    color: #888;
    font-family: 'SF Mono', 'Fira Code', monospace;
}
'''


def apply_theme():
    ui.add_css(DISTANCE_CSS)
    ui.query('body').style(f'background-color: {BACKGROUND}')
