import { describe, it, expect } from "vitest";
import { ActorMotion } from "../../src/game/ActorMotion";
describe("distance-driven pixel locomotion", () => {
  it("advances with travel and keeps planted pose at a wall", () => {
    const m = new ActorMotion();
    m.step(16, 0, true, false, "right", false, false);
    m.step(130, 2, true, false, "right", false, false);
    const a = m.step(30, 3, true, false, "right", false, false);
    expect(a).toMatch(/^walk-right-/);
    expect(m.step(100, 0, true, false, "right", false, false)).toBe(a);
    expect(m.step(30, 4, true, false, "right", false, false)).not.toBe(a);
  });
  it("freezes pause, preserves reduced-motion rest and returns from a thinking emote", () => {
    const m = new ActorMotion();
    expect(m.step(150, 0, false, false, "down", true, false)).toBe(
      "idle-down-0",
    );
    m.emote("think");
    const a = m.step(100, 0, false, false, "down", true, false);
    expect(a).toContain("think-down-");
    expect(m.step(100, 10, true, true, "left", false, true)).toBe(a);
    for (let i = 0; i < 20; i++)
      m.step(100, 0, false, false, "down", true, false);
    expect(m.frame).toBe("idle-down-0");
  });
  it("uses authored start, turn and settle transitions", () => {
    const m = new ActorMotion();
    expect(m.step(16, 0, true, false, "down", false, false)).toBe(
      "start-down-0",
    );
    expect(m.moveScale).toBe(0);
    m.step(130, 2, true, false, "down", false, false);
    expect(m.step(16, 1, true, false, "right", false, false)).toBe(
      "turn-right-0",
    );
    expect(m.step(16, 1, false, false, "right", false, false)).toBe(
      "stop-right-0",
    );
    expect(m.step(150, 0, false, false, "right", true, false)).toBe(
      "idle-right-0",
    );
  });
});
