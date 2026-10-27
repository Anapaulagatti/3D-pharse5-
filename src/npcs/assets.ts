import Phaser from "phaser";
import { addNativeTexture } from "../gate3/NativeTexture";
import type { AtlasData } from "../characters/types";
import { validateNPCAtlas, type NPCDefinition } from "./types";
interface Asset {
  key: string;
  image: HTMLImageElement;
  atlas: AtlasData;
  bytes: number;
}
/** Separate bounded NPC ownership; never touches player/Studio/world textures. */
export class NPCAssetPool {
  readonly limit = 4;
  readonly concurrency = 2;
  readonly loaded = new Map<string, Asset>();
  readonly pending = new Map<string, AbortController>();
  errors: { id: string; message: string }[] = [];
  closed = false;
  loads = 0;
  evictions = 0;
  constructor(
    private scene: Phaser.Scene,
    private base: string,
  ) {}
  async load(
    def: NPCDefinition,
    wanted: ReadonlySet<string>,
  ): Promise<boolean> {
    if (this.loaded.has(def.id)) return true;
    if (
      this.closed ||
      this.pending.has(def.id) ||
      this.pending.size >= this.concurrency
    )
      return false;
    while (this.loaded.size + this.pending.size >= this.limit) {
      const removable = [...this.loaded.keys()].find((id) => !wanted.has(id));
      if (!removable) return false;
      this.remove(removable);
    }
    const abort = new AbortController();
    this.pending.set(def.id, abort);
    let url: string | undefined;
    let image: HTMLImageElement | undefined;
    try {
      const responses = await Promise.all([
        fetch(this.base + def.assets.texture, { signal: abort.signal }),
        fetch(this.base + def.assets.atlas, { signal: abort.signal }),
      ]);
      if (responses.some((r) => !r.ok)) throw Error("Missing NPC art");
      const [blob, atlas] = await Promise.all([
        responses[0].blob(),
        responses[1].json() as Promise<AtlasData>,
      ]);
      url = URL.createObjectURL(blob);
      image = new Image();
      image.src = url;
      await image.decode();
      abort.signal.throwIfAborted();
      validateNPCAtlas(def, atlas, image.naturalWidth, image.naturalHeight);
      if (this.closed || !wanted.has(def.id)) {
        image.src = "";
        return false;
      }
      addNativeTexture(this.scene, def.assets.key, image);
      const texture = this.scene.textures.get(def.assets.key);
      for (const [name, row] of Object.entries(atlas.frames)) {
        const f = row.frame;
        texture.add(name, 0, f.x, f.y, f.w, f.h);
      }
      this.loaded.set(def.id, {
        key: def.assets.key,
        image,
        atlas,
        bytes: image.naturalWidth * image.naturalHeight * 4,
      });
      this.loads++;
      return true;
    } catch (error) {
      if (image) image.src = "";
      if (!abort.signal.aborted) {
        this.errors.push({ id: def.id, message: String(error) });
        if (this.errors.length > 32) this.errors.shift();
      }
      return false;
    } finally {
      if (url) URL.revokeObjectURL(url);
      this.pending.delete(def.id);
    }
  }
  cancelUnwanted(wanted: ReadonlySet<string>) {
    for (const [id, c] of this.pending) if (!wanted.has(id)) c.abort();
  }
  remove(id: string) {
    const a = this.loaded.get(id);
    if (!a) return;
    this.scene.textures.remove(a.key);
    a.image.src = "";
    this.loaded.delete(id);
    this.evictions++;
  }
  close() {
    this.closed = true;
    for (const c of this.pending.values()) c.abort();
    for (const id of [...this.loaded.keys()]) this.remove(id);
  }
  snapshot() {
    return {
      limit: this.limit,
      concurrency: this.concurrency,
      loaded: this.loaded.size,
      pending: this.pending.size,
      estimatedTextureBytes: [...this.loaded.values()].reduce(
        (a, b) => a + b.bytes,
        0,
      ),
      keys: [...this.loaded.keys()],
      loads: this.loads,
      evictions: this.evictions,
      errors: this.errors,
    };
  }
}
