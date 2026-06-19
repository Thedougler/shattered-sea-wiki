# Beautify Prompt — structure & rules

The beautify step feeds the image model **only two things**: the rendered guide PNG and this prompt.
No token manifest, no auto-legend — the agent writes the prompt. The guide is a *planning diagram*
(flat surfaces + colored outline boxes + UPPERCASE labels); the model must paint the scene and
**erase every annotation**.

This structure was tuned empirically (nano-banana-2). The load-bearing moves, in order:

1. **Lead with annotation-removal, and split labels by location.** State up front that the input is
   a diagram with text labels + colored outlines drawn on top. Then handle the labels explicitly by
   *where* they sit — the model removes them far more reliably when told the fate of each kind:
   - **BORDER labels** naming an off-map exit (the `ARCHWAY` labels at the map edges): **KEEP these** —
     they are useful exit markers. Leave the word legible at the edge AND paint a real open
     tunnel-mouth in the wall there. These are the **only** labels that survive into the final image.
   - **INTERIOR labels** naming something inside the play area (`DEEP WATER`, `SHALLOW WATER`,
     `RUBBLE`, `TORCH`, props, traps): these **must NOT remain as text or marks**. Replace each
     **entirely** with the real thing it names, naturally woven into the painted scene. No words,
     letters, boxes or outlines anywhere in the playable map.

   Tell the model "keep the edge labels, remove the inside ones" explicitly — a blanket "remove all
   text" scrubs the exit markers too (over-correction), and a blanket "keep the labels" leaks the
   interior ones. The location split is what makes it selective.
   Naming the labels and their location is load-bearing; a generic "remove annotations" alone leaks.
2. **Lock the layout, not the annotations.** Tell it to keep walls/floor/proportions/aspect exactly,
   but to paint *over* every colored box and label.
3. **Place, don't centre — but lock structure.** Loose props (barrels, sacks, crates, a lantern)
   should settle *naturally* — against the nearest wall or into a corner, never floating dead-centre.
   But **structural features (ladders, stairs, doors, archways, exits) must stay exactly in their
   marked cell** — they are tactical positions minis interact with; do not let the model relocate them.
3b. **Exactly one of each — no duplicates.** State plainly: paint exactly one feature per labelled
   box and **do not add, duplicate, or echo** any feature elsewhere (the model will happily paint a
   second ladder/door if not forbidden). "Do not invent extra exits" must also mean "do not invent
   extra *anything*."
4. **Hide what players must find.** Traps, trap doors, secret doors, hidden caches — only a *subtle*
   visual hint, never obvious. A trap door is shut and flush with the floor, not standing open; a
   secret door reads as plain wall. If a feature is meant to be discovered, it must not announce itself.
5. **Terrain is regions too — fill each within its bounds.** Water, deep water, lava, grass, etc. are
   outlined labeled *areas* (not just props). Tell the model to fill each region with its material
   **only within that outline** and not let it spread; call out the depth/material change at the
   boundary. Verified: an outlined `DEEP WATER` region holds its bounds; the old solid blue *fill*
   grew to swallow the room. **Word shallow water as a visible material**, e.g. "a thin sheet of
   reflective standing water *covering* the floor" — "ankle-deep over stone" reads as plain wet stone.
6. **Close with a clean-output check** — no boxes, outlines, rectangles, text, labels, letters, grid.

## Color roles in the guide

Only WALL (dark fill) and the default FLOOR (light fill) are flood-filled. Everything else — terrain
variations included — is an **outlined, labeled region** in a plain color:

| Outline color | Role | Prompt as |
|---|---|---|
| green (limegreen) | prop / furniture / stairs | the labelled object, placed naturally |
| orange | door / opening | a door set flush into the wall (or hidden — see rule 4) |
| yellow | hazard / trap | **subtle** — blended into the floor, not obvious |
| magenta | point of interest / marker | per label |
| cyan (deepskyblue) | shallow water | a thin sheet of reflective standing water covering the floor |
| royal blue | deep water | a deep, dark, still pool, within its bounds, clear depth change at the edge |
| orangered | lava | molten lava within its bounds |
| sienna / peru | rubble / wood floor | per label |
| (dark fill) | stone wall | keep exactly |
| (light fill) | stone floor | walkable damp/dry ground |

## Fill-in template

```
You are painting a single finished top-down tabletop battlemap FROM A PLANNING DIAGRAM.

THE INPUT IS A DIAGRAM, NOT A SCENE. It is a flat floor plan with colored outlined regions and
UPPERCASE TEXT LABELS drawn on top — annotations telling you what to paint where, not objects.
Handle the labels by WHERE they sit:
- BORDER labels naming an off-map exit (the ARCHWAY labels at the map's edges) → KEEP the word
  legible at the edge and paint a real open tunnel-mouth in the wall there. These are the only words
  that stay; the openings are plain arches — NO doors, gates, or hatches.
- INTERIOR labels naming anything inside the room (DEEP WATER, SHALLOW WATER, RUBBLE, TORCH, …) →
  these MUST NOT remain as text or marks. Replace each ENTIRELY with the real thing it names, woven
  naturally into the scene. NO words, letters, outlines, boxes or grid lines inside the playable map.

STYLE: a 2-Minute Tabletop hand-painted battlemap — painterly, illustrated, stylized realism,
strictly orthographic bird's-eye top-down, NOT a photo. Soft short contact shadows only;
<LIGHTING>; solid near-black outside the walls.

THEME: <one or two rich sentences: place, materials, wear, atmosphere, clutter>.

PAINT EXACTLY ONE of each labelled feature. Do NOT add, duplicate, echo, or invent any extra
feature anywhere.

LAYOUT — preserve exactly: the dark-grey border is stone WALL, keep every wall where it is; the
plain light region is walkable FLOOR. Keep the same aspect ratio and proportions. Do not add,
move, or remove any wall or opening.

FILL EACH OUTLINED TERRAIN REGION with its material, kept WITHIN its outline (do not spread past it):
- the cyan <SHALLOW WATER> region → a thin sheet of reflective standing water covering the floor.
- the royal-blue <DEEP WATER> region → a deep dark still pool, with a clear depth change at its edge.
- <other terrain regions per their label and color>.

STRUCTURAL FEATURES STAY LOCKED in the exact cell their box marks (do not relocate):
- the green <STAIRS/LADDER> box → one, exactly there.
- the orange <DOOR/ARCHWAY> box → one opening, exactly there.

LOOSE PROPS settle naturally — against the nearest wall or into a corner, never floating dead-centre:
- where the green <PROP LABEL> box is → <the object, placed naturally>.

HIDDEN FEATURES (players must search for these — hint only, never obvious):
- where the yellow <TRAP> box is → ordinary floor with at most a faint seam; no visible mechanism.
- where the orange <SECRET DOOR> box is → unbroken wall, no visible door.
- <trap doors are shut and flush, never open>.

FINAL OUTPUT = only the painted room. No boxes, outlines, rectangles, text, labels, letters, grid.
```

Worked examples that produced clean maps live in this skill's history; keep the five rules above
intact and only swap THEME and the per-box lines.
