# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Repo Is

An LLM-assisted D&D 5e (2024) campaign wiki ("Shattered Sea") that is both an **Obsidian vault** (`wiki/`) and a **Claude Code agent workspace** (`.claude/`). A companion **player-view** NiceGUI app (`player-view/`) handles live voice profiling, transcription, and OBS-ready overlays.

**System:** D&D 5e 2024 | **Style:** Sandbox | **Status:** Active

---

## Party

| PC | Notes |
|---|---|
| Crissdalynn Khinriss | Crow aarakocra monk |
| Perrin Black-Jaw | Rattkin sailor; bodhran, Minor Illusion |
| Jean-Claude Tabarnack | Poison dart frog ranger; holds secret about Simone |
| Delmar Fisk | Scarlet admiral coat; musket; party face |

**Home base:** *Uncertainty* (ex-HCS Surety) — `wiki/entities/vehicles/hcs-surety.md`
**Current arc:** Party in Calveno after Session 03; ship in dry dock at La Vasca (5-day repair); three new active situations (abyss vision, Umberlee's message, Nona's favor); Kyzil reunited with Crissdalynn.

---

## Active Factions (Clock Status)

Update this block after every session or faction-clock run.

| Faction | Clock | Next Trigger |
|---|---|---|
| Dravosi Crown | Moving — Rupert Knighton will send ships for Cap'n Gorgeous | Knighton's ships intercept or party enters Crown territory |
| The Passage | Nona met; attacks called off; favor owed (Perrin, unconditional); Anzolo status unknown | Nona uses sending stone; Anzolo surfaces |

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

PostToolUse hooks enforce: frontmatter completeness (`fix_frontmatter.py`), search index
updates (`qmd-reindex.sh`), Python linting (`lint-python.sh`). `index.md` is regenerated
via `regen_index.py`, not hand-edited.

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

No test suite exists for the wiki scripts — they're validated by the hooks on every edit.

---

## Commit Conventions

Commit messages follow these prefixes:
- `fix:` — structural corrections
- `ingest:` — source material processed into wiki
- `curation:` — content quality improvements
- `feat:` / `refactor:` — for player-view and script code changes

Commit directly to `main` — this is a solo content repo. Only branch when explicitly asked.

---

## Change Log

Use `git log` for structural change history.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
