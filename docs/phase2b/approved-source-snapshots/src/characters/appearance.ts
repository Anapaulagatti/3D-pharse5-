import rawManifest from "../../assets-src/characters/phase2a/cosmetics/catalog.json";
import type {
  AppearanceManifest,
  CharacterAppearance,
  CosmeticCategory,
  CosmeticItem,
} from "./appearanceTypes";
const idPattern = /^[a-z][a-z0-9-]*$/;
export function validateAppearanceManifest(
  value: AppearanceManifest,
): AppearanceManifest {
  if (
    value.schemaVersion !== 1 ||
    !Array.isArray(value.items) ||
    !Array.isArray(value.presets)
  )
    throw Error("Invalid appearance manifest");
  const ids = new Set<string>();
  for (const item of value.items) {
    if (!idPattern.test(item.id) || ids.has(item.id))
      throw Error("Invalid/duplicate cosmetic ID");
    ids.add(item.id);
    if (
      !["hairstyle", "outfit", "accessory"].includes(item.category) ||
      !item.name.vi ||
      !item.name.ko ||
      !item.name.en
    )
      throw Error("Invalid cosmetic definition");
    if (!item.compatibility.characterIds.length)
      throw Error("Empty cosmetic compatibility");
    if (!["free-review", "unavailable"].includes(item.availability.status))
      throw Error("Invalid cosmetic availability");
    for (const characterId of item.compatibility.characterIds) {
      const variant = item.variants.find((v) => v.characterId === characterId);
      if (
        !variant ||
        !variant.paint ||
        !variant.erase ||
        !variant.mapping ||
        !variant.preview ||
        !variant.provenance ||
        variant.registration.width !== 96 ||
        variant.registration.height !== 112 ||
        variant.registration.anchor[0] !== 48 ||
        variant.registration.anchor[1] !== 100 ||
        variant.registration.sampling !== "nearest" ||
        variant.registration.occlusion !== "baked-native-visibility"
      )
        throw Error(`Invalid cosmetic registration: ${item.id}`);
    }
  }
  for (const interaction of value.interactions ?? []) {
    if (
      !idPattern.test(interaction.id) ||
      ids.has(interaction.id) ||
      interaction.requiresItemIds.length < 2 ||
      interaction.requiresItemIds.some(
        (id) =>
          !value.items.some(
            (item) =>
              item.id === id &&
              item.compatibility.characterIds.includes(interaction.characterId),
          ),
      )
    )
      throw Error("Invalid cosmetic interaction");
    ids.add(interaction.id);
    const v = interaction.patch;
    if (
      !["before-accessories", "after-accessories"].includes(
        interaction.applyPhase,
      ) ||
      v.characterId !== interaction.characterId ||
      !v.paint ||
      !v.erase ||
      !v.mapping ||
      !v.preview ||
      !v.provenance ||
      v.registration.width !== 96 ||
      v.registration.height !== 112 ||
      v.registration.anchor[0] !== 48 ||
      v.registration.anchor[1] !== 100 ||
      v.registration.sampling !== "nearest" ||
      v.registration.occlusion !== "baked-native-visibility"
    )
      throw Error("Invalid interaction registration");
  }
  return value;
}
export const appearanceManifest = validateAppearanceManifest(
  rawManifest as AppearanceManifest,
);
export function defaultAppearance(characterId: string): CharacterAppearance {
  return {
    schemaVersion: 2,
    characterId,
    hairstyleId: null,
    outfitId: null,
    accessoryIds: [],
  };
}
export function compatibleItems(
  characterId: string,
  category?: CosmeticCategory,
  manifest = appearanceManifest,
) {
  return manifest.items.filter(
    (item) =>
      item.availability.status === "free-review" &&
      item.compatibility.characterIds.includes(characterId) &&
      (!category || category === item.category),
  );
}
export function normalizeAppearance(
  characterId: string,
  value: unknown,
  manifest = appearanceManifest,
): CharacterAppearance {
  const result = defaultAppearance(characterId);
  if (
    !value ||
    typeof value !== "object" ||
    !("characterId" in value) ||
    value.characterId !== characterId
  )
    return result;
  const q = value as Partial<CharacterAppearance>;
  if (q.schemaVersion !== 2) return result;
  const selected: CosmeticItem[] = [];
  const accept = (id: unknown, category: CosmeticCategory) => {
    if (typeof id !== "string") return null;
    const item = compatibleItems(characterId, category, manifest).find(
      (v) => v.id === id,
    );
    if (
      !item ||
      selected.some(
        (other) =>
          other.compatibility.excludes?.includes(id) ||
          item.compatibility.excludes?.includes(other.id),
      )
    )
      return null;
    selected.push(item);
    return item.id;
  };
  result.hairstyleId = accept(q.hairstyleId, "hairstyle");
  result.outfitId = accept(q.outfitId, "outfit");
  for (const id of Array.isArray(q.accessoryIds)
    ? [...new Set(q.accessoryIds)].sort().slice(0, 8)
    : []) {
    const accepted = accept(id, "accessory");
    if (accepted) result.accessoryIds.push(accepted);
  }
  return result;
}
export function appearanceItemIds(look: CharacterAppearance) {
  return [look.hairstyleId, look.outfitId, ...look.accessoryIds].filter(
    (id): id is string => !!id,
  );
}
export function appearanceKey(look: CharacterAppearance) {
  return `${look.characterId}:${appearanceItemIds(look).join("+") || "default"}`;
}
export function appearanceIsDefault(look: CharacterAppearance) {
  return appearanceItemIds(look).length === 0;
}
