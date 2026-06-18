# prep-map Token Library

The token manifest (`tokens/tokens.json`) is the single source of truth. Each token serves **four consumers**: the agent (the short CSV code), the renderer (a distinct flat `color` + an optional `glyph` SVG), and the img2img beautify pass (the `fragment` phrase, assembled into the auto color→material legend).

**This file is generated** — regenerate with `node scripts/gen-catalog.mjs` after editing the manifest; do not hand-edit.

**Layers.** `both` tokens are drawn in the base segmentation key and beautified. `dm` tokens are never beautified: they collapse to their `playerFallback` in the base key (so the player map hides them) and are drawn as crisp magenta overlay markers on the DM map only.

**Palette gate.** Large flat regions (terrain/structure) stay ≥16 ΔE2000 apart; small glyph-bearing objects (features/markers) stay ≥10 — several feature pairs sit intentionally near that floor, since the glyph (not the color) disambiguates them. Enforced by `palette.checkSeparation` as a unit test.

| Code | Name | Category | ASCII | Color | Glyph | Layer | Img2img fragment |
|---|---|---|---|---|---|---|---|
| `WL` | wall | structure | `#` | `#2a2723` | — | both | thick rough-hewn stone dungeon walls |
| `DR` | door | structure | `+` | `#8f1f15` | door.svg | both | a closed iron-banded oak door |
| `DL` | locked door | structure | `=` | `#e6c64a` | door-locked.svg | both | a heavy iron-banded locked door with a keyhole |
| `FL` | stone floor | terrain | `.` | `#9a948a` | — | both | worn flagstone floor |
| `FW` | wood floor | terrain | `,` | `#b3702f` | — | both | wooden plank floor |
| `WS` | shallow water | terrain | `~` | `#4aa3c7` | — | both | shallow clear water over stone |
| `WD` | deep water | terrain | `W` | `#15577e` | — | both | deep dark water |
| `RB` | rubble | terrain | `%` | `#6e5638` | — | both | broken rubble and debris, difficult terrain |
| `LV` | lava | terrain | `L` | `#ec4a14` | — | both | glowing molten lava |
| `CM` | chasm | terrain | `X` | `#1c2b4a` | — | both | a bottomless dark chasm |
| `CO` | column | feature | `o` | `#c0468a` | column.svg | both | a round stone column |
| `CH` | chest | feature | `$` | `#813099` | chest.svg | both | a closed wooden treasure chest |
| `AL` | altar | feature | `A` | `#280eaa` | altar.svg | both | a carved stone altar |
| `BR` | brazier | feature | `*` | `#aa0e85` | brazier.svg | both | a burning iron brazier casting warm light |
| `FP` | fireplace | feature | `f` | `#aa0e51` | fireplace.svg | both | a stone fireplace with a burning fire |
| `TO` | torch | feature | `i` | `#4b3285` | torch.svg | both | a wall-mounted flaming torch |
| `TB` | table | feature | `T` | `#85323b` | table.svg | both | a period-appropriate wooden table |
| `BE` | bed | feature | `b` | `#7311d4` | bed.svg | both | a wooden bed with linens |
| `BL` | bookshelf | feature | `B` | `#b411d4` | bookshelf.svg | both | a tall wooden bookshelf |
| `BA` | barrel | feature | `0` | `#d4114c` | barrel.svg | both | a wooden barrel |
| `CT` | crate | feature | `c` | `#d41125` | crate.svg | both | stacked wooden crates |
| `WR` | weapon rack | feature | `r` | `#e72bee` | weapon-rack.svg | both | a wooden weapon rack |
| `ST` | statue | feature | `I` | `#6a59c0` | statue.svg | both | a carved stone statue |
| `RG` | rug | feature | `_` | `#c05971` | — | both | a patterned woven rug on the floor |
| `SU` | stairs up | feature | `<` | `#9c5af2` | stairs-up.svg | both | stone stairs ascending |
| `SD` | stairs down | feature | `v` | `#f25ac4` | stairs-down.svg | both | stone stairs descending |
| `AR` | archway | feature | `'` | `#f25a92` | archway.svg | both | an open stone archway |
| `DS` | secret door | structure | `S` | `#7a2f8f` | door.svg | dm | _(dm marker; base→WL)_ |
| `TR` | trap | hazard | `^` | `#c02a2a` | trap.svg | dm | _(dm marker; base→FL)_ |
| `EN` | entrance | marker | `E` | `#27ae60` | entrance.svg | dm | _(dm marker; base→FL)_ |

_30 tokens._
