import { parseGrid } from "./grid.mjs";

/**
 * Assemble a dungeon spec into one master tile grid.
 *
 *   spec = {
 *     rooms: [{ csv, x, y }, ...],            // each room's CSV stamped at master cell (x,y)
 *     corridors: [{ from:[x,y], to:[x,y], token }]  // straight tile-runs (optional)
 *   }
 *
 * `loadCsv(name)` is injected so callers (and tests) control file IO. Returns
 * `{ grid, collisions }` — collisions list cells where two rooms disagree (shared
 * walls of the same token are fine and are not reported).
 */
export function assembleDungeon(spec, loadCsv) {
  const rooms = (spec.rooms ?? []).map((r) => ({ ...r, grid: parseGrid(loadCsv(r.csv)) }));

  const corridors = spec.corridors ?? [];
  for (const c of corridors) {
    if (c.from[0] !== c.to[0] && c.from[1] !== c.to[1]) {
      throw new Error(`corridor must be a straight horizontal or vertical run: ${JSON.stringify(c)}`);
    }
  }

  let width = 0;
  let height = 0;
  for (const r of rooms) {
    width = Math.max(width, r.x + r.grid.width);
    height = Math.max(height, r.y + r.grid.height);
  }
  for (const c of corridors) {
    width = Math.max(width, c.from[0] + 1, c.to[0] + 1);
    height = Math.max(height, c.from[1] + 1, c.to[1] + 1);
  }

  const cells = Array.from({ length: height }, () => Array(width).fill(null));
  const collisions = [];
  rooms.forEach((r, ri) => {
    for (let y = 0; y < r.grid.height; y++) {
      for (let x = 0; x < r.grid.width; x++) {
        const code = r.grid.cells[y][x];
        if (code === null) continue;
        const mx = r.x + x;
        const my = r.y + y;
        const existing = cells[my][mx];
        if (existing !== null && existing !== code) {
          collisions.push({ x: mx, y: my, existing, incoming: code, room: ri });
        }
        cells[my][mx] = code;
      }
    }
  });

  // Corridors carve last: a straight run overwrites whatever it crosses (walls → passage).
  const corridorCells = [];
  for (const c of corridors) {
    const [x1, y1] = c.from;
    const [x2, y2] = c.to;
    const token = (c.token ?? "FL").toUpperCase();
    const stepX = Math.sign(x2 - x1);
    const stepY = Math.sign(y2 - y1);
    let x = x1;
    let y = y1;
    for (;;) {
      cells[y][x] = token;
      corridorCells.push([x, y]);
      if (x === x2 && y === y2) break;
      x += stepX;
      y += stepY;
    }
  }

  // Auto-wall corridors: any VOID cell touching a corridor run (8-neighbourhood, so ends and
  // corners are capped too) becomes WL. Only null cells are filled — authored room and corridor
  // cells are never overwritten, so a corridor reads as a walled passage, not an exposed ledge.
  if (spec.autoWallCorridors !== false) {
    for (const [cx, cy] of corridorCells) {
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx < 0 || ny < 0 || nx >= width || ny >= height) continue;
          if (cells[ny][nx] === null) cells[ny][nx] = "WL";
        }
      }
    }
  }

  return { grid: { width, height, cells }, collisions };
}
