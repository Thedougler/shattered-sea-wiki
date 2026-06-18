# prep-map — Design Spec

**Date:** 2026-06-18
**Status:** Approved design, pre-implementation
**Topic:** A `prep-map` skill + bundled deterministic script that produces print-ready TTRPG battlemaps with a mathematically perfect 1×1 grid, beautified by a color-keyed image-to-image pass.

---

## 1. Goal & Success Criteria

Produce, for any room or dungeon in the Shattered Sea campaign, a **high-resolution, print-ready battlemap** that is:

- **Grid-perfect** — a 1×1 square grid that is exactly aligned in X and Y, by construction, never trusted to a diffusion model.
- **Print-quality** — 300 DPI, 1 tile = 1 inch = 300 px (the universal tabletop mini standard).
- **Beautiful** — flat schematic base art is restyled into a **premium hand-painted top-down battlemap** (the 2-Minute Tabletop quality bar — see §2.1) via a reliable, color-keyed img2img pass, not vague "beautify" prompting.
- **Deterministic where it matters** — layout, grid, dimensions, and the img2img instruction are all produced by a script, not improvised by the agent.
- **DM- and player-ready** — emits a DM version (traps, secret doors, entrance markers) and a player version (hidden DM elements).

A run is successful when: the grid overlays the final image with zero drift; every authored tile appears in the correct cell at the correct material; the image prints cleanly at the target physical size; and the agent never had to do pixel math or hand-write a per-map img2img prompt.

## 2. Core Concept: Paint-by-Numbers Segmentation

The base render is **not "basic art."** It is a deliberate **semantic segmentation map** — a paint-by-numbers key. Every tile is a flat, perceptually-distinct color (plus, for objects, a bold silhouette glyph). The img2img model is never asked to *infer* where a door goes; it is handed the door already placed in a unique color and told, region by region, "the rust-orange cells become iron-banded oak doors."

This is the load-bearing idea. It converts the unreliable task ("make this map beautiful") into a reliable one ("repaint each color region as its mapped material, keeping every region in place").

Three guarantees follow from it:
1. **The grid is composited last, as crisp vector** — the model never draws or keeps the grid, so the grid is perfect by construction.
2. **The img2img prompt is auto-generated** as a color→material legend from exactly the tokens present in the CSV — no per-map hand-prompting.
3. **Tiled beautify is low-risk** — every tile shares the same deterministic color-key legend, so independently-processed regions still agree on what each color means.

### 2.1 Quality Target — Premium Hand-Painted Battlemap

The aesthetic bar is **2-Minute Tabletop-class** top-down battlemap art (calibration reference: their "Underground Sanctuary" map). After all passes, an output should read as a **hand-painted, illustrated battlemap — not a photograph.** Photorealism is explicitly *not* the goal; it looks worse and plays worse than premium painterly art.

Concrete characteristics every finished map should hit:
- **Hand-painted / illustrated, stylized realism** — painterly materials (stone, wood, water, cloth), not photo textures.
- **Strictly orthographic top-down** — no perspective, no long cast shadows. Props cast only soft, short contact shadows for depth.
- **Warm atmospheric lighting** — soft orange glow pools radiating from light-source tokens (brazier, fireplace, torch); ambient shadow elsewhere. The map is *moody and lit*, not flatly uniform — but lighting never breaks top-down readability.
- **Dense, lived-in props** — furniture, rugs, barrels, crates, clutter. The richness is in the incidental detail.
- **Dark, textured void** — unmapped cells render as near-black with a faint marbled-stone texture, not flat black or transparent.
- **Per-room tonal variation** — rooms differ subtly in floor tone/material so spaces read as distinct.
- **Subtle grid** — low-opacity, understated lines (see §6.2), never harsh white.

**Two rules this imposes on the pipeline:**
- **Structure is locked; floors may be enriched.** The model must not move, add, or remove walls, doors, water, stairs, or keyed hazards (the color key is law there). Within *floor* regions it is *encouraged* to add period-appropriate incidental detail (cracks, wear, scattered debris, dust) and to render authored furniture richly — that controlled freedom is what produces the lived-in density.
- **Style is locked by description + optional reference images.** The legend prompt carries house-style descriptors (§7.2). For tighter consistency across a whole dungeon, the beautify pass may pass 1–3 **style-reference images** (via nano-banana, up to 14 refs) so every room matches one anchor look. The DM supplies the anchor(s); the campaign's chosen battlemap style can live in `art-style.md`.

**Scale reference:** 2MT's large multi-room master is **13200×9600 px** (≈44×32 tiles at our 300 DPI / 1-inch standard), confirming the print-resolution ballpark this pipeline targets for a full dungeon.

## 3. Architecture Overview (per room)

```
tile CSV ──► [render] ──► base segmentation key (flat colors + glyphs)
                          + vector grid layer (separate)
                          + auto-generated color→material legend prompt
                                   │
                                   ▼
                    [beautify · Stage A — global "stylist"]
                    downscale → FLUX Kontext (legend prompt, whole image)
                                   │
                                   ▼
                    [beautify · Stage B — "detailer"]
                    tiled-diffusion upscale → print resolution
                                   │
                                   ▼
                    [composite] crisp vector grid on top
                                   │
                       ┌───────────┴───────────┐
                       ▼                        ▼
              player.png (grid)        dm.png (grid + DM annotation overlay)
```

For a **dungeon** (multiple rooms): each room's *base segmentation key* is assembled onto a master grid with connective corridor tiles, then a **single** beautify pass runs on the combined map at reduced resolution (DM reference only — skips the expensive tiled detailer).

## 4. Component 1 — Token Library / Manifest

The keystone. Each token is defined **once** and serves three consumers: the agent (authoring code), the renderer (color + glyph), and the img2img model (prompt fragment).

### 4.1 Manifest schema

`tokens/tokens.json` — one entry per token:

```jsonc
"WL": {
  "name": "wall",
  "category": "structure",       // structure | terrain | hazard | feature | marker | primitive
  "color": "#2f3b45",            // flat fill, REQUIRED, perceptually separated (see 4.3)
  "glyph": null,                  // svg filename in tokens/svg/, or null for flat terrain
  "fragment": "thick rough-hewn stone dungeon wall",  // img2img material phrase
  "layer": "both",               // both | dm  (dm = DM-only annotation, not beautified)
  "playerFallback": null          // token code to substitute on the player map (e.g. DS → WL)
}
```

### 4.2 Starter token set (~28, extensible)

| Code | Tile | Category | Glyph? | layer | img2img fragment |
|---|---|---|---|---|---|
| `FL` | stone floor | terrain | flat | both | worn flagstone floor |
| `FW` | wood floor | terrain | flat | both | wooden plank floor |
| `WL` | wall | structure | flat | both | thick rough-hewn stone dungeon wall |
| `DR` | door | structure | ✓ | both | closed iron-banded oak door |
| `DL` | locked door | structure | ✓ | both | heavy iron-banded locked door with a keyhole |
| `DS` | secret door | structure | ✓ | dm | (player map: `playerFallback: WL`) |
| `AR` | archway / open passage | structure | ✓ | both | open stone archway |
| `SU` | stairs up | structure | ✓ | both | stone stairs ascending |
| `SD` | stairs down | structure | ✓ | both | stone stairs descending |
| `CO` | column | feature | ✓ | both | round stone column |
| `WS` | shallow water | terrain | flat | both | shallow clear water over stone |
| `WD` | deep water | terrain | flat | both | deep dark water |
| `RB` | rubble (difficult) | terrain | flat | both | broken rubble and debris |
| `LV` | lava | hazard | flat | both | glowing molten lava |
| `CM` | chasm / pit | hazard | flat | both | bottomless dark chasm |
| `TR` | trap | hazard | ✓ | dm | (DM annotation only) |
| `CH` | chest | feature | ✓ | both | closed wooden treasure chest |
| `AL` | altar | feature | ✓ | both | carved stone altar |
| `BR` | brazier (light) | feature | ✓ | both | burning iron brazier |
| `FP` | fireplace (light) | feature | ✓ | both | stone fireplace with burning fire |
| `TO` | torch sconce (light) | feature | ✓ | both | wall-mounted flaming torch |
| `TB` | table | feature | ✓ | both | wooden table, period-appropriate |
| `BE` | bed | feature | ✓ | both | wooden bed with linens |
| `BL` | bookshelf | feature | ✓ | both | tall wooden bookshelf |
| `BA` | barrel | feature | ✓ | both | wooden barrel |
| `CT` | crate | feature | ✓ | both | stacked wooden crates |
| `WR` | weapon rack | feature | ✓ | both | wooden weapon rack |
| `ST` | statue | feature | ✓ | both | carved stone statue |
| `RG` | rug | feature | flat | both | patterned woven rug |
| `EN` | entrance marker | marker | ✓ | dm | (DM annotation only) |

A human-readable catalog of all tokens lives in `references/token-library.md`. Light-source tokens (`BR`/`FP`/`TO`) drive the warm glow pools in the beautify pass; furniture/feature tokens are authored densely to produce the lived-in look from §2.1.

### 4.3 Palette discipline (color separation)

The palette is **engineered for perceptual separation** so the model never blends two materials:

- Every token's `color` is far apart in CIELAB space from every other token's color.
- **Invariant, enforced by test:** minimum pairwise ΔE2000 across all manifest colors ≥ a threshold (default 25; tuned during implementation). Adding a colliding token fails the test.
- Bulk terrain renders as **flat color only** (clean region for the model to texture). Objects/features render as **color + bold silhouette glyph** that the model replaces with the real object.
- No gradients, no anti-aliased blends in the base fill — gradients corrupt the color key.
- With ~28+ tokens, separating *all* of them perfectly is impossible. Priority: **terrain & structure colors stay maximally separated** (they carry identity by color alone); **feature/furniture tokens may cluster within a shared hue family** because their identity is carried primarily by glyph. The ΔE test weights terrain/structure pairs strictly and furniture pairs loosely.

### 4.4 Glyph rules

- Glyphs are bold, simple, high-contrast silhouettes — readable to both the agent and the model.
- Directional glyphs carry meaning the color cannot (stair direction, door swing, round column).
- The legend prompt explicitly instructs "render the object indicated by each icon," so the schematic icon is *replaced* by the real object, not preserved as line art.
- Glyph survival through img2img is an empirical quality question — validated during implementation; fallback is color-only + a stronger legend phrase.

### 4.5 Generic primitives & per-map legend overrides

The fixed library cannot anticipate every feature. Two mechanisms close the gap:

- **Generic primitives** — reserved tokens (`P1`…`P6`) with distinct reserved color+shape and `fragment: null`. Meaning is supplied per-map.
- **Per-map legend file** — an optional `legend.json` beside the CSV that (a) supplies fragments for generic primitives and (b) **overrides/re-skins standard tokens for the whole map** (e.g. turn a dungeon into an ice cave: `FL → "blue-white ice floor"`, `WL → "carved ice wall"`) with zero new SVGs.

Resolution order for a token's fragment: per-map `legend.json` → manifest default. Missing fragment for a used token is a validation error.

### 4.6 DM / player split (one beautify, two outputs)

DM-only tokens (`layer: "dm"`) are **not** beautified — they are crisp vector annotations composited on top, like a VTT GM layer. This means **one** beautify pass per room, two composited outputs:

- **player.png** = beautified terrain + vector grid.
- **dm.png** = beautified terrain + vector grid + DM annotation overlay (trap markers, secret-door highlights, entrance arrows).

Secret door (`DS`) renders as `WL` in the base key (so it beautifies as a wall and is genuinely hidden); the DM overlay marks where it is.

## 5. Component 2 — Tile CSV Authoring Format

The RimWorld / Dwarf Fortress model: whole-cell, glanceable, "plop down" tiles.

- **Format:** comma-delimited CSV. Row = grid Y, column = grid X. One token code per cell.
- **Empty cell = void** (unmapped space outside the dungeon; rendered transparent/black). Lets rooms be non-rectangular.
- **Whole-cell only:** walls, doors, floor each occupy a full 1×1 square. Walls are 1 square (5 ft) thick. No sub-cell/thin walls in v1 (see Non-Goals).

Example — a guard room (wall border, south door, a column, a chest, a shallow-water corner):

```
WL,WL,WL,WL,WL,WL
WL,FL,FL,FL,CH,WL
WL,FL,CO,FL,FL,WL
WL,FL,FL,FL,WS,WL
WL,WL,DR,WL,WL,WL
```

### 5.1 What the script does for the agent (the "fiddly deterministic work")

- **`preview`** — prints a DF-style ASCII render (one glyph per token) + a validation report, with **zero cost**, so the agent eyeball-confirms layout before spending on img2img.
- **Validation** — flags: ragged rows; unknown token codes; floating doors (a door not between two passable cells); unreachable regions; used tokens missing a fragment.
- **Auto-wall helper (optional)** — given a floor region, frame its perimeter with `WL`.
- **Geometry** — all pixel math, grid coordinates, prompt assembly, and the down/up/composite sequence are owned by the script.

## 6. Component 3 — Renderer & Geometry

**Stack: Node + `sharp`** (libvips). Rationale: matches the `use-replicate` Node toolchain; sharp is the best single library for SVG→raster + compositing + resize + format output. Tests use the built-in `node:test` — no extra test dependency.

### 6.1 Geometry

- `--ppi` = pixels per tile = pixels per inch (1 tile = 1 inch). **Default 300** (print master).
- Print dimensions: `width_px = cols × ppi`, `height_px = rows × ppi`.
- **Model-res render:** a separate render at `ppi_model` chosen so `max(width,height) ≤ model_max` (model_max pinned at implementation — see §11). Upscale factor to print = `ppi / ppi_model`.
- **Grid layer:** rendered at print res as crisp vector lines, composited last.

### 6.2 Layers & outputs

The renderer produces, deterministically:
1. **Base segmentation key** — flat token colors + object glyphs (the paint-by-numbers image). The deterministic master.
2. **Grid layer** — transparent PNG of pure grid lines at print res. Styling (color, opacity, weight) is configurable; the default is a **subtle low-opacity dark line** matched to the premium VTT look (§2.1), never harsh white.
3. **DM annotation layer** — transparent PNG of DM-only markers.
4. **Auto-generated legend prompt** — text, from the tokens present.

`render` (no img2img) emits the base key + layers + prompt for inspection and testing. `beautify` runs the full pipeline.

## 7. Component 4 — Beautify Pipeline

Modular two stages, then composite. Designed so model IDs and resolution thresholds are **swappable parameters**, with a simple fallback path.

- **Stage A — global "stylist":** downscale the base key to model res, run **one FLUX Kontext** pass (`edit-image.mjs edit`, default `kontext-pro`) on the whole image with the auto-generated legend prompt. Whole-image is required so the legend reads coherently and style/lighting stay consistent. This is where paint-by-numbers becomes materials.
- **Stage B — "detailer":** a **tiled-diffusion upscaler** (clarity/crystal/SUPIR-class, which tile internally and condition each tile on the global image) takes it from model res to print res, recovering crisp per-tile texture without global softening. The detailer is tuned to **preserve the painterly illustration style** (§2.1) — enhance brushwork and material texture, not push toward photo-realism or over-sharpen into a photographic look.
- **Composite:** crisp vector grid (and DM overlay for `dm.png`) on top.

### 7.1 Why tiling is safe here, and seam handling

- Every tile shares the same deterministic color-key legend → independently-processed regions agree on materials (free-form diffusion drifts; segmentation-keyed restyle does not).
- **Seam-to-gridline alignment:** when tiling is hand-rolled, cut beautify tiles on grid-line boundaries with overlap. Any residual seam sits exactly under a composited grid line and is invisible.

### 7.2 Auto-generated legend prompt

Assembled from the tokens present + a campaign-style preamble pulled from `wiki/system/art-style.md`. Shape:

```
Repaint this schematic top-down map as a premium hand-painted battlemap in the
style of 2-Minute Tabletop: painterly, illustrated, stylized realism — NOT a photo.
Repaint each flat-colored region as its material, keeping every wall, door, and
keyed region in EXACTLY the same position, size and shape — do not move, merge,
add, or remove any structure:
• <color descriptor>  → <fragment>
• ...
Warm atmospheric top-down lighting: soft orange glow pools around the light sources,
ambient shadow elsewhere. Strictly orthographic top-down — no perspective, no long
cast shadows. Within floor areas add subtle period-appropriate wear and clutter.
Dark marbled-stone texture in the surrounding void. No grid lines, no labels.
```

`No grid lines` is deliberate (the script composites its own — §6.2). The style and lighting lines encode the §2.1 quality target; the "do not move/add/remove any structure" clause locks the color key, while the "subtle wear and clutter" clause licenses the controlled floor enrichment that produces the lived-in density. Lighting is atmospheric but strictly orthographic — glow pools, not directional cast shadows, so the grid stays readable.

### 7.3 Fallback path & sequencing

- **Fallback:** downscale → single Kontext → `edit-image.mjs upscale` (Topaz) → composite. Faster/cheaper; the quality benchmark the tiled detailer must beat.
- **Sequencing:** Replicate burst-limits to **1 concurrent prediction**. The skill orchestrates rooms serially with a sleep between calls. `--dry-run` estimates call count and cost before spending.

## 8. Component 5 — Dungeon Compose

A dungeon is the same primitive at a larger scale: a grid of tiles (rooms + corridors).

- **Input:** a `dungeon.json` listing rooms — each with its tile CSV and an (x,y) offset onto the master grid — plus optional straight corridor tile-runs (start cell, end cell, token). No auto-pathfinding router in v1.
- **Script (deterministic):** merge room grids at offsets, paint any declared corridor runs, detect overlap/collision, render the master grid.
- **Agent (judgment):** decides placement, what connects to what, and authors the corridor runs (or hand-places connective tiles) so the dungeon is cohesive and fun. (Layout judgment is prep-dungeon's spatial-logic job, not the script's.)
- **Beautify:** assembly stacks the **base segmentation keys** (not already-beautified rooms — that would double-process and the corridors must be styled together), then **one** beautify pass at **reduced PPI** and **skipping the tiled detailer** — the combined map is a DM reference, not a print surface.
- **Output:** a cohesive whole-dungeon DM overview map.

## 9. File Layout & CLI Surface

```
.claude/skills/prep-map/
  SKILL.md
  references/
    token-library.md      # human-readable token catalog
    prompting.md          # legend-prompt construction
    pipeline.md           # geometry + beautify deep reference
  tokens/
    tokens.json           # the manifest
    svg/                  # one bold silhouette per glyph token
  scripts/
    map.mjs               # CLI entry
    lib/{manifest,grid,render,beautify,compose,palette}.mjs
    test/*.test.mjs       # node:test
```

Generated maps are stored per `ttrpg-visual-aids` conventions under `wiki/assets/maps/<area-or-dungeon>/`. Print masters are **lossless PNG** (`ttrpg-visual-aids` reserves `.png` for "maps needing lossless detail"): `<room>.player.png`, `<room>.dm.png`, `<dungeon>.overview.png`. An optional downscaled `.webp` per output is generated for wiki embedding / VTT screen use.

CLI:

| Command | Cost | Purpose |
|---|---|---|
| `map.mjs preview <tiles.csv>` | free | ASCII render + validation report |
| `map.mjs render <tiles.csv> [--ppi N] [--legend f] [--out dir]` | free | base key + grid/DM layers + legend prompt |
| `map.mjs beautify <tiles.csv> [...] [--fallback] [--dry-run]` | $ | full pipeline → player.png + dm.png (+ optional webp) |
| `map.mjs compose <dungeon.json> [--ppi N] [--dry-run]` | $ | assemble + beautify dungeon overview |

## 10. Integration

- **prep-dungeon** — its room list + spatial logic feed prep-map (one map per room, plus `compose` for the overview). prep-map is the visual realization of a prep-dungeon design.
- **ttrpg-visual-aids** — storage paths, embedding syntax, and `art-style.md` (the campaign style preamble injected into the legend prompt so maps look on-brand). Note: visual-aids uses OpenRouter/Gemini for scene art; prep-map deliberately uses Replicate/Kontext because it needs instruction-based, structure-preserving, color-keyed img2img + deterministic upscale.
- **use-replicate** — the beautify/upscale backend (`edit-image.mjs`, `replicate-run.mjs`).
- **player-view** — `*.player.png` maps are player-facing; `*.dm.png` stays DM-only.

## 11. Open Questions — verify at implementation, do not guess

- **Model max resolutions** for `flux-kontext-pro` (and `kontext-max`) — pins `ppi_model` and whether per-room tiling is needed. Pull from current Replicate/model docs (ctx7) before locking geometry math.
- **Tiled detailer choice** — `clarity-upscaler` vs `crystal-upscaler` vs `topaz`; whether the model tiles internally or we hand-roll seam-aligned tiling. Decide via ctx7 + an empirical A/B against the fallback path.
- **Glyph survival** through Kontext — empirically validate that object glyphs are replaced by real objects, not preserved as line art; tune glyph boldness / legend phrasing.
- **House-style lock (§2.1)** — whether descriptor-only prompting reliably hits the 2MT-class bar, or whether 1–3 style-reference images (nano-banana) are needed for cross-room consistency; and tuning the detailer so it *enhances* rather than photo-realizes the painterly style. Decide via an empirical A/B.

## 12. Testing Strategy

**Script — real TDD (deterministic assertions, money never spent in tests):**
- `grid.mjs` — CSV parse (valid / ragged rows error / void cells); validation (floating door, unreachable region, unknown token); geometry (exact px dimensions for given ppi/size); auto-wall helper.
- `palette.mjs` — min pairwise ΔE2000 ≥ threshold across all manifest colors; every token has required fields; every referenced glyph file exists.
- `render.mjs` — golden checks: render a known CSV, assert output dimensions, assert the pixel color at named tile centers equals the token color, assert grid-line positions. (sharp renders are stable → reliable goldens.)
- `beautify.mjs` — mock Replicate calls; assert the auto-generated legend prompt for a given CSV matches expected (deterministic from manifest + tiles); assert stage order and seam-alignment math.
- `compose.mjs` — assert master-grid offsets, collision detection, corridor insertion.

**Skill — writing-skills methodology:**
- **Baseline (RED):** a fresh agent asked to "make a print battlemap for this room" *without* the skill — document failure modes (hand-waved resolution, no grid guarantee, free-form img2img prompt, no DM/player split).
- **With skill (GREEN):** agent follows the pipeline, drives the script, produces a deterministic base + reliable beautify + both outputs.
- **Application scenarios:** single room; full dungeon via compose; ice-cave reskin via `legend.json`; a feature needing a generic primitive.

## 13. Build Phases (honors "script first")

1. **Phase A — core render:** manifest + palette (with ΔE test), tokens/SVGs, CSV parse/validate, geometry, base key + grid + DM layers, `preview`/`render`. Fully testable with no Replicate spend.
2. **Phase B — beautify:** legend-prompt generation, Stage A/B pipeline, composite, fallback path, `beautify`.
3. **Phase C — compose:** dungeon assembly + DM overview.
4. **Phase D — the `prep-map` SKILL.md** wrapping it all, tested via the writing-skills methodology.

## 14. Non-Goals (YAGNI)

- Sub-cell / thin / diagonal walls (whole-cell only) — documented future extension.
- VTT dynamic-lighting wall-segment export (line-of-sight data) — possible future.
- Animated/video maps.
- Procedural dungeon *generation* — the agent designs layout (via prep-dungeon); the script renders what it is given.
- A real-time interactive editor — CSV authoring + `preview` is the loop.

## 15. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Kontext drifts on whole-map restyle | structure-preserving instruction + segmentation key + grid composited last; ControlNet-seg as an upgrade if needed |
| Glyph line-art survives into output | bold silhouettes + explicit "render as object"; empirical validation; color-only fallback |
| Tiled-upscaler seams | seam-to-gridline alignment + global conditioning + grid composite |
| Cost at dungeon scale | DM overview skips tiled detailer; `--dry-run` cost estimate; cheap fallback path |
| Replicate 1-concurrent / rate limits | sequential orchestration in the skill, sleep between calls |
| Unknown model res limits | pin via ctx7 before locking geometry; modular swappable stages |
| Output drifts to photo-real or flat clip-art | §2.1 house-style descriptors in the legend prompt; optional style-reference images; detailer tuned to preserve illustration; §2.1 as the explicit acceptance bar |
