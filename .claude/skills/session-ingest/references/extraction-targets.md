# Extraction Targets

What to extract from session transcripts in Pass 2, how to tag it, and what to
skip. Each extract cites part number and source line IDs from the raw CSV.

---

## Tag Types

### [CANON] — Events That Happened

Facts about what occurred in the fiction. The core output.

- NPC actions, offers, threats, deals, departures
- PC actions with world-state consequences (not internal monologue)
- Location discoveries, changes, destruction
- Items gained, lost, spent, traded, transformed, promised
- Faction moves visible to the party
- Mechanical state changes (HP loss in narrative context, conditions applied)

```markdown
### [CANON]
- Jean-Claude sold 3 whip shark eggs to the merchant for 100gp each
  Source: lines 28–102
- The merchant revealed that fertilized eggs reduce value due to taste
  Source: lines 43–49
```

### [LORE] — World-Building Revealed

Facts about the world that were established or confirmed, not events.

- Geography, history, culture revealed through NPC dialogue
- Deity lore, faction structure, political relationships
- Creature biology, magical properties, trade goods
- Established names, titles, relationships

```markdown
### [LORE]
- Whip shark eggs are a delicacy; fertilization reduces culinary value
  Source: lines 29–49
```

### [COMBAT] — Encounter Data

Structured combat data for `pc-combat-primer` profiles and `combat-analytics.md`.
Use the two-part format below: an encounter header followed by a per-PC table.
This format feeds directly into combat profile session logs — capture it at
extraction time so downstream skills don't re-process transcripts.

#### Encounter Header (one per encounter)

- Encounter name/description
- Participants: PCs present and enemy types with count
- Round count (if discernible from turn flow; estimate with `~` if not)
- Estimated CR/difficulty (from prep notes, DM commentary, or post-hoc)
- Outcome: victory / retreat / social resolution / interrupted
- Downs, death saves, healing administered
- Tactical observations: what worked, what didn't

#### Per-PC Combat Table (mandatory for each participating PC)

| PC | Rounds | Damage Dealt | Damage Taken | Hits/Attacks | Saves (Pass/Fail) | Resources Spent | Key Moment |
|---|---|---|---|---|---|---|---|

Column rules:
- **Damage Dealt/Taken**: exact when stated, `~` prefix for estimates, `[unknown]` if not discernible
- **Hits/Attacks**: e.g. `2/3` — use `[unknown]` for either half if not discernible
- **Saves**: saves forced on the PC, e.g. `1/1` (1 passed of 1 forced) — omit if none
- **Resources Spent**: abilities, spell slots, class features, items consumed
- **Key Moment**: 1 notable tactical action, synergy, or failure

A PC who was present but dealt 0 damage or was incapacitated still gets a row.
Negative data feeds the counter profile.

#### Party State (append after the table)

- HP status per PC at encounter end (exact if stated, `low`/`healthy` if described)
- Rest before next encounter (short/long/none/unknown)
- Concentration spells still active

```markdown
### [COMBAT]
**Encounter:** Kyzil sparring match (non-lethal 4v1)
**Enemies:** Kyzil (1) | Est. CR: ~14
**Rounds:** 3 | **Outcome:** loss (Kyzil won)
**Healing:** Perrin cast Healing Word on Crissdalynn

| PC | Rounds | Damage Dealt | Damage Taken | Hits/Attacks | Saves (Pass/Fail) | Resources Spent | Key Moment |
|---|---|---|---|---|---|---|---|
| Delmar | 3 | 17 | ~29 | 1/[unknown] | — | — | SA through Empty Wing via inspiration; dropped to 2 HP |
| Crissdalynn | 3 | ~12 | [unknown] | [unknown] | — | 1 focus point (Stunning Strike) | Grappled R1 (nat 1 contest); stunning strike failed |
| Perrin | 3 | [unknown] | [unknown] | [unknown] | — | 1 Bardic Inspiration, 1 spell slot (Healing Word) | Inspiration enabled Delmar's SA |
| Jean-Claude | 3 | [unknown] | [unknown] | [unknown] | — | — | [no notable moment recorded] |

**Party state:** Delmar 2 HP, Crissdalynn ~12 HP, others healthy. No rest before next scene.
Source: part03 lines 1840–2150
```

### [RULING] — Mechanical Decisions

Rules interpretations or homebrew rulings made at the table.

- Ability check rulings (what DC, what skill)
- Spell interpretation decisions
- Homebrew mechanics introduced
- "We'll do it this way" moments

```markdown
### [RULING]
- DM ruled whip shark egg fertilization status is determinable by inspection
  Source: lines 33–34
```

### [ITEM] — Inventory Changes

Items that changed hands or state. Feeds entity pages and session notes.

- Items gained (purchase, loot, gift, craft)
- Items lost (sold, destroyed, given away, stolen)
- Items transformed (enchanted, broken, modified)
- Currency changes when amounts are stated

```markdown
### [ITEM]
- Jean-Claude: sold 3 whip shark eggs (100gp each, 300gp total gained)
  Source: lines 84–102
```

### [SIGNAL] — Player Engagement

What players leaned into or away from. Feeds `player-interests.md`.

- Topics a player drove conversation toward
- NPCs a player engaged with enthusiastically
- Moments of visible excitement or investment
- Topics a player actively avoided or seemed bored by
- Mechanical choices that reveal preferences (always choosing social over combat)

```markdown
### [SIGNAL]
- Jean-Claude's player drove the entire egg merchant negotiation — high engagement with trading/commerce gameplay
  Source: lines 20–102
- Perrin's player initiated food tangent during downtime — may signal preference for slice-of-life moments
  Source: lines 900–1024
```

### [NPC] — NPC Appearance Record

Track which NPCs appeared and what they did. Feeds entity pages.

```markdown
### [NPC]
- Egg merchant (unnamed): Calveno market vendor, specializes in exotic creature products. Offered 100gp per whip shark egg. Noted fertilized eggs have lower culinary value.
  Source: lines 29–102
  Status: new (needs entity page if named later)
```

---

## What NOT to Extract

- **OOC banter** with no in-world consequence (the Florida slug story, setup chatter)
- **Player theories** presented as speculation, not canon ("I bet he's secretly...")
- **Filler** ("Yeah", "Okay", "Um", "Uh-huh") even when tagged IC
- **Ambiguous speaker content** where the meaning changes based on who said it —
  flag these in `flags.md` instead
- **Repeated information** — extract once at first mention, not every callback
- **Table jokes** unless they became in-world texture the group now treats as canon

---

## IC/OOC Classification

Not everything said by a character-named speaker is in-character:

| Signal | Classification |
|---|---|
| Real-world references (Florida, France, camping) | OOC |
| Rules discussion ("what's the DC?", "do I add proficiency?") | META |
| "I do X" / "I say Y" — player narrating character action | IC |
| "He does X" — describing NPC action (DM) | IC |
| "As a player..." / "Out of character..." | OOC |
| "Can I roll for..." | META (but the outcome may be CANON) |
| Laughter, crosstalk, "wait what?" | OOC (skip) |
| Dice results ("that's a 17") | META (record if part of COMBAT/RULING) |

When uncertain, classify as OOC and skip. Under-extraction is safer than
false canon.

---

## Scene Format

Organize extracts by scene in `extracts.md`:

```markdown
# Session {NN} Extracts

Source: audio/sessions/session{NN}-part*.m4a.csv
Extraction date: {YYYY-MM-DD}

---

## Scene 1: {Location} — {Brief description}
Part {PP} lines {start}–{end}
Participants: {speakers present}
IC/OOC split: {approximate percentage}

### [CANON]
- ...

### [LORE]
- ...

(only include tag sections that have content)

---

## Scene 2: ...
```

---

## Merge Before Extract

Before extracting, merge fragmented utterances. The transcription tool often splits
one sentence across multiple 1–2 second lines:

```
# Before merge (raw):
975: Delmar: "What?"
976: DM: "I'm just like,"
977: DM: "how do you know that?"
978: DM: "How do you know that eel and slug taste basically the same?"

# After merge:
975: Delmar: "What?"
976-978: DM: "I'm just like, how do you know that? How do you know that eel and slug taste basically the same?"
```

Merge rules:
- Same speaker, consecutive lines, gap ≤ 3 seconds → merge
- Different speakers → never merge (even if gap is small)
- Merge across lines but preserve the original line range for citation

---

## Flags Format

Unresolved items go to `flags.md`:

```markdown
# Session {NN} Flags

## Unresolved

- [ ] Lines 34-35: Speaker 1 says "Yes" — could be Jean Claude or Crissdalyn based on context. Affects who sold the eggs.
- [ ] Lines 978-979: DM says "I've had both" — unclear if DM speaking as self (OOC) or as NPC. If NPC, which one?

## Resolved (DM reviewed)

- [x] Lines 34-35: Confirmed as Jean Claude per DM (2026-05-31)
```
