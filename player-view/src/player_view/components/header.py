from nicegui import ui

HEADER_HEIGHT = 100
HEADER_BG = "#0a0a12"
HEADER_BORDER = "#2a2a3a"


def operator_header(title: str = ""):
    ui.add_css(f"""
        .q-header {{
            height: {HEADER_HEIGHT}px !important;
            min-height: {HEADER_HEIGHT}px !important;
            max-height: {HEADER_HEIGHT}px !important;
        }}
        .q-page-container {{
            padding-top: {HEADER_HEIGHT}px !important;
        }}
        .operator-header {{
            font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
            font-size: 0.85rem;
            color: #999;
        }}
        .operator-header .q-field__label {{
            font-size: 0.75rem;
            color: #666;
        }}
        .operator-header .q-field__native,
        .operator-header .q-field__input {{
            font-size: 0.85rem;
            color: #ccc;
        }}
        .operator-header .q-btn {{
            font-size: 0.75rem;
            padding: 4px 12px;
        }}
    """)
    header = (
        ui.header()
        .classes("operator-header items-center gap-3 px-4 no-wrap")
        .style(
            f"background: {HEADER_BG}; "
            f"border-bottom: 2px solid {HEADER_BORDER}; "
            f"overflow: hidden;"
        )
    )
    with header:
        if title:
            ui.label(title).style(
                "color: #c9a84c; font-weight: bold; font-size: 0.9rem; "
                "min-width: 100px; white-space: nowrap;"
            )
        ui.separator().props("vertical").classes("self-stretch")
    return header
