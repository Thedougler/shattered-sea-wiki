# Shattered Sea

An LLM-assisted campaign wiki for **Shattered Sea**, a sandbox D&D 5e (2024) game. The
repo is two things at once:

- An **Obsidian vault** (`wiki/`) holding all campaign canon — NPCs, locations, ships,
  factions, situations, session notes, and current world state.
- A **Claude Code agent workspace** (`.claude/`) with skills that prep sessions, ingest
  source material, lint the vault, and co-DM live at the table — plus a set of
  **Python voice/transcription tools** you run yourself.

If you just want to read or edit the campaign, open `wiki/` in Obsidian. Everything below
is for running the tooling.

---

## Layout

| Path | What's there |
|---|---|
| `wiki/` | The Obsidian vault — all campaign content. Start at `wiki/hot.md` (current state) and `wiki/index.md`. |
| `wiki/sessions/` | Session notes, recaps, run-guides, and committed finalized transcripts. |
| `wiki/system/` | Doctrine, party primers, routing rules (agent-facing reference). |
| `.claude/skills/` | Claude Code skills (campaign prep, ingest, lint, live co-DM). |
| `.claude/scripts/` | Pure-stdlib maintenance scripts (index regen, frontmatter, ingest helpers). |
| `voice-transcription/` | The voice-profile + transcription Python tools (this README's main subject). |
| `Inbox/`, `.raw/` | Source material waiting to be ingested into the wiki. |

---

## The wiki

Open the repo root as an Obsidian vault. Conventions worth knowing:

- **`wiki/hot.md`** is the single source of current truth — faction clocks, live threads,
  what's happening right now. Read it first.
- Frontmatter and the `updated` date are maintained automatically by a Claude Code hook;
  you don't hand-edit them.
- `wiki/index.md` is generated, not hand-edited — regenerate with
  `python3 .claude/scripts/regen_index.py`.
- Most content work happens by talking to the Claude Code agent (`prep-session`,
  `ttrpg-wiki-ingest`, etc.), not by editing raw files. See `CLAUDE.md` / `AGENTS.md` for
  the governance rules the agent follows.

---

## Voice & transcription tools

These are the tools you run by hand. They capture per-character **voice profiles**, then
**transcribe a 4-hour+ session** with overlap-aware speaker separation tuned for a noisy
table (≈5 players, heavy crosstalk, each voicing several characters).

The code lives in `voice-transcription/` — a proper Python package with `pyproject.toml`.
Apple Silicon required (Parakeet via MLX + pyannote on MPS/CPU).

Three convenience wrappers live at the repo root — **start here**. Each one creates the
virtualenv, installs dependencies on first run, reads `HF_TOKEN` from `.env`, and then runs
the underlying Python tool. Flags pass straight through.

```bash
./save_voice.sh         --name "Grigori" --player "Dave"
./transcribe_session.sh --session 4 --speakers 5
./finalize_session.sh   --session 4 --speakers 5
```

### One-time setup

```bash
# 1. Virtualenv + dependencies (the venv is gitignored)
python3.11 -m venv voice-transcription/.venv
source voice-transcription/.venv/bin/activate
pip install -e voice-transcription/

# 2. Hugging Face token (pyannote models are gated — free account)
#    Accept the license for pyannote/speaker-diarization-3.1 + the embedding model
#    on their HF model pages, then:
export HF_TOKEN=hf_xxxxxxxxxxxxxxxxx

# 3. macOS microphone permission
#    System Settings -> Privacy & Security -> Microphone -> enable your terminal app
```

> The wrappers do all of the above for you. Put your token in `.env` once
> (`HF_TOKEN=hf_...`) and you never need to activate the venv or export anything.

### Save a voice profile

One profile per **character voice**. Run once per voice each table member performs.

```bash
./save_voice.sh --name "Grigori" --player "Dave"
```

Then open the printed URL (default `http://localhost:8080`), click **Start** (the ASR
model loads, then recording begins). Read the teleprompter aloud *in character* — words
grey out as they are recognized. Click **Stop & Save**; the process exits cleanly.

| Flag | Meaning |
|---|---|
| `--name` | The **character voice** (e.g. `Grigori`, `Captain Nona`). One profile per voice. |
| `--player` | The **physical person** performing it (e.g. `Dave`). Groups one person's many voices. |
| `--script-file PATH` | Optional. Use your own teleprompter text instead of the bundled passage. |
| `--port N` | Optional. Change the web port. |

Profiles are written to `voice-transcription/profiles/<slug>.json` and **committed** to the
repo. Re-running with the same `--name` overwrites that profile.

### Transcribe a session

**Pass 1 — live capture.** Start at session open and leave running; `Ctrl-C` to stop.

```bash
./transcribe_session.sh --session 4 --speakers 5
```

| Flag | Meaning |
|---|---|
| `--session N` | Session number. Omit to auto-pick the next one. |
| `--speakers N` | **Physical people at the table** (not character count). Always set it. |
| `--threshold` | Cosine match cutoff for voice ID (default `0.5`). |

**Pass 2 — finalize** (after the session):

```bash
./finalize_session.sh --session 4 --speakers 5
```

Output: `wiki/sessions/session-04-transcript.md` (committed).

### Correction loop

Profiles get sharper every session: correct the finalized transcript, then re-save the
affected profiles. The profiler harvests corrected audio automatically. Keep the session's
`.live/` audio until you're done improving profiles from it.

### Transcript markers

```
**Delmar** (Ben) [01:12:04]: hold fast, she's coming about
**Nona (?)** (Sam) [01:12:05] [overlap]: belay that
```

`(?)` = low-confidence attribution. `[overlap]` = crosstalk region.

---

## Maintenance scripts

Pure-stdlib helpers in `.claude/scripts/` (no venv needed). The agent usually runs these,
but they're plain CLI:

| Command | Does |
|---|---|
| `python3 .claude/scripts/regen_index.py` | Regenerate `wiki/index.md`. |
| `python3 .claude/scripts/wiki_lint.py` | Lint the vault — frontmatter, broken wikilinks, orphans. |
| `python3 .claude/scripts/check_ingest.py` | List source material still pending ingest. |

---

## Tests

The voice/transcription logic has a unit suite that needs **no ML stack**:

```bash
cd voice-transcription && pip install -e ".[dev]" && pytest tests/
```

Optional real-adapter checks (venv active + `HF_TOKEN` set):

```bash
RUN_ML_TESTS=1 pytest tests/test_ml_integration.py -v
```
