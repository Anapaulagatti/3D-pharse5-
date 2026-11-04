import { describe, it, expect } from "vitest";
import { cropVisual } from "../../src/economy/presentation";
import { moveReviewPlayer } from "../../src/gate3/ReviewMovement";
import { repairedReviewPath } from "../../src/gate3/Accessibility";
import type { PlotState } from "../../src/economy/catalog";
describe("visible farming lifecycle", () => {
  it.each(["radish", "scallion"] as const)(
    "shows every stage of %s, water and reset without mutating saves",
    (crop) => {
      const p: PlotState = {
        stage: "watered",
        cycle: 1,
        crop,
        wateredAt: 1000,
        growMs: 10000,
      };
      const before = JSON.stringify(p);
      expect(
        [0, 1600, 3600, 6200, 10000].map((t) => cropVisual(p, 1000 + t).stage),
      ).toEqual(["sown", "sprout", "young", "growing", "ready"]);
      expect(cropVisual(p, 5000).wet).toBe(true);
      expect(cropVisual({ ...p, stage: "planted" }, 50000)).toMatchObject({
        stage: "sown",
        wet: false,
      });
      expect(cropVisual({ stage: "empty", cycle: 2 }, 50000).stage).toBe(
        "empty",
      );
      expect(cropVisual({ stage: "tilled", cycle: 2 }, 50000).stage).toBe(
        "tilled",
      );
      expect(JSON.stringify(p)).toBe(before);
    },
  );
});
describe("safe narrow path control", () => {
  it("keeps diagonal speed and no tunnelling through solid walls", () => {
    const p = moveReviewPlayer(0, 0, Math.SQRT1_2, Math.SQRT1_2, 5, () => true);
    expect(Math.hypot(p.x, p.y)).toBeCloseTo(5);
    expect(moveReviewPlayer(0, 0, 1, 0, 20, (x) => x < 3).x).toBeLessThan(3);
  });
  it("slides past a small corner without crossing it or increasing speed", () => {
    const allows = (x: number, y: number) =>
      !(x >= 1 && x <= 2 && Math.abs(y) < 2);
    let p = { x: 0, y: 0 };
    for (let i = 0; i < 12; i++) {
      const next = moveReviewPlayer(p.x, p.y, 1, 0, 1, allows);
      expect(allows(next.x, next.y)).toBe(true);
      expect(Math.hypot(next.x - p.x, next.y - p.y)).toBeLessThanOrEqual(1);
      p = next;
    }
    expect(p.x).toBeGreaterThan(5);
  });
  it("does not open planter or expand patch beyond explicitly inspected paving", () => {
    expect(repairedReviewPath(458, 2400)).toBe(true);
    expect(repairedReviewPath(454, 2400)).toBe(false);
    expect(repairedReviewPath(485, 2400)).toBe(false);
    expect(repairedReviewPath(458, 2480)).toBe(false);
  });
});
