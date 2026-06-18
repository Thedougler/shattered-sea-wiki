#!/usr/bin/env node
// Regenerate references/token-library.md from the token manifest. Run after editing tokens.json:
//   node scripts/gen-catalog.mjs
import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { loadManifest } from "./lib/manifest.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = resolve(HERE, "../references/token-library.md");

const m = loadManifest();
let out = "# prep-map Token Library\n\n";
out +=
  "The token manifest (`tokens/tokens.json`) is the single source of truth. Each token serves **four consumers**: the agent (the short CSV code), the renderer (a distinct flat `color` + an optional `glyph` SVG), and the img2img beautify pass (the `fragment` phrase, assembled into the auto color→material legend).\n\n";
out += "**This file is generated** — regenerate with `node scripts/gen-catalog.mjs` after editing the manifest; do not hand-edit.\n\n";
out +=
  "**Layers.** `both` tokens are drawn in the base segmentation key and beautified. `dm` tokens are never beautified: they collapse to their `playerFallback` in the base key (so the player map hides them) and are drawn as crisp magenta overlay markers on the DM map only.\n\n";
out +=
  "**Palette gate.** Large flat regions (terrain/structure) stay ≥16 ΔE2000 apart; small glyph-bearing objects (features/markers) stay ≥10 — several feature pairs sit intentionally near that floor, since the glyph (not the color) disambiguates them. Enforced by `palette.checkSeparation` as a unit test.\n\n";
out += "| Code | Name | Category | ASCII | Color | Glyph | Layer | Img2img fragment |\n|---|---|---|---|---|---|---|---|\n";
for (const [code, e] of Object.entries(m)) {
  const frag = e.fragment || (e.layer === "dm" ? `_(dm marker; base→${e.playerFallback})_` : "—");
  const glyph = e.glyph || "—";
  out += `| \`${code}\` | ${e.name} | ${e.category} | \`${e.ascii}\` | \`${e.color}\` | ${glyph} | ${e.layer} | ${frag} |\n`;
}
out += `\n_${Object.keys(m).length} tokens._\n`;

writeFileSync(OUT, out);
console.log(`wrote ${OUT} (${Object.keys(m).length} tokens)`);
