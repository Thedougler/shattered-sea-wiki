import { test } from "node:test";
import assert from "node:assert/strict";
import sharp from "sharp";

test("sharp rasterizes an SVG to exact pixel dimensions", async () => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"><rect width="20" height="10" fill="#ff0000"/></svg>`;
  const { data, info } = await sharp(Buffer.from(svg))
    .raw()
    .toBuffer({ resolveWithObject: true });
  assert.equal(info.width, 20);
  assert.equal(info.height, 10);
  assert.equal(data[0], 255);
  assert.equal(data[1], 0);
  assert.equal(data[2], 0);
});
