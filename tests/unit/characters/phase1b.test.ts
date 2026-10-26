import { readFileSync } from "node:fs";
import { describe, it, expect } from "vitest";
import { characterRegistry } from "../../../src/characters/registry";
import { validateAtlas } from "../../../src/characters/types";
import { RegistryMotion } from "../../../src/characters/RegistryMotion";

describe("Phase1B authored packs", () => {
  for (const id of ["haneul", "bomi", "minjun"]) {
    it(`${id}: every native clip resolves in the shipped atlas`, () => {
      const def = characterRegistry.get(id)!;
      expect(def.availability.status).toBe("playable");
      expect(def.assets!.texture).not.toContain("juni");
      const atlas = JSON.parse(
        readFileSync(`public/${def.assets!.atlas}`, "utf8"),
      );
      expect(() => validateAtlas(def, atlas)).not.toThrow();
      expect(Object.keys(atlas.frames)).toHaveLength(112);
      for (const direction of ["front", "back", "left", "right"]) {
        for (const action of ["walk", "run"])
          expect(
            new Set(def.animations[`${action}-${direction}`].frames).size,
          ).toBe(8);
        expect(def.animations[`start-${direction}`].loop).toBe(false);
        expect(def.animations[`stop-${direction}`].loop).toBe(false);
      }
    });
  }
  it("plays start, distance gait, authored direction turn, stop and emote without phase advancement against walls or while paused", () => {
    const m = new RegistryMotion(characterRegistry.get("haneul")!);
    m.step(16, 0, true, false, "front", false, false);
    expect(m.action).toBe("start");
    for (let i = 0; i < 3; i++)
      m.step(100, 2, true, false, "front", false, false);
    expect(m.action).toBe("walk");
    const phase = m.phase;
    m.step(100, 0, true, false, "front", false, false);
    expect(m.phase).toBe(phase);
    m.step(16, 1, true, false, "back", false, false);
    expect(m.action).toBe("turn");
    expect(m.frame).toBe("idle-front-0");
    m.step(50, 1, true, false, "back", false, false);
    expect(m.frame).toBe("idle-right-0");
    m.step(100, 1, true, false, "back", false, false);
    expect(m.frame).toMatch(/^walk-back/);
    m.step(16, 0, false, false, "back", false, false);
    expect(m.action).toBe("stop");
    for (let i = 0; i < 3; i++)
      m.step(100, 0, false, false, "back", false, false);
    expect(m.action).toBe("idle");
    m.gesture("wave");
    m.step(16, 0, false, false, "back", false, false);
    expect(m.frame).toMatch(/^wave-front/);
    const frozen = m.frame;
    m.step(100, 8, true, true, "right", false, true);
    expect(m.frame).toBe(frozen);
    for (let i = 0; i < 10; i++)
      m.step(100, 0, false, false, "front", true, false);
    expect(m.action).toBe("idle");
  });
});
