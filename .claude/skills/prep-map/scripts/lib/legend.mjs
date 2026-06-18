import { effectiveCode, resolveFragment } from "./manifest.mjs";

const STYLE_PREAMBLE =
  "Repaint this schematic top-down map as a premium hand-painted battlemap in the style of 2-Minute Tabletop: painterly, illustrated, stylized realism — NOT a photo.";
const STRUCTURE_LOCK =
  "Repaint each flat-colored region as its material, keeping every wall, door, and keyed region in EXACTLY the same position, size and shape — do not move, merge, add, or remove any structure:";
const LIGHTING =
  "Warm atmospheric top-down lighting: soft orange glow pools around the light sources, ambient shadow elsewhere. Strictly orthographic top-down — no perspective, no long cast shadows. Within floor areas add subtle period-appropriate wear and clutter. Dark marbled-stone texture in the surrounding void. No grid lines, no labels.";

/**
 * Build the img2img legend prompt for a grid.
 * dm-layer tokens collapse to their playerFallback (the base key hides them), so only
 * beautified materials appear. `opts.legend` overrides fragments; `opts.stylePreamble`
 * overrides the house-style line (Phase B injects art-style.md here).
 */
export function buildLegendPrompt(grid, manifest, opts = {}) {
  const { legend = {}, stylePreamble = STYLE_PREAMBLE } = opts;
  const present = new Set();
  for (const row of grid.cells) {
    for (const raw of row) {
      const code = effectiveCode(manifest, raw);
      if (code) present.add(code);
    }
  }
  const lines = [];
  for (const code of [...present].sort()) {
    const e = manifest[code];
    if (!e || e.layer === "dm") continue;
    const frag = resolveFragment(manifest, code, legend);
    if (!frag) continue;
    lines.push(`• ${e.colorName} → ${frag}`);
  }
  return [stylePreamble, STRUCTURE_LOCK, ...lines, LIGHTING].join("\n");
}
