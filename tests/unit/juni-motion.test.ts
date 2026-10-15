import { describe, expect, it } from "vitest";
import { JuniMotion } from "../../src/review/JuniMotion";

describe("Juni generated-frame runtime", () => {
  it("uses actual travel and preserves phase across run changes and blocked input", () => {
    const motion = new JuniMotion();
    motion.step(16, 0, true, false, "front", false, false);
    motion.step(100, 0, true, false, "front", false, false);
    motion.step(100, 0, true, false, "front", false, false);
    const contacts = new Set<string>();
    for (let i = 0; i < 8; i++)
      contacts.add(motion.step(16, 5.5, true, false, "front", false, false));
    expect(contacts.size).toBe(8);
    const phase = motion.phase;
    const held = motion.frame;
    for (let i = 0; i < 20; i++)
      expect(motion.step(16, 0, true, false, "front", false, false)).toBe(held);
    motion.step(16, 0, true, true, "front", false, false);
    expect(motion.phase).toBe(phase);
    expect(motion.frame).toMatch(/^run-front-/);
  });

  it("plays real turn/start/stop poses and gestures recover to idle", () => {
    const motion = new JuniMotion();
    expect(motion.step(16, 0, true, false, "front", false, false)).toBe(
      "start-front-0",
    );
    motion.step(100, 2, true, false, "front", false, false);
    motion.step(100, 2, true, false, "front", false, false);
    expect(motion.step(16, 1, true, false, "right", false, false)).toBe(
      "turn-7",
    );
    motion.step(100, 2, true, false, "right", false, false);
    expect(motion.view).toBe("right");
    expect(motion.step(16, 1, false, false, "right", false, false)).toBe(
      "stop-right-0",
    );
    for (let i = 0; i < 4; i++)
      motion.step(100, 0, false, false, "right", false, false);
    for (const gesture of ["wave", "celebrate", "social"] as const) {
      motion.gesture(gesture);
      const seen = new Set<string>();
      for (let i = 0; i < 40; i++)
        seen.add(motion.step(50, 0, false, false, "right", false, false));
      expect(
        [...seen].filter((f) => f.startsWith(`${gesture}-front-`)).length,
      ).toBe(8);
      expect(motion.action).toBe("idle");
    }
  });

  it("freezes pause and reduced idle while retaining user-controlled locomotion", () => {
    const motion = new JuniMotion();
    for (let i = 0; i < 30; i++)
      expect(motion.step(100, 0, false, false, "front", true, false)).toBe(
        "idle-front-0",
      );
    motion.step(16, 0, true, false, "front", true, false);
    motion.step(100, 2, true, false, "front", true, false);
    motion.step(100, 2, true, false, "front", true, false);
    const before = motion.snapshot;
    for (let i = 0; i < 8; i++)
      motion.step(100, 8, true, true, "back", false, true);
    expect(motion.snapshot).toEqual(before);
    expect(motion.step(16, 5.5, true, false, "front", true, false)).not.toBe(
      before.frame,
    );
  });
});
