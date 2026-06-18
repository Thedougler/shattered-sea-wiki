/** Parse a tile CSV into { width, height, cells[][] }. Empty cell = null (void). */
export function parseGrid(csvText) {
  const lines = csvText.replace(/\r\n?/g, "\n").split("\n");
  while (lines.length && lines[lines.length - 1].trim() === "") lines.pop();
  if (lines.length === 0) throw new Error("empty grid");
  const rows = lines.map((line) => line.split(",").map((c) => c.trim()));
  const width = rows[0].length;
  rows.forEach((r, i) => {
    if (r.length !== width) throw new Error(`ragged row ${i + 1}: ${r.length} cols, expected ${width}`);
  });
  const cells = rows.map((r) => r.map((c) => (c === "" ? null : c.toUpperCase())));
  return { width, height: cells.length, cells };
}

const DOOR_CODES = new Set(["DR", "DL", "DS"]);
const BLOCKING_TERRAIN = new Set(["WD", "LV", "CM"]); // deep water, lava, chasm

/** Validate a parsed grid against the manifest. Returns { ok, errors, warnings }. */
export function validateGrid(grid, manifest, legend = {}) {
  const { cells, width, height } = grid;
  const errors = [];
  const warnings = [];
  const used = new Set();

  const at = (x, y) => (y < 0 || x < 0 || y >= height || x >= width ? null : cells[y][x]);
  const isPassable = (code) => {
    if (!code) return false;
    const e = manifest[code];
    if (!e) return false;
    if (e.category === "structure") return false;
    if (BLOCKING_TERRAIN.has(code)) return false;
    return true;
  };

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const code = cells[y][x];
      if (code === null) continue;
      used.add(code);
      if (!manifest[code]) {
        errors.push(`(${x},${y}) unknown token: ${code}`);
        continue;
      }
      // A door is "floating" only if it leads nowhere — no passable orthogonal neighbor.
      // (Exterior/entrance doors with void on one side are valid.)
      if (DOOR_CODES.has(code)) {
        const neighbors = [at(x, y - 1), at(x, y + 1), at(x - 1, y), at(x + 1, y)];
        if (!neighbors.some(isPassable)) {
          errors.push(`(${x},${y}) floating door ${code}: no passable neighbor`);
        }
      }
    }
  }

  for (const code of used) {
    const e = manifest[code];
    if (!e || e.layer === "dm") continue;
    const frag = legend[code] ?? e.fragment ?? null;
    if (!frag) warnings.push(`token ${code} has no img2img fragment (beautify will need one)`);
  }

  return { ok: errors.length === 0, errors, warnings };
}
