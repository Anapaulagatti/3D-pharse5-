import { describe, expect, it } from "vitest";
import { walkable } from "../../src/world-gate1/geometry";

describe("targeted Gate 1 transport and Jeju collision", () => {
  it("blocks the rail bed and eastern rail approach", () => {
    expect(walkable(3070, 2530)).toBe(false);
    expect(walkable(3500, 2200)).toBe(false);
  });
  it("connects both platforms through the pedestrian overpass", () => {
    expect(walkable(2970, 2530)).toBe(true);
    expect(walkable(3300, 2530)).toBe(true);
    expect(walkable(3070, 2680)).toBe(true);
    expect(walkable(3180, 2680)).toBe(true);
  });
  it("keeps the full-sized station building solid", () => {
    expect(walkable(2500, 2500)).toBe(false);
  });
  it("keeps the oreum core solid and its rim accessible", () => {
    expect(walkable(3750, 3500)).toBe(false);
    expect(walkable(3910, 3530)).toBe(true);
  });
  it("keeps orchard aisles and basalt exploration accessible", () => {
    expect(walkable(3710, 3950)).toBe(false);
    expect(walkable(3650, 4050)).toBe(true);
    expect(walkable(3400, 3700)).toBe(false);
    expect(walkable(3550, 3780)).toBe(true);
  });
  it("allows physical piers without making the ferry sea link walkable", () => {
    expect(walkable(2560, 4100)).toBe(true);
    expect(walkable(3240, 4100)).toBe(true);
    expect(walkable(2900, 4100)).toBe(false);
  });
});
