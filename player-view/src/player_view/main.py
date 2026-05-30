from pathlib import Path

from nicegui import app, ui

from player_view import services
from player_view.theme import apply_theme
import player_view.pages  # noqa: F401 — triggers @ui.page registration

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _init_services():
    services.init(profile_dir=PROJECT_ROOT / 'profiles')


def _teardown_services():
    services.teardown()


@ui.page('/')
def index():
    ui.navigate.to('/dm')


app.on_startup(_init_services)
app.on_shutdown(_teardown_services)
app.add_static_files('/assets', str(PROJECT_ROOT / 'assets'))


def run():
    ui.run(
        title='Shattered Sea',
        dark=True,
        show=False,
        host='0.0.0.0',
        port=8080,
        reload=True,
    )


if __name__ in {'__main__', '__mp_main__'}:
    run()
