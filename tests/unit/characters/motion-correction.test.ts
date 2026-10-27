import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { characterRegistry } from "../../../src/characters/registry";
const D = "docs/phase2b-motion/",
  ids = ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"];
const json = (p: string) => JSON.parse(readFileSync(p, "utf8"));
const sha = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
describe("focused motion correction preservation and forward stance", () => {
  it("recomputes exact atlas cell scope and protects every other frozen asset/runtime file", () => {
    // The newer authorized front-only amendment supersedes the old whole-file
    // freeze. Its per-cell audit retains the accepted right motion exactly.
    execFileSync("python3", ["tools/phase2b-walkfront/audit.py"], {
      encoding: "utf8",
    });
    const q = json(D + "walk-front/audit.json");
    expect(q.unexpected).toEqual([]);
    expect(q.modifiedFiles).toHaveLength(72);
    for (const r of q.modifiedFiles) expect(sha(r.file)).toBe(r.afterSHA256);
    for (const c of q.characters) {
      expect(c.changed).toHaveLength(8);
      expect(c.unchanged).toHaveLength(104);
      expect(c.headHairFirst47Rows).toBe("EXACT");
      for (let i = 0; i < 8; i++)
        expect(c.unchanged).toContain(`walk-right-${i}`);
    }
  }, 30000);
  it("independently tracks actual raster soles: rejects old same-direction stance and verifies corrected source quantization", () => {
    execFileSync("python3", ["tools/phase2b-motion/pixel_gait.py"], {
      encoding: "utf8",
    });
    const q = json(D + "directional-pixel-qa.json");
    expect(q.rows).toHaveLength(12);
    for (const r of q.rows) {
      expect(r.beforeWorldStanceDriftPixels).toBeGreaterThan(r.stride * 0.6);
      expect(r.afterWorldStanceDriftPixels).toBeLessThanOrEqual(1);
      for (let i = 0; i < 4; i++)
        expect(r.after[i + 1].nativeSole[0]).toBeLessThan(
          r.after[i].nativeSole[0],
        );
    }
  }, 20000);
  for (const id of ids)
    it(`${id}: keeps clip order, timing, native contact and speed; settles stops to original idle`, () => {
      const d = characterRegistry.get(id)!;
      const old = json("docs/phase2b-motion/before-manifest.json");
      expect(sha(`assets-src/characters/phase2b/${id}/clips.json`)).toBe(
        old.files[`assets-src/characters/phase2b/${id}/clips.json`],
      );
      expect(sha(`public/assets/characters/${id}/atlas.json`)).toBe(
        old.files[`public/assets/characters/${id}/atlas.json`],
      );
      expect(d.native).toEqual({ width: 96, height: 112, anchor: [48, 100] });
      expect(d.movement).toEqual({
        walkSpeed: 60,
        runSpeed: 100,
        walkStride: 44,
        runStride: 64,
      });
      for (const direction of ["front", "back", "right"])
        expect(
          sha(
            `assets-src/characters/phase2b/${id}/frames/stop-${direction}-2.png`,
          ),
        ).toBe(
          sha(
            `assets-src/characters/phase2b/${id}/frames/idle-${direction}-0.png`,
          ),
        );
      for (const action of ["walk", "run"])
        for (const direction of ["front", "back", "right"])
          expect(
            new Set(
              d.animations[`${action}-${direction}`].frames.map((n) =>
                sha(`assets-src/characters/phase2b/${id}/frames/${n}.png`),
              ),
            ).size,
          ).toBe(8);
    });
});
