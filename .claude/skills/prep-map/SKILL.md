---
name: prep-map
description: >
  Use when a Shattered Sea encounter needs a top-down, grid-accurate battlemap — a dungeon
  room, lair, cave, building interior, ship deck, or any tactical space minis move across.
  Triggers: "make a battlemap", "map this room", "map the dungeon", "I need a tactical/grid
  map", "render a map for the fight", and any prep-dungeon / prep-encounter / prep-session
  step that calls for a playable map. NOT for scene illustrations, portraits, or banners —
  that is ttrpg-visual-aids. Full trigger list in the skill body.
---

# prep-map

## Overview

prep-map turns a **paint-by-numbers guide you author** into a print-ready, grid-perfect,
hand-painted battlemap. A bundled deterministic script (`map.mjs`) owns all the geometry, so the
1-inch grid is **exact by construction**; a SOTA image model (nano-banana) does only the styling
and never invents layout — the guide pins it. Quality bar: **2-Minute Tabletop-class** painterly
top-down art (not photoreal).

**The load-bearing idea — you author the legend.** There is no fixed token library boxing you in.
For each map you write a tiny **scene** — a character grid plus a legend *you choose*: which colors
flood-fill as surfaces (walls, floor) and which are outlined, labeled regions (water, a ladder, a
trap, a chest…), in whatever colors and labels fit the scene. `render` draws that guide; you write a
prompt telling the model what each color/label becomes; the model repaints it; the script composites
its crisp vector grid back on top last. The model sees **only the guide image + your prompt** — no
other noise.

```
author scene.json ─► preview ─► render ─► beautify ──────────► composite ─► finished map
                     (free)     (free)    (beautify.mjs · $)    (free)
```

## When to use

Any space players fight or move through room-by-room: dungeon rooms, lairs, caves, ship decks,
building interiors, ambush sites. Usually invoked by **prep-dungeon** (it designs the layout;
prep-map draws it) or **prep-encounter**. NOT for scene illustration, NPC portraits, or location
banners → use `ttrpg-visual-aids`.

## Setup (first run only)

```bash
cd .claude/skills/prep-map/scripts && npm install   # installs sharp, isolated + gitignored
```

## The scene file

A scene is a small JSON: a `grid` of row-strings (one char per cell, a **space = void**, which lets
rooms be non-rectangular) plus a `legend` mapping each char to how it draws.

```json
{
  "grid": [
    "########",
    "#..TB..#",
    "#.~~~.C#",
    "L..~~..#",
    "########"
  ],
  "legend": {
    "#": { "fill": "dimgray",     "as": "rough wet stone wall" },
    ".": { "fill": "#cfc9ba",     "as": "damp flagstone floor" },
    "~": { "outline": "deepskyblue", "label": "WATER",     "as": "ankle-deep standing water" },
    "L": { "outline": "limegreen",   "label": "ARCHWAY",   "as": "an open tunnel-mouth exit" },
    "T": { "outline": "yellow",      "label": "TRAP",      "as": "a hidden pressure plate" },
    "B": { "outline": "orange",      "label": "BARRELS",   "as": "a stack of powder barrels" },
    "C": { "outline": "gold",        "label": "CHEST",     "as": "a banded strongbox" }
  }
}
```

Two kinds of legend entry — **pick your own colors and labels**:

- **`fill`** = a flood-filled surface (a CSS name or `#hex`). Use it for **only the base surfaces** —
  walls and the default floor.
- **`outline` + `label`** = an outlined, labeled **region** (terrain, prop, exit, hazard). Contiguous
  cells of the same key merge into **one** labeled region — that is how you author a multi-cell feature
  (three `T` cells in a row = one 15-ft `TRAP` region the model improvises).
- **`as`** is *your* note of what to paint there — it's for you when writing the prompt; the renderer
  ignores it. (Recording it keeps your prompt and guide in sync.)

Rules of thumb: fill **only** wall + floor; make everything else an `outline` region (solid-color
blobs leak into the art and drift their bounds — outlines hold). Use **simple, distinct, obvious
colors** so your prompt can name them ("the gold CHEST region…"). Frame the room with wall on every
side and put exits in that border ring.

## Commands

Run from the repo root. `--ppi` = pixels per tile = pixels per inch (300 = print master).

| Command | Cost | Produces |
|---|---|---|
| `map.mjs preview <scene.json>` | free | ASCII map + dims / legend size |
| `map.mjs render <scene.json> [--ppi N] [--out dir]` | free | `base.png` (the **guide**), `grid.png`, `flat.png` |
| `beautify.mjs <base.png> <prompt.txt> --out <art.png> [--model id] [--res 1K\|2K\|4K] [--in px]` | **$** | the styled `art.png` (aspect locked) |
| `map.mjs composite <art.png> <scene.json> [--ppi N] [--out dir]` | free | `<stem>.player.png` (finished, gridded) |

`render`, `composite` also accept a `.csv` (legacy token path) or `dungeon.json` (see **Dungeons**).
`beautify.mjs` downsamples the guide, locks output aspect to it (`match_input_image`), and runs the
model with web search **off** so it can't invent geometry. It is the only paid step.

## Pipeline — one room

1. **Author `scene.json`** — grid + legend (above). Frame with wall; exits in the border.
2. **`preview` then `render --ppi 300` (free).** `render` writes the **`base.png`** guide. **Look at
   it** — confirm every region is outlined and labeled where you meant.
3. **Write the prompt** from [beautify-prompt.md](references/beautify-prompt.md) — this is the real
   authoring job. It is a nano-banana *edit brief*: name what each color/label becomes, **preserve-lock**
   the walls + aspect, keep the **edge exit labels** but replace every interior label with its entity,
   one of each (no duplicates), hidden things only subtly hinted. Save as `prompt.txt`.
4. **Beautify ($) → composite (free).**
   ```bash
   node .claude/skills/prep-map/scripts/beautify.mjs room.base.png prompt.txt --out room.art.png --res 2K
   node .claude/skills/prep-map/scripts/map.mjs composite room.art.png room.json --ppi 300 --out <dir>
   ```
   → **`room.player.png`** (styled art + crisp grid).
5. **Validate before accepting:** geometry/exits/terrain match the guide; aspect unchanged; only the
   edge exit labels survive; nothing invented. **Wrong terrain extent is an *authoring* bug — fix the
   grid, don't re-prompt.** Then store + embed per `ttrpg-visual-aids`.

## Choosing the model

`beautify.mjs` defaults to **`google/nano-banana-2`** — fast, cheap, ~95% of flagship quality; right
for drafts and most maps. For a **hero / print final**, pass `--model google/nano-banana-pro`: it is
the best text renderer (sharper kept `ARCHWAY` labels) and the print/4K tier. Pro is slower and
2–3× the cost — reach for it on the final pass, not iterations.

## Outputs

`render` → the guide; `beautify.mjs` → styled art; `composite` → the finished map.

| File | What it is |
|---|---|
| `<stem>.base.png` | The **guide** (filled surfaces + outlined labeled regions) — the beautify input. |
| `<stem>.flat.png` | base + grid: a flat schematic you can play from as-is if you skip beautify. |
| `<stem>.grid.png` | Transparent grid layer (the script reuses it; rarely opened directly). |
| `<stem>.art.png` | The styled painting from `beautify.mjs` — aspect-locked, not yet gridded. |
| `<stem>.player.png` | **Finished, table-ready map:** styled art + crisp grid. |

## Dungeons — `compose` (legacy token path)

Multi-room dungeons use the original **CSV + token library** path (not scenes yet): author each room
as a `.csv` of 2-letter token codes ([token-library.md](references/token-library.md)), place them in a
`dungeon.json`, and `compose` assembles a master grid, auto-walling connective corridors.

```json
{ "name": "den", "rooms": [ {"csv":"a.csv","x":0,"y":0}, {"csv":"b.csv","x":12,"y":4} ],
  "corridors": [ {"from":[6,2],"to":[12,2],"token":"FL"} ] }
```

`x`/`y` place a room's top-left cell on the master grid (tiles); corridor `from`/`to` are inclusive
master cells (straight H/V), carved through walls and auto-walled; room `csv` paths resolve relative
to the `dungeon.json`. Then `compose dungeon.json --ppi 90` → master guide → beautify → `composite
master.art.png dungeon.json` → whole-dungeon `player.png`. (A single big scene works too — `compose`
just spares you hand-placing rooms.)

## Storage & embedding

Store and embed per `ttrpg-visual-aids` (the authoritative paths/syntax). Maps are **lossless `.png`**.
Embed `*.player.png` for players; name by area in kebab-case; session-specific maps live under that
session's asset folder.

## Common mistakes

| Mistake | Fix |
|---|---|
| Filling regions with solid color | Fill **only** wall + floor; everything else is an `outline`+`label` region. Solid blobs leak/drift. |
| Stopping at `render`/`flat.png` | The guide isn't the map. The finished map is `player.png`, after **beautify → composite**. |
| Feeding `flat.png` (with grid) to beautify | Feed `base.png` (the guide, no grid). The grid is composited last, crisp. |
| Re-prompting to fix wrong terrain extent | That's an **authoring** bug — fix the grid; each region holds its own bounds. |
| Interior labels leaking into the art | Prompt per-location: **keep** edge exit labels, **replace** every interior label with its entity. |
| Duplicated/invented features | Say "**exactly one of each, no duplicates**" — the model adds extras unless forbidden. |
| Hidden trap/door rendered obviously | The prompt hints **subtly** (a trap door shut and flush); the guide still labels it normally. |
| Colors too similar to read | Pick simple, distinct CSS colors; your prompt references them by name. |
| `Cannot find module 'sharp'` | First-run setup: `cd scripts && npm install`. |
| Using prep-map for scene art | That's `ttrpg-visual-aids`; prep-map is top-down tactical only. |

## Related

- [beautify-prompt.md](references/beautify-prompt.md) — **the prompt template + rules. Read it before
  every beautify** — it's the real authoring work, tuned for nano-banana.
- `prompting-nano-banana-2` — deeper nano-banana prompting (brief-not-tags, edit locks, 2 vs Pro).
- `ttrpg-visual-aids` — storage paths, embedding syntax, campaign art style.
- `use-replicate` — `beautify.mjs` reuses its Replicate client/auth; default model `google/nano-banana-2`.
- `prep-dungeon` — designs the room layouts and dungeon connectivity that prep-map renders.
- [token-library.md](references/token-library.md) — the legacy 2-letter token vocabulary for the
  CSV / `compose` path.
