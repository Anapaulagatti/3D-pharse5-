import Phaser from "phaser";
import { rasterOrigin } from "./Registration";
import { addNativeTexture } from "./NativeTexture";
import type { Diagnostics } from "./Diagnostics";
import { ResourcePool, type Resource } from "./ResourcePool";
import {
  containsPoint,
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
  private unculled = new URLSearchParams(location.search).has("unculled");
  private legacy = new URLSearchParams(location.search).has("baseline");
  private lookup = new Map<string, Chunk>();
  private dependencies = new Map<string, Foreground[]>();
  private admissionKey = "";
  private lastAdmission = 0;
  constructor(
    private scene: Phaser.Scene,
    readonly data: Manifest,
    private base: string,
    private diagnostics?: Diagnostics,
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
    for (const c of data.chunks) {
      this.lookup.set(`${Math.floor(c.x / 512)},${Math.floor(c.y / 512)}`, c);
      this.dependencies.set(
        c.id,
        data.objects.filter((o) => intersects(bounds(o), bounds(c))),
      );
    }
    this.pool = new ResourcePool(
      data.budgetBytes,
      data.maxConcurrent,
      (r, s) => this.load(r as Item, s),
      (r, v) => {
        const t = performance.now();
        v.image.destroy();
        scene.textures.remove(r.id);
        v.source.src = "";
        diagnostics?.sample("resource.dispose", performance.now() - t);
        diagnostics?.count("resource.evictions");
      },
    );
    scene.events.once("shutdown", () => this.pool.close());
  }
  private async load(r: Item, signal: AbortSignal): Promise<Value> {
    const source = new Image();
    const loadStarted = performance.now();
    this.diagnostics?.count("resource.admissions");
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
      const decodeStarted = performance.now();
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
      this.diagnostics?.sample(
        "resource.decode",
        performance.now() - decodeStarted,
      );
      if (combined.aborted) throw Error("cancelled");
      if (source.width !== spec.width || source.height !== spec.height)
        throw Error("native dimension mismatch");
      if (r.chunk && buffer?.byteLength !== r.chunk.width * r.chunk.height)
        throw Error("collision size mismatch");
      const uploadStarted = performance.now();
      if (this.legacy) this.scene.textures.addImage(r.id, source);
      else addNativeTexture(this.scene, r.id, source);
      this.diagnostics?.sample(
        "resource.addTexture",
        performance.now() - uploadStarted,
      );
      texture = true;
      const native = this.scene.textures.get(r.id);
      if (
        this.legacy ||
        native.source[0].scaleMode !== Phaser.Textures.FilterMode.NEAREST
      )
        native.setFilter(Phaser.Textures.FilterMode.NEAREST);
      const position = r.object?.sourceAnchor
        ? rasterOrigin(r.object.sourceAnchor, r.object.sourcePivot ?? [0, 0])
        : [spec.x, spec.y];
      if (!position.every(Number.isInteger))
        throw Error(
          "Fractional native raster placement requires an explicit source pivot",
        );
      if (position[0] !== spec.x || position[1] !== spec.y)
        throw Error("Manifest source pivot/raster mismatch");
      const image = this.scene.add
        .image(position[0], position[1], r.id)
        .setOrigin(0)
        .setDepth(r.object?.sortY ?? -100);
      this.diagnostics?.trackImage(image, r.chunk ? "ground" : "foreground");
      const maskStarted = performance.now(),
        mask = buffer ? new Uint8Array(buffer) : undefined;
      this.diagnostics?.sample(
        "resource.maskView",
        performance.now() - maskStarted,
      );
      this.diagnostics?.sample(
        "resource.load",
        performance.now() - loadStarted,
      );
      return {
        image,
        mask,
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
    const spans = (r: Rect) =>
      [
        Math.floor(r[0] / 512),
        Math.floor(r[1] / 512),
        Math.floor((r[0] + r[2] - 1e-6) / 512),
        Math.floor((r[1] + r[3] - 1e-6) / 512),
      ].join(",");
    const key = spans(player) + "/" + spans(visible) + "/" + spans(prefetch);
    if (
      this.legacy ||
      key !== this.admissionKey ||
      performance.now() - this.lastAdmission > 250
    ) {
      this.admissionKey = key;
      this.lastAdmission = performance.now();
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
          Math.hypot(
            (a.chunk ?? a.object!).x - x,
            (a.chunk ?? a.object!).y - y,
          ) -
            Math.hypot(
              (b.chunk ?? b.object!).x - x,
              (b.chunk ?? b.object!).y - y,
            ),
      );
      const pinned = new Set(
        specs.filter((r) => priority(r) < 2).map((r) => r.id),
      );
      this.pool.update(specs, pinned);
    }
    for (const e of this.pool.resident.values()) {
      const item = e.resource as Item,
        o = item.object;
      const painted: Rect = [
        view[0] - 2,
        view[1] - 2,
        view[2] + 4,
        view[3] + 4,
      ];
      e.value.image.setVisible(
        !overview &&
          (this.legacy ||
            this.unculled ||
            intersects(bounds(item.chunk ?? o!), painted)),
      );
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
    if (this.data.logicalSolids?.some((s) => containsPoint(x, y, s.rect)))
      return false;
    x = Math.round(x);
    y = Math.round(y);
    const c = this.legacy
      ? this.data.chunks.find(
          (c) =>
            x >= c.x && y >= c.y && x < c.x + c.width && y < c.y + c.height,
        )
      : this.lookup.get(`${Math.floor(x / 512)},${Math.floor(y / 512)}`);
    if (!c) return false;
    const entry = this.pool.resident.get("g/" + c.id);
    if (!entry?.value.mask) return false;
    // Don't enter a chunk before all touching foreground is ready (no invisible tree/planter).
    if (
      this.dependencies
        .get(c.id)!
        .some((o) => !this.pool.resident.has("f/" + o.id))
    )
      return false;
    return entry.value.mask[(y - c.y) * c.width + x - c.x] > 127;
  }
}
