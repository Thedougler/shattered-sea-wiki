import { test } from "node:test";
import assert from "node:assert/strict";
import { hexToLab, ciede2000, checkSeparation } from "../lib/palette.mjs";
import { loadManifest } from "../lib/manifest.mjs";

test("ciede2000 of identical colors is 0", () => {
  const lab = hexToLab("#3c6e9a");
  assert.equal(ciede2000(lab, lab), 0);
});

test("ciede2000 is symmetric", () => {
  const a = hexToLab("#112233"), b = hexToLab("#aabbcc");
  assert.ok(Math.abs(ciede2000(a, b) - ciede2000(b, a)) < 1e-9);
});

test("ciede2000 black vs white is large (~100)", () => {
  const d = ciede2000(hexToLab("#000000"), hexToLab("#ffffff"));
  assert.ok(d > 95 && d < 105, `expected ~100, got ${d}`);
});

test("the shipped manifest passes the separation gate", () => {
  const violations = checkSeparation(loadManifest());
  assert.deepEqual(violations, [], `palette collisions: ${JSON.stringify(violations)}`);
});
