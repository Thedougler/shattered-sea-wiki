import { test } from "node:test";
import assert from "node:assert/strict";
import { parseGrid } from "../lib/grid.mjs";
import { loadManifest } from "../lib/manifest.mjs";
import { buildLegendPrompt } from "../lib/legend.mjs";

test("buildLegendPrompt lists only present, beautified tokens (sorted), with overrides", () => {
  const m = loadManifest();
  const g = parseGrid("WL,FL\nFL,WS");
  const prompt = buildLegendPrompt(g, m);
  assert.match(prompt, /premium hand-painted battlemap in the style of 2-Minute Tabletop/);
  assert.match(prompt, /warm grey squares → worn flagstone floor/);
  assert.match(prompt, /light cyan squares → shallow clear water over stone/);
  assert.match(prompt, /Warm atmospheric top-down lighting/);
  // overrides win
  const ice = buildLegendPrompt(g, m, { legend: { FL: "blue-white ice floor" } });
  assert.match(ice, /→ blue-white ice floor/);
});

test("buildLegendPrompt excludes dm-layer tokens and uses playerFallback in the key", () => {
  const m = loadManifest();
  const g = parseGrid("WL,DS\nFL,TR"); // DS (dm) hides as WL; TR (dm) hides as FL
  const prompt = buildLegendPrompt(g, m);
  assert.doesNotMatch(prompt, /secret/i);
  assert.doesNotMatch(prompt, /trap/i);
  assert.match(prompt, /dungeon walls/); // DS collapsed to WL
  assert.match(prompt, /flagstone floor/); // TR collapsed to FL
});
