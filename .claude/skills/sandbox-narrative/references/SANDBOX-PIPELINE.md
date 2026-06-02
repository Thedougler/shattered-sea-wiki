# Sandbox Generation Pipeline

Use this reference when the user wants to build a large sandbox from scratch: a dungeon, a region, a hex map, a city district, or any multi-node structure that doesn't yet exist in the vault.

**Dungeon routing:** For keyed dungeons and adventure sites, use `prep-dungeon` instead
of this generic pipeline. That skill specializes the four phases below for room-by-room
site generation with topology testing, OSE formatting, and encounter calibration.

Multi-pass generation prevents context collapse and slop re-emergence. Never attempt a full sandbox in one pass — each phase constrains what the next phase can invent.

---

## Pre-Flight

Before generating anything:

1. Read `wiki/index.md` — confirm no overlapping entities already exist
2. Read `wiki/hot.md` — pull current campaign context
3. Run the Relevance Pre-Screen from `PREP.md` — which PC's thread anchors this sandbox?

---

## Phase 1 — Architecture

Generate the skeleton. No room descriptions, no NPC prose, no flavor yet.

**Outputs:**
- The overarching conflict (one sentence — what is building toward a breaking point?)
- Major factions (2–4) with a single proactive goal each
- Node map or hex structure as a list of named locations and their connections
- 3–5 faction timelines: what each faction does on days 1, 3, 7 if players don't intervene

**Three Clue Rule pass:** For every conclusion players must reach to progress, identify three distinct, mechanically discoverable clues at this phase — before detailing rooms. Retrofit clue distribution into the node map now, not after.

**Constraint:** No NPC names, no room descriptions, no secrets yet. Structure only.

Get user confirmation on the architecture before proceeding.

---

## Phase 2 — Entity Generation

Populate the node map with NPCs and factions using the Alexandrian template from `SKILL.md § NPC Construction`. Do not write backstories — write dossiers.

For each NPC:
- Roleplay Concept (mashup format)
- Quote (one line capturing voice)
- Background (strictly what impacts current sandbox state)
- Three actionable behavioral quirks
- Proactive objectives (bulleted — NPCs pursue, they don't wait)
- Which PC's thread they connect to

**Constraint:** Every NPC must have at least one proactive objective that advances even if the party never meets them. Reactive NPCs who only respond to players are a prep failure.

Route to `references/NPC.md` for full NPC page generation. Route to `references/FACTION.md` for faction pages.

---

## Phase 3 — Spatial Logic

Generate high-level map keys: named locations, their connections, and the tactical structure of each space.

Apply Bryce Lynch standards throughout:
- Multiple loops and varied elevations — no linear corridors with one exit
- At least two routes between significant locations (one fast/loud, one slow/quiet)
- Every space presents a meaningful tactical choice
- No read-aloud boxed text at this phase — DM notes only

For dungeons: sketch the map key as a numbered list of rooms with connections. No room descriptions yet — just `Room 3: connected to 2 (west door), 4 (trapdoor), 7 (hidden passage behind altar)`.

**Constraint:** If the map has a single chokepoint that all paths must pass through, redesign it.

---

## Phase 4 — Micro-Detail

Fill each node room by room using OSE point-first format from `references/dm-reference-standards.md`.

**Format per room:**
```
Room Name
──────────────
[1–2 evocative sensory details. No prose paragraphs.]

- **Noun**: State. (Mechanic or DC)
- **NPC Name**: Role, current behavior. (Hidden agenda)
- *Item*: Description. (Effect or trigger)

*(DM Note: authorial intent, Three Clue placement, tactical note.)*
```

**Anti-Slop Pass — run before finalizing every room:**
- Deletion Test: remove every adjective that isn't a mechanical signal. If "rusty" means "noisy and weakened", keep it. If "imposing" means nothing, cut it.
- Negation Limit: no more than two negative constructions per room ("didn't move", "without speaking"). Rewrite the rest as affirmatives.
- Banned Structures: scan for "It wasn't just X", "Little did they know", "the kind of [noun] that", rhetorical questions used only for atmosphere. Delete all of them.
- Rule of Threes: each room conveys its primary fact plus no more than three supporting sub-points. If you have four, one is redundant — cut it or make it its own element.

**Mechanic Validation:** Before writing any DC, damage die, or stat value, load `references/CR-TABLES.md` or grep the rules pages rather than inventing values.

---

## Phase Sequencing Rule

Never skip phases or merge them. Architecture constrains Entity Gen — you can't place NPCs without knowing the factions. Entity Gen constrains Spatial Logic — you can't place clues without knowing the secrets. Spatial Logic constrains Micro-Detail — you can't write room flavor without knowing the room's role in the larger structure.

If the user wants to jump straight to room descriptions: complete Phase 1 and Phase 3 (skeleton + map key) at minimum before writing any micro-detail.

---

## Context Management

Write each completed phase to disk before starting the next. Use the vault filing sequence from `PREP.md § Vault Filing`. Keeping all world data in the active context window causes hallucination and slop re-emergence as the context fills.

When expanding an existing node later: load only the files relevant to that node, not the full sandbox.
