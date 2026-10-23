import { describe, it, expect } from "vitest";
import { rasterOrigin, pixelCenter } from "../../src/gate3/Registration";
import { containsPoint } from "../../src/gate3/types";
describe("candidate registration conventions", () => {
  it("preserves the protected half-pixel station anchor with an explicit source pivot", () => {
    const anchor: [number, number] = [2238.5, 2180];
    const edge = rasterOrigin(anchor, [0.5, 0]);
    expect(edge).toEqual([2238, 2180]);
    expect(anchor).toEqual([2238.5, 2180]);
    expect(pixelCenter(edge, 360, 429)[0]).toBe(2598.5);
    expect(pixelCenter(edge, 84, 200)[0]).toBe(2322.5);
  });
  it("rejects the legacy half-pixel edge as a raster placement instead of silently rounding it", () => {
    expect(() => rasterOrigin([2238.5, 2180], [0, 0])).toThrow(
      "explicit source pivot",
    );
  });
  it("keeps the protected555px logical footprint fractional, without snapping the near/far edge", () => {
    const rect: [number, number, number, number] = [2322.5, 2380, 555, 210];
    expect(containsPoint(2322.4999, 2400, rect)).toBe(false);
    expect(containsPoint(2322.5, 2400, rect)).toBe(true);
    expect(containsPoint(2877.4999, 2400, rect)).toBe(true);
    expect(containsPoint(2877.5, 2400, rect)).toBe(false);
    expect(containsPoint(2598.5, 2610, rect)).toBe(false);
  });
});
