# player-view

NiceGUI web app serving two roles: player-facing display pages (added to OBS as browser sources) and a DM control panel for managing everything from a browser tab.

## Running

```
cd player-view
.venv/bin/python -m player_view.main
```

Serves on `http://localhost:8080`.

## Pages

### DM-only (browser tab)

- [/dm](http://localhost:8080/dm) — control panel: manage voice profiles, slideshow, maps, session status

### Player-facing (OBS browser sources)

Each page has a 100px operator header with controls. In OBS, crop the top 100px to hide it from players.

- [/save-speaker](http://localhost:8080/save-speaker) — teleprompter for voice profile enrollment
- [/test-speaker](http://localhost:8080/test-speaker) — raw ASR output + profile matching
- [/session](http://localhost:8080/session) — live transcription chat log (last 30 messages)
- [/slideshow](http://localhost:8080/slideshow) — random image rotation from a folder
- [/map/{name}](http://localhost:8080/map/overworld) — full-screen named map image

## Voice profiling

Uses parakeet-mlx for streaming ASR and pyannote for speaker embeddings. Profiles are saved as JSON in `profiles/` and can be strengthened with additional samples.

## Dependencies

Requires Python 3.11+, HF_TOKEN in repo-root `.env` (for pyannote/embedding gated model).
