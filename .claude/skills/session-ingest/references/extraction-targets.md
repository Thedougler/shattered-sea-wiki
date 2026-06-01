# Extraction Targets

What to extract from session transcripts in Pass 3, how to tag it, and what to
skip. Each extract cites source line range from `resolved.csv`.

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

Mechanical combat information for `combat-analytics.md`.

- Encounter name/description and participants
- Round count (if discernible from turn flow)
- Per-PC actions: what each PC did on their turns
- Damage dealt/taken (when stated or inferable)
- Conditions, saves, DCs mentioned
- Tactical observations: what worked, what didn't
- Downs, healing, death saves

```markdown
### [COMBAT]
- Encounter: Kyzil sparring match
- Participants: Crissdalynn vs Kyzil
- Rounds: ~4 (estimated from turn flow)
- Notable: Kyzil landed a heavy hit (Crissdalynn at 12 HP), Perrin used healing word
- DCs mentioned: DC 19 Strength save
- Bardic inspiration used
  Source: lines 1840–2150
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

Source: audio/sessions/session{NN}/resolved.csv
Parts assembled: {list from parts.txt}
Extraction date: {YYYY-MM-DD}

---

## Scene 1: {Location} — {Brief description}
Lines {start}–{end} | Duration: {MM:SS}–{MM:SS}
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
