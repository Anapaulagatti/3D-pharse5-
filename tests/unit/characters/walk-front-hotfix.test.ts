import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { characterRegistry } from "../../../src/characters/registry";
const D = "docs/phase2b-motion/walk-front/";
const json = (p: string) => JSON.parse(readFileSync(p, "utf8"));
const sha = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
describe("authorized walk-front-only hotfix", () => {
  it("protects every frozen file outside the64 authorized walk-front cells and8 atlas containers", () => {
    execFileSync("python3", ["tools/phase2b-walkfront/audit.py"]);
    const q = json(D + "audit.json");
    expect(q.unexpected).toEqual([]);
    expect(q.modifiedFiles).toHaveLength(72);
    for (const [file, h] of Object.entries(json(D + "before.json").files)) {
      const change = q.modifiedFiles.find(
        (r: { file: string }) => r.file === file,
      );
      expect(sha(file), file).toBe(change ? change.afterSHA256 : h);
    }
    for (const r of q.characters) {
      expect(r.changed).toHaveLength(8);
      expect(r.unchanged).toHaveLength(104);
      for (let i = 0; i < 8; i++)
        expect(r.unchanged).toContain(`walk-right-${i}`);
      expect(r.headHairFirst47Rows).toBe("EXACT");
    }
  }, 30000);
  for (const id of [
    "ara",
    "doyun",
    "sori",
    "jiwon",
    "nari",
    "taeyang",
    "yuna",
    "hyunwoo",
  ])
    it(`${id} preserves timing, native registration, original order and all movement settings`, () => {
      const d = characterRegistry.get(id)!;
      const base = json(D + "before.json");
      const phase = id === "ara" || id === "doyun" ? "phase2a" : "phase2b";
      for (const p of [
        `assets-src/characters/${phase}/${id}/clips.json`,
        `public/assets/characters/${id}/atlas.json`,
      ])
        expect(sha(p)).toBe(base.files[p]);
      expect(d.native).toEqual({ width: 96, height: 112, anchor: [48, 100] });
      expect(d.movement).toEqual({
        walkSpeed: 60,
        runSpeed: 100,
        walkStride: 44,
        runStride: 64,
      });
      expect(d.animations["walk-front"].frames).toEqual(
        Array.from({ length: 8 }, (_, i) => `walk-front-${i}`),
      );
      expect(
        new Set(
          d.animations["walk-front"].frames.map((n) =>
            sha(`assets-src/characters/${phase}/${id}/frames/${n}.png`),
          ),
        ).size,
      ).toBe(8);
    });
});
