# Prep-Family Standards

Shared conventions for every `prep-*` content-creation skill (prep-npc, prep-faction,
prep-location, prep-creature, prep-encounter, prep-dungeon, prep-situation, prep-island,
prep-ship, prep-hb-item, prep-session). Each prep skill points here instead of restating these
rules. The skill's own file covers only what is specific to its content type (its structure,
toy fields, templates, and domain reference files).

When a prep skill says *"Follow prep-family-standards,"* apply everything below.

---

## 1. Stub check (before creating anything)

Always check `wiki/index.md` for an existing stub or page before creating a new one. If a stub
exists, expand it in place — do not create a duplicate. If two pages may describe the same
entity, stop and ask the DM (ambiguous identity is a DM-escalation, not an auto-merge).

## 2. Interview (before generating)

If the user's message doesn't already answer what you need, ask all open questions **at once** —
never one at a time. The questions vary by content type (the skill lists its own), but every
interview must resolve:

- **The PC connection.** Which specific PC's backstory, goal, fear, or wound does this element
  pull on? Name that PC explicitly. If you cannot name one, the element isn't ready — ask the DM
  before generating. (This is the PC-Connection Requirement from CLAUDE.md, enforced here.)

State the connecting PC in the output. "Connects to the party" is not an answer; "pressures
Kael's debt to the Tessarine" is.

## 3. Sandbox discipline (while writing)

These come from CLAUDE.md and bind all wiki content:

- **PC Boundary.** Never write what a PC decides, feels, thinks, intends, or wants. Write what
  the environment does and what NPCs do.
- **NPC Agency.** NPC/faction goals predate the party and advance independently. Write a vector
  (what they move toward), not a static state.
- **Pressures, not plots.** Frame as pressures and possibilities. No "if players do X then Y"
  chains more than one step deep.

## 4. Combat calibration (creatures, encounters, dungeons, items)

Before finalizing anything with combat numbers, read `wiki/system/party-combat-primer.md`
(party combat profile). CR alone is not calibration — check it against what this party actually
does at the table. `pc-combat-primer` owns that profile; defer to it for difficulty questions.

## 5. Toy fields

Entity pages carry "toy" frontmatter the DM can play in five seconds. The universal model and
field rules live in `../../ttrpg-writing/references/UNIVERSAL-TOYS.md`. Each skill lists the specific fields for its
type and shows them as a body table kept in sync with frontmatter. Rules of thumb: goals are
vectors not states; methods are behaviors doable at the table, not personality analysis;
problems are situations, not feelings about them.

## 6. Three-Clue Rule (mysteries, situations, dungeons, islands)

For any conclusion the players must *reach* (a culprit, a hidden door, a betrayal), seed **at
least three** independent clues pointing to it, placed across different scenes/sources so no
single failed check or skipped room dead-ends the thread. Don't gate a revelation behind one
roll. Full treatment in `sandbox-narrative`.

## 7. Prose pass (before finalizing prose)

Load `ttrpg-writing` before writing any prose:

- **DM-facing reference** standard for DM notes, lore sheets, toy fields, NPC handles —
  terse, scannable, devoid of false mystery (`../../ttrpg-writing/references/dm-reference-standards.md`).
- **Player-facing prose** standard for `> [!read-aloud]` callouts — sensory, present tense
  (`../../ttrpg-writing/references/player-facing-prose.md`).
- **Callout types** must be correct (`../../ttrpg-writing/references/callout-standard.md`).
- Naming a new entity: `../../ttrpg-writing/references/NAMES.md`.

Then load `sandbox-narrative` for an anti-railroading pass on the finished content.

## 8. Filing (after writing)

1. Save to the correct path for the content type (the skill states it).
2. Add the page to `wiki/index.md` under its section (the `regen-index.sh` hook also keeps
   `index.md` current, but author the entry intentionally).
3. Add reciprocal links to every referenced entity (durable relationships are bidirectional).
4. If the element warrants a `hot.md` change (new faction clock, live situation), update `hot.md`.
5. Commit with the right prefix (`prep:` for prep outputs) and a one-line summary.

## Standard reference files (shared by all prep skills)

| File | Read when |
|---|---|
| `../../ttrpg-writing/references/dm-reference-standards.md` | Writing any DM-facing prose |
| `../../ttrpg-writing/references/player-facing-prose.md` | Writing `[!read-aloud]` callouts |
| `../../ttrpg-writing/references/callout-standard.md` | Callout type enforcement |
| `../../ttrpg-writing/references/NAMES.md` | Naming a new entity |
| `../../ttrpg-writing/references/UNIVERSAL-TOYS.md` | Toy-field model and rules |
| `./auto-correct.md` | Fixing structural issues during/after creation |
| `./wikilink-standards.md` | Creating or fixing wikilinks |
