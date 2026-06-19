import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";
import { normalizeScene } from "../lib/scene.mjs";
import { renderSceneLayers } from "../lib/render.mjs";

test("normalizeScene accepts a legend+grid and rejects malformed scenes", () => {
  const ok = normalizeScene({ grid: ["##", "#."], legend: { "#": { fill: "dimgray" }, ".": { fill: "#ccc" } } });
  assert.equal(ok.grid.width, 2);
  assert.equal(ok.grid.height, 2);
  assert.equal(ok.grid.cells[1][1], ".");
  assert.equal(ok.grid.cells[0][0], "#");
  assert.throws(() => normalizeScene({ grid: ["#"], legend: { "#": {} } }), /fill.*or.*outline/i);
  assert.throws(() => normalizeScene({ grid: ["#X"], legend: { "#": { fill: "black" } } }), /not in the legend/i);
  assert.throws(() => normalizeScene({ grid: ["#"], legend: { "#": { outline: "red" } } }), /label/i);
});

test("buildSceneSvg flood-fills surfaces and outlines regions in the agent's colors", async () => {
  const scene = normalizeScene({
    grid: ["##", "~."],
    legend: { "#": { fill: "#202020" }, ".": { fill: "#d8d2c4" }, "~": { outline: "deepskyblue", label: "WATER" } },
  });
  const TILE = 64;
  const { base } = await renderSceneLayers(scene.grid, scene.legend, TILE);
  const { data, info } = await sharp(base).raw().toBuffer({ resolveWithObject: true });
  const at = (x, y) => {
    const i = (y * info.width + x) * info.channels;
    return [data[i], data[i + 1], data[i + 2]];
  };
  // wall fill (#202020) at cell (0,0) center
  const [wr, wg, wb] = at(TILE / 2, TILE / 2);
  assert.ok(wr < 50 && wg < 50 && wb < 50, "wall flood-filled dark");
  // water region (0,1) sits on the floor bg and carries a cyan (deepskyblue) outline in-cell
  let cyan = false;
  for (let y = TILE; y < 2 * TILE; y++) {
    for (let x = 0; x < TILE; x++) {
      const [r, g, b] = at(x, y);
      if (r < 70 && g > 150 && b > 200) cyan = true;
    }
  }
  assert.ok(cyan, "water region drawn as a cyan outline on floor, not a solid fill");
});
