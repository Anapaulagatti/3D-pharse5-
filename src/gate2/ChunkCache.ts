import Phaser from "phaser";
export type GroundChunk = {
  id?: string;
  image: string;
  x: number;
  y: number;
  width?: number;
  height?: number;
};
/** Bounded three-chunk prototype cache; eager adjacent prefetch, retain once decoded until scene shutdown.
 * Full-world LRU eviction/streaming is deliberately not claimed by this validation prototype.
 */
export class ChunkCache {
  private images = new Map<number, Phaser.GameObjects.Image>();
  private pending = new Set<number>();
  private requests: { chunk: string; ms: number; event: string }[] = [];
  private queue: number[] = [];
  private busy = false;
  private dead = false;
  private forceAll = false;
  constructor(
    private scene: Phaser.Scene,
    private chunks: GroundChunk[],
    private base: string,
    private initial: number[],
  ) {
    for (const i of initial) this.mount(i);
    scene.events.once("shutdown", () => {
      this.dead = true;
      for (let i = 0; i < chunks.length; i++) {
        this.images.get(i)?.destroy();
        if (scene.textures.exists(this.key(i)))
          scene.textures.remove(this.key(i));
      }
    });
  }
  private key(i: number) {
    return "ground-" + i;
  }
  private mount(i: number) {
    if (this.images.has(i)) return;
    const g = this.chunks[i];
    this.images.set(
      i,
      this.scene.add
        .image(g.x, g.y, this.key(i))
        .setOrigin(0)
        .setDepth(-100 + i * 0.001),
    );
    this.requests.push({
      chunk: g.id ?? String(i),
      ms: performance.now(),
      event: "ready",
    });
  }
  update(x: number, view: number[], all = false) {
    this.chunks.forEach((g, i) => {
      const w = g.width ?? 0;
      const desired =
        all ||
        this.forceAll ||
        (g.x < view[0] + view[2] + 512 && g.x + w > view[0] - 512) ||
        Math.abs(g.x + w / 2 - x) < 1300;
      if (desired && !this.images.has(i) && !this.pending.has(i)) {
        this.pending.add(i);
        this.queue.push(i);
        this.requests.push({
          chunk: g.id ?? String(i),
          ms: performance.now(),
          event: "request",
        });
      }
    });
    if (!this.busy && this.queue.length) {
      const i = this.queue.shift()!;
      this.busy = true;
      this.scene.load.image(this.key(i), this.base + this.chunks[i].image);
      this.scene.load.once("complete", () => {
        this.busy = false;
        if (this.dead) return;
        this.pending.delete(i);
        this.mount(i);
      });
      this.scene.load.start();
    }
  }
  prepareAll(): Promise<void> {
    this.forceAll = true;
    return new Promise((resolve, reject) => {
      const start = performance.now();
      const check = () => {
        if (this.dead || performance.now() - start > 8000) {
          reject(Error("Chunk overview load timed out"));
          return;
        }
        if (this.images.size === this.chunks.length) {
          resolve();
          return;
        }
        this.scene.time.delayedCall(20, check);
      };
      check();
    });
  }
  readyAt(x: number, y: number) {
    const covering = this.chunks
      .map((g, i) => ({ g, i }))
      .filter(
        ({ g }) =>
          x >= g.x &&
          x < g.x + (g.width ?? 0) &&
          y >= g.y &&
          y < g.y + (g.height ?? 0),
      );
    return covering.length > 0 && covering.every(({ i }) => this.images.has(i));
  }
  snapshot() {
    return {
      resident: [...this.images.keys()].map((i) => this.chunks[i].id),
      pending: [...this.pending],
      events: this.requests,
      capacity: 3,
      eviction: "retain bounded prototype textures until scene shutdown",
      groundRGBABytes: [...this.images.keys()].reduce(
        (n, i) =>
          n + (this.chunks[i].width ?? 0) * (this.chunks[i].height ?? 0) * 4,
        0,
      ),
    };
  }
}
