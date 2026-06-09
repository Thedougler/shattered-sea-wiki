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

## Automatic Behaviors & Self-Healing Writes

PreToolUse hooks block edits to `.env` and lockfiles. PostToolUse hooks (see `.claude/hooks/`)
fire on every Write/Edit: they complete frontmatter, rebuild the search index and `wiki/index.md`
(backgrounded — never hand-edit `index.md`), and format/lint Python + TS. Most are silent on success.

**You must act on hook output that needs judgment:**
- `FLAG: summary is default` → write a real `summary` before committing.
- `Unresolved wikilinks` → fix the target or create a stub before committing.
- A `lint-python` failure blocks the edit → fix it.

Commit only clean files (a re-edit produces no warnings). Never suppress or work around hook output.

Read order: `wiki/hot.md` → `wiki/system/task-routing.md` → only the entity/situation files the
task needs. Never read the full vault before generating. Operational references (auto-correct,
wikilinks, frontmatter defaults) live in `.claude/skills/ttrpg-llm-wiki-init/references/`.

Hooks auto-fix mechanics and *flag* the rest — they never silently move, rename, or restructure.
Escalate to the DM only for: genuine lore contradictions between two established facts; ambiguous
entity identity (two pages may describe the same entity); and lifecycle decisions (active → resolved).

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

Global git rules (commit and push by default, stage specific paths, never amend/force-push/skip hooks)
live in `~/.claude/CLAUDE.md` and apply here. After completing any operation, commit and push to `Thedougler/shattered-sea-wiki` (main) as the final step. Use the `gh` CLI for all GitHub operations (PRs, issues, checks, releases) — never the GitHub MCP server when `gh` can do the job. Project-specific deltas only:

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

## Change Log

Use `git log` for structural change history.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
