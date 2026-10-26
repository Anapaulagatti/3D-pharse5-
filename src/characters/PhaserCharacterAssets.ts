import type Phaser from "phaser";
import {
  validateAtlas,
  type AtlasData,
  type CharacterDefinition,
} from "./types";
/** Load/validate every atlas frame before a sprite can replace the live player. */
export class PhaserCharacterAssets {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly base: string,
  ) {}
  async ensure(def: CharacterDefinition) {
    if (!def.assets) throw Error(`No completed atlas for ${def.id}`);
    const signal = AbortSignal.timeout(15000);
    const response = await fetch(this.base + def.assets.atlas, { signal });
    if (!response.ok) throw Error(`Missing atlas: ${def.id}`);
    const atlas: AtlasData = await response.json();
    validateAtlas(def, atlas);
    if (this.scene.textures.exists(def.assets.key)) return;
    const imageResponse = await fetch(this.base + def.assets.texture, {
      signal,
    });
    if (!imageResponse.ok) throw Error(`Missing texture: ${def.id}`);
    const url = URL.createObjectURL(await imageResponse.blob());
    try {
      const source = new Image();
      source.src = url;
      await source.decode();
      for (const q of Object.values(atlas.frames)) {
        const f = q.frame;
        if (f.x + f.w > source.naturalWidth || f.y + f.h > source.naturalHeight)
          throw Error(`Frame exceeds decoded image: ${def.id}`);
      }
      this.scene.textures.addAtlas(def.assets.key, source, atlas);
      this.scene.textures.get(def.assets.key).setFilter(1);
    } finally {
      URL.revokeObjectURL(url);
    }
  }
}
