import Phaser from "phaser";
import { ResourcePool, type Resource } from "./ResourcePool";
import {
  bounds,
  intersects,
  type Manifest,
  type Rect,
  type Foreground,
  type Chunk,
} from "./types";
type Item = Resource & { chunk?: Chunk; object?: Foreground };
type Value = {
  image: Phaser.GameObjects.Image;
  mask?: Uint8Array;
  source: HTMLImageElement;
};
/** Single native texture per chunk/object; foreground bounds, rather than root chunk, own residency. */
export class WorldCache {
  readonly pool: ResourcePool<Value>;
  private items: Item[];
  constructor(
    private scene: Phaser.Scene,
    readonly data: Manifest,
    private base: string,
  ) {
    this.items = [
      ...data.chunks.map((chunk) => ({
        id: "g/" + chunk.id,
        bytes: chunk.bytes,
        chunk,
      })),
      ...data.objects.map((object) => ({
        id: "f/" + object.id,
        bytes: object.bytes,
        object,
      })),
    ];
    this.pool = new ResourcePool(
      data.budgetBytes,
      data.maxConcurrent,
      (r, s) => this.load(r as Item, s),
      (r, v) => {
        v.image.destroy();
        scene.textures.remove(r.id);
        v.source.src = "";
      },
    );
    scene.events.once("shutdown", () => this.pool.close());
  }
  private async load(r: Item, signal: AbortSignal): Promise<Value> {
    const source = new Image();
    let url: string | undefined;
    let texture = false;
    const abort = () => {
      source.src = "";
    };
    signal.addEventListener("abort", abort, { once: true });
    const timer = setTimeout(() => abort(), 15000);
    try {
      const combined = AbortSignal.any([signal, AbortSignal.timeout(15000)]);
      const spec = r.chunk ?? r.object!;
      const [blob, buffer] = await Promise.all([
        fetch(this.base + spec.image, { signal: combined }).then((resp) => {
          if (!resp.ok) throw Error("texture " + resp.status);
          return resp.blob();
        }),
        r.chunk
          ? fetch(this.base + r.chunk.mask, { signal: combined }).then(
              (resp) => {
                if (!resp.ok) throw Error("collision " + resp.status);
                return resp.arrayBuffer();
              },
            )
          : Promise.resolve(undefined),
      ]);
      url = URL.createObjectURL(blob);
      source.src = url;
      await Promise.race([
        source.decode(),
        new Promise<never>((_, reject) =>
          combined.addEventListener(
            "abort",
            () => reject(Error("aborted decode")),
            { once: true },
          ),
        ),
      ]);
      if (combined.aborted) throw Error("cancelled");
      if (source.width !== spec.width || source.height !== spec.height)
        throw Error("native dimension mismatch");
      if (r.chunk && buffer?.byteLength !== r.chunk.width * r.chunk.height)
        throw Error("collision size mismatch");
      this.scene.textures.addImage(r.id, source);
      texture = true;
      this.scene.textures
        .get(r.id)
        .setFilter(Phaser.Textures.FilterMode.NEAREST);
      const image = this.scene.add
        .image(spec.x, spec.y, r.id)
        .setOrigin(0)
        .setDepth(r.object?.sortY ?? -100);
      return {
        image,
        mask: buffer ? new Uint8Array(buffer) : undefined,
        source,
      };
    } catch (error) {
      if (texture) this.scene.textures.remove(r.id);
      source.src = "";
      throw error;
    } finally {
      clearTimeout(timer);
      signal.removeEventListener("abort", abort);
      if (url) URL.revokeObjectURL(url);
    }
  }
  update(view: Rect, x: number, y: number, overview: boolean) {
    // Overview is a separate small planning proxy. Never request all world chunks to zoom out.
    const player: Rect = [x - 96, y - 96, 192, 192];
    const visible = overview ? player : view;
    const prefetch: Rect = [
      visible[0] - 384,
      visible[1] - 384,
      visible[2] + 768,
      visible[3] + 768,
    ];
    const chunks = this.items.filter(
      (r) =>
        r.chunk &&
        (intersects(bounds(r.chunk), prefetch) ||
          intersects(bounds(r.chunk), player)),
    );
    const groundPriority = (r: Item) =>
      intersects(bounds(r.chunk!), player)
        ? 0
        : intersects(bounds(r.chunk!), visible)
          ? 1
          : 2;
    // A chunk's full foreground dependencies must be requested even when their roots
    // lie beyond prefetch. Otherwise collision readiness could wait forever at an edge.
    const specs = this.items.filter((r) =>
      r.chunk
        ? chunks.includes(r)
        : chunks.some((c) => intersects(bounds(r.object!), bounds(c.chunk!))),
    );
    const priority = (r: Item) =>
      r.chunk
        ? groundPriority(r)
        : Math.min(
            ...chunks
              .filter((c) => intersects(bounds(r.object!), bounds(c.chunk!)))
              .map(groundPriority),
          );
    specs.sort(
      (a, b) =>
        priority(a) - priority(b) ||
        Math.hypot((a.chunk ?? a.object!).x - x, (a.chunk ?? a.object!).y - y) -
          Math.hypot(
            (b.chunk ?? b.object!).x - x,
            (b.chunk ?? b.object!).y - y,
          ),
    );
    const pinned = new Set(
      specs.filter((r) => priority(r) < 2).map((r) => r.id),
    );
    this.pool.update(specs, pinned);
    for (const e of this.pool.resident.values()) {
      const item = e.resource as Item,
        o = item.object;
      e.value.image.setVisible(!overview);
      if (o)
        e.value.image.setAlpha(
          x > o.x - 30 &&
            x < o.x + o.width + 30 &&
            y < o.sortY &&
            y > o.y &&
            y - 100 < o.y + o.height
            ? o.alphaSoftening
            : 1,
        );
    }
  }
  walkable(x: number, y: number) {
    x = Math.round(x);
    y = Math.round(y);
    const c = this.data.chunks.find(
      (c) => x >= c.x && y >= c.y && x < c.x + c.width && y < c.y + c.height,
    );
    if (!c) return false;
    const entry = this.pool.resident.get("g/" + c.id);
    if (!entry?.value.mask) return false;
    // Don't enter a chunk before all touching foreground is ready (no invisible tree/planter).
    if (
      this.data.objects.some(
        (o) =>
          intersects(bounds(o), bounds(c)) &&
          !this.pool.resident.has("f/" + o.id),
      )
    )
      return false;
    return entry.value.mask[(y - c.y) * c.width + x - c.x] > 127;
  }
}
