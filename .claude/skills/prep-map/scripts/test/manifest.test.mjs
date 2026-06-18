import { test } from "node:test";
import assert from "node:assert/strict";
import { loadManifest, resolveFragment, effectiveCode } from "../lib/manifest.mjs";

test("loadManifest returns valid entries with required fields", () => {
  const m = loadManifest();
  assert.ok(m.WL && m.FL && m.DR, "core tokens present");
  for (const [code, e] of Object.entries(m)) {
    assert.ok(/^#[0-9a-fA-F]{6}$/.test(e.color), `${code} has hex color`);
    assert.ok(["both", "dm"].includes(e.layer), `${code} has valid layer`);
    assert.ok(
      ["structure", "terrain", "hazard", "feature", "marker", "primitive"].includes(e.category),
      `${code} has valid category`,
    );
  }
});

test("dm-layer tokens declare a playerFallback", () => {
  const m = loadManifest();
  for (const [code, e] of Object.entries(m)) {
    if (e.layer === "dm") assert.ok(e.playerFallback, `${code} (dm) needs playerFallback`);
  }
});

test("resolveFragment prefers per-map legend override over manifest default", () => {
  const m = loadManifest();
  assert.equal(resolveFragment(m, "FL", {}), m.FL.fragment);
  assert.equal(resolveFragment(m, "FL", { FL: "blue-white ice floor" }), "blue-white ice floor");
});

test("effectiveCode substitutes playerFallback for dm tokens", () => {
  const m = loadManifest();
  assert.equal(effectiveCode(m, "FL"), "FL");
  assert.equal(effectiveCode(m, "DS"), "WL"); // secret door hides as wall
  assert.equal(effectiveCode(m, "TR"), "FL"); // trap sits on floor in the base key
  assert.equal(effectiveCode(m, null), null);
});

test("loadManifest throws on a malformed entry", () => {
  assert.throws(() => loadManifest(new URL("./fixtures/bad-manifest.json", import.meta.url)));
});
