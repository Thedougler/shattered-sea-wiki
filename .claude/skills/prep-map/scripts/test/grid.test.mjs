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
