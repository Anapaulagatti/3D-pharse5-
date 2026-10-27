import type { CharacterDefinition, AtlasData } from "./types";
import { validateAtlas } from "./types";
import {
  appearanceManifest,
  appearanceItemIds,
  appearanceKey,
  defaultAppearance,
  normalizeAppearance,
} from "./appearance";
import type {
  AppearanceManifest,
  CharacterAppearance,
  CosmeticPatchMapping,
} from "./appearanceTypes";
export class BoundedCache<K, V> {
  private entries = new Map<K, V>();
  constructor(readonly limit: number) {
    if (!Number.isInteger(limit) || limit < 1)
      throw Error("Positive cache limit required");
  }
  get(key: K) {
    const value = this.entries.get(key);
    if (value !== undefined) {
      this.entries.delete(key);
      this.entries.set(key, value);
    }
    return value;
  }
  set(key: K, value: V) {
    this.entries.delete(key);
    this.entries.set(key, value);
    while (this.entries.size > this.limit)
      this.entries.delete(this.entries.keys().next().value!);
  }
  clear() {
    this.entries.clear();
  }
  values() {
    return [...this.entries.values()];
  }
  get size() {
    return this.entries.size;
  }
}
interface BaseImage {
  digest?: string;
  image: HTMLImageElement;
  atlas: AtlasData;
}
export interface RenderedAppearance {
  image: HTMLImageElement | HTMLCanvasElement;
  atlas: AtlasData;
  key: string;
  appearance: CharacterAppearance;
  fallbackReason?: string;
}
/** Native-frame composition runs once when a look is requested, never per gameplay
 * frame. Packed erase/paint rectangles already own anatomical depth/visibility. */
export class AppearanceRenderer {
  private bases = new BoundedCache<string, BaseImage>(2);
  private digests = new WeakMap<HTMLImageElement,string>();
  private composites = new BoundedCache<string, RenderedAppearance>(2);
  private pendingBases = new Map<string, Promise<BaseImage>>();
  private queue: Promise<unknown> = Promise.resolve();
  private compositions = 0;
  constructor(private manifest: AppearanceManifest = appearanceManifest) {}
  async base(def: CharacterDefinition, base: string): Promise<BaseImage> {
    if (!def.assets) throw Error("No native character asset");
    const id = base + def.assets.texture,
      cached = this.bases.get(id);
    if (cached) return cached;
    if (this.pendingBases.has(id)) return this.pendingBases.get(id)!;
    const task = (async () => {
      const response = await fetch(base + def.assets!.atlas, {
        signal: AbortSignal.timeout(15000),
      });
      if (!response.ok) throw Error("Missing native preview atlas");
      const atlas: AtlasData = await response.json();
      validateAtlas(def, atlas);
      const image = await this.image(base + def.assets!.texture, undefined, true);
      for (const { frame: f } of Object.values(atlas.frames))
        if (f.x + f.w > image.naturalWidth || f.y + f.h > image.naturalHeight)
          throw Error("Frame outside native texture");
      const asset = { image, atlas, digest: this.digests.get(image) };
      this.bases.set(id, asset);
      return asset;
    })();
    this.pendingBases.set(id, task);
    try {
      return await task;
    } finally {
      this.pendingBases.delete(id);
    }
  }
  private async image(path: string, signal?: AbortSignal, trackDigest = false) {
    const response = await fetch(path, {
      signal: signal ?? AbortSignal.timeout(15000),
    });
    if (!response.ok) throw Error("Missing native cosmetic image");
    const blob = await response.blob();
    const digest = trackDigest ? Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",await blob.arrayBuffer())),v=>v.toString(16).padStart(2,"0")).join("") : undefined;
    const url = URL.createObjectURL(blob);
    try {
      const image = new Image();
      if(digest) this.digests.set(image,digest);
      image.src = url;
      await image.decode();
      return image;
    } finally {
      URL.revokeObjectURL(url);
    }
  }
  async render(
    def: CharacterDefinition,
    requested: unknown,
    base: string,
    signal?: AbortSignal,
  ): Promise<RenderedAppearance> {
    const appearance = normalizeAppearance(def.id, requested, this.manifest),
      source = await this.base(def, base);
    signal?.throwIfAborted();
    const original: RenderedAppearance = {
      ...source,
      key: def.assets!.key,
      appearance: defaultAppearance(def.id),
    };
    if (!appearanceItemIds(appearance).length) return original;
    const revision = appearanceItemIds(appearance).map(id=>this.manifest.items.find(i=>i.id===id)!.variants.find(v=>v.characterId===def.id)!.assetRevision ?? "legacy").join("-");
    const key = `studio-${appearanceKey(appearance)}-${revision}`,
      cached = this.composites.get(base + key);
    if (cached) return cached;
    const work = async () => {
      signal?.throwIfAborted();
      const again = this.composites.get(base + key);
      if (again) return again;
      const canvas = document.createElement("canvas");
      canvas.width = source.image.naturalWidth;
      canvas.height = source.image.naturalHeight;
      const ctx = canvas.getContext("2d", { willReadFrequently: false })!;
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(source.image, 0, 0);
      try {
        const selectedIds = appearanceItemIds(appearance);
        const selected = selectedIds.map((id) =>
          this.manifest.items.find((item) => item.id === id)!,
        );
        const interactions = (this.manifest.interactions ?? []).filter(
          (i) =>
            i.characterId === def.id &&
            i.requiresItemIds.every((id) => selectedIds.includes(id)),
        );
        const variantFor = (item: (typeof selected)[number]) =>
          item.variants.find((v) => v.characterId === def.id)!;
        const variants = [
          ...selected
            .filter((item) => item.category !== "accessory")
            .map(variantFor),
          ...interactions
            .filter((i) => i.applyPhase === "before-accessories")
            .map((i) => i.patch),
          ...selected
            .filter((item) => item.category === "accessory")
            .map(variantFor),
          ...interactions
            .filter((i) => i.applyPhase === "after-accessories")
            .map((i) => i.patch),
        ];
        for (const variant of variants) {
          if(variant.baseAtlasSHA256 && variant.baseAtlasSHA256 !== source.digest) throw Error("Cosmetic pose revision mismatch");
          signal?.throwIfAborted();
          const response = await fetch(base + variant.mapping, {
            signal: signal ?? AbortSignal.timeout(15000),
          });
          if (!response.ok) throw Error("Missing cosmetic registration");
          const mapping: CosmeticPatchMapping = await response.json();
          if (mapping.schemaVersion !== 1 || mapping.characterId !== def.id)
            throw Error("Cosmetic identity mismatch");
          const [paint, erase] = await Promise.all([
            this.image(base + variant.paint, signal),
            this.image(base + variant.erase, signal),
          ]);
          for (const [name, { frame }] of Object.entries(source.atlas.frames)) {
            if (!(name in mapping.frames))
              throw Error(`Unregistered cosmetic frame ${name}`);
            const rect = mapping.frames[name];
            if (!rect) continue; // explicit baked occlusion
            if (
              ![
                rect.x,
                rect.y,
                rect.w,
                rect.h,
                rect.offsetX,
                rect.offsetY,
              ].every(Number.isInteger) ||
              rect.w < 1 ||
              rect.h < 1 ||
              rect.x < 0 ||
              rect.y < 0 ||
              rect.x + rect.w > paint.width ||
              rect.y + rect.h > paint.height ||
              paint.width !== erase.width ||
              paint.height !== erase.height ||
              rect.offsetX < 0 ||
              rect.offsetY < 0 ||
              rect.offsetX + rect.w > frame.w ||
              rect.offsetY + rect.h > frame.h
            )
              throw Error("Invalid native cosmetic rectangle");
            const x = frame.x + rect.offsetX,
              y = frame.y + rect.offsetY;
            ctx.globalCompositeOperation = "destination-out";
            ctx.drawImage(
              erase,
              rect.x,
              rect.y,
              rect.w,
              rect.h,
              x,
              y,
              rect.w,
              rect.h,
            );
            ctx.globalCompositeOperation = "source-over";
            ctx.drawImage(
              paint,
              rect.x,
              rect.y,
              rect.w,
              rect.h,
              x,
              y,
              rect.w,
              rect.h,
            );
          }
        }
        signal?.throwIfAborted();
        const result: RenderedAppearance = {
          image: canvas,
          atlas: source.atlas,
          appearance,
          key,
        };
        this.composites.set(base + key, result);
        this.compositions++;
        return result;
      } catch (error) {
        if (signal?.aborted) throw error;
        return {
          ...original,
          fallbackReason:
            "Unavailable cosmetic asset; approved default restored",
        };
      }
    };
    const task = this.queue.then(work, work);
    this.queue = task.catch(() => undefined);
    return task;
  }
  snapshot() {
    return {
      baseImages: this.bases.size,
      baseLimit: this.bases.limit,
      compositeImages: this.composites.size,
      compositeLimit: this.composites.limit,
      pendingBaseLoads: this.pendingBases.size,
      compositions: this.compositions,
      estimatedBaseBytes: this.bases
        .values()
        .reduce((n, v) => n + v.image.width * v.image.height * 4, 0),
      estimatedCompositeBytes: this.composites
        .values()
        .reduce((n, v) => n + v.image.width * v.image.height * 4, 0),
    };
  }
  clear() {
    this.bases.clear();
    this.composites.clear();
  }
}
export const appearanceRenderer = new AppearanceRenderer();
