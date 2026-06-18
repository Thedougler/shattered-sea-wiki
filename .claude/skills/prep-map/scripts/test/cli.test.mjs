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
