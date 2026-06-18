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
  assert.equal(hex(await centerPixel(base, 0, 0)), "#2a2723"); // WL
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
