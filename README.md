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
| `wiki/sessions/` | Session notes, recaps, and run-guides (canon session records). |
| `wiki/system/` | Doctrine, party primers, routing rules (agent-facing reference). |
| `.claude/skills/` | Claude Code skills (campaign prep, ingest, lint, live co-DM). |
| `.claude/scripts/` | Pure-stdlib maintenance scripts (index regen, frontmatter, ingest helpers). |
| `tools/audio/` | `shattered-audio` — Python voice/transcription package (venv at `tools/audio/.venv`). |
| `.raw/sessions/session-NN/` | Session source packets: raw audio, transcripts, ingest artifacts. |
| `Inbox/sessions/session-NN/` | Mutable processing workbench (processing/, scratch/, incoming/). |
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

The audio pipeline lives in `tools/audio/` (`shattered-audio` Python package, venv at
`tools/audio/.venv`). Apple Silicon required (MLX Whisper + pyannote on MPS/CPU).
Use the Claude Code skills — they wrap the underlying CLI and handle venv/token setup.

### Session lifecycle

```
Record  →  .raw/sessions/session-NN/audio/raw/mic-XX/part-000.m4a
              + .raw/sessions/session-NN/audio/manifest.json

Transcribe  →  .raw/sessions/session-NN/transcripts/raw/session-NN-part-PP.csv

Assemble  →  .raw/sessions/session-NN/transcripts/assembled/session-NN-assembled.csv

Ingest (session-ingest skill)  →  .raw/sessions/session-NN/ingest/{speaker-map,recap,extracts,flags,combat-summary}.md

Active processing workbench  →  Inbox/sessions/session-NN/{processing,scratch,incoming}/

Canon session notes  →  wiki/sessions/session-NN*.md  (UNCHANGED)
```

### Skills

| Skill | What it does |
|---|---|
| `record-session-audio` | Captures every mic to isolated chunked m4a tracks (ffmpeg per mic). |
| `transcribe-session-audio` | Whisper large-v3 + pyannote over per-mic tracks; speaker-labeled by voice profile. |
| `manage-voice-profiles` | CRUD for actor/persona voice profiles used by the transcription engine. |
| `session-ingest` | Multi-pass mining of transcript CSVs → wiki propagation. |

### One-time setup

```bash
# Virtualenv + dependencies
pip install -e "tools/audio/[all]"

# Hugging Face token (pyannote models are gated)
# Accept license at https://huggingface.co/pyannote/speaker-diarization-3.1
# Then put in .env:
HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
```

### Correction loop

After each session: review the assembled transcript, correct speaker labels, then run
`shattered-audio retrain` with the corrected file and a `--speaker-map` from session-ingest.
Profiles improve automatically each session via weighted blending.

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
cd tools/audio && pip install -e ".[dev]" && pytest tests/
```

Optional real-adapter checks (venv active + `HF_TOKEN` set):

```bash
pytest tools/audio/tests/test_session_transcribe.py tools/audio/tests/test_record.py -v
```
