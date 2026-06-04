# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Repo Is

An LLM-assisted D&D 5e (2024) campaign wiki ("Shattered Sea") that is both an **Obsidian vault** (`wiki/`) and a **Claude Code agent workspace** (`.claude/`).

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
| `packages/lib/` | `@shattered-sea/lib` — shared TS library (vault, frontmatter, schema, wikilinks, taxonomy). |
| `packages/cli/` | `@shattered-sea/cli` — `sea` CLI (fix, fm, index, taxonomy). Thin wrappers around lib. |
| `tools/audio/` | `shattered-audio` — Python tool for session transcription + diarization (separate venv). |
| `Inbox/`, `.raw/` | Source material waiting to be ingested into the wiki. |

### Wiki Structure Notes

- `entities/places/` root is empty (index only). Every place goes in a typed subfolder: `regions/`, `islands/`, `settlements/`, `buildings/`, `dungeons/`, `sites/`, `planes/`.
- `entities/items/` is subdivided by rarity: `common/`, `uncommon/`, `rare/`, `legendary/`, `artifact/`. Items without rarity stay at root.
- `entities/creatures/` is subdivided by usage: `active/` (used in session), `planned/` (in prep/situations), `background/` (unused stat blocks).
- Subtypes must match path inference. Run `sea fm drift --subtype` to check, `sea fm sync --subtype` to fix.

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
(`qmd-reindex.sh`), `wiki/index.md` regeneration (`regen-index.sh`, debounced + backgrounded —
never hand-edit `index.md`), Python formatting (`format-python.sh`), and Python linting
(`lint-python.sh`).

Read order: `wiki/hot.md` first → `wiki/system/task-routing.md` → entity/situation files
the task needs. Never read the full vault before generating content.

Operational references (auto-correct, wikilinks, frontmatter defaults) live in
`.claude/skills/ttrpg-llm-wiki-init/references/`.

Hooks auto-fix mechanical issues and *flag* the rest — they do not silently move, rename, or
restructure content. Escalate to the DM only for: genuine lore contradictions between two
established facts; ambiguous entity identity (two pages may describe the same entity); and
lifecycle decisions (e.g. moving a situation active → resolved).

---

## Scripts & Commands

Script catalog and commands: `.claude/scripts/README.md`.

### Monorepo (pnpm workspace)

- `pnpm build` — build all TS packages. `pnpm build:lib`, `build:cli`, `build:ui` for individual packages.
- `pnpm dev` — start UI dev server (`:4321`). `pnpm dev:lib` for lib watch mode.
- `pnpm test` / `pnpm test:lib` — run tests. `pnpm test:watch` for interactive Vitest.
- `pnpm typecheck` — fast `tsc --noEmit` across lib + cli.
- `pnpm lint` / `pnpm lint:fix` — Biome lint + format check (or auto-fix).
- `pnpm check` — typecheck + lint in one command.
- `pnpm clean` — remove all dist/build artifacts.
- `node packages/cli/dist/cli.js <command>` — run sea CLI (or `npx sea` if linked).
- UI imports `@shattered-sea/lib` — delete nothing from `packages/lib/src/` without checking UI builds.
- The lib uses standalone `zod`, not `astro/zod`. Astro content validation works but JSON schema generation warns.

### sea CLI — frontmatter operations

- `sea fm get <field> [--dir <path>] [--filter field=value]` — read field values across files.
- `sea fm set <field> <value> [files...] [--dir <path>] [--filter field=value] [--dry-run]` — idempotent field update.
- `sea fm drift [--type] [--subtype] [--dir <path>]` — report type/subtype mismatches vs path inference.
- `sea fm sync [--type] [--subtype] [--dir <path>] [--dry-run]` — bulk-fix type/subtype to match path inference.

---

## Git Discipline

Global git rules (commit by default, stage specific paths, never amend/force-push/skip hooks)
live in `~/.claude/CLAUDE.md` and apply here. Project-specific deltas only:

- This is a solo content repo — commit directly to `main`. Only branch when explicitly asked.
- Use the commit-prefix table below.

### Commit Prefixes

| Prefix | Use for |
|---|---|
| `fix:` | Structural corrections (broken links, wrong frontmatter) |
| `ingest:` | Source material processed into wiki |
| `curation:` | Content quality improvements |
| `prep:` | Prep-skill outputs (encounters, NPCs, locations, items, etc.) |
| `feat:` | New features in packages or scripts |
| `refactor:` | Code restructuring in packages or scripts |

---

## Self-Healing Writes

PostToolUse hooks run automatically on every Write/Edit to wiki files. They enforce
correctness that the agent must not duplicate manually — but agents **must act on their
output**.

### What the hooks do

| Hook | Action | Agent responsibility |
|---|---|---|
| `validate-frontmatter.sh` | Adds missing fields, stamps `updated:` (TS CLI preferred, Python fallback) | If it prints `FLAG: summary is default`, write a real summary before committing |
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
closes the loop on anything that requires judgment. Never suppress, ignore, or work around
hook output — the hooks are the source of truth for mechanical correctness.

---

## Change Log

Use `git log` for structural change history.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
