import sharp from "sharp";
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";
import { isObjectToken } from "./manifest.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const SVG_DIR = resolve(HERE, "../../tokens/svg");
const VOID_COLOR = "#0c0c10";
const DM_TINT = "#ff2bd6";

// Simple, obvious colors — the graphic is a "replace the contents of the <color> area" guide, so
// the model is prompted by plain color names, never hex. Big surfaces flood-fill; objects sit on a
// floor tile inside a colored OUTLINE + text label, so the model improvises the real thing in place.
const FLOOR = "#d8d2c4"; // light grey
const WALL = "#3a3a3a"; // dark grey
function fillColor(e) {
  if (e.name === "wall") return WALL; // only the two base surfaces flood-fill
  return FLOOR; // floor, terrain variations, doors and objects all rest on a floor tile
}
// Outline color by role/terrain — plain CSS color names the prompt can reference directly.
// Terrain areas get a water/earth color; the LABEL ("DEEP WATER", "LAVA") disambiguates same hues.
const TERRAIN_COLOR = {
  "wood floor": "peru",
  "shallow water": "deepskyblue",
  "deep water": "royalblue",
  rubble: "sienna",
  lava: "orangered",
  chasm: "blueviolet",
};
function outlineColor(e) {
  if (/door/.test(e.name)) return "orange";
  if (e.category === "hazard") return "yellow";
  if (e.category === "marker") return "magenta";
  if (e.category === "terrain") return TERRAIN_COLOR[e.name] ?? "deepskyblue";
  return "limegreen"; // furniture / props / stairs / features
}

/** Connected same-token feature regions (4-connectivity) → one label per region. */
function featureRegions(grid, manifest) {
  const seen = Array.from({ length: grid.height }, () => Array(grid.width).fill(false));
  const isFeat = (code) => isObjectToken(manifest[code]);
  const out = [];
  for (let y = 0; y < grid.height; y++) {
    for (let x = 0; x < grid.width; x++) {
      const code = grid.cells[y][x];
      if (seen[y][x] || !isFeat(code)) continue;
      const cells = [];
      const stack = [[x, y]];
      seen[y][x] = true;
      while (stack.length) {
        const [cx, cy] = stack.pop();
        cells.push([cx, cy]);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx < 0 || ny < 0 || nx >= grid.width || ny >= grid.height || seen[ny][nx]) continue;
          if (grid.cells[ny][nx] === code) {
            seen[ny][nx] = true;
            stack.push([nx, ny]);
          }
        }
      }
      out.push({ code, cells });
    }
  }
  return out;
}

/** SVG <g> tracing the outer perimeter of a connected region, inset slightly inward. */
function regionOutline(cells, tile, color, sw) {
  const set = new Set(cells.map(([x, y]) => `${x},${y}`));
  const inn = sw / 2;
  const seg = [];
  for (const [x, y] of cells) {
    const L = x * tile, R = (x + 1) * tile, T = y * tile, B = (y + 1) * tile;
    if (!set.has(`${x},${y - 1}`)) seg.push([L, T + inn, R, T + inn]); // top edge → nudge inward
    if (!set.has(`${x},${y + 1}`)) seg.push([L, B - inn, R, B - inn]); // bottom
    if (!set.has(`${x - 1},${y}`)) seg.push([L + inn, T, L + inn, B]); // left
    if (!set.has(`${x + 1},${y}`)) seg.push([R - inn, T, R - inn, B]); // right
  }
  const lines = seg.map(([x1, y1, x2, y2]) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/>`).join("");
  return `<g fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="square">${lines}</g>`;
}

function loadGlyphInner(file) {
  const p = join(SVG_DIR, file);
  if (!existsSync(p)) return "";
  return readFileSync(p, "utf8")
    .replace(/<\?xml.*?\?>/s, "")
    .replace(/<svg[^>]*>/, "")
    .replace(/<\/svg>\s*$/, "")
    .trim();
}

function placeGlyph(file, x, y, tile) {
  const inner = loadGlyphInner(file);
  if (!inner) return "";
  return `<svg x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">${inner}</svg>`;
}

/** SVG guide: surfaces flood-filled in simple colors; feature regions outlined + labelled. */
export function buildBaseSvg(grid, manifest, tile) {
  const W = grid.width * tile, H = grid.height * tile;
  const fills = [];
  const outlines = [];
  for (let y = 0; y < grid.height; y++) {
    for (let x = 0; x < grid.width; x++) {
      const code = grid.cells[y][x];
      if (!code) continue;
      const e = manifest[code];
      if (!e) continue;
      fills.push(`<rect x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" fill="${fillColor(e)}"/>`);
    }
  }
  // One contiguous perimeter outline + one bold label per connected region, in its role color.
  const labels = [];
  for (const r of featureRegions(grid, manifest)) {
    const e = manifest[r.code];
    const col = outlineColor(e);
    const sw = Math.max(2, tile * 0.05);
    outlines.push(regionOutline(r.cells, tile, col, sw));
    const cx = (r.cells.reduce((s, c) => s + c[0], 0) / r.cells.length + 0.5) * tile;
    const cy = (r.cells.reduce((s, c) => s + c[1], 0) / r.cells.length + 0.5) * tile;
    const fs = Math.max(11, tile * 0.2);
    labels.push(
      `<text x="${cx}" y="${cy}" font-family="Helvetica, Arial, sans-serif" font-weight="bold" font-size="${fs}" fill="${col}" stroke="#000" stroke-width="${fs * 0.08}" paint-order="stroke" text-anchor="middle" dominant-baseline="central">${e.name.toUpperCase()}</text>`,
    );
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="${VOID_COLOR}"/>${fills.join("")}${outlines.join("")}${labels.join("")}</svg>`;
}

/** SVG of the grid overlay — subtle low-opacity dark lines (transparent elsewhere). */
export function buildGridSvg(grid, tile, { stroke = "#15151b", opacity = 0.55, weight = 2 } = {}) {
  const W = grid.width * tile, H = grid.height * tile;
  const h = weight / 2;
  // Inset the outermost lines by half the stroke width so the full border stays on-canvas;
  // a centered stroke at x=0 or x=W would clip to half thickness (asymmetric border).
  const cx = (x) => (x === 0 ? h : x === grid.width ? W - h : x * tile);
  const cy = (y) => (y === 0 ? h : y === grid.height ? H - h : y * tile);
  const lines = [];
  for (let x = 0; x <= grid.width; x++) lines.push(`<line x1="${cx(x)}" y1="0" x2="${cx(x)}" y2="${H}"/>`);
  for (let y = 0; y <= grid.height; y++) lines.push(`<line x1="0" y1="${cy(y)}" x2="${W}" y2="${cy(y)}"/>`);
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

// ctx7: /lovell/sharp — .resize(w,h,{fit:fill}) forces exact dims (no aspect preservation).
/** Force any image buffer to exact pixel dimensions (img2img returns arbitrary sizes). */
export async function resizeTo(buf, W, H) {
  return sharp(buf).resize(W, H, { fit: "fill" }).png().toBuffer();
}

/**
 * Finish a beautified base image into the two table-ready outputs: normalize it to the
 * grid's exact pixel size, then composite the crisp vector grid (player) and grid + DM
 * annotation overlay (dm) on top. This is how the perfect grid lands last, by construction.
 */
export async function finishMap(beautifiedBuf, grid, manifest, tile = 300, gridStyle = {}) {
  const W = grid.width * tile;
  const H = grid.height * tile;
  const base = await resizeTo(beautifiedBuf, W, H);
  const gridL = await rasterize(buildGridSvg(grid, tile, gridStyle), W, H);
  const dm = await rasterize(buildDmSvg(grid, manifest, tile), W, H);
  const [player, dmMap] = await Promise.all([
    compositePng(base, [gridL]),
    compositePng(base, [gridL, dm]),
  ]);
  return { player, dm: dmMap };
}
