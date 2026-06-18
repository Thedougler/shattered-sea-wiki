import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_PATH = resolve(HERE, "../../tokens/tokens.json");

const REQUIRED = ["name", "category", "color", "layer"];
const CATEGORIES = new Set(["structure", "terrain", "hazard", "feature", "marker", "primitive"]);
const HEX = /^#[0-9a-fA-F]{6}$/;

/** Load + validate the token manifest. `pathOrUrl` is for tests; defaults to tokens/tokens.json. */
export function loadManifest(pathOrUrl = DEFAULT_PATH) {
  const text = readFileSync(pathOrUrl, "utf8");
  const raw = JSON.parse(text);
  for (const [code, e] of Object.entries(raw)) {
    for (const f of REQUIRED) {
      if (!(f in e)) throw new Error(`token ${code}: missing required field "${f}"`);
    }
    if (!CATEGORIES.has(e.category)) throw new Error(`token ${code}: bad category "${e.category}"`);
    if (!HEX.test(e.color)) throw new Error(`token ${code}: color must be #RRGGBB, got "${e.color}"`);
    if (e.layer !== "both" && e.layer !== "dm") throw new Error(`token ${code}: layer must be "both"|"dm"`);
    if (e.layer === "dm" && !e.playerFallback) throw new Error(`token ${code}: dm-layer token needs a playerFallback`);
  }
  return raw;
}

/** Resolve the img2img fragment for a token, applying per-map legend overrides. */
export function resolveFragment(manifest, code, legend = {}) {
  return legend[code] ?? manifest[code]?.fragment ?? null;
}

/** The code actually drawn in the base segmentation key: dm tokens collapse to their playerFallback. */
export function effectiveCode(manifest, code) {
  if (!code) return null;
  const e = manifest[code];
  if (e && e.layer === "dm") return e.playerFallback ?? "FL";
  return code;
}
