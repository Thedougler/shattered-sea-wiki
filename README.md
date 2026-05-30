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
| `.claude/skills/live-co-dm/scripts/` | The voice-profile + transcription Python tools (this README's main subject). |
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

## Voice & transcription tools (live-co-dm)

These are the scripts you run by hand. They capture per-character **voice profiles**, then
**transcribe a 4-hour+ session** with overlap-aware speaker separation tuned for a noisy
table (≈5 players, heavy crosstalk, each voicing several characters).

All paths below are relative to the repo root. Apple Silicon required (Parakeet via MLX +
pyannote on MPS/CPU).

### One-time setup

```bash
# 1. Virtualenv + dependencies (the venv is gitignored)
python3 -m venv .claude/skills/live-co-dm/.venv
source .claude/skills/live-co-dm/.venv/bin/activate
pip install -r .claude/skills/live-co-dm/requirements.txt

# 2. Hugging Face token (pyannote models are gated — free account)
#    Accept the license for pyannote/speaker-diarization-3.1 + the embedding model
#    on their HF model pages, then:
export HF_TOKEN=hf_xxxxxxxxxxxxxxxxx

# 3. macOS microphone permission
#    System Settings -> Privacy & Security -> Microphone -> enable your terminal app
```

First run downloads the Parakeet and pyannote weights (a few minutes); they cache after
that. Full detail: `.claude/skills/live-co-dm/references/setup.md`.

Every session below assumes the venv is active and `HF_TOKEN` is exported:

```bash
source .claude/skills/live-co-dm/.venv/bin/activate
export HF_TOKEN=hf_...
```

### Save a voice profile

One profile per **character voice**. Run once per voice each table member performs, before
your first transcription.

```bash
python3 .claude/skills/live-co-dm/scripts/voice_profiler.py \
    --name "Grigori" --player "Dave"
```

Then open the printed URL (default `http://localhost:8080`), click **Start**, read the
auto-scrolling teleprompter aloud *in character* (~60–90s), then **Stop & Save**.

| Flag | Meaning |
|---|---|
| `--name` | The **character voice** (e.g. `Grigori`, `Captain Nona`). One profile per voice. |
| `--player` | The **physical person** performing it (e.g. `Dave`). Groups one person's many voices so they can be told apart. |
| `--script-file PATH` | Optional. Use your own teleprompter text instead of the bundled passage. |
| `--port N` | Optional. Change the web port. |

Profiles are written to `.claude/skills/live-co-dm/profiles/<slug>.json` and **committed**
to the repo, so the table's voices travel with the wiki. Re-running with the same `--name`
overwrites that profile. Detail: `references/voice-profiler.md`.

### Transcribe a session

**Pass 1 — live capture.** Start at session open and leave running the whole game; `Ctrl-C`
to stop.

```bash
python3 .claude/skills/live-co-dm/scripts/transcribe_session.py \
    --session 4 --speakers 5
```

| Flag | Meaning |
|---|---|
| `--session N` | Session number. Omit to auto-pick the next one. |
| `--speakers N` | **Physical people at the table** (not character count). The single biggest accuracy win on crosstalk — always set it. |
| `--threshold` | Cosine match cutoff for voice ID (default `0.5`). Raise to split confused voices; lower to rescue known ones falling through to `Unknown-N`. |

It writes a growing transcript to `wiki/sessions/.live/session-04/live_transcript.md` and
silence-chunked audio under `.live/session-04/audio/`. Everything under `.live/` is
gitignored scratch, flushed to disk immediately so a crash at hour three loses nothing.

**Pass 2 — finalize** (after the session). Re-diarizes the entire recording at once with the
known speaker count — far more accurate on overlap — and writes the canonical transcript.

```bash
python3 .claude/skills/live-co-dm/scripts/finalize_session.py \
    --session 4 --speakers 5
```

Output: `wiki/sessions/session-04-transcript.md` (committed; the audio stays gitignored).
From there, ask the agent to fold it into canon via the `ttrpg-wiki-ingest` transcript path.

### Correction loop (profiles that improve over time)

Profiles get sharper every session if you close the loop:

1. Correct the finalized `wiki/sessions/session-NN-transcript.md` — fix any mislabeled
   `(?)` lines or wrong speakers.
2. **Re-save** the affected characters' profiles (`voice_profiler.py --name ...`). The
   profiler harvests each character's corrected lines, slices the matching `.live` audio,
   and folds that real in-character speech into the profile. Overlap/low-confidence lines
   are skipped and outliers rejected, so correction only ever sharpens.

For this to work, **keep the session's `.live/session-NN/audio/` directory** until you're
done improving profiles from it. Detail: `references/transcription.md`.

### Transcript markers

```
**Delmar** (Ben) [01:12:04]: hold fast, she's coming about
**Nona (?)** (Sam) [01:12:05] [overlap]: belay that
```

`(?)` = low-confidence attribution. `[overlap]` = crosstalk region; both speakers get a
stacked line so no one is dropped. This is honest uncertainty, not a bug — the finalize
pass resolves much of it.

### If separation is poor

- Confirm `--speakers` matches the people actually talking.
- Re-enroll thin/echoey profiles in a quieter room.
- Nudge `--threshold` (up to split confused voices, down to rescue known ones).

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

The voice/transcription logic has a unit suite that needs **no ML stack** — pure stdlib:

```bash
cd .claude/skills/live-co-dm/scripts
python3 -m unittest discover -s . -p 'test_*.py'
```

Optional real-adapter checks (venv active + `HF_TOKEN` set):

```bash
RUN_ML_TESTS=1 python3 -m unittest test_ml_integration -v
```
