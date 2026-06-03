---
name: prep-npc
description: >
  Create or expand a named NPC wiki page for the Shattered Sea campaign. Invoke for:
  "prep an NPC", "create a page for [NPC]", "flesh out [NPC]", "I need an NPC who...",
  "expand [NPC]'s entry", any NPC that will appear at the table. Generates frontmatter,
  toy fields, lore sheet, read-aloud appearance, voice notes, connections, and DM
  companion page. Checks wiki/index.md for stubs before creating. Also use for villain
  NPCs needing stat block integration.
---

> **Shared prep conventions** — stub check, interview + PC-connection requirement, combat calibration, prose pass, and filing — live in [`prep-family-standards`](../ttrpg-llm-wiki-init/references/prep-family-standards.md). Read it before generating; this file covers only what's specific to this content type.
## Interview

If the user message doesn't already answer these, ask all at once — not one at a time:
- Setting/campaign context and which location this NPC appears in
- Race/species
- Role or function in the story (merchant, villain, faction leader, contact, etc.)
- Which specific PC's backstory, goal, or fear does this NPC connect to?

Name the connecting PC or ask before generating.

---

## Toy Fields (Frontmatter + Body)

Write these in YAML frontmatter AND as a `## Toy Chest` table in the body. Keep both in sync.

| Field | What goes here |
|---|---|
| `primary_goal` | What they always want — a vector, not a state. What they're moving toward. |
| `consistent_method` | How they pursue it — a gimmick, not a personality. Doable at the table in 5 seconds. |
| `active_problem` | The situation only. A problem for THIS NPC, right now. Not their response to it. |
| `performance_hooks` | Roleplay Concept mashup + one speech pattern. Nothing more. |
| `link_of_relevance` | Which PC's backstory, fear, or goal connects here. Required. One sentence. |

**Field rules:**
- `primary_goal` — vector: ✓ "Accumulate enough to retire before the audit." ✗ "Is ambitious."
- `consistent_method` — behavior only: ✓ "Feigns helplessness, then names his price. Never in writing." ✗ Analysis after the em dash.
- `active_problem` — situation only: ✓ "A dockworker witnessed his last handoff and is demanding money." ✗ Feelings about it.
- `performance_hooks` — vibe + speech: one real-world cultural shorthand the DM can inhabit instantly + one verbal tic. Nothing more.

---

## Output Structure

**Roleplay Concept** — first line of the body, above everything else. Mashup format: [cultural shorthand the DM can inhabit instantly] + [role that shouldn't work but does].

**Quote** — mandatory. One sentence, in character. Immediately after Roleplay Concept. If this quote could belong to any NPC, rewrite it. The DM reads this line, then speaks.

**Lore Sheet** — 2–4 sentences. Dossier, not backstory. Each sentence gives the DM something usable.

**Callouts:**
- `> [!read-aloud]` — 1–2 sentence first impression. Sensory, present tense, player-facing prose mode.
- `> [!dm]` — one concrete staging note or watch-for.

**Sections (in order):**
1. `## Toy Chest` — five toy fields as a markdown table
2. `## Voice & Delivery` — speech pattern, 2–3 table-ready lines, physical mannerisms, emotional default
3. `## Connections` — wikilinks to related entities
4. `## Stat Block` — optional; use only when needed for combat
5. `## Session Events` — Activity Log (append-only chronological record)

**Activity Log format:**
```
**Session [N] — [YYYY-MM-DD]**: [What they did, said, or decided. Observable facts only.]
```

---

## Villain NPC Additions

When the NPC is a recurring antagonist, add after the standard structure:

**Three Villain Questions:**
1. What do they want? (Specific, concrete — not "power")
2. What do they fear? (The crack in the armour — emotional and mechanical)
3. What is their tell? (One physical habit or speech pattern)

**Villain mechanics:** escape mechanic (recurring villains need a way out), personal shield (something that feels like invulnerability until players solve it), optional monologue trait.

Full detail: `references/NPC.md`

---

## Publish Pairing

For any NPC introduced to players: create paired pages.
- Wiki page at `wiki/entities/characters/npcs/npc-slug.md` — `publish: true`, `audience: players`
- DM companion noted in frontmatter via `dm_companion:` field
- DM-only content (secrets, mechanics, hidden agenda) goes in a separate audience:dm file or in wiki sections marked with `audience: dm` frontmatter

---

## Frontmatter

Universal and entity fields are auto-completed by the write hook. You must author the NPC-specific values: the five toy fields (`primary_goal`, `consistent_method`, `active_problem`, `performance_hooks`, `link_of_relevance` — see Toy Fields above) and `quote`. Keep these in sync with the `## Toy Chest` body table.

---

## Visual Aid

Load `ttrpg-visual-aids` to generate a portrait after writing the page. Category:
**Portraits** (3:4 vertical, chest-up). Place after the Quote, before the Lore Sheet.
Skip for minor NPCs who won't appear at the table.

---

## Filing

After writing the page:
1. Add entry to `wiki/index.md` under `## entities/characters/npcs`
2. Add reciprocal links to all referenced entities
3. Commit: `feat: npc — {slug} — {one-line summary}`

---

Load `ttrpg-writing` before writing any prose. **DM-facing reference** for lore sheet,
toy fields, voice notes, and DM companion. **Player-facing prose** for `[!read-aloud]`
callouts. Anti-slop, Brennan voice, callout types, and publish contracts all apply.

---

## Reference Files

| File | Read when |
|---|---|
| `references/NPC.md` | Full NPC template, villain variant, activity log format, detailed field rules |
| `../ttrpg-writing/references/dm-reference-standards.md` | Writing lore sheet, toy fields, voice notes, DM companion |
| `../ttrpg-writing/references/player-facing-prose.md` | Writing `[!read-aloud]` appearance callout |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement and conversion |
| `../ttrpg-writing/references/NAMES.md` | Naming a new NPC — linguistic roots by race |
| `../ttrpg-llm-wiki-init/references/auto-correct.md` | Fixing structural issues during or after content creation |
| `../ttrpg-llm-wiki-init/references/wikilink-standards.md` | Creating or fixing wikilinks |
