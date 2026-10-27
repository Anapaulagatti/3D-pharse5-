import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import {
  appearanceManifest,
  compatibleItems,
  defaultAppearance,
  normalizeAppearance,
  validateAppearanceManifest,
} from "../../../src/characters/appearance";
import {
  AppearancePreferences,
  CharacterPreferences,
  PREFERENCES_KEY,
  APPEARANCE_PREFERENCES_KEY,
  MAX_APPEARANCE_PRESETS,
} from "../../../src/characters/preferences";
import { characterRegistry } from "../../../src/characters/registry";
import { sha256Fallback } from "../../../src/characters/assetDigest";
import { BoundedCache } from "../../../src/characters/AppearanceRenderer";
const json = (p: string) => JSON.parse(readFileSync(p, "utf8"));
const old = json("assets-src/characters/phase2a/cosmetics/catalog.json");
const bindings = json("assets-src/characters/phase2c/base-bindings.json");
const storage = () => {
  const values = new Map<string, string>();
  return {
    values,
    getItem: (k: string) => values.get(k) ?? null,
    setItem: (k: string, v: string) => {
      values.set(k, v);
    },
  };
};
describe("Phase2C approved-pose wardrobe", () => {
  it("has28 genuine definitions, retains10 stable legacy IDs and supplies18 new designs", () => {
    expect(appearanceManifest.items).toHaveLength(28);
    expect(new Set(appearanceManifest.items.map((i) => i.id)).size).toBe(28);
    for (const i of old.items)
      expect(appearanceManifest.items.some((n) => n.id === i.id)).toBe(true);
    for (const category of ["hairstyle", "outfit", "accessory"] as const)
      expect(
        appearanceManifest.items.filter(
          (i) => i.id.startsWith("kr-") && i.category === category,
        ),
      ).toHaveLength(6);
  });
  it("every active identity has a registered hair,outfit,accessory and curated full alternative", () => {
    for (const def of characterRegistry.all) {
      for (const c of ["hairstyle", "outfit", "accessory"] as const)
        expect(compatibleItems(def.id, c).length).toBeGreaterThanOrEqual(1);
      const preset = appearanceManifest.presets.find(
        (p) => p.id === "fashion-" + def.id,
      )!;
      expect(preset.appearance.hairstyleId).toBeTruthy();
      expect(preset.appearance.outfitId).toBeTruthy();
      expect(preset.appearance.accessoryIds.length).toBeGreaterThan(0);
      expect(normalizeAppearance(def.id, preset.appearance)).toEqual(
        preset.appearance,
      );
    }
  });
  it("all claimed variant/frame mappings bind exact approved pixels and cover complete native atlases", () => {
    for (const item of appearanceManifest.items)
      for (const v of item.variants) {
        expect(v.baseAtlasSHA256).toBe(bindings[v.characterId]);
        expect(v.assetRevision).toMatch(/^[a-f0-9]{36}$/);
        for (const p of [v.paint, v.erase, v.mapping, v.preview, v.provenance])
          expect(existsSync("public/" + p)).toBe(true);
        const source =
          v.characterId === "juni"
            ? "public/assets/juni/juni.json"
            : `public/assets/characters/${v.characterId}/atlas.json`;
        const m = json("public/" + v.mapping);
        expect(Object.keys(m.frames).sort()).toEqual(
          Object.keys(json(source).frames).sort(),
        );
        expect(m.baseAtlasSHA256).toBe(bindings[v.characterId]);
      }
  });
  it("rejects invented universal variants and duplicate registrations", () => {
    const m = structuredClone(appearanceManifest);
    m.items[0].compatibility.characterIds.push("unknown");
    expect(() => validateAppearanceManifest(m)).toThrow();
    const n = structuredClone(appearanceManifest);
    n.items[0].variants.push(n.items[0].variants[0]);
    expect(() => validateAppearanceManifest(n)).toThrow();
  });
  it("hat exclusions and unsupported character pairs normalize safely without changing the identity", () => {
    const q = normalizeAppearance("doyun", {
      ...defaultAppearance("doyun"),
      hairstyleId: "doyun-curly-crop",
      accessoryIds: ["kr-garden-hat"],
    });
    expect(q.hairstyleId).toBe("doyun-curly-crop");
    expect(q.accessoryIds).toEqual([]);
    expect(
      normalizeAppearance("juni", {
        ...defaultAppearance("juni"),
        outfitId: "kr-campus",
      }),
    ).toEqual(defaultAppearance("juni"));
  });
  it("original defaults remain fully reversible and cosmetics carry no economy claim", () => {
    for (const d of characterRegistry.all)
      expect(normalizeAppearance(d.id, defaultAppearance(d.id))).toEqual(
        defaultAppearance(d.id),
      );
    for (const i of appearanceManifest.items)
      expect(i.availability.status).toBe("free-review");
  });
});
describe("non-destructive local personalization", () => {
  it("retains v1 selection and existing v2 looks,presets,world and progress keys", () => {
    const s = storage();
    const legacy = '{"version":1,"characterId":"ara"}';
    s.values.set(PREFERENCES_KEY, legacy);
    s.values.set("world-position-sentinel", "[2048,1930]");
    s.values.set("lesson-progress-sentinel", "KEEP");
    const look = old.presets[0].appearance;
    s.values.set(
      APPEARANCE_PREFERENCES_KEY,
      JSON.stringify({
        version: 2,
        selectedCharacterId: "ara",
        appearances: { ara: look },
        presets: [{ id: "local-kept", name: "Bộ cũ", appearance: look }],
      }),
    );
    const p = new AppearancePreferences(s, characterRegistry);
    expect(p.read("ara")).toEqual(look);
    expect(p.presets().some((v) => v.id === "local-kept")).toBe(true);
    expect(
      new CharacterPreferences(s, characterRegistry).read().characterId,
    ).toBe("ara");
    expect(s.values.get(PREFERENCES_KEY)).toBe(legacy);
    expect(s.values.get("lesson-progress-sentinel")).toBe("KEEP");
  });
  it("renames/deletes only personal presets without applying or losing another actor's look", () => {
    const s = storage(),
      p = new AppearancePreferences(s, characterRegistry);
    const a = appearanceManifest.presets.find(
      (v) => v.id === "fashion-sori",
    )!.appearance;
    expect(p.save(a, "Dạo phố")).toBe(true);
    const local = p.userPresets()[0];
    expect(p.renamePreset(local.id, "Ngày ở Seoul")).toBe(true);
    expect(p.userPresets()[0].name).toBe("Ngày ở Seoul");
    expect(p.read("sori")).toEqual(a);
    expect(p.deletePreset(local.id)).toBe(true);
    expect(p.read("sori")).toEqual(a);
    expect(p.renamePreset("fashion-sori", "bad")).toBe(false);
    expect(p.deletePreset("fashion-sori")).toBe(false);
  });
  it("bounds storage at12 without evicting old named looks; validates names and IDs", () => {
    const s = storage(),
      p = new AppearancePreferences(s, characterRegistry);
    for (let i = 0; i < MAX_APPEARANCE_PRESETS; i++)
      expect(p.save(defaultAppearance("juni"), "Bộ " + i)).toBe(true);
    const before = s.values.get(APPEARANCE_PREFERENCES_KEY);
    expect(p.save(defaultAppearance("sori"), "Bộ vượt giới hạn")).toBe(false);
    expect(s.values.get(APPEARANCE_PREFERENCES_KEY)).toBe(before);
    expect(p.userPresets()).toHaveLength(12);
    expect(p.canSavePreset("")).toBe(true);
    expect(p.canSavePreset("Bộ 0")).toBe(true);
    expect(p.renamePreset(p.userPresets()[0].id, "")).toBe(false);
    expect(p.renamePreset(p.userPresets()[0].id, "Bộ 1")).toBe(false);
  });
  it("makes a requested-item cache invalidation selective", () => {
    const c = new BoundedCache<string, { actor: string }>(2);
    c.set("a", { actor: "juni" });
    c.set("b", { actor: "sori" });
    c.deleteWhere((v) => v.actor === "juni");
    expect(c.get("a")).toBeUndefined();
    expect(c.get("b")?.actor).toBe("sori");
  });
});
describe("offline/LAN asset content binding", () => {
  for (const data of [
    new Uint8Array(),
    new TextEncoder().encode("abc"),
    new Uint8Array(100000).fill(171),
    new Uint8Array(readFileSync("public/assets/juni/juni.png")),
  ])
    it(`matches standardSHA256 for${data.length} bytes`, () =>
      expect(sha256Fallback(data)).toBe(
        createHash("sha256").update(data).digest("hex"),
      ));
});
