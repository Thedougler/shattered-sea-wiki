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
