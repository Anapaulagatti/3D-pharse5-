import type Phaser from "phaser";
import type { CharacterDefinition } from "./types";
import type { CharacterAppearance } from "./appearanceTypes";
import { appearanceRenderer } from "./AppearanceRenderer";
import {
  appearanceIsDefault,
  appearanceKey,
  defaultAppearance,
  normalizeAppearance,
} from "./appearance";
/** Only the requested atlas is loaded. Three live actor textures at most; world
 * textures have separate ownership and are never touched by this cache. */
export class PhaserCharacterAssets {
  private lru = new Map<string, true>();
  private activeKey = "";
  private closed = false;
  readonly limit = 3;
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly base: string,
  ) {}
  private touch(key: string) {
    this.lru.delete(key);
    this.lru.set(key, true);
  }
  async ensure(def: CharacterDefinition, requested?: CharacterAppearance) {
    if (this.closed) throw Error("Character asset owner disposed");
    if (!def.assets) throw Error(`No completed atlas for ${def.id}`);
    let appearance = normalizeAppearance(
      def.id,
      requested ?? defaultAppearance(def.id),
    );
    let key = appearanceIsDefault(appearance)
      ? def.assets.key
      : `studio-${appearanceKey(appearance)}`;
    let fallbackReason: string | undefined;
    if (!this.scene.textures.exists(key)) {
      const rendered = await appearanceRenderer.render(
        def,
        appearance,
        this.base,
      );
      key = rendered.key;
      appearance = rendered.appearance;
      fallbackReason = rendered.fallbackReason;
      if (this.closed) throw Error("Character scene closed during load");
      if (!this.scene.textures.exists(key)) {
        const source =
          rendered.image instanceof HTMLCanvasElement
            ? this.scene.textures.addCanvas(key, rendered.image)
            : rendered.image;
        if (!source) throw Error("Native texture registration failed");
        this.scene.textures.addAtlas(key, source, rendered.atlas);
      }
    }
    this.scene.textures.get(key).setFilter(1);
    this.touch(key);
    const definition =
      key === def.assets.key ? def : { ...def, assets: { ...def.assets, key } };
    return { definition, appearance, fallbackReason };
  }
  activate(def: CharacterDefinition) {
    if (!def.assets) return;
    this.activeKey = def.assets.key;
    this.touch(this.activeKey);
    for (const key of [...this.lru.keys()]) {
      if (this.lru.size <= this.limit) break;
      if (key !== this.activeKey) {
        this.scene.textures.remove(key);
        this.lru.delete(key);
      }
    }
  }
  snapshot() {
    const textures = [...this.lru.keys()]
      .filter((key) => this.scene.textures.exists(key))
      .map((key) => {
        const source = this.scene.textures.get(key).getSourceImage() as
          HTMLImageElement | HTMLCanvasElement;
        return {
          key,
          width: source.width,
          height: source.height,
          estimatedBytes: source.width * source.height * 4,
        };
      });
    return {
      activeKey: this.activeKey,
      limit: this.limit,
      textures,
      estimatedBytes: textures.reduce((n, t) => n + t.estimatedBytes, 0),
      composition: appearanceRenderer.snapshot(),
    };
  }
  dispose() {
    this.closed = true;
    for (const key of this.lru.keys()) this.scene.textures.remove(key);
    this.lru.clear();
  }
}
