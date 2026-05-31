# DM Reference Standards

DM-facing content is a technical manual, not a story. The DM reads it under cognitive load
while managing players, rules, and improvisation simultaneously. Every sentence must give
the DM something to say, do, or decide. Cut everything that doesn't serve that purpose.

---

## The Gavin Norman / OSE Standard

Old-School Essentials represents the benchmark for DM-facing information delivery. These
rules encode it for use here.

### Terse Delivery
Long paragraphs are prohibited. Primary delivery method: indented lists and discrete,
focused data points. If a DM has to read more than two sentences to understand what an
element does, the element is written wrong.

### Point-First Structure
Every descriptive element begins with the core noun, followed immediately by its state,
condition, or function. Mechanical details go in parentheses after.

```
Iron Door: Locked, rusted hinges, reeks of oxidation. (DC 15 Athletics to force open)
Shrine: Active, recent offerings — bread, fish bones, a copper coin. (Umberlee)
Guard Captain: Drunk, armor half-buckled. (disadvantage on Perception; unaware of north corridor)
```

Never bury the noun in an atmospheric opener. Not "A massive iron door blocks your path" —
that's fiction. "Iron Door: [state] [mechanic]" is reference material.

### Typographic Encoding
- **Bold** = monsters, NPCs, and immediate physical threats. The DM's eye finds these first.
- *Italic* = magical items, spells, and named treasure. Mechanically significant.
- Plain text = environment, architecture, non-threatening objects.

This lets the DM scan a page and immediately identify what's alive or magical.

### Objective Third Person
Always "the characters" or "the party", never "you". The DM is reading the text, not
experiencing it. Second person dissolves the boundary between GM and player and creates
cognitive blur at the table.

```
✅ If the characters touch the altar, the guardian activates.
❌ If you touch the altar, the guardian activates.
```

---

## The Bryce Lynch Standard (Interactivity)

### Read-Aloud as Service, Not Script
DM-facing material should never force the DM to recite a mandatory script. But pre-written
`> [!read-aloud]` callouts embedded in DM documents are a *service* — they give the DM
something ready to speak, adapt, or skip. The difference:

- Mandatory boxed text the scene depends on = **bad**. The scene should work from the DM notes alone.
- Optional read-aloud the DM can grab when they want it = **good**. Saves the DM from
  improvising a description under pressure.

Apply `references/player-facing-prose.md` to any read-aloud section. Keep it to 4 sentences
max. Never include conditional framing ("if the party succeeded...") — that logic belongs
in a `> [!dm]` callout above the read-aloud.

### Evocative, Not Exhaustive
Don't inventory every crate. Isolate the 2–3 sensory details that define the atmosphere
and make the location feel real. The DM can invent crates. They cannot invent the smell of
ozone that signals a magical trap, or the scrape marks on the floor that indicate something
heavy was dragged.

Good targets: sound, smell, texture, temperature, something slightly wrong. Bad targets:
architectural dimensions, furniture inventory, general "darkness".

### Design for Non-Linearity
Maps and node connections should have multiple loops, varied elevations, multiple entry
points. Locations must present meaningful tactical choices — loud fast route vs. quiet
dangerous route — not a sequence of mandatory encounters.

### No Generic Magic Items
"+1 sword" doesn't interact with the world. Every magical item needs:
- A specific physical description (what does it look like, feel like, smell like)
- The exact manipulation required to activate it (if applicable)
- One concrete behavioral or narrative hook

This turns treasure into something players experiment with rather than loot and forget.

---

## The Skerples Standard (Authorial Intent)

### DM Notes Are Transparent
When a trap, encounter, or faction dynamic serves a specific purpose, say so. Brief DM-facing
notes explaining the intended function of a design element — what it teaches, what it rewards,
what decision it creates — let the DM deploy it effectively without having to reverse-engineer
the designer's intent.

Format: italicized note after the element, clearly marked as a DM aside.

```
Pressure Plate Trap: 10-ft corridor, triggers on 20+ lbs, drops portcullis behind the party.
(Teaches players to probe ahead of the group; rewards cautious movement. If the party is 
already doing this, let the rogue's check notice the worn stone pattern before they trigger it.)
```

### Rule of Threes
Any discrete element — room description, faction goal, trap mechanism — should convey its
primary intent plus no more than three supporting sub-points. More than three and the DM
cannot hold it in working memory. If you have four sub-points, one is redundant or should
be its own element.

---

## The Alexandrian Standard (Information Architecture)

### Three Clue Rule
For any conclusion the party must reach to progress the scenario, the design must include
at least three distinct, mechanically discoverable clues pointing to that conclusion,
distributed across different nodes. Redundancy is structural reliability, not repetition.

When writing a mystery or investigation element, explicitly list the three clues in the
DM notes. Don't leave redundancy to chance.

### DM Notes Format for Mysteries
```
**Conclusion**: The harbormaster is working for the Chain Council.
**Clue 1**: His ledger (Harbourmaster's Office, locked drawer) has payments in Chain cipher.
**Clue 2**: Rael Corven mentions "Holst's arrangement" if characters ask about shipping manifests.
**Clue 3**: The crate inspection schedule suspiciously excludes Pier 7 — the Chain's primary berth.
```

---

## The Scanability Test

After writing any DM-facing content, test it: can the DM find the answer to "what do I do
right now?" in three seconds? If not, restructure.

**Checklist:**
- Section headers work as scan targets — a DM looking for "what does this NPC want" can find
  it without reading the whole page
- Bold marks threats, NPCs, and decision points — the DM's eye catches them first
- No paragraph exceeds 3 sentences in DM-facing content — split or convert to a list
- Field ordering is consistent across pages of the same type — the DM builds muscle memory
  for where information lives
- Every callout does one job — if a `[!dm]` is doing two things, split it

This test is separate from the content test ("does every sentence give the DM something to
say, do, or decide"). Both must pass. A page can have excellent content in unscannable format,
or scannable format with useless content.

---

## Formatting Summary

```
Location Name
──────────────
Brief atmosphere: 1–2 evocative sensory details. No prose paragraphs.

Key Features:
- **Noun**: State. (Mechanic)
- **NPC Name**: Role, immediate behavior. (Hidden fact or agenda)
- *Item*: Description. (Effect or trigger condition)

DM Notes:
(Italicized aside — authorial intent, tactical notes, or Three Clue listings)
```
