import { test } from "node:test";
import assert from "node:assert/strict";
import { assembleDungeon } from "../lib/compose.mjs";

// In-memory CSV loader so tests never touch disk.
const loader = (files) => (name) => {
  if (!(name in files)) throw new Error(`no such csv: ${name}`);
  return files[name];
};

test("rooms are stamped onto the master grid at their (x,y) offsets", () => {
  const files = {
    "a.csv": "WL,WL\nWL,FL",
    "b.csv": "CH",
  };
  const { grid, collisions } = assembleDungeon(
    { rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 4, y: 1 }] },
    loader(files),
  );
  assert.equal(grid.width, 5); // room b right edge at x=4 → width 5
  assert.equal(grid.height, 2);
  assert.equal(grid.cells[0][0], "WL"); // room a top-left
  assert.equal(grid.cells[1][1], "FL"); // room a bottom-right
  assert.equal(grid.cells[1][4], "CH"); // room b at offset (4,1)
  assert.equal(grid.cells[0][4], null); // void where nothing was stamped
  assert.deepEqual(collisions, []);
});

test("overlapping rooms with different tokens report a collision; matching walls do not", () => {
  const files = { "a.csv": "FL,FL", "b.csv": "WL,WL" };
  const { collisions } = assembleDungeon(
    { rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 1, y: 0 }] },
    loader(files),
  );
  // a occupies (0,0)=FL (1,0)=FL ; b occupies (1,0)=WL (2,0)=WL → (1,0) disagrees
  assert.equal(collisions.length, 1);
  assert.deepEqual(collisions[0], { x: 1, y: 0, existing: "FL", incoming: "WL", room: 1 });

  // two rooms sharing a wall of the SAME token = no collision
  const shared = assembleDungeon(
    { rooms: [{ csv: "wall.csv", x: 0, y: 0 }, { csv: "wall.csv", x: 1, y: 0 }] },
    loader({ "wall.csv": "WL,WL" }),
  );
  assert.deepEqual(shared.collisions, []);
});

test("a straight corridor run paints its token through every cell, carving walls", () => {
  // two 2x2 rooms with a 2-cell gap; a horizontal corridor links them through the wall.
  const files = { "a.csv": "WL,WL\nFL,WL", "b.csv": "WL,WL\nWL,FL" };
  const { grid } = assembleDungeon(
    {
      rooms: [{ csv: "a.csv", x: 0, y: 0 }, { csv: "b.csv", x: 4, y: 0 }],
      corridors: [{ from: [1, 1], to: [4, 1], token: "FL" }],
    },
    loader(files),
  );
  for (let x = 1; x <= 4; x++) assert.equal(grid.cells[1][x], "FL", `corridor cell (${x},1)`);
  assert.notEqual(grid.cells[0][2], "FL"); // corridor floor never bleeds into an adjacent row
});

test("corridors are auto-walled: void cells bordering the run become WL, floor stays open", () => {
  // one floor room at (0,0); a corridor running through open void at y=2.
  const { grid } = assembleDungeon(
    {
      rooms: [{ csv: "a.csv", x: 0, y: 0 }],
      corridors: [{ from: [0, 2], to: [3, 2], token: "FL" }],
    },
    loader({ "a.csv": "FL" }),
  );
  for (let x = 0; x <= 3; x++) assert.equal(grid.cells[2][x], "FL", `corridor floor (${x},2) stays open`);
  for (let x = 0; x <= 3; x++) assert.equal(grid.cells[1][x], "WL", `wall flanks corridor above (${x},1)`);
  assert.equal(grid.cells[0][0], "FL"); // the authored room cell is never overwritten by auto-walls
});

test("a non-straight (diagonal) corridor is rejected", () => {
  assert.throws(
    () => assembleDungeon({ rooms: [], corridors: [{ from: [0, 0], to: [2, 2], token: "FL" }] }, loader({})),
    /straight/i,
  );
});
