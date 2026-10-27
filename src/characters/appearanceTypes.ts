/** Cosmetics are visual-only. Unlock ownership is deliberately a separate contract. */
export type CosmeticCategory = "hairstyle" | "outfit" | "accessory";
export interface CosmeticCompatibility {
  characterIds: string[];
  excludes?: string[];
}
export interface CosmeticVariant {
  /** Binds patches to an exact approved base; mismatch safely falls back. */
  baseAtlasSHA256?: string;
  poseRevision?: string;
  assetRevision?: string;
  characterId: string;
  paint: string;
  erase: string;
  mapping: string;
  preview: string;
  registration: {
    width: 96;
    height: 112;
    anchor: [48, 100];
    sampling: "nearest";
    occlusion: "baked-native-visibility";
  };
  provenance: string;
}
export interface CosmeticItem {
  id: string;
  name: { vi: string; ko: string; en: string };
  category: CosmeticCategory;
  compatibility: CosmeticCompatibility;
  variants: CosmeticVariant[];
  /** Future reward provenance; no economy/ownership claim is implemented. */
  rewardOrigins?: CosmeticRewardOrigin[];
  availability: {
    status: "free-review" | "unavailable";
    reason: string;
    acquisition?:
      | { kind: "free-review" }
      | {
          kind: "server-entitlement";
          entitlementId: string;
          origins: CosmeticRewardOrigin[];
        };
  };
}
export interface CharacterAppearance {
  schemaVersion: 2;
  characterId: string;
  hairstyleId: string | null;
  outfitId: string | null;
  accessoryIds: string[];
}
export interface AppearancePreset {
  id: string;
  name: string;
  appearance: CharacterAppearance;
}
export interface AppearanceManifest {
  schemaVersion: 1;
  items: CosmeticItem[];
  presets: AppearancePreset[];
  interactions?: AppearanceInteraction[];
}
export interface CosmeticPatchRect {
  x: number;
  y: number;
  w: number;
  h: number;
  offsetX: number;
  offsetY: number;
}
export interface CosmeticPatchMapping {
  schemaVersion: 1;
  characterId: string;
  frames: Record<string, CosmeticPatchRect | null>;
  baseAtlasSHA256?: string;
}
/** Future authoritative unlock providers validate ownership server-side. Local review
 * availability is never proof of a shop purchase, quest or lesson completion. */
export interface CosmeticOwnershipProvider {
  ownedItems(): Promise<ReadonlySet<string>>;
  canEquip(itemId: string): Promise<boolean>;
}
export type CosmeticRewardOrigin =
  | "shop"
  | "quest"
  | "crafting"
  | "learning-achievement"
  | "exploration"
  | "event";
export interface CosmeticRewardRequest {
  itemId: string;
  origin: CosmeticRewardOrigin;
  serverReceipt: string;
}
/** Small baked ownership corrections for non-commuting garment/head occlusion.
 * These are sparse patch packs, not eagerly generated combination atlases. */
export interface AppearanceInteraction {
  id: string;
  characterId: string;
  requiresItemIds: string[];
  applyPhase: "before-accessories" | "after-accessories";
  patch: CosmeticVariant;
}
