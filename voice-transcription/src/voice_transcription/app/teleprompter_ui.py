"""Read-only teleprompter WebUI — voice actor faces this screen.

Dark background, large serif text, auto-scroll, word grey-out. No controls.
Optimized for readability at 2-3 feet distance.

The page polls a shared SessionOrchestrator snapshot for state updates. New
paragraphs appear dynamically when the LLM extends the script.
"""

from __future__ import annotations

import html as html_mod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.session_orchestrator import SessionOrchestrator

TELEPROMPTER_CSS = """\
html, body {
    margin: 0;
    padding: 0;
    background: #111118;
    color: #e8e8e8;
    font-family: 'Georgia', 'Libre Baskerville', 'Times New Roman', serif;
    font-size: 2.6rem;
    line-height: 2.0;
    letter-spacing: 0.02em;
    overflow: hidden;
}
.teleprompter-container {
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 15vh 2rem 40vh 2rem;
    height: 100vh;
    overflow-y: auto;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}
.teleprompter-container::-webkit-scrollbar {
    display: none;
}
.teleprompter-para {
    margin-bottom: 2.5rem;
    text-align: left;
}
.word-span {
    transition: color 0.4s ease;
}
.word-span.read {
    color: #444450;
}
.nicegui-content {
    padding: 0 !important;
}
"""


def render_paragraphs(text: str) -> str:
    if not text.strip():
        return ""
    paragraphs = text.split("\n\n")
    parts: list[str] = []
    word_idx = 0
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        words = para.split()
        spans: list[str] = []
        for word in words:
            escaped = html_mod.escape(word)
            spans.append(
                f'<span id="word-{word_idx}" class="word-span">{escaped}</span>'
            )
            word_idx += 1
        parts.append(
            f'<p class="teleprompter-para">{" ".join(spans)}</p>'
        )
    return "\n".join(parts)


def run_teleprompter(orchestrator: SessionOrchestrator, *, port: int = 8080) -> None:  # pragma: no cover
    """Start the teleprompter via NiceGUI's own ``ui.run`` (blocking).

    Designed to be called from a daemon thread so it doesn't conflict with the
    TUI on the main thread. We must go through ``ui.run`` rather than serving
    the bare FastAPI app under uvicorn directly: NiceGUI's startup hook aborts
    unless ``ui.run`` has populated the run config and wired up storage and the
    required middlewares. uvicorn only installs signal handlers on the main
    thread, so ``ui.run`` is safe to call from this daemon thread.
    """
    from nicegui import ui

    @ui.page("/", dark=True)
    def index() -> None:
        ui.add_head_html(f"<style>{TELEPROMPTER_CSS}</style>")

        container = ui.html("").classes("teleprompter-container")
        last_rendered = {"token_count": 0, "matched": -1}

        def _update() -> None:
            snap = orchestrator.snapshot()
            new_count = snap["total_tokens"]
            new_matched = snap["matched_up_to"]

            if new_count != last_rendered["token_count"]:
                container.content = render_paragraphs(snap["full_text"])
                last_rendered["token_count"] = new_count

            if new_matched != last_rendered["matched"]:
                last_rendered["matched"] = new_matched
                if new_matched >= 0:
                    ui.run_javascript(f'''
                        for (let i = 0; i <= {new_matched}; i++) {{
                            const el = document.getElementById("word-" + i);
                            if (el) el.classList.add("read");
                        }}
                        const cur = document.getElementById("word-{new_matched}");
                        if (cur) cur.scrollIntoView({{behavior: "smooth", block: "center"}});
                    ''')

        ui.timer(0.4, _update)

    ui.run(
        host="0.0.0.0",
        port=port,
        title="Teleprompter",
        show=False,
        reload=False,
        uvicorn_logging_level="warning",
    )
