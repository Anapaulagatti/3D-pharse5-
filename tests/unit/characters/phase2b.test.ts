import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { characterRegistry } from "../../../src/characters/registry";
import { validateAtlas } from "../../../src/characters/types";
import { RegistryMotion } from "../../../src/characters/RegistryMotion";
import {
  compatibleItems,
  normalizeAppearance,
} from "../../../src/characters/appearance";
import {
  AppearancePreferences,
  CharacterPreferences,
  PREFERENCES_KEY,
  APPEARANCE_PREFERENCES_KEY,
} from "../../../src/characters/preferences";
const ids = ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"];
const json = (p: string) => JSON.parse(readFileSync(p, "utf8"));
const digest = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
describe("Phase2B accepted baseline protection", () => {
  it("preserves approved files outside the explicit eight-cell Ara/Doyun walk-front amendment", () => {
    // Latest human directive permits Ara/Doyun walk-front only. Preserve the
    // historical manifest; independently verify every other atlas cell/file.
    execFileSync("python3", ["tools/phase2b-walkfront/audit.py"]);
    const hotfix = json("docs/phase2b-motion/walk-front/audit.json");
    const authorized = new Map(
      hotfix.modifiedFiles.map((r: { file: string; afterSHA256: string }) => [
        r.file,
        r.afterSHA256,
      ]),
    );
    const m = json("docs/phase2b/approved-six.json");
    for (const [p, h] of Object.entries({ ...m.files, ...m.sourceSnapshots }))
      expect(digest(p), p).toBe(authorized.get(p) ?? h);
  }, 20000);
  it("keeps all six registered identities, clips, movement and registration byte-equivalent in data", () => {
    for (const old of json("docs/phase2b/approved-identity-records.json")
      .characters)
      expect(characterRegistry.get(old.id)).toEqual(old);
  });
  it("keeps persistence implementation, schema, current wardrobe and motion engine unchanged", () => {
    for (const file of [
      "preferences.ts",
      "appearanceTypes.ts",
      "appearance.ts",
      "AppearanceRenderer.ts",
      "PhaserCharacterAssets.ts",
      "PlayerCharacterManager.ts",
      "RegistryMotion.ts",
      "newCharacters.ts",
      "types.ts",
      "futureRoster.ts",
      "selection.css",
      "session.ts",
      "studioI18n.ts",
    ])
      expect(digest("src/characters/" + file)).toBe(
        digest("docs/phase2b/approved-source-snapshots/src/characters/" + file),
      );
    expect(digest("assets-src/characters/phase2a/cosmetics/catalog.json")).toBe(
      digest("docs/phase2b/approved-cosmetic-catalog.json"),
    );
  });
});
describe("twelve complete free identities", () => {
  it("promotes six stable planned IDs without duplicates or placeholders and retains Juni fallback", () => {
    expect(characterRegistry.all).toHaveLength(12);
    expect(characterRegistry.planned).toHaveLength(0);
    expect(new Set(characterRegistry.all.map((d) => d.id)).size).toBe(12);
    expect(characterRegistry.resolve("invalid").id).toBe("juni");
    for (const d of characterRegistry.all) {
      expect(d.availability.status).toBe("playable");
      expect(d.availability.unlock).toBe("free");
    }
  });
  for (const id of ids) {
    it(`${id}: complete independent native pack, real eight-pose gaits, all clips and compatible registration`, () => {
      const d = characterRegistry.get(id)!;
      expect(d).toBeDefined();
      expect(d.native).toEqual({ width: 96, height: 112, anchor: [48, 100] });
      expect(d.movement).toEqual({
        walkSpeed: 60,
        runSpeed: 100,
        walkStride: 44,
        runStride: 64,
      });
      const a = json("public/" + d.assets!.atlas);
      validateAtlas(d, a);
      expect(Object.keys(a.frames)).toHaveLength(112);
      expect(
        Object.keys(json(`assets-src/characters/phase2b/${id}/clips.json`)),
      ).toHaveLength(34);
      expect(d.animations["social-front"]).toEqual(d.animations["wave-front"]);
      for (const direction of ["front", "back", "left", "right"]) {
        for (const action of ["walk", "run"]) {
          const frames = d.animations[`${action}-${direction}`].frames;
          expect(frames).toHaveLength(8);
          expect(
            new Set(
              frames.map((n) =>
                digest(`assets-src/characters/phase2b/${id}/frames/${n}.png`),
              ),
            ).size,
          ).toBe(8);
        }
        for (const action of ["idle", "start", "stop"])
          expect(
            d.animations[`${action}-${direction}`].frames.length,
          ).toBeGreaterThan(1);
      }
      for (const clip of Object.values(d.animations))
        for (const name of clip.frames)
          expect(
            existsSync(
              `assets-src/characters/phase2b/${id}/frames/${name}.png`,
            ),
          ).toBe(true);
      expect(compatibleItems(id)).toEqual([]);
      expect(
        normalizeAppearance(id, {
          hairstyleId: "ara-braided-bun",
          outfitId: "doyun-field-jacket",
          accessoryIds: ["ara-shell-barrette"],
        }),
      ).toEqual({
        schemaVersion: 2,
        characterId: id,
        hairstyleId: null,
        outfitId: null,
        accessoryIds: [],
      });
    });
    it(`${id}: shared distance-driven motion starts, loops eight frames, stops, turns and supports existing gestures`, () => {
      const d = characterRegistry.get(id)!,
        m = new RegistryMotion(d),
        seen = new Set<string>();
      for (const view of ["front", "back", "left", "right"] as const) {
        for (const run of [false, true]) {
          for (let i = 0; i < 120; i++) {
            const frame = m.step(
              16,
              run ? 1.6 : 0.96,
              true,
              run,
              view,
              false,
              false,
            );
            expect(
              d.animations[
                Object.keys(d.animations).find((k) =>
                  d.animations[k].frames.includes(frame),
                )!
              ],
            ).toBeDefined();
            if (frame.startsWith((run ? "run" : "walk") + "-" + view))
              seen.add(frame);
          }
          expect(
            [...seen].filter((f) =>
              f.startsWith((run ? "run" : "walk") + "-" + view),
            ),
          ).toHaveLength(8);
          m.step(16, 0, false, run, view, false, false);
          expect(m.action).toBe("stop");
          for (let i = 0; i < 20; i++)
            m.step(16, 0, false, false, view, false, false);
          expect(m.action).toBe("idle");
        }
      }
      for (const gesture of ["wave", "celebrate", "social"] as const) {
        m.gesture(gesture);
        expect(m.step(16, 0, false, false, "front", false, false)).toBe(
          d.animations[`${gesture}-front`].frames[0],
        );
        for (let i = 0; i < 60; i++)
          m.step(16, 0, false, false, "front", false, false);
        expect(m.action).toBe("idle");
      }
    });
  }
  it("preserves approved v1/v2 looks and named presets while selecting and reloading all new identities", () => {
    const values = new Map<string, string>();
    const s = {
      getItem: (k: string) => values.get(k) ?? null,
      setItem: (k: string, v: string) => {
        values.set(k, v);
      },
    };
    values.set(
      PREFERENCES_KEY,
      JSON.stringify({ version: 1, characterId: "ara" }),
    );
    values.set("world-progress-sentinel", "KEEP");
    const p = new AppearancePreferences(s, characterRegistry),
      v1 = new CharacterPreferences(s, characterRegistry);
    p.save(
      {
        schemaVersion: 2,
        characterId: "ara",
        hairstyleId: "ara-braided-bun",
        outfitId: "ara-coastal-parka",
        accessoryIds: ["ara-shell-barrette"],
      },
      "Biển",
    );
    for (const id of ids) {
      v1.save(id);
      p.save(normalizeAppearance(id, {}));
      expect(
        new CharacterPreferences(s, characterRegistry).read().characterId,
      ).toBe(id);
      expect(
        new AppearancePreferences(s, characterRegistry).read(id).characterId,
      ).toBe(id);
    }
    expect(p.read("ara").hairstyleId).toBe("ara-braided-bun");
    expect(values.get(APPEARANCE_PREFERENCES_KEY)).toContain("Biển");
    expect(values.get("world-progress-sentinel")).toBe("KEEP");
  });
});
