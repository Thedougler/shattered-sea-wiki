# prep-map Phase A — Deterministic Core Render Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deterministic, zero-cost core of `prep-map` — a Node/sharp tool that turns a tile CSV into a validated, pixel-exact base segmentation key (the "paint-by-numbers" image), a crisp grid layer, and a DM-annotation layer, plus an ASCII preview and an auto-generated img2img legend prompt.

**Architecture:** A token manifest (`tokens.json`) is the single source of truth: each token carries a color, an optional glyph SVG, an img2img fragment, an ASCII char, and layer/fallback metadata. Pure-logic libs (`manifest`, `palette`, `grid`, `legend`) parse/validate/measure with no I/O cost; `render` builds SVG documents and rasterizes them with sharp; `map.mjs` is the CLI. Everything here is deterministic and unit-tested — **no Replicate spend**. Beautify (Phase B), dungeon compose (Phase C), and the SKILL.md (Phase D) are separate plans.

**Tech Stack:** Node 22 (ESM `.mjs`), `sharp` (libvips — SVG raster + composite + resize + raw pixels), `node:test` + `node:assert` (built-in test runner, no extra deps). Skill-local `npm` install isolated from the pnpm workspace.

**Spec:** `docs/superpowers/specs/2026-06-18-prep-map-design.md` (Phase A = its §4, §5, §6, and the `render`/`preview` parts of §9).

---

## ⚠️ Worktree git note (read once)

This worktree lives inside a git submodule and its `core.worktree` resolves to the submodule git-dir, so plain `git` reports phantom "deleted" files and `git add <newfile>` fails with "pathspec did not match". **Run this once at the start of the session, then use git normally:**

```bash
export GIT_WORK_TREE="$(pwd)"
# verify: should show real untracked files as ?? (not phantom D deletes)
git status --short
```

All `git` commands in this plan assume that env var is exported. Do **not** mutate `core.worktree` (it touches shared submodule linkage).

---

## File Structure

```
.claude/skills/prep-map/
  tokens/
    tokens.json                 # the manifest — single source of truth (data)
    svg/                        # one 0 0 100 100 silhouette per glyph-bearing token
      door.svg door-locked.svg column.svg chest.svg trap.svg entrance.svg
  scripts/
    package.json                # type:module, sharp dep, `npm test` → node --test
    .gitignore                  # node_modules/
    map.mjs                     # CLI: `preview`, `render`
    lib/
      manifest.mjs              # load + validate manifest; fragment/fallback resolution
      palette.mjs               # sRGB→Lab, CIEDE2000, color-separation gate
      grid.mjs                  # CSV parse, validation, geometry, ASCII preview
      legend.mjs                # auto-generate the color→material legend prompt
      render.mjs                # build base/grid/dm SVGs, rasterize + composite via sharp
    test/
      manifest.test.mjs palette.test.mjs grid.test.mjs
      legend.test.mjs render.test.mjs cli.test.mjs
      fixtures/guard-room.csv
```

**Module responsibilities (each file has one job):**
- `manifest.mjs` — owns the manifest contract. Nothing else loads `tokens.json`.
- `palette.mjs` — owns color math. Pure functions; no manifest knowledge except the gate helper.
- `grid.mjs` — owns the grid model: text→cells, validation, pixel geometry, ASCII.
- `legend.mjs` — owns prompt assembly (consumed by Phase B, emitted by `render` now).
- `render.mjs` — owns all SVG generation + sharp rasterization/compositing.
- `map.mjs` — argument parsing + wiring only; no business logic.

---

## Task 0: Package setup + sharp install + smoke test

**Files:**
- Create: `.claude/skills/prep-map/scripts/package.json`
- Create: `.claude/skills/prep-map/scripts/.gitignore`
- Create: `.claude/skills/prep-map/scripts/test/smoke.test.mjs`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "@shattered-sea/prep-map",
  "private": true,
  "type": "module",
  "version": "0.1.0",
  "description": "Deterministic battlemap render engine (Phase A) for the prep-map skill.",
  "scripts": {
    "test": "node --test"
  }
}
```

- [ ] **Step 2: Create `.gitignore`**

```
node_modules/
/tmp-out/
```

- [ ] **Step 3: Install sharp (skill-local, isolated from the pnpm workspace)**

Run:
```bash
cd .claude/skills/prep-map/scripts && npm install sharp && cd -
```
Expected: `node_modules/sharp` appears; `package.json` gains a `dependencies.sharp` entry. (`.claude/**` is outside `pnpm-workspace.yaml` globs, so this does not touch the workspace; sharp is already an approved native build in `.npmrc`.)

- [ ] **Step 4: Write the smoke test**

`scripts/test/smoke.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";

test("sharp rasterizes an SVG to exact pixel dimensions", async () => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"><rect width="20" height="10" fill="#ff0000"/></svg>`;
  const { data, info } = await sharp(Buffer.from(svg))
    .raw()
    .toBuffer({ resolveWithObject: true });
  assert.equal(info.width, 20);
  assert.equal(info.height, 10);
  // first pixel is red (channels are R,G,B[,A])
  assert.equal(data[0], 255);
  assert.equal(data[1], 0);
  assert.equal(data[2], 0);
});
```

- [ ] **Step 5: Run the smoke test**

Run:
```bash
cd .claude/skills/prep-map/scripts && node --test test/smoke.test.mjs; cd -
```
Expected: PASS (1 test). If sharp fails to load, re-run `npm install sharp` and confirm Node is v22 (`node --version`).

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/prep-map/scripts/package.json .claude/skills/prep-map/scripts/package-lock.json .claude/skills/prep-map/scripts/.gitignore .claude/skills/prep-map/scripts/test/smoke.test.mjs
git commit -m "feat(prep-map): scaffold render engine package + sharp smoke test"
```

---

## Task 1: Token manifest + manifest loader/validator

**Files:**
- Create: `.claude/skills/prep-map/tokens/tokens.json`
- Create: `.claude/skills/prep-map/scripts/lib/manifest.mjs`
- Test: `.claude/skills/prep-map/scripts/test/manifest.test.mjs`

This task ships a **core 12-token set** that exercises every code path (flat terrain, glyph object, structure, hazard, dm-layer + playerFallback, missing-fragment). The full ~28-token set is added as data in Task 9.

- [ ] **Step 1: Write the failing test**

`scripts/test/manifest.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import { loadManifest, resolveFragment, effectiveCode } from "../lib/manifest.mjs";

test("loadManifest returns valid entries with required fields", () => {
  const m = loadManifest();
  assert.ok(m.WL && m.FL && m.DR, "core tokens present");
  for (const [code, e] of Object.entries(m)) {
    assert.ok(/^#[0-9a-fA-F]{6}$/.test(e.color), `${code} has hex color`);
    assert.ok(["both", "dm"].includes(e.layer), `${code} has valid layer`);
    assert.ok(
      ["structure", "terrain", "hazard", "feature", "marker", "primitive"].includes(e.category),
      `${code} has valid category`,
    );
  }
});

test("dm-layer tokens declare a playerFallback", () => {
  const m = loadManifest();
  for (const [code, e] of Object.entries(m)) {
    if (e.layer === "dm") assert.ok(e.playerFallback, `${code} (dm) needs playerFallback`);
  }
});

test("resolveFragment prefers per-map legend override over manifest default", () => {
  const m = loadManifest();
  assert.equal(resolveFragment(m, "FL", {}), m.FL.fragment);
  assert.equal(resolveFragment(m, "FL", { FL: "blue-white ice floor" }), "blue-white ice floor");
});

test("effectiveCode substitutes playerFallback for dm tokens", () => {
  const m = loadManifest();
  assert.equal(effectiveCode(m, "FL"), "FL");
  assert.equal(effectiveCode(m, "DS"), "WL"); // secret door hides as wall
  assert.equal(effectiveCode(m, "TR"), "FL"); // trap sits on floor in the base key
  assert.equal(effectiveCode(m, null), null);
});

test("loadManifest throws on a malformed entry", () => {
  assert.throws(() => loadManifest(new URL("./fixtures/bad-manifest.json", import.meta.url)));
});
```

- [ ] **Step 2: Create the bad-manifest fixture (for the throw test)**

`scripts/test/fixtures/bad-manifest.json`:
```json
{ "XX": { "name": "broken", "category": "terrain", "color": "not-a-hex", "layer": "both" } }
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `cd .claude/skills/prep-map/scripts && node --test test/manifest.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../lib/manifest.mjs").

- [ ] **Step 4: Write the manifest data**

`tokens/tokens.json`:
```json
{
  "WL": { "name": "wall", "category": "structure", "color": "#2f3b45", "colorName": "dark slate-blue blocks", "ascii": "#", "glyph": null, "fragment": "thick rough-hewn stone dungeon walls", "layer": "both", "playerFallback": null },
  "FL": { "name": "stone floor", "category": "terrain", "color": "#9a948a", "colorName": "warm grey squares", "ascii": ".", "glyph": null, "fragment": "worn flagstone floor", "layer": "both", "playerFallback": null },
  "FW": { "name": "wood floor", "category": "terrain", "color": "#b3702f", "colorName": "warm wood-brown squares", "ascii": ",", "glyph": null, "fragment": "wooden plank floor", "layer": "both", "playerFallback": null },
  "WS": { "name": "shallow water", "category": "terrain", "color": "#4aa3c7", "colorName": "light cyan squares", "ascii": "~", "glyph": null, "fragment": "shallow clear water over stone", "layer": "both", "playerFallback": null },
  "WD": { "name": "deep water", "category": "terrain", "color": "#1f4e6b", "colorName": "deep blue squares", "ascii": "W", "glyph": null, "fragment": "deep dark water", "layer": "both", "playerFallback": null },
  "DR": { "name": "door", "category": "structure", "color": "#a8442a", "colorName": "brick-red cells marked with a door icon", "ascii": "+", "glyph": "door.svg", "fragment": "a closed iron-banded oak door", "layer": "both", "playerFallback": null },
  "DL": { "name": "locked door", "category": "structure", "color": "#d9a528", "colorName": "brass-gold cells marked with a lock icon", "ascii": "=", "glyph": "door-locked.svg", "fragment": "a heavy iron-banded locked door with a keyhole", "layer": "both", "playerFallback": null },
  "DS": { "name": "secret door", "category": "structure", "color": "#7a2f8f", "colorName": "(hidden)", "ascii": "S", "glyph": "door.svg", "fragment": null, "layer": "dm", "playerFallback": "WL" },
  "CO": { "name": "column", "category": "feature", "color": "#b0479e", "colorName": "magenta cells marked with a circle", "ascii": "o", "glyph": "column.svg", "fragment": "a round stone column", "layer": "both", "playerFallback": null },
  "CH": { "name": "chest", "category": "feature", "color": "#8e44ad", "colorName": "purple cells marked with a chest icon", "ascii": "$", "glyph": "chest.svg", "fragment": "a closed wooden treasure chest", "layer": "both", "playerFallback": null },
  "TR": { "name": "trap", "category": "hazard", "color": "#c02a2a", "colorName": "(dm only)", "ascii": "^", "glyph": "trap.svg", "fragment": null, "layer": "dm", "playerFallback": "FL" },
  "EN": { "name": "entrance", "category": "marker", "color": "#27ae60", "colorName": "(dm only)", "ascii": ">", "glyph": "entrance.svg", "fragment": null, "layer": "dm", "playerFallback": "FL" }
}
```

- [ ] **Step 5: Write `lib/manifest.mjs`**

```javascript
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_PATH = resolve(HERE, "../../tokens/tokens.json");

const REQUIRED = ["name", "category", "color", "layer"];
const CATEGORIES = new Set(["structure", "terrain", "hazard", "feature", "marker", "primitive"]);
const HEX = /^#[0-9a-fA-F]{6}$/;

/** Load + validate the token manifest. `pathOrUrl` is for tests; defaults to tokens/tokens.json. */
export function loadManifest(pathOrUrl = DEFAULT_PATH) {
  const text = readFileSync(pathOrUrl, "utf8");
  const raw = JSON.parse(text);
  for (const [code, e] of Object.entries(raw)) {
    for (const f of REQUIRED) {
      if (!(f in e)) throw new Error(`token ${code}: missing required field "${f}"`);
    }
    if (!CATEGORIES.has(e.category)) throw new Error(`token ${code}: bad category "${e.category}"`);
    if (!HEX.test(e.color)) throw new Error(`token ${code}: color must be #RRGGBB, got "${e.color}"`);
    if (e.layer !== "both" && e.layer !== "dm") throw new Error(`token ${code}: layer must be "both"|"dm"`);
    if (e.layer === "dm" && !e.playerFallback) throw new Error(`token ${code}: dm-layer token needs a playerFallback`);
  }
  return raw;
}

/** Resolve the img2img fragment for a token, applying per-map legend overrides. */
export function resolveFragment(manifest, code, legend = {}) {
  return legend[code] ?? manifest[code]?.fragment ?? null;
}

/** The code actually drawn in the base segmentation key: dm tokens collapse to their playerFallback. */
export function effectiveCode(manifest, code) {
  if (!code) return null;
  const e = manifest[code];
  if (e && e.layer === "dm") return e.playerFallback ?? "FL";
  return code;
}
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/manifest.test.mjs; cd -`
Expected: PASS (5 tests).

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/prep-map/tokens/tokens.json .claude/skills/prep-map/scripts/lib/manifest.mjs .claude/skills/prep-map/scripts/test/manifest.test.mjs .claude/skills/prep-map/scripts/test/fixtures/bad-manifest.json
git commit -m "feat(prep-map): token manifest + validated loader (core 12-token set)"
```

---

## Task 2: Palette color-separation gate (CIEDE2000)

**Files:**
- Create: `.claude/skills/prep-map/scripts/lib/palette.mjs`
- Test: `.claude/skills/prep-map/scripts/test/palette.test.mjs`

The base render is a color key — two tokens that look alike to the model are a bug. This task gives us a perceptual-distance gate enforced as a test.

- [ ] **Step 1: Write the failing test**

`scripts/test/palette.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import { hexToLab, ciede2000, checkSeparation } from "../lib/palette.mjs";
import { loadManifest } from "../lib/manifest.mjs";

test("ciede2000 of identical colors is 0", () => {
  const lab = hexToLab("#3c6e9a");
  assert.equal(ciede2000(lab, lab), 0);
});

test("ciede2000 is symmetric", () => {
  const a = hexToLab("#112233"), b = hexToLab("#aabbcc");
  assert.ok(Math.abs(ciede2000(a, b) - ciede2000(b, a)) < 1e-9);
});

test("ciede2000 black vs white is large (~100)", () => {
  const d = ciede2000(hexToLab("#000000"), hexToLab("#ffffff"));
  assert.ok(d > 95 && d < 105, `expected ~100, got ${d}`);
});

test("the shipped manifest passes the separation gate", () => {
  const violations = checkSeparation(loadManifest());
  assert.deepEqual(violations, [], `palette collisions: ${JSON.stringify(violations)}`);
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd .claude/skills/prep-map/scripts && node --test test/palette.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../lib/palette.mjs").

- [ ] **Step 3: Write `lib/palette.mjs`**

```javascript
// ctx7: CIEDE2000 per Sharma, Wu & Dalal (2005) — standard perceptual color difference.

function srgbToLinear(c) {
  c /= 255;
  return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

/** "#rrggbb" -> CIELab (D65). */
export function hexToLab(hex) {
  const r = srgbToLinear(parseInt(hex.slice(1, 3), 16));
  const g = srgbToLinear(parseInt(hex.slice(3, 5), 16));
  const b = srgbToLinear(parseInt(hex.slice(5, 7), 16));
  // linear sRGB -> XYZ (D65)
  const X = r * 0.4124 + g * 0.3576 + b * 0.1805;
  const Y = r * 0.2126 + g * 0.7152 + b * 0.0722;
  const Z = r * 0.0193 + g * 0.1192 + b * 0.9505;
  const Xn = 0.95047, Yn = 1.0, Zn = 1.08883;
  const f = (t) => (t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
  const fx = f(X / Xn), fy = f(Y / Yn), fz = f(Z / Zn);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

const rad = (d) => (d * Math.PI) / 180;
const deg = (r) => (r * 180) / Math.PI;

/** CIEDE2000 color difference between two CIELab triples. */
export function ciede2000([L1, a1, b1], [L2, a2, b2]) {
  const kL = 1, kC = 1, kH = 1;
  const C1 = Math.hypot(a1, b1), C2 = Math.hypot(a2, b2);
  const Cbar = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)));
  const a1p = (1 + G) * a1, a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
  const h1p = (deg(Math.atan2(b1, a1p)) + 360) % 360;
  const h2p = (deg(Math.atan2(b2, a2p)) + 360) % 360;

  const dLp = L2 - L1;
  const dCp = C2p - C1p;
  let dhp;
  if (C1p * C2p === 0) dhp = 0;
  else if (Math.abs(h2p - h1p) <= 180) dhp = h2p - h1p;
  else dhp = h2p - h1p > 180 ? h2p - h1p - 360 : h2p - h1p + 360;
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(rad(dhp) / 2);

  const Lbarp = (L1 + L2) / 2;
  const Cbarp = (C1p + C2p) / 2;
  let hbarp;
  if (C1p * C2p === 0) hbarp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbarp = (h1p + h2p) / 2;
  else hbarp = h1p + h2p < 360 ? (h1p + h2p + 360) / 2 : (h1p + h2p - 360) / 2;

  const T =
    1 -
    0.17 * Math.cos(rad(hbarp - 30)) +
    0.24 * Math.cos(rad(2 * hbarp)) +
    0.32 * Math.cos(rad(3 * hbarp + 6)) -
    0.2 * Math.cos(rad(4 * hbarp - 63));
  const dTheta = 30 * Math.exp(-(((hbarp - 275) / 25) ** 2));
  const Rc = 2 * Math.sqrt(Cbarp ** 7 / (Cbarp ** 7 + 25 ** 7));
  const Sl = 1 + (0.015 * (Lbarp - 50) ** 2) / Math.sqrt(20 + (Lbarp - 50) ** 2);
  const Sc = 1 + 0.045 * Cbarp;
  const Sh = 1 + 0.015 * Cbarp * T;
  const Rt = -Math.sin(rad(2 * dTheta)) * Rc;

  return Math.sqrt(
    (dLp / (kL * Sl)) ** 2 +
      (dCp / (kC * Sc)) ** 2 +
      (dHp / (kH * Sh)) ** 2 +
      Rt * (dCp / (kC * Sc)) * (dHp / (kH * Sh)),
  );
}

const STRICT_CATS = new Set(["terrain", "structure"]);
const isStrict = (cat) => STRICT_CATS.has(cat);

/**
 * Return the list of color-pair violations. Empty array = pass.
 * Terrain/structure carry identity by color → strict threshold against everything.
 * Feature/marker tokens cluster (identity via glyph) → loose threshold among themselves.
 */
export function checkSeparation(manifest, { strict = 20, loose = 10 } = {}) {
  const entries = Object.entries(manifest);
  const labs = entries.map(([code, e]) => ({ code, cat: e.category, lab: hexToLab(e.color) }));
  const violations = [];
  for (let i = 0; i < labs.length; i++) {
    for (let j = i + 1; j < labs.length; j++) {
      const d = ciede2000(labs[i].lab, labs[j].lab);
      const thr = isStrict(labs[i].cat) || isStrict(labs[j].cat) ? strict : loose;
      if (d < thr) violations.push({ a: labs[i].code, b: labs[j].code, deltaE: +d.toFixed(2), threshold: thr });
    }
  }
  return violations;
}
```

- [ ] **Step 4: Run the test**

Run: `cd .claude/skills/prep-map/scripts && node --test test/palette.test.mjs; cd -`
Expected: PASS (4 tests). **If the manifest gate fails**, the violation list names the colliding pair + their ΔE — nudge one token's `color` in `tokens.json` (shift hue/lightness away) and re-run until green. Do not lower the thresholds to force a pass.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/prep-map/scripts/lib/palette.mjs .claude/skills/prep-map/scripts/test/palette.test.mjs .claude/skills/prep-map/tokens/tokens.json
git commit -m "feat(prep-map): CIEDE2000 palette-separation gate"
```

---

## Task 3: CSV → grid model (parse)

**Files:**
- Create: `.claude/skills/prep-map/scripts/lib/grid.mjs`
- Create: `.claude/skills/prep-map/scripts/test/fixtures/guard-room.csv`
- Test: `.claude/skills/prep-map/scripts/test/grid.test.mjs`

- [ ] **Step 1: Create the fixture**

`scripts/test/fixtures/guard-room.csv`:
```
WL,WL,WL,WL,WL,WL
WL,FL,FL,FL,CH,WL
WL,FL,CO,FL,FL,WL
WL,FL,FL,FL,WS,WL
WL,WL,DR,WL,WL,WL
```

- [ ] **Step 2: Write the failing test**

`scripts/test/grid.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { parseGrid } from "../lib/grid.mjs";

const fixture = (name) => readFileSync(new URL(`./fixtures/${name}`, import.meta.url), "utf8");

test("parseGrid yields width/height and uppercased codes", () => {
  const g = parseGrid(fixture("guard-room.csv"));
  assert.equal(g.width, 6);
  assert.equal(g.height, 5);
  assert.equal(g.cells[0][0], "WL");
  assert.equal(g.cells[4][2], "DR");
});

test("parseGrid treats empty cells as void (null) and trims whitespace", () => {
  const g = parseGrid("WL, ,WL\nFL,FL,FL");
  assert.equal(g.cells[0][1], null);
  assert.equal(g.cells[0][2], "WL");
});

test("parseGrid lowercases-insensitive: 'wl' -> 'WL'", () => {
  const g = parseGrid("wl,fl");
  assert.equal(g.cells[0][0], "WL");
  assert.equal(g.cells[0][1], "FL");
});

test("parseGrid drops trailing blank lines", () => {
  const g = parseGrid("WL,FL\nFL,WL\n\n");
  assert.equal(g.height, 2);
});

test("parseGrid throws on a ragged row", () => {
  assert.throws(() => parseGrid("WL,FL,WL\nFL,WL"), /ragged row 2/);
});

test("parseGrid throws on empty input", () => {
  assert.throws(() => parseGrid("   \n  "), /empty grid/);
});
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../lib/grid.mjs").

- [ ] **Step 4: Write `parseGrid` in `lib/grid.mjs`**

```javascript
/** Parse a tile CSV into { width, height, cells[][] }. Empty cell = null (void). */
export function parseGrid(csvText) {
  const lines = csvText.replace(/\r\n?/g, "\n").split("\n");
  while (lines.length && lines[lines.length - 1].trim() === "") lines.pop();
  if (lines.length === 0) throw new Error("empty grid");
  const rows = lines.map((line) => line.split(",").map((c) => c.trim()));
  const width = rows[0].length;
  rows.forEach((r, i) => {
    if (r.length !== width) throw new Error(`ragged row ${i + 1}: ${r.length} cols, expected ${width}`);
  });
  const cells = rows.map((r) => r.map((c) => (c === "" ? null : c.toUpperCase())));
  return { width, height: cells.length, cells };
}
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: PASS (6 tests).

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/prep-map/scripts/lib/grid.mjs .claude/skills/prep-map/scripts/test/grid.test.mjs .claude/skills/prep-map/scripts/test/fixtures/guard-room.csv
git commit -m "feat(prep-map): CSV tile-grid parser"
```

---

## Task 4: Grid validation

**Files:**
- Modify: `.claude/skills/prep-map/scripts/lib/grid.mjs` (add `validateGrid`)
- Modify: `.claude/skills/prep-map/scripts/test/grid.test.mjs` (add cases)

`validateGrid` returns `{ ok, errors, warnings }`. Errors: unknown token, floating door. Warnings: a beautified (`both`-layer) token used with no img2img fragment (Phase B will need it). Reachability is intentionally **not** in Phase A — noted in §Self-Review.

- [ ] **Step 1: Add the failing tests**

Append to `scripts/test/grid.test.mjs`:
```javascript
import { validateGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";

test("validateGrid passes a well-formed room", () => {
  const m = loadManifest();
  const g = parseGrid(fixture("guard-room.csv"));
  const r = validateGrid(g, m);
  assert.equal(r.ok, true, JSON.stringify(r.errors));
});

test("validateGrid flags an unknown token", () => {
  const m = loadManifest();
  const g = parseGrid("WL,ZZ\nFL,FL");
  const r = validateGrid(g, m);
  assert.equal(r.ok, false);
  assert.match(r.errors.join("\n"), /unknown token: ZZ/);
});

test("validateGrid flags a floating door (not between two passable cells)", () => {
  const m = loadManifest();
  // door surrounded by walls on all sides → floating
  const g = parseGrid("WL,WL,WL\nWL,DR,WL\nWL,WL,WL");
  const r = validateGrid(g, m);
  assert.equal(r.ok, false);
  assert.match(r.errors.join("\n"), /floating door/);
});

test("validateGrid accepts a door between two passable cells", () => {
  const m = loadManifest();
  // door with floor north and south
  const g = parseGrid("WL,FL,WL\nWL,DR,WL\nWL,FL,WL");
  const r = validateGrid(g, m);
  assert.equal(r.ok, true, JSON.stringify(r.errors));
});
```

- [ ] **Step 2: Run to verify failure**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: FAIL ("validateGrid is not a function").

- [ ] **Step 3: Implement `validateGrid` in `lib/grid.mjs`**

Append:
```javascript
const DOOR_CODES = new Set(["DR", "DL", "DS"]);
const BLOCKING_TERRAIN = new Set(["WD", "LV", "CM"]); // deep water, lava, chasm

/** Validate a parsed grid against the manifest. Returns { ok, errors, warnings }. */
export function validateGrid(grid, manifest, legend = {}) {
  const { cells, width, height } = grid;
  const errors = [];
  const warnings = [];
  const used = new Set();

  const at = (x, y) => (y < 0 || x < 0 || y >= height || x >= width ? null : cells[y][x]);
  const isPassable = (code) => {
    if (!code) return false;
    const e = manifest[code];
    if (!e) return false;
    if (e.category === "structure") return false;
    if (BLOCKING_TERRAIN.has(code)) return false;
    return true;
  };

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const code = cells[y][x];
      if (code === null) continue;
      used.add(code);
      if (!manifest[code]) {
        errors.push(`(${x},${y}) unknown token: ${code}`);
        continue;
      }
      if (DOOR_CODES.has(code)) {
        const ns = isPassable(at(x, y - 1)) && isPassable(at(x, y + 1));
        const ew = isPassable(at(x - 1, y)) && isPassable(at(x + 1, y));
        if (!ns && !ew) errors.push(`(${x},${y}) floating door ${code}: not between two passable cells`);
      }
    }
  }

  for (const code of used) {
    const e = manifest[code];
    if (!e || e.layer === "dm") continue;
    const frag = legend[code] ?? e.fragment ?? null;
    if (!frag) warnings.push(`token ${code} has no img2img fragment (beautify will need one)`);
  }

  return { ok: errors.length === 0, errors, warnings };
}
```

- [ ] **Step 4: Run to verify passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: PASS (10 tests total).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/prep-map/scripts/lib/grid.mjs .claude/skills/prep-map/scripts/test/grid.test.mjs
git commit -m "feat(prep-map): grid validation (unknown tokens, floating doors, missing fragments)"
```

---

## Task 5: Geometry + ASCII preview

**Files:**
- Modify: `.claude/skills/prep-map/scripts/lib/grid.mjs` (add `geometry`, `asciiPreview`)
- Modify: `.claude/skills/prep-map/scripts/test/grid.test.mjs` (add cases)

- [ ] **Step 1: Add the failing tests**

Append to `scripts/test/grid.test.mjs`:
```javascript
import { geometry, asciiPreview } from "../lib/grid.mjs";

test("geometry computes exact pixel dimensions at the given ppi", () => {
  const g = parseGrid(fixture("guard-room.csv")); // 6 x 5
  assert.deepEqual(geometry(g, 300), { ppi: 300, tilePx: 300, widthPx: 1800, heightPx: 1500 });
  assert.deepEqual(geometry(g, 64), { ppi: 64, tilePx: 64, widthPx: 384, heightPx: 320 });
});

test("asciiPreview renders one glyph char per cell, space for void", () => {
  const m = loadManifest();
  const g = parseGrid("WL,WL,WL\nWL,FL,WL\nWL,DR,WL");
  assert.equal(asciiPreview(g, m), "###\n#.#\n#+#");
  const v = parseGrid("WL, ,WL");
  assert.equal(asciiPreview(v, m), "# #");
});
```

- [ ] **Step 2: Run to verify failure**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: FAIL ("geometry is not a function").

- [ ] **Step 3: Implement in `lib/grid.mjs`**

Append:
```javascript
/** Pixel geometry at a given pixels-per-tile (= pixels-per-inch; 1 tile = 1 inch). */
export function geometry(grid, ppi = 300) {
  return { ppi, tilePx: ppi, widthPx: grid.width * ppi, heightPx: grid.height * ppi };
}

/** Dwarf-Fortress-style ASCII render: manifest `ascii` char per token, space for void. */
export function asciiPreview(grid, manifest) {
  return grid.cells
    .map((row) => row.map((code) => (code ? manifest[code]?.ascii ?? code[0] : " ")).join(""))
    .join("\n");
}
```

- [ ] **Step 4: Run to verify passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/grid.test.mjs; cd -`
Expected: PASS (12 tests total).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/prep-map/scripts/lib/grid.mjs .claude/skills/prep-map/scripts/test/grid.test.mjs
git commit -m "feat(prep-map): pixel geometry + ASCII preview"
```

---

## Task 6: Legend prompt generation

**Files:**
- Create: `.claude/skills/prep-map/scripts/lib/legend.mjs`
- Test: `.claude/skills/prep-map/scripts/test/legend.test.mjs`

Generates the auto color→material legend prompt (spec §7.2) from exactly the tokens present. dm-layer tokens are excluded (not beautified). Deterministic → exact string assertion.

- [ ] **Step 1: Write the failing test**

`scripts/test/legend.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import { parseGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";
import { buildLegendPrompt } from "../lib/legend.mjs";

test("buildLegendPrompt lists only present, beautified tokens (sorted), with overrides", () => {
  const m = loadManifest();
  const g = parseGrid("WL,FL\nFL,WS");
  const prompt = buildLegendPrompt(g, m);
  assert.match(prompt, /premium hand-painted battlemap in the style of 2-Minute Tabletop/);
  assert.match(prompt, /warm grey squares → worn flagstone floor/);
  assert.match(prompt, /light cyan squares → shallow clear water over stone/);
  assert.match(prompt, /Warm atmospheric top-down lighting/);
  // overrides win
  const ice = buildLegendPrompt(g, m, { legend: { FL: "blue-white ice floor" } });
  assert.match(ice, /→ blue-white ice floor/);
});

test("buildLegendPrompt excludes dm-layer tokens and uses playerFallback in the key", () => {
  const m = loadManifest();
  const g = parseGrid("WL,DS\nFL,TR"); // DS (dm) hides as WL; TR (dm) hides as FL
  const prompt = buildLegendPrompt(g, m);
  assert.doesNotMatch(prompt, /secret/i);
  assert.doesNotMatch(prompt, /trap/i);
  assert.match(prompt, /dungeon walls/); // DS collapsed to WL
  assert.match(prompt, /flagstone floor/); // TR collapsed to FL
});
```

- [ ] **Step 2: Run to verify failure**

Run: `cd .claude/skills/prep-map/scripts && node --test test/legend.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../lib/legend.mjs").

- [ ] **Step 3: Write `lib/legend.mjs`**

```javascript
import { effectiveCode, resolveFragment } from "./manifest.mjs";

const STYLE_PREAMBLE =
  "Repaint this schematic top-down map as a premium hand-painted battlemap in the style of 2-Minute Tabletop: painterly, illustrated, stylized realism — NOT a photo.";
const STRUCTURE_LOCK =
  "Repaint each flat-colored region as its material, keeping every wall, door, and keyed region in EXACTLY the same position, size and shape — do not move, merge, add, or remove any structure:";
const LIGHTING =
  "Warm atmospheric top-down lighting: soft orange glow pools around the light sources, ambient shadow elsewhere. Strictly orthographic top-down — no perspective, no long cast shadows. Within floor areas add subtle period-appropriate wear and clutter. Dark marbled-stone texture in the surrounding void. No grid lines, no labels.";

/**
 * Build the img2img legend prompt for a grid.
 * dm-layer tokens collapse to their playerFallback (the base key hides them), so only
 * beautified materials appear. `opts.legend` overrides fragments; `opts.stylePreamble`
 * overrides the house-style line (Phase B injects art-style.md here).
 */
export function buildLegendPrompt(grid, manifest, opts = {}) {
  const { legend = {}, stylePreamble = STYLE_PREAMBLE } = opts;
  const present = new Set();
  for (const row of grid.cells) {
    for (const raw of row) {
      const code = effectiveCode(manifest, raw);
      if (code) present.add(code);
    }
  }
  const lines = [];
  for (const code of [...present].sort()) {
    const e = manifest[code];
    if (!e || e.layer === "dm") continue;
    const frag = resolveFragment(manifest, code, legend);
    if (!frag) continue;
    lines.push(`• ${e.colorName} → ${frag}`);
  }
  return [stylePreamble, STRUCTURE_LOCK, ...lines, LIGHTING].join("\n");
}
```

- [ ] **Step 4: Run to verify passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/legend.test.mjs; cd -`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/prep-map/scripts/lib/legend.mjs .claude/skills/prep-map/scripts/test/legend.test.mjs
git commit -m "feat(prep-map): auto-generated color→material legend prompt"
```

---

## Task 7: Render — SVG build + sharp rasterization

**Files:**
- Create: `.claude/skills/prep-map/tokens/svg/{door,door-locked,column,chest,trap,entrance}.svg`
- Create: `.claude/skills/prep-map/scripts/lib/render.mjs`
- Test: `.claude/skills/prep-map/scripts/test/render.test.mjs`

Glyph SVGs here are **functional silhouettes** in a `0 0 100 100` viewBox (dark shape on the token's fill color). Artistic quality is refined in Phase B against the §2.1 bar — Phase A only needs them to rasterize and to sit in the right cell.

- [ ] **Step 1: Create the six glyph SVGs**

`tokens/svg/door.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="24" y="14" width="52" height="72" rx="4" fill="#160d10" stroke="#000" stroke-width="3"/><circle cx="64" cy="50" r="5" fill="#000"/></svg>
```
`tokens/svg/door-locked.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="24" y="14" width="52" height="72" rx="4" fill="#160d10" stroke="#000" stroke-width="3"/><rect x="42" y="44" width="16" height="14" rx="2" fill="#000"/><rect x="46" y="36" width="8" height="12" fill="none" stroke="#000" stroke-width="3"/></svg>
```
`tokens/svg/column.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="30" fill="#160d10" stroke="#000" stroke-width="4"/></svg>
```
`tokens/svg/chest.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="20" y="40" width="60" height="36" rx="3" fill="#160d10" stroke="#000" stroke-width="3"/><rect x="20" y="40" width="60" height="13" fill="#000"/><rect x="46" y="52" width="8" height="10" fill="#000"/></svg>
```
`tokens/svg/trap.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="50,18 84,80 16,80" fill="none" stroke="#000" stroke-width="6"/><line x1="50" y1="38" x2="50" y2="62" stroke="#000" stroke-width="7"/><circle cx="50" cy="72" r="4" fill="#000"/></svg>
```
`tokens/svg/entrance.svg`:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="28,26 74,50 28,74" fill="#000"/></svg>
```

- [ ] **Step 2: Write the failing test**

`scripts/test/render.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";
import { parseGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";
import { renderLayers } from "../lib/render.mjs";

const TILE = 16; // tiny ppi keeps tests fast

// read the RGBA byte at the center of tile (cx,cy)
async function centerPixel(buf, cx, cy, tile = TILE) {
  const { data, info } = await sharp(buf).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const x = cx * tile + Math.floor(tile / 2);
  const y = cy * tile + Math.floor(tile / 2);
  const i = (y * info.width + x) * info.channels;
  return [data[i], data[i + 1], data[i + 2], data[i + 3]];
}
const hex = ([r, g, b]) => "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");

test("base layer has exact dimensions and the wall color at a wall-cell center", async () => {
  const m = loadManifest();
  const g = parseGrid("WL,FL\nFL,WS"); // 2x2
  const { base } = await renderLayers(g, m, TILE);
  const meta = await sharp(base).metadata();
  assert.equal(meta.width, 2 * TILE);
  assert.equal(meta.height, 2 * TILE);
  assert.equal(hex(await centerPixel(base, 0, 0)), "#2f3b45"); // WL
  assert.equal(hex(await centerPixel(base, 1, 1)), "#4aa3c7"); // WS
});

test("dm token renders its playerFallback color in the base layer (TR -> floor)", async () => {
  const m = loadManifest();
  const g = parseGrid("FL,TR\nFL,FL");
  const { base } = await renderLayers(g, m, TILE);
  assert.equal(hex(await centerPixel(base, 1, 0)), "#9a948a"); // FL, not the trap red
});

test("grid layer is transparent in cell interiors and opaque on a gridline", async () => {
  const m = loadManifest();
  const g = parseGrid("FL,FL\nFL,FL");
  const { grid } = await renderLayers(g, m, TILE);
  const interior = await centerPixel(grid, 0, 0); // middle of a cell → transparent
  assert.equal(interior[3], 0);
  // sample exactly on the vertical line x = TILE
  const { data, info } = await sharp(grid).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const px = (x, y) => data[(y * info.width + x) * info.channels + 3]; // alpha
  assert.ok(px(TILE, Math.floor(TILE / 2)) > 0, "gridline should be drawn");
});

test("dm layer is empty when there are no dm tokens, present when there are", async () => {
  const m = loadManifest();
  const none = await renderLayers(parseGrid("FL,FL\nFL,FL"), m, TILE);
  const { data } = await sharp(none.dm).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  assert.ok(data.every((_, i) => (i % 4 === 3 ? data[i] === 0 : true)), "all alpha 0 (empty)");
  const some = await renderLayers(parseGrid("FL,TR\nFL,FL"), m, TILE);
  const { data: d2, info } = await sharp(some.dm).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let anyOpaque = false;
  for (let i = 3; i < d2.length; i += 4) if (d2[i] > 0) anyOpaque = true;
  assert.ok(anyOpaque, "dm marker drawn");
  assert.equal(info.width, 2 * TILE);
});
```

- [ ] **Step 3: Run to verify failure**

Run: `cd .claude/skills/prep-map/scripts && node --test test/render.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../lib/render.mjs").

- [ ] **Step 4: Write `lib/render.mjs`**

```javascript
import sharp from "sharp";
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";
import { effectiveCode } from "./manifest.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const SVG_DIR = resolve(HERE, "../../tokens/svg");
const VOID_COLOR = "#0c0c10";
const DM_TINT = "#ff2bd6";

function loadGlyphInner(file) {
  const p = join(SVG_DIR, file);
  if (!existsSync(p)) return "";
  return readFileSync(p, "utf8")
    .replace(/<\?xml.*?\?>/s, "")
    .replace(/<svg[^>]*>/, "")
    .replace(/<\/svg>\s*$/, "")
    .trim();
}

function placeGlyph(file, x, y, tile, extraAttrs = "") {
  const inner = loadGlyphInner(file);
  if (!inner) return "";
  return `<svg x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet"${extraAttrs}>${inner}</svg>`;
}

/** SVG of the base segmentation key (flat token colors + object glyphs), dm tokens collapsed. */
export function buildBaseSvg(grid, manifest, tile) {
  const W = grid.width * tile, H = grid.height * tile;
  const fills = [];
  const glyphs = [];
  for (let y = 0; y < grid.height; y++) {
    for (let x = 0; x < grid.width; x++) {
      const code = effectiveCode(manifest, grid.cells[y][x]);
      if (!code) continue;
      const e = manifest[code];
      if (!e) continue;
      fills.push(`<rect x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" fill="${e.color}"/>`);
      if (e.glyph) glyphs.push(placeGlyph(e.glyph, x, y, tile));
    }
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="${VOID_COLOR}"/>${fills.join("")}${glyphs.join("")}</svg>`;
}

/** SVG of the grid overlay — subtle low-opacity dark lines (transparent elsewhere). */
export function buildGridSvg(grid, tile, { stroke = "#15151b", opacity = 0.55, weight = 2 } = {}) {
  const W = grid.width * tile, H = grid.height * tile;
  const lines = [];
  for (let x = 0; x <= grid.width; x++) lines.push(`<line x1="${x * tile}" y1="0" x2="${x * tile}" y2="${H}"/>`);
  for (let y = 0; y <= grid.height; y++) lines.push(`<line x1="0" y1="${y * tile}" x2="${W}" y2="${y * tile}"/>`);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><g stroke="${stroke}" stroke-opacity="${opacity}" stroke-width="${weight}">${lines.join("")}</g></svg>`;
}

/** SVG of the DM annotation overlay — tinted highlight + glyph for each dm-layer cell. */
export function buildDmSvg(grid, manifest, tile) {
  const W = grid.width * tile, H = grid.height * tile;
  const marks = [];
  for (let y = 0; y < grid.height; y++) {
    for (let x = 0; x < grid.width; x++) {
      const code = grid.cells[y][x];
      if (!code) continue;
      const e = manifest[code];
      if (!e || e.layer !== "dm") continue;
      marks.push(`<rect x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" fill="${DM_TINT}" fill-opacity="0.3"/>`);
      if (e.glyph) marks.push(placeGlyph(e.glyph, x, y, tile));
    }
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${marks.join("")}</svg>`;
}

// ctx7: /lovell/sharp — sharp(Buffer<svg>).resize(w,h,{fit:fill}).png() rasterizes SVG to exact px.
async function rasterize(svg, W, H) {
  return sharp(Buffer.from(svg)).resize(W, H, { fit: "fill" }).png().toBuffer();
}

/** Render the three deterministic layers as PNG buffers. */
export async function renderLayers(grid, manifest, tile = 300, gridStyle = {}) {
  const W = grid.width * tile, H = grid.height * tile;
  const [base, gridL, dm] = await Promise.all([
    rasterize(buildBaseSvg(grid, manifest, tile), W, H),
    rasterize(buildGridSvg(grid, tile, gridStyle), W, H),
    rasterize(buildDmSvg(grid, manifest, tile), W, H),
  ]);
  return { base, grid: gridL, dm };
}

// ctx7: /lovell/sharp — .composite([{input,top,left}]) overlays layers onto a base.
/** Flatten base + overlays into one PNG buffer (used by `render` for a no-beautify preview image). */
export async function compositePng(baseBuf, overlayBufs) {
  return sharp(baseBuf)
    .composite(overlayBufs.map((input) => ({ input, top: 0, left: 0 })))
    .png()
    .toBuffer();
}
```

- [ ] **Step 5: Run to verify passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/render.test.mjs; cd -`
Expected: PASS (4 tests). If a glyph nesting issue makes the base test fail on dimensions, confirm each glyph file starts with `<svg ... viewBox="0 0 100 100">` and the regex stripped the outer tag.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/prep-map/tokens/svg .claude/skills/prep-map/scripts/lib/render.mjs .claude/skills/prep-map/scripts/test/render.test.mjs
git commit -m "feat(prep-map): SVG base/grid/dm render + sharp rasterization"
```

---

## Task 8: CLI (`preview` + `render`)

**Files:**
- Create: `.claude/skills/prep-map/scripts/map.mjs`
- Test: `.claude/skills/prep-map/scripts/test/cli.test.mjs`

- [ ] **Step 1: Write the failing test**

`scripts/test/cli.test.mjs`:
```javascript
import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import sharp from "sharp";

const CLI = new URL("../map.mjs", import.meta.url).pathname;
const FIX = new URL("./fixtures/guard-room.csv", import.meta.url).pathname;
const run = (args) => execFileSync("node", [CLI, ...args], { encoding: "utf8" });

test("preview prints the ASCII map and a valid line", () => {
  const out = run(["preview", FIX]);
  assert.match(out, /#{6}/);
  assert.match(out, /valid — 6x5 tiles/);
});

test("preview exits non-zero on an invalid map", () => {
  const dir = mkdtempSync(join(tmpdir(), "pm-"));
  const bad = join(dir, "bad.csv");
  writeFileSync(bad, "WL,ZZ\nFL,FL");
  assert.throws(() => run(["preview", bad]));
});

test("render writes base/grid/dm/flat PNGs + legend.txt at the right size", async () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  run(["render", FIX, "--ppi", "16", "--out", out]);
  for (const f of ["guard-room.base.png", "guard-room.grid.png", "guard-room.dm.png", "guard-room.flat.png", "guard-room.legend.txt"]) {
    assert.ok(existsSync(join(out, f)), `${f} written`);
  }
  const meta = await sharp(join(out, "guard-room.base.png")).metadata();
  assert.equal(meta.width, 96);
  assert.equal(meta.height, 80);
  assert.match(readFileSync(join(out, "guard-room.legend.txt"), "utf8"), /flagstone floor/);
});
```

- [ ] **Step 2: Run to verify failure**

Run: `cd .claude/skills/prep-map/scripts && node --test test/cli.test.mjs; cd -`
Expected: FAIL ("Cannot find module ../map.mjs").

- [ ] **Step 3: Write `scripts/map.mjs`**

```javascript
#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, join, basename } from "node:path";
import { loadManifest } from "./lib/manifest.mjs";
import { parseGrid, validateGrid, geometry, asciiPreview } from "./lib/grid.mjs";
import { buildLegendPrompt } from "./lib/legend.mjs";
import { renderLayers, compositePng } from "./lib/render.mjs";

function parseArgs(argv) {
  const out = { _: [], ppi: 300, out: ".", legend: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--ppi") out.ppi = Number(argv[++i]);
    else if (a === "--out") out.out = argv[++i];
    else if (a === "--legend") out.legend = argv[++i];
    else out._.push(a);
  }
  return out;
}

function loadLegendFile(path) {
  if (!path) return {};
  return JSON.parse(readFileSync(resolve(path), "utf8"));
}

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

const args = parseArgs(process.argv.slice(2));
const [cmd, csvPath] = args._;
if (!cmd || !csvPath) fail("usage: map.mjs <preview|render> <tiles.csv> [--ppi N] [--out dir] [--legend f]");

const manifest = loadManifest();
const grid = parseGrid(readFileSync(resolve(csvPath), "utf8"));
const legend = loadLegendFile(args.legend);
const report = validateGrid(grid, manifest, legend);

if (cmd === "preview") {
  console.log(asciiPreview(grid, manifest));
  console.log("");
  for (const w of report.warnings) console.log(`warning: ${w}`);
  for (const e of report.errors) console.log(`error:   ${e}`);
  console.log(report.ok ? `valid — ${grid.width}x${grid.height} tiles` : `INVALID — ${report.errors.length} error(s)`);
  process.exit(report.ok ? 0 : 1);
}

if (cmd === "render") {
  if (!report.ok) {
    for (const e of report.errors) console.error(`error: ${e}`);
    fail("refusing to render an invalid map");
  }
  const geo = geometry(grid, args.ppi);
  const { base, grid: gridL, dm } = await renderLayers(grid, manifest, geo.tilePx);
  const flat = await compositePng(base, [gridL]);
  const prompt = buildLegendPrompt(grid, manifest, { legend });

  mkdirSync(resolve(args.out), { recursive: true });
  const stem = basename(csvPath).replace(/\.csv$/i, "");
  const w = (suffix, buf) => writeFileSync(join(resolve(args.out), `${stem}.${suffix}`), buf);
  w("base.png", base);
  w("grid.png", gridL);
  w("dm.png", dm);
  w("flat.png", flat);
  w("legend.txt", prompt);

  console.log(`rendered ${stem} @ ${geo.widthPx}x${geo.heightPx}px (${args.ppi} ppi) → ${args.out}`);
  for (const wn of report.warnings) console.log(`warning: ${wn}`);
  process.exit(0);
}

fail(`unknown command: ${cmd}`);
```

- [ ] **Step 4: Run to verify passes**

Run: `cd .claude/skills/prep-map/scripts && node --test test/cli.test.mjs; cd -`
Expected: PASS (3 tests).

- [ ] **Step 5: Run the full suite**

Run: `cd .claude/skills/prep-map/scripts && npm test; cd -`
Expected: PASS — all suites (smoke, manifest, palette, grid, legend, render, cli).

- [ ] **Step 6: Eyeball the real output (manual sanity, optional)**

```bash
cd .claude/skills/prep-map/scripts && node map.mjs preview test/fixtures/guard-room.csv && node map.mjs render test/fixtures/guard-room.csv --ppi 64 --out /tmp/pm && cd -
```
Open `/tmp/pm/guard-room.flat.png` — expect a 384×320 schematic: dark slate walls, grey floor, a magenta column glyph, a purple chest glyph, a cyan water cell, a brick-red door on the south wall, with subtle grid lines.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/prep-map/scripts/map.mjs .claude/skills/prep-map/scripts/test/cli.test.mjs
git commit -m "feat(prep-map): map.mjs CLI — preview + render"
```

---

## Task 9: Expand to the full token set

**Files:**
- Modify: `.claude/skills/prep-map/tokens/tokens.json` (add the remaining spec §4.2 tokens)
- Create: `.claude/skills/prep-map/tokens/svg/*.svg` (one silhouette per new glyph token)
- Create: `.claude/skills/prep-map/references/token-library.md` (human catalog)

This is a **data** task — no new logic. The palette gate (Task 2) and render tests (Task 7) already protect it.

- [ ] **Step 1: Add the remaining tokens to `tokens.json`**

Add these entries (terrain/structure get distinct natural-material colors; features cluster in the magenta/purple band + glyph, per spec §4.3). Pick initial colors, then let the ΔE gate tune them:
```json
  "AR": { "name": "archway", "category": "structure", "color": "#6b5b73", "colorName": "muted violet-grey cells with an arch icon", "ascii": "'", "glyph": "archway.svg", "fragment": "an open stone archway", "layer": "both", "playerFallback": null },
  "SU": { "name": "stairs up", "category": "structure", "color": "#8a8f98", "colorName": "cool grey cells with up-stair lines", "ascii": "<", "glyph": "stairs-up.svg", "fragment": "stone stairs ascending", "layer": "both", "playerFallback": null },
  "SD": { "name": "stairs down", "category": "structure", "color": "#5a6068", "colorName": "darker grey cells with down-stair lines", "ascii": ">", "glyph": "stairs-down.svg", "fragment": "stone stairs descending", "layer": "both", "playerFallback": null },
  "RB": { "name": "rubble", "category": "terrain", "color": "#7d6f5a", "colorName": "speckled tan-brown squares", "ascii": "%", "glyph": null, "fragment": "broken rubble and debris (difficult terrain)", "layer": "both", "playerFallback": null },
  "LV": { "name": "lava", "category": "hazard", "color": "#e0631c", "colorName": "bright orange squares", "ascii": "L", "glyph": null, "fragment": "glowing molten lava", "layer": "both", "playerFallback": null },
  "CM": { "name": "chasm", "category": "hazard", "color": "#101418", "colorName": "near-black squares", "ascii": "X", "glyph": null, "fragment": "a bottomless dark chasm", "layer": "both", "playerFallback": null },
  "AL": { "name": "altar", "category": "feature", "color": "#9b59b6", "colorName": "lavender cells with an altar icon", "ascii": "A", "glyph": "altar.svg", "fragment": "a carved stone altar", "layer": "both", "playerFallback": null },
  "BR": { "name": "brazier", "category": "feature", "color": "#c0398e", "colorName": "pink-magenta cells with a flame icon", "ascii": "*", "glyph": "brazier.svg", "fragment": "a burning iron brazier casting warm light", "layer": "both", "playerFallback": null },
  "FP": { "name": "fireplace", "category": "feature", "color": "#a83275", "colorName": "deep pink cells with a fire icon", "ascii": "f", "glyph": "fireplace.svg", "fragment": "a stone fireplace with a burning fire", "layer": "both", "playerFallback": null },
  "TO": { "name": "torch", "category": "feature", "color": "#d14fa0", "colorName": "bright pink cells with a torch icon", "ascii": "i", "glyph": "torch.svg", "fragment": "a wall-mounted flaming torch", "layer": "both", "playerFallback": null },
  "TB": { "name": "table", "category": "feature", "color": "#8e5fa8", "colorName": "violet cells with a table icon", "ascii": "T", "glyph": "table.svg", "fragment": "a period-appropriate wooden table", "layer": "both", "playerFallback": null },
  "BE": { "name": "bed", "category": "feature", "color": "#7d5ba6", "colorName": "violet cells with a bed icon", "ascii": "b", "glyph": "bed.svg", "fragment": "a wooden bed with linens", "layer": "both", "playerFallback": null },
  "BL": { "name": "bookshelf", "category": "feature", "color": "#6f4a9c", "colorName": "deep violet cells with a shelf icon", "ascii": "B", "glyph": "bookshelf.svg", "fragment": "a tall wooden bookshelf", "layer": "both", "playerFallback": null },
  "BA": { "name": "barrel", "category": "feature", "color": "#a64ca6", "colorName": "purple cells with a barrel icon", "ascii": "0", "glyph": "barrel.svg", "fragment": "a wooden barrel", "layer": "both", "playerFallback": null },
  "CT": { "name": "crate", "category": "feature", "color": "#8a4a9e", "colorName": "purple cells with a crate icon", "ascii": "c", "glyph": "crate.svg", "fragment": "stacked wooden crates", "layer": "both", "playerFallback": null },
  "WR": { "name": "weapon rack", "category": "feature", "color": "#9d4e8c", "colorName": "mauve cells with a rack icon", "ascii": "r", "glyph": "weapon-rack.svg", "fragment": "a wooden weapon rack", "layer": "both", "playerFallback": null },
  "ST": { "name": "statue", "category": "feature", "color": "#7a6f9e", "colorName": "slate-violet cells with a statue icon", "ascii": "I", "glyph": "statue.svg", "fragment": "a carved stone statue", "layer": "both", "playerFallback": null },
  "RG": { "name": "rug", "category": "feature", "color": "#b5559e", "colorName": "rose cells", "ascii": "_", "glyph": null, "fragment": "a patterned woven rug on the floor", "layer": "both", "playerFallback": null }
```

- [ ] **Step 2: Run the palette gate; tune until green**

Run: `cd .claude/skills/prep-map/scripts && node --test test/palette.test.mjs; cd -`
Expected: PASS. If violations are reported, the feature-band colors are too close to each other *and* to a terrain/structure color — adjust the flagged `color` values (the gate treats feature↔feature loosely at ΔE 10 but feature↔terrain strictly at ΔE 20). Iterate to green. Do not weaken thresholds.

- [ ] **Step 3: Create one `0 0 100 100` silhouette SVG per new glyph token**

Create these files in `tokens/svg/` following the exact pattern from Task 7 (dark `#160d10`/`#000` shape, `viewBox="0 0 100 100"`, no XML prolog), each a recognizable silhouette of its object: `archway.svg` (arch outline), `stairs-up.svg` (≡ with up chevron), `stairs-down.svg` (≡ with down chevron), `altar.svg` (pedestal block), `brazier.svg` (bowl + flame), `fireplace.svg` (hearth arch + flame), `torch.svg` (stick + flame), `table.svg` (rectangle + legs), `bed.svg` (rectangle + pillow band), `bookshelf.svg` (rectangle + shelf lines), `barrel.svg` (cask oval), `crate.svg` (square + X), `weapon-rack.svg` (vertical bar + 2 diagonals), `statue.svg` (standing figure). These are functional placeholders — Phase B refines glyph art (or regenerates via `recraft-svg`) against the §2.1 bar.

- [ ] **Step 4: Verify render still works with the full set**

Run: `cd .claude/skills/prep-map/scripts && npm test; cd -`
Expected: PASS (all suites). Then a visual spot-check:
```bash
cd .claude/skills/prep-map/scripts && printf 'WL,WL,WL,WL\nWL,TB,BE,WL\nWL,BR,FP,WL\nWL,WL,DR,WL\n' > /tmp/parlor.csv && node map.mjs render /tmp/parlor.csv --ppi 64 --out /tmp/pm; cd -
```
Open `/tmp/pm/parlor.flat.png` — every furniture/light glyph should render in its cell.

- [ ] **Step 5: Write the human catalog `references/token-library.md`**

Create `.claude/skills/prep-map/references/token-library.md` with a table: Code | Name | Category | ASCII | Color | Layer | Fragment — generated from `tokens.json` (one row per token). Include a short header explaining the four-consumer model (agent code / renderer color / renderer glyph / img2img fragment) and the dm-layer/playerFallback behavior.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/prep-map/tokens .claude/skills/prep-map/references/token-library.md
git commit -m "feat(prep-map): full token set + glyph library + catalog"
```

---

## Self-Review

**Spec coverage (Phase A scope):**
- §4.1 manifest schema → Task 1 (`loadManifest` validates required fields, category, color, layer, dm/playerFallback).
- §4.2 token set → Task 1 (core 12) + Task 9 (full set).
- §4.3 palette separation + ΔE test → Task 2; the terrain-strict / feature-loose weighting is implemented and tested.
- §4.4 glyph rules → Task 7 (glyphs replace icon; functional silhouettes; refinement deferred to Phase B — noted).
- §4.5 generic primitives & per-map legend overrides → `resolveFragment`/`buildLegendPrompt` honor a `--legend` override file (Task 1/6/8). Reserved `P1…P6` primitive tokens are **not** in the core/full data sets here — add them when Phase B needs them (the loader already accepts category `primitive`). Flagged as a deliberate scope edge, not a silent gap.
- §4.6 DM/player split → `effectiveCode` + `buildDmSvg`; base key hides dm tokens via playerFallback (Tasks 1, 7).
- §5 CSV authoring → Tasks 3 (parse), 4 (validate), 5 (geometry + ASCII preview), 8 (`preview` CLI).
- §6 renderer & geometry → Tasks 5, 7 (base/grid/dm layers; exact px dims; subtle configurable grid).
- §6.2 output #4 "auto-generated legend prompt" → Task 6, emitted by `render` (Task 8).
- §9 `preview`/`render` CLI + storage → Task 8 (PNG masters; `wiki/assets/maps/` wiring lands with the SKILL in Phase D).

**Deliberately deferred (documented, not dropped):**
- **Reachability validation** (spec §5.1 "unreachable regions") — more complex flood-fill; add as a follow-up validation task. `validateGrid`'s shape (`warnings[]`) already accommodates it.
- **`auto-wall` helper** (spec §5.1) — ergonomic, not on the render critical path; add as a small follow-up to `grid.mjs`.
- **Beautify, compose, SKILL.md** — Phases B/C/D, separate plans.

**Placeholder scan:** No "TBD"/"add error handling"-style placeholders. Task 9 Step 3/Step 5 describe asset/doc creation (genuinely data/art, not logic) with the exact pattern, viewBox convention, and field list to follow — not "similar to Task N."

**Type/name consistency:** `parseGrid → {width,height,cells}`, `validateGrid → {ok,errors,warnings}`, `geometry → {ppi,tilePx,widthPx,heightPx}`, `renderLayers → {base,grid,dm}`, `effectiveCode`/`resolveFragment`/`buildLegendPrompt`/`compositePng` signatures match across tasks and tests. `glyph` field is always an SVG filename or `null`. `layer` is `"both"|"dm"`; dm tokens always carry `playerFallback`.

**Worktree note:** every commit step relies on the one-time `export GIT_WORK_TREE="$(pwd)"` at the top.
