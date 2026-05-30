from pathlib import Path

from nicegui import app, ui
from pydantic import BaseModel

from player_view.components.header import operator_header
from player_view.theme import apply_theme

_maps: dict[str, str] = {}

MAPS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "maps"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


class MapPayload(BaseModel):
    image_path: str


@app.post("/api/map/{name}")
def set_map(name: str, payload: MapPayload):
    _maps[name] = payload.image_path
    return {"ok": True}


def _discover_maps():
    if not MAPS_DIR.is_dir():
        return
    for path in MAPS_DIR.iterdir():
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            name = path.stem.lower().replace(" ", "-")
            if name not in _maps:
                _maps[name] = f"/assets/maps/{path.name}"


@ui.page("/map/{name}")
def map_page(name: str):
    apply_theme()
    _discover_maps()

    src = _maps.get(name, "")
    available = ", ".join(sorted(_maps.keys())) or "none"

    with operator_header(f"Map: {name}"):
        ui.label(f"available: {available}").style("color: #666")

    ui.query("body").style("overflow: hidden")

    if src:
        ui.image(src).classes("w-full").style(
            "height: calc(100vh - 100px); object-fit: contain;"
        )
    else:
        with (
            ui.column()
            .classes("w-full items-center justify-center")
            .style("height: calc(100vh - 100px);")
        ):
            ui.label(f'Map "{name}" not found').classes("text-3xl").style(
                "color: #c9a84c"
            )
            ui.label(f"Available: {available}").classes("text-xl").style("color: #888")
