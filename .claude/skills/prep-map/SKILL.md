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

prep-map turns a tile grid you author into a **print-ready, grid-perfect, hand-painted
battlemap**. A bundled deterministic script (`map.mjs`) owns all the geometry, so the 1-inch grid
is **exact by construction**; an AI image pass does only the styling. Quality bar: **2-Minute
Tabletop-class** painterly top-down art (not photoreal).

**The load-bearing idea — a planning guide, not art.** `render` emits a flat **guide diagram**:
the two base surfaces (stone **wall** = dark fill, **floor** = light fill) are flood-filled, and
**everything else is an outlined, labeled region in a plain named color** — terrain variations
(cyan `SHALLOW WATER`, royal-blue `DEEP WATER`, …), props (green `CHEST`/`BARREL`), doors (orange),
hazards (yellow `TRAP`). The outline marks *where* each thing must go; the label says *what* it is.
The **agent writes a beautify prompt** (theme + per-region styling) and the image model repaints the
guide into a finished scene — erasing every outline/label, arranging things naturally, holding the
layout — while the script composites its crisp vector grid back on top last. The model gets **only
the guide image + the agent's prompt** — no auto-legend, no other noise.

You drive these steps; the script does the fiddly work at every one:

```
author CSV ─► preview ─► render ─► beautify ──────────► composite ─► finished map
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

## Commands

Run from the repo root. `--ppi` = pixels per tile = pixels per inch (300 = print master).

| Command | Cost | Produces |
|---|---|---|
| `map.mjs preview <room.csv>` | free | ASCII map + validation report |
| `map.mjs render <room.csv> [--ppi N] [--out dir]` | free | `base.png` (the **guide**), `grid.png`, `flat.png` |
| `beautify.mjs <base.png> <prompt.txt> --out <art.png> [--model id] [--res 1K\|2K\|4K] [--in px]` | **$** | the styled `art.png` (nano-banana-2, aspect locked) |
| `map.mjs composite <art.png> <room.csv\|dungeon.json> [--ppi N] [--out dir]` | free | `<stem>.player.png` (finished, gridded) |
| `map.mjs compose <dungeon.json> [--ppi N] [--out dir]` | free | assembled master `base.png` + layers |

`beautify.mjs` downsamples the guide, locks the output aspect ratio to it (`match_input_image`), and
runs a SOTA image model with web search **off** so it can't invent geometry. It is the only paid step.

## Pipeline — one room

1. **Size the grid.** Count interior tiles, then add a **1-tile `WL` border on every side**
   (1 tile = 1 inch = 5 ft). A 6-wide × 4-deep room → an **8 × 6** grid (width × height).
2. **Author `room.csv`.** Comma-delimited, **one token code per cell**; an empty cell = void
   (unmapped — lets rooms be non-rectangular). Token codes: [token-library.md](references/token-library.md).
3. **`preview` (free).** `map.mjs preview room.csv` prints a Dwarf-Fortress-style ASCII map +
   validation. Fix every error (unknown token, floating door) *before* you spend on img2img.
4. **`render --ppi 300` (free).** Writes the **`base.png`** guide (outlined labeled regions),
   `grid.png`, and `flat.png` (a schematic you can already play from). **Look at `base.png`** —
   confirm every region is outlined and labeled correctly before spending.
5. **Write the beautify prompt** from the template in
   [beautify-prompt.md](references/beautify-prompt.md) — this is your real authoring job. Fill in
   THEME + per-region styling, and keep its rules intact: **annotation-removal first** (the guide's
   outlines/labels must NOT survive), **fill each terrain region within its bounds**, **structural
   features (ladders/stairs/doors) locked to their cell** while **loose props settle naturally**,
   **exactly one of each — no duplicates**, and **hidden features only subtly hinted** (a trap door
   is shut and flush; a secret door reads as plain wall). Save it as `prompt.txt`.
6. **Beautify ($) then composite (free).**
   ```bash
   node .claude/skills/prep-map/scripts/beautify.mjs room.base.png prompt.txt --out room.art.png --res 2K
   node .claude/skills/prep-map/scripts/map.mjs composite room.art.png room.csv --ppi 300 --out <dir>
   ```
   `beautify.mjs` returns aspect-locked art at whatever size; `composite` normalizes it to exact grid
   pixels, lays the crisp grid on top, and stamps the print DPI → **`room.player.png`**.
7. **Validate before accepting:** exits, stairs/ladders, and water zones match the guide; aspect
   unchanged; no labels/outlines survived. **A wrong water extent or terrain edge is an *authoring*
   bug — fix the CSV, do not chase it by re-prompting.** Then store + embed per `ttrpg-visual-aids`.

## Outputs

`render` emits the guide; `beautify.mjs` emits the styled art; `composite` emits the finished map.

| File | What it is |
|---|---|
| `<stem>.base.png` | The **guide** (outlined labeled regions on wall/floor fills) — the beautify input. |
| `<stem>.flat.png` | base + grid: a flat **schematic you can play from as-is** if you skip beautify. |
| `<stem>.grid.png` | Transparent grid layer (the script reuses it; rarely opened directly). |
| `<stem>.art.png` | The styled painting from `beautify.mjs` — aspect-locked, not yet gridded. |
| `<stem>.player.png` | **Finished, table-ready map:** styled art + crisp grid, exact DPI. (composite also writes a `dm.png` twin; ignore it unless you want DM markers.) |

## Authoring rules

- **One code per cell, whole-cell only.** Walls/floor each fill a full 1×1 tile; walls are 1 square
  (5 ft) thick. No sub-cell or diagonal walls.
- **The render is a *guide*, not the art.** Only `WL` (wall) and `FL` (floor) flood-fill; every other
  token draws as an **outlined region in a role color + a text label** (terrain = water/lava/…, props,
  doors, hazards). Contiguous same-token cells merge into one labeled region — that is how you author a
  multi-cell feature (a 3-tile `TR` run = one 15-ft `TRAP` region the model improvises).
- **Frame every room with `WL`.** Doors/stairs/archways replace a wall cell in that border ring.
- **One token per cell.** For a *trapped chest*, put the chest on its cell and a `TR` on the floor cell
  in front of it. Hidden things (traps, secret doors) render as normal labeled regions in the guide —
  the **beautify prompt** is what keeps them subtle in the final art (see the template).
- **Terrain fidelity is authored, not prompted.** If deep water covers the wrong area, fix the CSV
  tiles — don't re-prompt. Each terrain type is its own outlined region and holds its bounds.
- **Preview before render, render before beautify.** Each step is cheaper than the next.

## Dungeons — `compose`

A dungeon is the same primitive at larger scale: room CSVs placed on a master grid, joined by
corridors.

1. **Author each room** as its own CSV, then a `dungeon.json`:
   ```json
   {
     "name": "smugglers-den",
     "rooms": [
       { "csv": "entry.csv", "x": 0,  "y": 0 },
       { "csv": "vault.csv", "x": 12, "y": 4 }
     ],
     "corridors": [ { "from": [6, 2], "to": [12, 2], "token": "FL" } ]
   }
   ```
   **Coordinates are master-grid tiles.** A room's `x`/`y` places its **top-left cell** on the
   master grid. A corridor's `from`/`to` are **inclusive `[x,y]` cells on that same master grid**;
   the run paints every cell between them (straight H/V only) and carves through any wall it
   crosses. `compose` then **auto-walls** the passage — void beside a corridor becomes `WL` — so
   leave a void margin between rooms for the walls to land in. Room `csv` paths resolve **relative
   to the `dungeon.json` file's location**. Overlapping rooms that disagree are reported as
   collisions and refuse to render.
2. **`compose dungeon.json --ppi 90`** assembles the master and renders its `base.png` guide. Use a
   **reduced ppi** — the dungeon overview is a DM reference, not a print surface.
3. **Beautify** the master guide once with `beautify.mjs` and one prompt covering the whole dungeon
   (same template, §5).
4. **`composite master.art.png dungeon.json --ppi 90`** → the whole-dungeon `player.png`.

## Worked example — a smugglers' cellar

`cellar.csv` (6×4 interior + border = 8×6; trapped chest = `CH` + `TR` in front; secret door
`DS` and stairs-down `SD` in the border ring):

```
WL,WL,WL,WL,WL,WL,WL,WL
WL,FL,FL,TB,FL,FL,CH,WL
WL,CT,CT,FL,FL,FL,TR,WL
WL,BA,FL,FL,FL,FL,FL,WL
DS,FL,FL,FL,FL,FL,DL,WL
WL,WL,WL,SD,WL,WL,WL,WL
```

```bash
M=.claude/skills/prep-map/scripts/map.mjs
node $M preview cellar.csv                                  # ASCII + "valid — 8x6 tiles"
node $M render  cellar.csv --ppi 300 --out maps/cellar      # → cellar.base.png (the guide)
# look at cellar.base.png, then write the beautify prompt from references/beautify-prompt.md:
#   theme = damp smugglers' cellar; per-region styling; keep all the template rules.
$EDITOR maps/cellar/prompt.txt
node .claude/skills/prep-map/scripts/beautify.mjs maps/cellar/cellar.base.png maps/cellar/prompt.txt \
     --out maps/cellar/cellar.art.png --res 2K
node $M composite maps/cellar/cellar.art.png cellar.csv --ppi 300 --out maps/cellar
# → maps/cellar/cellar.player.png  (finished, gridded)
```

## Storage & embedding

Store and embed per `ttrpg-visual-aids` (the authoritative paths/syntax). Maps are **lossless
`.png`**. Embed **`*.player.png`** for players and keep **`*.dm.png`** DM-only. Name by area in
kebab-case (e.g. `calveno-cellar.player.png`); session-specific maps live under that session's
asset folder.

## Common mistakes

| Mistake | Fix |
|---|---|
| Stopping at `render`/`flat.png` and calling it done | The guide isn't the map. The finished map is `player.png`, after **beautify → composite**. |
| Feeding `flat.png` (with grid) to beautify | Feed `base.png` (the guide, no grid). The grid is composited last, crisp. |
| Re-prompting to fix wrong water/terrain extent | That's an **authoring** bug — fix the tile CSV; each terrain region holds its own bounds. |
| Guide outlines/labels showing in the final art | Strengthen the **annotation-removal-first** opener in the prompt (template rule 1). |
| Duplicated/invented features (two ladders, extra door) | Add "**exactly one of each, no duplicates**" — the model adds extras unless forbidden. |
| Hidden trap/door rendered obviously | The beautify prompt must hint **subtly** (template rule 4), not the guide. |
| No wall border around a room | Frame the interior with `WL`; put doors/stairs *in* the border ring. |
| Authoring a big map blind | `preview` first — the ASCII shows mistakes instantly, for free. |
| Bare corridor exposed to void in a dungeon | `compose` auto-walls it; just leave a void margin between rooms. |
| `Cannot find module 'sharp'` | First-run setup: `cd scripts && npm install`. |
| Using prep-map for scene art | That's `ttrpg-visual-aids`; prep-map is top-down tactical only. |

## Related

- [beautify-prompt.md](references/beautify-prompt.md) — **the prompt template + rules. Read it before
  every beautify** — it's the real authoring work.
- `ttrpg-visual-aids` — storage paths, embedding syntax, and the campaign art style.
- `use-replicate` — `beautify.mjs` reuses its Replicate client/auth; the default model is
  `google/nano-banana-2` (override with `--model`). See use-replicate for the current model menu.
- `prep-dungeon` — designs the room layouts and dungeon connectivity that prep-map renders.
- Token codes: [token-library.md](references/token-library.md) (the cell vocabulary; rendering now
  uses role colors + labels, not the per-token hex).
