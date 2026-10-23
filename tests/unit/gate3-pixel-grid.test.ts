import { describe, it, expect } from "vitest";
import { nativeCanvasOffset } from "../../src/gate3/PixelGrid";
import { rasterOrigin } from "../../src/gate3/Registration";
describe("native display registration", () => {
  it("centers odd windows without half-pixel canvas translations", () => {
    expect(nativeCanvasOffset(1281, 1280)).toBe(0);
    expect(nativeCanvasOffset(1001, 900)).toBe(50);
    expect(nativeCanvasOffset(1000, 900)).toBe(50);
    expect(nativeCanvasOffset(843, 843)).toBe(0);
    expect(nativeCanvasOffset(843, 1280)).toBe(-219);
  });
  it("station half-unit logical anchor produces integer raster placement", () => {
    expect(rasterOrigin([2313.5, 2196], [0.5, 0])).toEqual([2313, 2196]);
    expect(() => rasterOrigin([2313.5, 2196], [0, 0])).toThrow();
  });
});
