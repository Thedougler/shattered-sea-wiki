# Wiki DnD — NPC Prep

> **Prerequisite:** `../PREP.md` loaded (philosophy, universal rules, PC gravity, roleplay method, naming conventions).

---

## Interview

If the user message doesn't already answer these, ask all at once — not one at a time:

- Campaign/setting context
- Race/species
- Role or function in the story
- Which PC is the hook, and how

---

## Toy Fields (5)

| Field | Content |
|---|---|
| `primary_goal` | What they always want |
| `consistent_method` | How they pursue it — a gimmick, not a personality. Must be doable at the table in 5 seconds. |
| `active_problem` | What's going wrong for them right now |
| `performance_hooks` | Roleplay Concept + one physical tic |
| `link_of_relevance` | Which PC's thread connects here, and how |

### Field Rules

**Primary Goal** — a vector, not a state. What the NPC is moving toward regardless of players.
- ✓ "Accumulate enough wealth to retire before the audit."
- ✗ "Is ambitious and greedy."

**Consistent Method** — behaviour only. How they pursue the goal: tactics, moral limits, resources. Cut everything after an em dash that analyses rather than describes.
- ✓ "Feigns helplessness, then names his price. Never in writing."
- ✗ "Feigns helplessness while quietly naming his price — which signals she prefers soft power but will escalate if needed."

**Active Problem** — the situation only. Must be a problem *for this NPC*, right now. Not their feelings about it, not their response to it, not a countdown.
- ✓ "A dockworker witnessed his last handoff and is demanding silence money."
- ✗ "Is being blackmailed and has decided to pay — deadline in three days."

**Performance Hooks** — one vibe reference + one speech pattern. Nothing more. Vibe = a real-world cultural/aesthetic shorthand the DM can inhabit instantly. Speech = one verbal tic, pattern, or signature line. Do not write physical stage directions. Do not write multiple hooks. Do not explain what the hook means.

**Link of Relevance** — which PC's backstory, fear, or goal does this NPC connect to? Required. One sentence. If you can't answer this, the NPC isn't ready.

---

## Output Structure

**Roleplay Concept** — first line above everything else. Mashup format per `../PREP.md` § Roleplay Method. Mandatory.

**Quote** — mandatory. One sentence, in character. Immediately after Roleplay Concept. If this quote could belong to any NPC, rewrite it. The DM reads this line, then speaks.

**Lore Sheet** — 2–4 sentences of concrete facts. Not a backstory — a dossier. Each sentence gives the DM something usable. No adjective piles, no dramatic commentary.

**Callouts:**

- `> [!read-aloud]` — 1–2 sentence first impression. Sensory, present tense, player-facing prose mode. Load `ttrpg-writing` and read `references/player-facing-prose.md`.
- `> [!appearance]` — build, colouring, bearing. One signature detail. 1–3 sentences.
- `> [!secret]` — only for genuinely hidden info. Omit if nothing is hidden.

**Sections (in order):**

1. `## Toy Chest` — five toy fields as a markdown table (mirrors frontmatter)
2. `columns` codeblock with stable `id` — left: Appearance + Voice & Delivery; right: Lore Sheet
3. `## Connections` — wikilinks to related entities
4. `## Stat Block` — optional; use `../STATBLOCK.md` if included
5. `## Session Events` — Activity Log; format below

---

## Villain NPC (Combat-Oriented)

Use when the NPC is a recurring antagonist with a stat block. Layer this on top of the standard NPC structure.

### Three Villain Questions

1. **What do they want?** Specific, not "power" — *"they want to resurrect their dead sister by sacrificing the city"*
2. **What do they fear?** The crack in the armour — emotionally and mechanically
3. **What is their tell?** One physical habit, speech pattern, or recurring motif that makes them recognisable

### Stat Block Approach

Villain NPCs follow class-inspired frameworks rather than pure creature design.

- Assign an effective class level (CR ≈ class level as a rough guide)
- **Spellcaster villains**: 5–7 prepared spells maximum; choose spells with clear tactical intent
- **Martial villains**: one signature combat technique (called shot, defensive riposte, weapon trick)
- **Hybrid villains**: one martial feature + limited spellcasting (3 spells max)

### Villain-Specific Mechanics

- **Escape mechanic**: Recurring villains almost always need a way out — misty step, legendary action dash, a lackey who sacrifices themselves. Killing a villain too early ends a story arc.
- **Personal shield**: Something that feels like invulnerability until players figure it out (Magic Resistance, *Shield* spell, an amulet to destroy first).
- **Monologue trait** *(flavour)*: Once per combat, the villain can speak without using their action. This is for the DM. Include a suggested line.

### Villain Stat Block Tag

Add this block after the stat block:

> **Personality.** [Two sentences: their affect/manner, then one specific habit or tell.]
> **Motivation.** [One sentence stating exactly what they want right now in this encounter.]
> **Escape Condition.** [What triggers their retreat and how they do it.]

---

## Activity Log

The `## Session Events` section is an Activity Log — a chronological record of the NPC's interactions with the party. Fill it during and after sessions. Never retroactively edit entries; if a new development contradicts an older entry, add a `> [!contradiction]` callout below it.

**Entry format:**
```
**Session [N] — [YYYY-MM-DD]**: [What the NPC did, said, or decided. What changed in their status, goals, or relationship with the party. Observable facts only — no analysis.]
```

**Example:**
```
**Session 03 — 2026-05-18**: Refused to name the Chain Council contact. Offered Delmar passage to Calvino in exchange for dropping the inquiry. Took the deal.
**Session 04 — 2026-05-25**: Recognized Jean-Claude from the Blacktide job. Demeanor shifted — warmer, or more careful. Unclear which.
```

The log is the NPC's history as the players actually experienced it. It prevents continuity breaks when the NPC reappears and gives the GM a fast summary before a session.

---

## Filing

Read `templates/npc.md` (or `templates/person.md` for non-NPC individuals) before generating page content — the template defines required frontmatter and section structure. Directory: `content/shattered-sea/characters/npcs/` (see `templates/CLAUDE.md` for the full map). Run vault filing sequence from `../PREP.md` § Vault Filing after writing.
