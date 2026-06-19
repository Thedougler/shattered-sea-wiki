import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";
import { parseGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";
import { renderLayers } from "../lib/render.mjs";

const TILE = 64; // big enough that label/outline don't crowd the sampled pixels

// read the RGBA byte at the center of tile (cx,cy)
async function centerPixel(buf, cx, cy, tile = TILE) {
  const { data, info } = await sharp(buf).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const x = cx * tile + Math.floor(tile / 2);
  const y = cy * tile + Math.floor(tile / 2);
  const i = (y * info.width + x) * info.channels;
  return [data[i], data[i + 1], data[i + 2], data[i + 3]];
}
const hex = ([r, g, b]) => "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");

// is a color ~(r,g,b) present anywhere inside tile (cx,cy)? (used to detect outline/label color)
async function cellHasColor(buf, cx, cy, pred, tile = TILE) {
  const { data, info } = await sharp(buf).raw().toBuffer({ resolveWithObject: true });
  for (let y = cy * tile; y < (cy + 1) * tile; y++) {
    for (let x = cx * tile; x < (cx + 1) * tile; x++) {
      const i = (y * info.width + x) * info.channels;
      if (pred(data[i], data[i + 1], data[i + 2])) return true;
    }
  }
  return false;
}

test("only wall and floor flood-fill; terrain is drawn as an outline on floor", async () => {
  const m = loadManifest();
  const g = parseGrid("WL,FL\nFL,WS"); // 2x2
  const { base } = await renderLayers(g, m, TILE);
  const meta = await sharp(base).metadata();
  assert.equal(meta.width, 2 * TILE);
  assert.equal(meta.height, 2 * TILE);
  assert.equal(hex(await centerPixel(base, 0, 0)), "#3a3a3a"); // WL → dark wall fill
  assert.equal(hex(await centerPixel(base, 1, 0)), "#d8d2c4"); // FL → light floor fill
  // WS is no longer a solid blue fill — it's a cyan (deepskyblue ~0,191,255) outline on floor
  const cyan = (r, gg, b) => r < 70 && gg > 150 && b > 200;
  assert.ok(await cellHasColor(base, 1, 1, cyan), "shallow water drawn as a cyan outline");
});

test("a non-surface token (TR) rests on floor with a colored outline, not a solid fill", async () => {
  const m = loadManifest();
  const g = parseGrid("FL,TR\nFL,FL");
  const { base } = await renderLayers(g, m, TILE);
  // floor (~#d8d2c4) shows under the trap (sampling presence dodges the centered label)
  const floorP = (r, gg, b) => r > 200 && r < 230 && gg > 195 && gg < 225 && b > 175 && b < 215;
  assert.ok(await cellHasColor(base, 1, 0, floorP), "floor shows under the trap");
  const yellow = (r, gg, b) => r > 200 && gg > 200 && b < 90;
  assert.ok(await cellHasColor(base, 1, 0, yellow), "trap drawn as a yellow outline");
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
