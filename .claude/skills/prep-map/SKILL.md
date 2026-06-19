---
name: prep-map
description: >
  Use when a Shattered Sea encounter needs a top-down, grid-accurate battlemap — a dungeon
  room, lair, cave, building interior, or any tactical space minis move across. Triggers:
  "make a battlemap", "map this room", "map the dungeon", "I need a tactical/grid map",
  "render a map for the fight", and any prep-dungeon / prep-encounter / prep-session step
  that calls for a playable map. NOT for scene illustrations, portraits, or banners — that
  is ttrpg-visual-aids. Full trigger list in the skill body.
---

# prep-map

## Overview

prep-map renders **print-ready, grid-perfect battlemaps** from a tile grid you author — the
RimWorld / Dwarf Fortress model: every cell is one tile (wall, floor, door, water, chest…).
A bundled deterministic script does the fiddly pixel work; the **grid is mathematically exact
by construction**, never trusted to an AI model.

**Core idea — paint-by-numbers.** The script renders a flat **base key** where every material
has a distinct color + glyph, plus an auto-generated **color→material prompt**. An optional
image-to-image "beautify" pass restyles the colored regions into premium hand-painted art (the
2-Minute Tabletop bar) while the script composites its crisp vector grid back on top.

## Status (read this)

**Wired today (Phase A):** authoring → validation → `preview` → `render`. You get a
grid-perfect schematic map (`*.flat.png`, immediately usable at the table) plus a ready-to-run
beautify prompt (`*.legend.txt`).

**Not yet automated:** the one-command beautify (FLUX Kontext + upscale + grid re-composite)
and dungeon `compose`. To beautify now, run the prompt through **use-replicate** by hand (see
below). Automating it is Phase B/C.

## When to use

Battlemaps and tactical maps for any space players fight or move through room-by-room:
dungeon rooms, lairs, caves, ship decks, building interiors, ambush sites. Usually invoked by
**prep-dungeon** (it designs the room layout; prep-map draws it) or **prep-encounter**.

**Not** for scene illustrations, NPC portraits, location banners, or handouts → use
`ttrpg-visual-aids`.

## Workflow

1. **Size the grid.** Pick rows×cols to fit the space *including a 1-tile wall border*
   (a 6×4 interior room → ~8×6 grid). Tiles are 1 inch / 5 ft each.
2. **Author the tile CSV.** Comma-delimited, one token code per cell; empty cell = unmapped
   void (lets rooms be non-rectangular). Token codes: see [token-library.md](references/token-library.md).
3. **Preview (free).** `map.mjs preview <tiles.csv>` prints a DF-style ASCII map + a validation
   report. Fix any errors (unknown token, floating door) *before* spending on img2img.
4. **Render.** `map.mjs render <tiles.csv> --ppi 300 --out <dir>` writes `base.png`,
   `grid.png`, `dm.png`, `flat.png` (base+grid, usable as-is), and `legend.txt`.
5. **Beautify (optional, manual today).** Pass `legend.txt` through use-replicate
   `edit-image.mjs edit base.png "<legend>"` (FLUX Kontext), upscale if needed, then overlay
   `grid.png` (and `dm.png` for the DM copy). See `use-replicate`.
6. **Store + embed** per `ttrpg-visual-aids`: maps go in `wiki/assets/maps/` as lossless `.png`.

## Commands

```bash
# First run only — install sharp (isolated, gitignored):
cd .claude/skills/prep-map/scripts && npm install

node .claude/skills/prep-map/scripts/map.mjs preview room.csv
node .claude/skills/prep-map/scripts/map.mjs render  room.csv --ppi 300 --out wiki/assets/maps/<area>
```

Flags: `--ppi N` (pixels per tile; 300 = print), `--out <dir>`, `--legend <file>` (per-map
reskin overrides). Token catalog: [token-library.md](references/token-library.md). Regenerate
that catalog after editing the manifest: `node scripts/gen-catalog.mjs`.

## Authoring rules

- **Whole-cell only.** Walls/doors occupy a full 1×1 tile; walls are 1 square thick. Frame
  every room with a `WL` border, or the model has no wall to paint.
- **DM vs player.** `⚑dm` tokens (traps, secret doors, entrance) never show on the player map —
  they collapse to plain floor/wall in the base key and appear only as markers on `dm.png`.
- **Reskin per map.** A sidecar `legend.json` overrides any token's material for one map
  (e.g. turn a dungeon into an ice cave: `{"FL":"blue-white ice floor","WL":"carved ice wall"}`)
  — no new tokens needed.
- **Preview before you render, render before you beautify.** Each step is cheaper than the next.

## Common mistakes

| Mistake | Fix |
|---|---|
| No wall border around a room | Frame the interior with `WL`; img2img needs a wall region to paint |
| Authoring a big map blind | `preview` first — the ASCII shows mistakes instantly, for free |
| Using prep-map for scene art | That's `ttrpg-visual-aids`; prep-map is top-down tactical only |
| `Cannot find module 'sharp'` | First-run setup: `cd scripts && npm install` |
| Expecting a finished pretty map from `render` | `render` is the schematic + prompt; beautify is the manual use-replicate pass (Phase B will fold it in) |

## Related

- `ttrpg-visual-aids` — storage paths, embedding syntax, and `art-style.md` (campaign look).
- `use-replicate` — the image-to-image backend for the beautify pass.
- `prep-dungeon` — designs the room layouts that prep-map renders.
