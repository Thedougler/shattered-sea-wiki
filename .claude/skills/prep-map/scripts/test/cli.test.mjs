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

test("render writes base/grid/dm-overlay/flat PNGs at the right size", async () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  run(["render", FIX, "--ppi", "16", "--out", out]);
  for (const f of ["guard-room.base.png", "guard-room.grid.png", "guard-room.dm-overlay.png", "guard-room.flat.png"]) {
    assert.ok(existsSync(join(out, f)), `${f} written`);
  }
  const meta = await sharp(join(out, "guard-room.base.png")).metadata();
  assert.equal(meta.width, 96);
  assert.equal(meta.height, 80);
});

test("composite finishes a beautified base into player.png + dm.png at the target size", async () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  run(["render", FIX, "--ppi", "16", "--out", out]); // base.png stands in for the beautified art
  run(["composite", join(out, "guard-room.base.png"), FIX, "--ppi", "16", "--out", out]);
  for (const f of ["guard-room.player.png", "guard-room.dm.png"]) {
    assert.ok(existsSync(join(out, f)), `${f} written`);
  }
  const meta = await sharp(join(out, "guard-room.player.png")).metadata();
  assert.equal(meta.width, 96);
  assert.equal(meta.height, 80);
});

test("compose assembles a 2-room dungeon and renders the master grid under its name", async () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  writeFileSync(join(out, "a.csv"), "WL,WL\nWL,FL");
  writeFileSync(join(out, "b.csv"), "FL,WL\nWL,WL");
  writeFileSync(
    join(out, "dungeon.json"),
    JSON.stringify({
      name: "lair",
      rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 3, y: 0 }],
      corridors: [{ from: [1, 1], to: [3, 1], token: "FL" }],
    }),
  );
  run(["compose", join(out, "dungeon.json"), "--ppi", "16", "--out", out]);
  assert.ok(existsSync(join(out, "lair.base.png")), "master base written under spec name");
  const meta = await sharp(join(out, "lair.base.png")).metadata();
  assert.equal(meta.width, 5 * 16); // room b right edge at x=4 → 5 cols wide
  assert.equal(meta.height, 2 * 16);
});

test("composite accepts a dungeon.json and finishes the assembled master", async () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  writeFileSync(join(out, "a.csv"), "WL,WL\nWL,FL");
  writeFileSync(join(out, "b.csv"), "FL,WL\nWL,WL");
  writeFileSync(
    join(out, "dungeon.json"),
    JSON.stringify({ name: "lair", rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 3, y: 0 }] }),
  );
  run(["compose", join(out, "dungeon.json"), "--ppi", "16", "--out", out]);
  run(["composite", join(out, "lair.base.png"), join(out, "dungeon.json"), "--ppi", "16", "--out", out]);
  assert.ok(existsSync(join(out, "lair.player.png")), "dungeon player map finished");
  const meta = await sharp(join(out, "lair.player.png")).metadata();
  assert.equal(meta.width, 5 * 16);
});

test("compose refuses a dungeon with colliding rooms", () => {
  const out = mkdtempSync(join(tmpdir(), "pm-"));
  writeFileSync(join(out, "a.csv"), "FL,FL");
  writeFileSync(join(out, "b.csv"), "WL,WL");
  writeFileSync(
    join(out, "bad.json"),
    JSON.stringify({ rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 1, y: 0 }] }),
  );
  assert.throws(() => run(["compose", join(out, "bad.json"), "--ppi", "16", "--out", out]), /collision|status 1/i);
});
