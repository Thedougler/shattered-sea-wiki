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

function placeGlyph(file, x, y, tile) {
  const inner = loadGlyphInner(file);
  if (!inner) return "";
  return `<svg x="${x * tile}" y="${y * tile}" width="${tile}" height="${tile}" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">${inner}</svg>`;
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
