import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";
import { parseGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";
import { finishMap } from "../lib/render.mjs";

const TILE = 16;

// a solid-color "beautified" image at a deliberately wrong size — finishMap must normalize it.
const solid = (w, h, rgb) =>
  sharp({ create: { width: w, height: h, channels: 3, background: rgb } }).png().toBuffer();

async function centerAlphaRGB(buf, cx, cy, tile = TILE) {
  const { data, info } = await sharp(buf).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const x = cx * tile + Math.floor(tile / 2);
  const y = cy * tile + Math.floor(tile / 2);
  const i = (y * info.width + x) * info.channels;
  return [data[i], data[i + 1], data[i + 2], data[i + 3]];
}

test("finishMap normalizes the beautified image to exact grid px and shows it through cell interiors", async () => {
  const m = loadManifest();
  const g = parseGrid("FL,FL\nFL,FL"); // 2x2
  const beautified = await solid(5, 7, { r: 0, g: 255, b: 0 }); // wrong size on purpose
  const { player } = await finishMap(beautified, g, m, TILE);

  const meta = await sharp(player).metadata();
  assert.equal(meta.width, 2 * TILE);
  assert.equal(meta.height, 2 * TILE);
  const [r, gg, b, a] = await centerAlphaRGB(player, 0, 0); // interior of a cell
  assert.equal(a, 255);
  assert.ok(gg > 200 && r < 60 && b < 60, "beautified green shows through cell interior");
});

test("DM markers appear on the dm copy only, never on the player copy", async () => {
  const m = loadManifest();
  const g = parseGrid("FL,TR\nFL,FL"); // a trap in cell (1,0)
  const beautified = await solid(8, 8, { r: 0, g: 255, b: 0 });
  const { player, dm } = await finishMap(beautified, g, m, TILE);

  const playerCell = await centerAlphaRGB(player, 1, 0); // still beautified green — trap hidden
  assert.ok(playerCell[1] > 200 && playerCell[0] < 80, "player copy hides the trap");

  const dmCell = await centerAlphaRGB(dm, 1, 0); // DM tint over the trap cell — not plain green
  assert.ok(!(dmCell[1] > 200 && dmCell[0] < 80), "dm copy marks the trap");
});
