# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Repo Is

An LLM-assisted D&D 5e (2024) campaign wiki ("Shattered Sea") that is both an **Obsidian vault** (`wiki/`) and a **Claude Code agent workspace** (`.claude/`). A companion **player-view** NiceGUI app (`player-view/`) handles live voice profiling, transcription, and OBS-ready overlays.

**System:** D&D 5e 2024 | **Style:** Sandbox | **Status:** Active

---

## Campaign State

Party roster, current arc, faction clocks, and live situations are all in `wiki/hot.md`.
Read that file — do not rely on summaries here.

---

## Repo Layout

| Path | Purpose |
|---|---|
| `wiki/` | Obsidian vault — all campaign content. Start at `wiki/hot.md` then `wiki/index.md`. |
| `wiki/system/` | Agent-facing system files: task-routing, PC primers. |
| `wiki/narrative-islands/` | Plot-device clusters (not geographic islands — see memory). |
| `wiki/situations/active/` | Live threads. `resolved/` for closed ones. |
| `.claude/skills/` | Claude Code skills (prep, ingest, lint, live co-DM). |
| `.claude/scripts/` | Pure-stdlib maintenance scripts (no venv needed). |
| `player-view/` | NiceGUI web app — voice profiling, live transcription, OBS overlays. Has its own `CLAUDE.md`. |
| `Inbox/`, `.raw/` | Source material waiting to be ingested into the wiki. |

---

## Sandbox Rules (apply to all wiki content)

**PC Boundary.** Never write what a PC decides, chooses, intends, feels, thinks, or wants.
Write what the environment does and what NPCs do.

**NPC Agency.** NPC goals predate the party. NPCs pursue their goals — they don't wait for
players to arrive.

**Pressures, Not Plots.** Frame content as pressures and possibilities, never scripted
outcomes. No "if players do X then Y" chains more than one step deep.

**PC-Connection Requirement.** Every NPC, location, faction, and situation must pull on at
least one PC's internal tensions. If you can't name the connection, the element isn't ready —
ask the DM before generating.

**Ideal State.** Every file has complete frontmatter with a concrete `summary`; all wikilinks
resolve; durable relationships are bidirectional; no orphans; `hot.md` reflects current state.

## Automatic Behaviors

A PreToolUse hook (`block-env-edits.sh`) prevents edits to `.env` files. PostToolUse hooks
enforce: frontmatter completeness (`validate-frontmatter.sh`), search index updates
(`qmd-reindex.sh`), Python formatting (`format-python.sh`), and Python linting
(`lint-python.sh`). `index.md` is regenerated via `regen_index.py`, not hand-edited.

Read order: `wiki/hot.md` first → `wiki/system/task-routing.md` → entity/situation files
the task needs. Never read the full vault before generating content.

Operational references (auto-correct, wikilinks, frontmatter defaults) live in
`.claude/skills/ttrpg-llm-wiki-init/references/`.

---

## Scripts & Commands

### Wiki maintenance (pure stdlib, no venv)

```bash
python3 .claude/scripts/regen_index.py --write   # regenerate wiki/index.md
python3 .claude/scripts/wiki_lint.py              # lint vault (auto-detects Obsidian CLI + markdownlint)
python3 .claude/scripts/wiki_lint.py --obsidian on  # force Obsidian CLI for deeper cross-file checks
python3 .claude/scripts/check_ingest.py           # list source material still pending ingest
python3 .claude/scripts/fix_frontmatter.py <file> # add missing frontmatter fields to a single file
python3 .claude/scripts/archive_source.py <file>   # git-mv ingested source from Inbox/ to .raw/
python3 .claude/scripts/ingest_packet.py <dir>     # compile context packet for subagent ingest
python3 .claude/scripts/assemble_transcript.py     # assemble transcript chunks into a single file
python3 .claude/scripts/preprocess_pdf.py <file>   # extract text from PDF source material
python3 .claude/scripts/sync_skills.py             # sync .claude/skills/ to mirror directories
python3 .claude/scripts/tag_taxonomy.py            # validate/report on tag usage across the vault
python3 .claude/scripts/wiki_health_snapshot.py    # capture vault health metrics (--save to persist)
markdownlint-cli2 "wiki/**/*.md"                  # markdown formatting (config: .markdownlint-cli2.jsonc)
```

### player-view app (requires venv)

```bash
cd player-view
python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"  # first-time setup
.venv/bin/python -m player_view.main                            # serves on localhost:8080
```

### Tests

```bash
cd player-view && .venv/bin/pytest tests/   # unit tests (no ML stack needed)
```

Script tests live in `.claude/scripts/test_*.py` — run with `python3 .claude/scripts/test_<name>.py -v`.

---

## Git Discipline

This is a solo content repo. Commit directly to `main`. Only branch when explicitly asked.

**Commit by default.** When you finish a coherent unit of work, commit it without being
asked. Group related changes into one logical commit with a clear, conventional message.
Skills that define their own commit cadence (e.g. ingest commits per-source) take precedence.

**Stage specific paths.** Use `git add <path>…`, not `git add -A` or `git add .`.
Path-scoped staging of the directories you changed is fine (e.g., `git add wiki/`).

**Never** amend published commits, skip hooks (`--no-verify`), or force-push to main.

### Commit Prefixes

| Prefix | Use for |
|---|---|
| `fix:` | Structural corrections (broken links, wrong frontmatter) |
| `ingest:` | Source material processed into wiki |
| `curation:` | Content quality improvements |
| `prep:` | Prep-skill outputs (encounters, NPCs, locations, items, etc.) |
| `feat:` | New features in player-view or scripts |
| `refactor:` | Code restructuring in player-view or scripts |

---

## Self-Healing Writes

PostToolUse hooks run automatically on every Write/Edit to wiki files. They enforce
correctness that the agent must not duplicate manually — but agents **must act on their
output**.

### What the hooks do

| Hook | Action | Agent responsibility |
|---|---|---|
| `validate-frontmatter.sh` | Adds missing fields, stamps `updated:` | If it prints `FLAG: summary is default`, write a real summary before committing |
| `check-wikilinks.sh` | Warns on unresolved `[[wikilinks]]` | Fix the link target or create a stub file before committing |
| `qmd-reindex.sh` | Rebuilds search index (background) | None — fully automatic |
| `format-python.sh` | Runs ruff format on Python edits | None — fully automatic |
| `lint-python.sh` | Runs ruff check on Python edits | Fix any lint errors it surfaces |

### The protocol

1. **Write the file.** Hooks fire automatically.
2. **Read hook output.** If a hook prints a `FLAG:` or `Unresolved wikilinks` warning, fix
   the issue in a follow-up edit before moving to the next file.
3. **Commit only clean files.** Do not commit a file with unresolved hook warnings. A file
   is clean when a re-edit produces no warnings.

This makes every wiki write self-healing: hooks catch mechanical errors, and the agent
closes the loop on anything that requires judgment.

---

## Change Log

Use `git log` for structural change history.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
