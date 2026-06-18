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

import { validateGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";

test("validateGrid passes a well-formed room (incl. an exterior door)", () => {
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

test("validateGrid flags a floating door (no passable neighbor)", () => {
  const m = loadManifest();
  const g = parseGrid("WL,WL,WL\nWL,DR,WL\nWL,WL,WL");
  const r = validateGrid(g, m);
  assert.equal(r.ok, false);
  assert.match(r.errors.join("\n"), /floating door/);
});

test("validateGrid accepts a door between two passable cells", () => {
  const m = loadManifest();
  const g = parseGrid("WL,FL,WL\nWL,DR,WL\nWL,FL,WL");
  const r = validateGrid(g, m);
  assert.equal(r.ok, true, JSON.stringify(r.errors));
});

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
