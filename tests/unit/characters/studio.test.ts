import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import ts from "typescript";
import {
  characterRegistry,
  CharacterRegistry,
} from "../../../src/characters/registry";
import { validateAtlas } from "../../../src/characters/types";
import {
  appearanceManifest,
  defaultAppearance,
  normalizeAppearance,
  compatibleItems,
  appearanceKey,
  validateAppearanceManifest,
} from "../../../src/characters/appearance";
import {
  AppearancePreferences,
  CharacterPreferences,
  APPEARANCE_PREFERENCES_KEY,
  PREFERENCES_KEY,
} from "../../../src/characters/preferences";
import {
  PlayerCharacterManager,
  type PlayerSprite,
} from "../../../src/characters/PlayerCharacterManager";
import { RegistryMotion } from "../../../src/characters/RegistryMotion";
import { BoundedCache } from "../../../src/characters/AppearanceRenderer";
import type { CharacterAppearance } from "../../../src/characters/appearanceTypes";
const json = (p: string) => JSON.parse(readFileSync(p, "utf8"));
const digest = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
function storage() {
  const values = new Map<string, string>();
  return {
    values,
    getItem: (k: string) => values.get(k) ?? null,
    setItem: (k: string, v: string) => {
      values.set(k, v);
    },
  };
}
const look = (): CharacterAppearance => ({
  schemaVersion: 2,
  characterId: "ara",
  hairstyleId: "ara-braided-bun",
  outfitId: "ara-sunlit-linen",
  accessoryIds: ["ara-shell-barrette"],
});
describe("Phase2A immutable approval baseline", () => {
  it("preserves all four original source/atlas/config/preview/tool files and definition snapshots byte-for-byte", () => {
    const m = json("docs/phase2a/approved-four-characters.json");
    expect(m.approvedCommit).toBe("51ac4b4f20f0af2f26d1566988580d92c0612356");
    for (const [p, h] of Object.entries({
      ...m.files,
      ...m.definitionSnapshots,
    }))
      expect(digest(p), p).toBe(h);
  });
  it("preserves original identities, poses, anchors and speeds; only human-approval description metadata changes", () => {
    for (const previous of json("docs/phase2a/approved-identity-records.json")
      .characters) {
      const current = structuredClone(characterRegistry.get(previous.id)!);
      current.availability.reason = previous.availability.reason;
      expect(current).toEqual(previous);
    }
  });
  it("does not change the original distance-driven RegistryMotion.step implementation", () => {
    const method = (p: string) => {
      const ast = ts.createSourceFile(
        p,
        readFileSync(p, "utf8"),
        ts.ScriptTarget.Latest,
        true,
      );
      let found: ts.Node | undefined;
      const visit = (n: ts.Node) => {
        if (ts.isMethodDeclaration(n) && n.name.getText(ast) === "step")
          found = n;
        ts.forEachChild(n, visit);
      };
      visit(ast);
      return ts
        .createPrinter({ removeComments: true })
        .printNode(ts.EmitHint.Unspecified, found!, ast);
    };
    expect(method("src/characters/RegistryMotion.ts")).toBe(
      method(
        "docs/phase2a/approved-definition-snapshots/src/characters/RegistryMotion.ts",
      ),
    );
  });
  it("preserves frozen world pixels, collision, camera, tour, controller and Juni", () => {
    for (const [p, h] of Object.entries(
      json("docs/phase1/protected-world.json").protectedFiles,
    ))
      expect(digest(p), p).toBe(h);
    for (const [p, h] of Object.entries(
      json("docs/phase1/protected-juni.json").files,
    ))
      expect(digest(p), p).toBe(h);
  }, 20000); // Cold CI storage may need more than5s to hash the full frozen archive.
});
describe("twelve genuine identities, completed planned catalog", () => {
  it("has twelve playable identities and no remaining planned-only placeholders; no duplicate IDs", () => {
    expect(characterRegistry.all).toHaveLength(12);
    expect(characterRegistry.planned).toHaveLength(0);
    expect(
      new Set(
        [...characterRegistry.all, ...characterRegistry.planned].map(
          (v) => v.id,
        ),
      ).size,
    ).toBe(12);
    for (const slot of characterRegistry.planned) {
      expect(characterRegistry.get(slot.id)).toBeUndefined();
      expect(slot).not.toHaveProperty("assets");
      expect(characterRegistry.resolve(slot.id).id).toBe("juni");
    }
  });
  it("promotes a later data registration without changing gallery code", () => {
    const fixture = { ...characterRegistry.resolve("juni"), id: "sori" };
    const registry = new CharacterRegistry([
      characterRegistry.resolve("juni"),
      fixture,
    ]);
    expect(registry.get("sori")).toBeDefined();
    expect(registry.planned.some((v) => v.id === "sori")).toBe(false);
  });
  for (const id of ["ara", "doyun"])
    it(`${id}: real own atlas, eight distinct PNG poses for each four-direction gait and all transition/emote frames`, () => {
      const d = characterRegistry.get(id)!;
      expect(d.availability.status).toBe("playable");
      expect(d.assets!.texture).toContain(`/${id}/`);
      const atlas = json(`public/${d.assets!.atlas}`);
      expect(() => validateAtlas(d, atlas)).not.toThrow();
      expect(Object.keys(atlas.frames)).toHaveLength(112);
      for (const direction of ["front", "back", "left", "right"]) {
        for (const action of ["walk", "run"]) {
          const clip = d.animations[`${action}-${direction}`];
          expect(clip.frames).toHaveLength(8);
          expect(
            new Set(
              clip.frames.map((name) =>
                digest(
                  `assets-src/characters/phase2a/${id}/frames/${name}.png`,
                ),
              ),
            ).size,
          ).toBe(8);
        }
        for (const action of ["idle", "start", "stop"])
          expect(
            d.animations[`${action}-${direction}`].frames.length,
          ).toBeGreaterThan(1);
      }
      for (const action of ["wave", "celebrate"])
        expect(d.animations[`${action}-front`].frames).toHaveLength(8);
    });
});
describe("native cosmetic catalog and compatibility", () => {
  it("provides two hairstyles and two constructed outfits each for two identities, plus two accessories", () => {
    for (const id of ["ara", "doyun"])
      for (const category of ["hairstyle", "outfit"] as const)
        expect(compatibleItems(id, category).length).toBeGreaterThanOrEqual(2);
    expect(
      appearanceManifest.items.filter((v) => v.category === "accessory").length,
    ).toBeGreaterThanOrEqual(2);
    expect(new Set(appearanceManifest.items.map((v) => v.id)).size).toBe(
      appearanceManifest.items.length,
    );
  });
  it("every item and ownership interaction registers every actual animation frame at native dimensions", () => {
    const variants = appearanceManifest.items
      .flatMap((item) => item.variants)
      .concat((appearanceManifest.interactions ?? []).map((v) => v.patch));
    for (const v of variants) {
      const d = characterRegistry.get(v.characterId)!;
      expect(d.availability.status).toBe("playable");
      expect(v.registration).toMatchObject({
        width: 96,
        height: 112,
        anchor: [48, 100],
        sampling: "nearest",
      });
      for (const field of [
        "paint",
        "erase",
        "mapping",
        "preview",
        "provenance",
      ] as const)
        expect(existsSync(`public/${v[field]}`), v[field]).toBe(true);
      expect(Object.keys(json(`public/${v.mapping}`).frames).sort()).toEqual(
        Object.keys(json(`public/${d.assets!.atlas}`).frames).sort(),
      );
    }
  });
  it("rejects duplicate item IDs and invalid registration, and never equips incompatible/unknown categories", () => {
    const duplicate = structuredClone(appearanceManifest);
    duplicate.items.push(duplicate.items[0]);
    expect(() => validateAppearanceManifest(duplicate)).toThrow();
    const bad = structuredClone(appearanceManifest);
    bad.items[0].variants[0].registration.anchor[0] = 47 as 48;
    expect(() => validateAppearanceManifest(bad)).toThrow();
    expect(
      normalizeAppearance("juni", { ...look(), characterId: "juni" }),
    ).toEqual(defaultAppearance("juni"));
    expect(
      normalizeAppearance("ara", {
        ...look(),
        hairstyleId: "doyun-curly-crop",
        outfitId: "ara-braided-bun",
        accessoryIds: ["unknown", "ara-shell-barrette", "ara-shell-barrette"],
      }),
    ).toEqual({
      ...defaultAppearance("ara"),
      accessoryIds: ["ara-shell-barrette"],
    });
    expect(
      normalizeAppearance("ara", { ...look(), schemaVersion: 99 }),
    ).toEqual(defaultAppearance("ara"));
  });
  it("all36 supported combinations match direct own-layer construction across4,032 poses", () => {
    const qa = json("docs/phase2a/composition-qa.json");
    for (const [p, h] of Object.entries(qa.assetSHA256))
      expect(digest(p), p).toBe(h);
    expect(qa.combinations).toHaveLength(36);
    expect(qa.failures).toHaveLength(0);
    expect(
      qa.combinations.reduce(
        (n: number, row: { frames: number }) => n + row.frames,
        0,
      ),
    ).toBe(4032);
    expect(
      qa.combinations.every(
        (row: { differentPixelsFromDirectOwnLayerReference: number }) =>
          row.differentPixelsFromDirectOwnLayerReference === 0,
      ),
    ).toBe(true);
  });
});
describe("appearance persistence remains independent from world/learning state", () => {
  it("reads legacy v1 selection without rewriting it, while starting with original appearance", () => {
    const s = storage(),
      legacy = '{"version":1,"characterId":"haneul"}';
    s.values.set(PREFERENCES_KEY, legacy);
    s.values.set("learning-progress-sentinel", "KEEP");
    const p = new AppearancePreferences(s, characterRegistry);
    expect(
      new CharacterPreferences(s, characterRegistry).read().characterId,
    ).toBe("haneul");
    expect(p.read("haneul")).toEqual(defaultAppearance("haneul"));
    expect(s.values.get(PREFERENCES_KEY)).toBe(legacy);
    expect(s.values.has(APPEARANCE_PREFERENCES_KEY)).toBe(false);
  });
  it("round-trips all appearance categories, a named preset and defaults; retains per-character looks and unrelated keys", () => {
    const s = storage();
    s.values.set("world-position-sentinel", "[2048,1930]");
    s.values.set("visited-sentinel", "station");
    s.values.set("lesson-progress-sentinel", "KEEP");
    const p = new AppearancePreferences(s, characterRegistry);
    expect(p.save(look(), "Ngày biển")).toBe(true);
    expect(new AppearancePreferences(s, characterRegistry).read("ara")).toEqual(
      look(),
    );
    expect(p.presets().some((v) => v.name === "Ngày biển")).toBe(true);
    p.save(defaultAppearance("doyun"));
    expect(p.read("ara")).toEqual(look());
    p.save(defaultAppearance("ara"));
    expect(p.read("ara")).toEqual(defaultAppearance("ara"));
    expect(s.values.get("lesson-progress-sentinel")).toBe("KEEP");
    expect(s.values.get("visited-sentinel")).toBe("station");
    expect(s.values.get("world-position-sentinel")).toBe("[2048,1930]");
  });
  it("handles invalid cosmetic references, unknown store versions and blocked/quota-exhausted storage safely", () => {
    const s = storage();
    s.values.set(PREFERENCES_KEY, '{"version":1,"characterId":"bomi"}');
    s.values.set(
      APPEARANCE_PREFERENCES_KEY,
      JSON.stringify({
        version: 2,
        appearances: { bomi: { ...look(), characterId: "bomi" } },
        presets: [
          null,
          {},
          { id: "bad", name: "bad", appearance: { characterId: "unknown" } },
        ],
      }),
    );
    expect(
      new AppearancePreferences(s, characterRegistry).read("bomi"),
    ).toEqual(defaultAppearance("bomi"));
    s.values.set(APPEARANCE_PREFERENCES_KEY, '{"version":99,"appearances":{}}');
    expect(
      new AppearancePreferences(s, characterRegistry).read("bomi"),
    ).toEqual(defaultAppearance("bomi"));
    const blocked = new AppearancePreferences(
      {
        getItem() {
          throw Error("blocked");
        },
        setItem() {
          throw Error("quota");
        },
      },
      characterRegistry,
    );
    expect(blocked.save(look())).toBe(false);
    expect(blocked.read("ara")).toEqual(look());
  });
});
class LiveSprite implements PlayerSprite {
  frame = "idle-front-0";
  key = "juni";
  dead = false;
  x = 2598.5;
  y = 2760;
  data = "juni";
  setPosition(x: number, y: number) {
    this.x = x;
    this.y = y;
    return this;
  }
  setDepth() {
    return this;
  }
  setFrame(f: string) {
    this.frame = f;
    return this;
  }
  setVisible() {
    return this;
  }
  setTexture(key: string, frame?: string) {
    this.key = key;
    if (frame) this.frame = frame;
    return this;
  }
  setData(_key: string, value: string) {
    this.data = value;
    return this;
  }
  destroy() {
    this.dead = true;
  }
}
describe("transactional cosmetics on the existing single sprite", () => {
  it("keeps sprite, coordinates and phase for appearance-only changes; handles missing cosmetic fallback", async () => {
    const s = storage(),
      prefs = new CharacterPreferences(s, characterRegistry),
      appearances = new AppearancePreferences(s, characterRegistry),
      sprite = new LiveSprite();
    let creates = 0;
    let fallback = false;
    const manager = new PlayerCharacterManager(
      {
        async ensure(def, appearance) {
          return {
            definition: {
              ...def,
              assets: {
                ...def.assets!,
                key: fallback
                  ? def.assets!.key
                  : "studio-" + appearanceKey(appearance!),
              },
            },
            appearance: fallback ? defaultAppearance(def.id) : appearance!,
          };
        },
      },
      () => {
        creates++;
        return sprite;
      },
      prefs,
      characterRegistry.get("ara")!,
      { x: sprite.x, y: sprite.y },
      characterRegistry,
      appearances,
    );
    const motion = manager.motion as RegistryMotion;
    motion.phase = 0.375;
    await manager.select("ara", { x: sprite.x, y: sprite.y }, look());
    expect(manager.sprite).toBe(sprite);
    expect(manager.motion).toBe(motion);
    expect(motion.phase).toBe(0.375);
    expect(creates).toBe(1);
    expect(sprite).toMatchObject({ x: 2598.5, y: 2760, dead: false });
    expect(manager.appearance).toEqual(look());
    fallback = true;
    await manager.select(
      "doyun",
      { x: sprite.x, y: sprite.y },
      { ...look(), characterId: "doyun" },
    );
    expect(manager.appearance).toEqual(defaultAppearance("doyun"));
    expect(creates).toBe(1);
    expect(sprite.data).toBe("doyun");
  });
  it("a failed load or scene shutdown cannot replace/save an in-flight choice", async () => {
    const s = storage(),
      sprite = new LiveSprite();
    let finish!: () => void;
    const loading = new Promise<void>((resolve) => {
      finish = resolve;
    });
    const manager = new PlayerCharacterManager(
      { ensure: () => loading },
      () => sprite,
      new CharacterPreferences(s, characterRegistry),
      characterRegistry.resolve("juni"),
      { x: 0, y: 0 },
    );
    const task = manager.select("ara", { x: 0, y: 0 }, look());
    manager.dispose();
    finish();
    await expect(task).rejects.toThrow("Scene changed");
    expect(s.values.size).toBe(0);
  });
  it("cache ownership is bounded and touches keep recently used entries", () => {
    const cache = new BoundedCache<string, number>(2);
    cache.set("a", 1);
    cache.set("b", 2);
    expect(cache.get("a")).toBe(1);
    cache.set("c", 3);
    expect(cache.get("b")).toBeUndefined();
    expect(cache.size).toBe(2);
    cache.clear();
    expect(cache.size).toBe(0);
    expect(() => new BoundedCache(0)).toThrow();
  });
});
