---
type: system
subtype: system-file
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "Single source of truth for cross-cutting wiki rules: reading order, sandbox constraints, the PC-connection requirement, the auto-correct protocol, frontmatter requirements, and wikilink standards. Skills point here instead of restating these."
created: 2026-05-28
updated: 2026-05-28
tags: [system, doctrine]
sources: []
system_role: doctrine
token_profile: on-demand
mandatory_for: []
update_trigger: "When a cross-cutting rule changes that more than one skill depends on."
---

# Wiki Doctrine — Shattered Sea

These rules used to be restated in CLAUDE.md, `ttrpg-writing`, `sandbox-narrative`,
`ttrpg-llm-wiki-init`, and every `prep-*` skill. They now live here once. Skills load this
file on demand instead of carrying their own copy, which keeps more context free for actual
wiki content. Read the section you need; you rarely need all of it.

---

## What is enforced automatically (don't do this by hand)

A PostToolUse hook runs `.claude/scripts/fix_frontmatter.py` after every wiki write. It
**already**: adds any missing required frontmatter field with a path-inferred default, and
stamps `updated:` to today. So you do not need to hand-maintain frontmatter completeness or the
`updated` date — write the content and let the hook complete it. The hook surfaces only the
things that need *your* judgment (a still-default `summary`).

`index.md` is regenerated, not hand-edited: run `python3 .claude/scripts/regen_index.py --write`.
Other deterministic helpers live in `.claude/scripts/` (`regen_index`, `archive_source`,
`check_ingest`, `sync_skills`). Reach for a script before doing its job token-by-token.

---

## Reading order (context budget protocol)

Read in this order. **Stop as soon as you have enough context for the task. Never read the
full vault before generating content.**

1. `wiki/hot.md` — always first. Current state, live threads, predictions.
2. `wiki/system/task-routing.md` — find which files and skill the task needs.
3. This file (`doctrine.md`) — for any cross-cutting rule.
4. Entity files for relevant NPCs/locations/factions — read the `summary` frontmatter first.
   If the summary answers the question, do not open the full file.
5. Situation files in `wiki/situations/active/` — for live threads.
6. Session notes in `wiki/sessions/` — only when continuity or sequence matters.
7. Raw sources in `.raw/` — only when the compiled page is insufficient.

CLAUDE.md is already in context every session — do not re-read it.

---

## Sandbox constraints (apply to all content)

The Shattered Sea is a player-driven sandbox. These override standard fiction technique
wherever they conflict: fiction builds toward authored outcomes, sandbox builds toward
interesting decisions.

**The Player Character Boundary.** Never write what a PC decides, chooses, intends, feels,
thinks, or wants. Write what the environment does and what NPCs do. If a sentence ends with a
player character taking action or having a feeling, rewrite it to end with the world doing
something instead.

```
❌ Your breath catches as the ship crests the wave.
✅ The ship crests the wave, and for one suspended moment the whole sea is below you.
❌ You feel the weight of what you've done.
✅ The square is empty now. The torch they lit is still burning.
```

**Independent NPC Agency.** Write NPC goals as if the party doesn't exist yet. Faction
objectives predate the party. NPCs pursue their goals — they don't wait for players to arrive.

**Pressures, Not Plots.** Frame content as pressures (things that are true and building) and
possibilities (what the environment affords), never as scripted outcomes. Avoid "if the players
do X, then Y happens" chains scripted more than one step deep.

- ❌ "Players will discover the cult and stop the ritual."
- ✅ "There is a cult. They are recruiting. The ritual happens in 5 days. Here's what they want and what happens if no one stops them."

---

## The PC-connection requirement

Every NPC, location, faction, and situation must pull on at least one PC's internal tensions
(their dials, terminal node, or active friction — see `sandbox-narrative`). When creating or
expanding one of these, name the PC connection. **If you cannot name it, the element isn't
ready — ask the DM before generating.** This is the single gravity filter all prep skills share.

---

## Auto-correct protocol (act, don't ask)

Structural problems are fixed immediately and committed — never ask for confirmation. This is
safe because every fix is reversible in git and none of them invents canon.

| Violation | Auto-correction |
|---|---|
| File in wrong path | Move to correct path; update inbound wikilinks; commit |
| Missing frontmatter field | Handled by the hook (`fix_frontmatter.py`) |
| Broken wikilink | Create stub at correct path; add to index; commit |
| Naming-convention violation | Rename to kebab-case; update inbound wikilinks; commit |
| Missing bidirectional relationship | Add the reciprocal link to the target file; commit |
| Orphaned file | Add to index; link from a natural parent; commit |
| Situation/island in wrong lifecycle folder | Move; update `lifecycle`/`status`; update links; commit |
| Stub `summary` still default text | `FLAG: summary-stale — {file}` — do **not** guess content |

**Escalate to the DM only for:** a genuine contradiction between two established facts (append
to `wiki/discrepancy-log.md`, leave both traces visible), or ambiguous entity identity (two
pages may describe the same thing). Everything else: fix and move on.

Commit message conventions: `fix: {type} — {file} — {what}` · `ingest: {source} — {outputs}` ·
`curation: {file} — {what changed}`.

---

## Frontmatter requirements by type

The hook completes these automatically; this table is the reference for what "complete" means.

**Universal (every file):** `type` · `subtype` · `campaign` · `status` · `audience` ·
`publish` · `summary` · `created` · `updated` · `tags` · `sources`

**Additional by type:**
- Entities (characters, places, factions, items, vehicles, deities): + `confidence_level` · `relationships`
- Situations: + `lifecycle` (dormant/active/resolved) · `island`
- Islands: + `portable` · `entry_points` · `contains_situations`
- Sessions: + `session_number` · `session_date`
- System files (audience: agent): + `system_role` · `token_profile` · `mandatory_for` · `update_trigger`

Full default values and path-inference tables:
`.claude/skills/ttrpg-llm-wiki-init/references/frontmatter-defaults.md`.

**The `summary` is the most important field** — it is often the only thing read before deciding
whether to open a file. It must answer *what is this RIGHT NOW, and why does it matter*, in ≤2
sentences, with concrete facts. Bad: "An important NPC." Good: "Rattkin matriarch of the
Black-Jaw Run; reunited with Perrin in Calveno, has a favor to ask."

---

## Wikilink standards

- Always alias: `[[npc-slug|NPC Display Name]]` — never bare slugs in body text.
- First mention of a named entity in a section gets a link; later mentions in the same section don't.
- When a wikilink target doesn't exist, create a stub immediately at the correct path with
  `status: stub` and a `summary` of `"Stub — referenced in [[source]]. No page yet."`, then add
  it to the index. The hook fills the rest of the frontmatter.
- Bidirectional rule: if A links B as a durable relationship, B gets the reciprocal link. Use the
  standardized relationship labels in `frontmatter-defaults.md`.

---

## Ideal state

The vault is healthy when: every file has complete frontmatter and a concrete, current
`summary`; all wikilinks resolve; durable relationships are bidirectional; each file sits at the
correct path with no duplication (cross-link, don't copy); no file is orphaned; `hot.md` reflects
actual current world state; and `wiki/log.md` records every structural change.
