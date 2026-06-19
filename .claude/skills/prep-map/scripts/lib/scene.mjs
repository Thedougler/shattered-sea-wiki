import { readFileSync } from "node:fs";
import { resolve } from "node:path";

// A scene is an agent-authored paint-by-numbers spec — no fixed token library:
//   { grid: ["#####", "#.L.#", ...],
//     legend: { "#": {fill:"dimgray", as:"..."}, "L": {outline:"limegreen", label:"LADDER UP", as:"..."} } }
// `fill` = a flood-filled surface (wall/floor/...); `outline`+`label` = an outlined, labelled region
// (terrain, prop, exit, hazard) in whatever CSS color the agent picks. `as` is the agent's note of
// what to paint there — handy when writing the beautify prompt; the renderer ignores it.
const COLOR_RE = /^#[0-9a-fA-F]{3,8}$|^[a-zA-Z]+$/; // #hex or a CSS color name

/** Parse a scene's row-strings into { width, height, cells } (one char per cell; space = void). */
export function parseSceneGrid(rows) {
  if (!Array.isArray(rows) || rows.length === 0) throw new Error("scene grid must be a non-empty array of strings");
  const width = Math.max(...rows.map((r) => r.length));
  const cells = rows.map((r) => {
    const row = [];
    for (let x = 0; x < width; x++) {
      const ch = r[x];
      row.push(ch && ch !== " " ? ch : null);
    }
    return row;
  });
  return { width, height: cells.length, cells };
}

/** Validate + normalize a raw scene object into { legend, grid }. Throws on a malformed scene. */
export function normalizeScene(raw) {
  if (!raw || !Array.isArray(raw.grid) || typeof raw.legend !== "object" || raw.legend === null) {
    throw new Error("scene needs { grid: string[], legend: { <char>: {...} } }");
  }
  for (const [k, e] of Object.entries(raw.legend)) {
    if (k.length !== 1) throw new Error(`legend key "${k}" must be a single character`);
    if (!e || (!e.fill && !e.outline)) throw new Error(`legend "${k}" needs a "fill" or an "outline" color`);
    if (e.outline && !e.label) throw new Error(`legend "${k}" has an outline but no "label"`);
    for (const c of [e.fill, e.outline]) {
      if (c && !COLOR_RE.test(c)) throw new Error(`legend "${k}" has an invalid color "${c}" (use a CSS name or #hex)`);
    }
  }
  const grid = parseSceneGrid(raw.grid);
  const unknown = new Set();
  for (const row of grid.cells) for (const k of row) if (k && !raw.legend[k]) unknown.add(k);
  if (unknown.size) throw new Error(`grid uses keys not in the legend: ${[...unknown].sort().join(", ")}`);
  return { legend: raw.legend, grid };
}

/** True if a parsed JSON object looks like a scene (vs a dungeon spec). */
export function isSceneSpec(obj) {
  return !!obj && Array.isArray(obj.grid) && typeof obj.legend === "object" && obj.legend !== null;
}

export function loadScene(path) {
  return normalizeScene(JSON.parse(readFileSync(resolve(path), "utf8")));
}
