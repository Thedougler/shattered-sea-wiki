# LLM-Wiki Infrastructure — Optimization Backlog

Deferred items from the 2026-06-03 comprehensive infrastructure audit. The high-confidence fixes
(context dedup, multi-harness removal, index-regen hook, skill merges, prep-family extraction,
description fixes) shipped in commits `e4edfc0`, `e61eeff`, `23d5d0f`. The rest is captured here,
roughly in value order. The `continuous-self-improvement` / `enforced-in-code` skills are the
right entry points for working this list.

## Scripts — deterministic loop orchestration (design-only for now)

Turn prose-driven deterministic loops into enforced, resumable scripts so the agent spends
context on judgment, not bookkeeping:

- `world_update.py` — drive the post-session tick: triage threads, call `roll-dice/roll.sh` for
  each (scripted d20, logged), enforce one-thread-at-a-time write, prevent skipped steps.
- `daily_update.py` — chain init → lint → ingest with per-phase error handling and checkpoints.
- `session_ingest.py --resume` — persist multi-pass state, prevent double-processing, validate
  speaker maps. (`assemble_transcript.py` already covers part of this.)
- `csi_loop.py` — enforce the continuous-self-improvement MEASURE→IDENTIFY→FIX→ENFORCE→VERIFY→LOG
  order using `wiki_health_snapshot.py` as the measure/verify bookends.

## Skills — bloat trimming (move procedure to references/)

Four SKILL.md files carry procedural detail that belongs in `references/` so the body stays
scannable:

- `ttrpg-wiki-lint` (~554 lines) → move the "working the report" walkthrough to a reference.
- `skill-creator` (~485) → move the step-by-step creation tutorial to a reference.
- `session-ingest` (~469) → move per-pass detail to `references/pass-architecture.md`.
- `continuous-self-improvement` (~408) → move steps 2–6 detail to `references/csi-steps.md`.

## Skills — registry refresh (stale)

`ttrpg-llm-wiki-init/references/skill-registry.md` references skills that don't exist:
`prep-strong-start`, `player-interest-tracker`, `combat-data-extract`, `wiki-categorize`,
`transcript-ingest`, `hot-update`. Reconcile the registry against the actual skill set
(`ls .claude/skills/`) — it's the routing brain and should match reality.

## Hooks — judgment-heavy automations (not high-confidence)

- Auto-stub creation for unresolved `[[wikilinks]]` (extend `check-wikilinks.sh`): create a
  minimal stub via `fix_frontmatter.py` instead of only warning. Risk: spurious stubs.
- Bidirectional-backlink hook: after an entity write, add reciprocal links to targets. Risk:
  rewriting prose / wrong insertion point. Needs careful, idempotent design.

## Scripts — quality / hygiene

- Consolidate duplicate test files: fold `test_wiki_health_snapshot.py` into `_ext` and
  `test_check_ingest.py` into `_ext` (the basic versions are subsets).
- `tag_taxonomy.py` ↔ `wiki/system/taxonomy.md` drift check (module is source of truth; the
  human-readable copy can silently diverge).

## Settings — permission tightening

- Replace the blanket `Bash(python3 .../.claude/scripts/*)` allow with an explicit script
  allowlist.
- Replace directory-level `git add .claude/*` / `git add wiki/*` with narrower patterns if a
  tighter blast radius is wanted.

## Loose ends

- `soultrace/` skill is **untracked** in git — decide whether to track or remove it.
- `ttrpg-llm-wiki-init/SKILL.md` has a non-standard `version` frontmatter key (skill-creator
  `quick_validate.py` flags it). Remove or move under `metadata:`.
- prep-* stub-check variants in `prep-hb-item`, `prep-ship`, `prep-location` still carry a local
  stub line; they could point fully at `prep-family-standards.md` once their extra content is
  reconciled.
