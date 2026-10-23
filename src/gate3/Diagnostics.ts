import Phaser from "phaser";
class Series {
  n = 0;
  sum = 0;
  max = 0;
  bins = new Uint32Array(4001);
  add(ms: number) {
    if (!Number.isFinite(ms) || ms < 0) return;
    this.n++;
    this.sum += ms;
    this.max = Math.max(this.max, ms);
    this.bins[Math.min(4000, Math.floor(ms * 10))]++;
  }
  snapshot() {
    const pct = (p: number) => {
      let n = 0;
      for (let i = 0; i < this.bins.length; i++) {
        n += this.bins[i];
        if (n >= this.n * p) return i / 10;
      }
      return null;
    };
    return {
      samples: this.n,
      totalMs: this.sum,
      meanMs: this.n ? this.sum / this.n : null,
      p50Ms: pct(0.5),
      p95Ms: pct(0.95),
      maxMs: this.max,
    };
  }
}
/** Opt-in CPU/API diagnostics. Render submission time is not asynchronous GPU completion. */
export class Diagnostics {
  private series = new Map<string, Series>();
  private counters = new Map<string, number>();
  private restores: (() => void)[] = [];
  private observer?: PerformanceObserver;
  private scene?: Phaser.Scene;
  layer(mode: string) {
    if (!this.scene) return;
    for (const child of this.scene.children.list) {
      const key = (child as Phaser.GameObjects.Image).texture?.key;
      const layer = key?.startsWith("g/")
        ? "ground"
        : key?.startsWith("f/")
          ? "foreground"
          : "other";
      child.cameraFilter =
        mode === "all" || mode === layer ? 0 : this.scene.cameras.main.id;
    }
  }
  sample(name: string, ms: number) {
    let s = this.series.get(name);
    if (!s) this.series.set(name, (s = new Series()));
    s.add(ms);
  }
  count(name: string, n = 1) {
    this.counters.set(name, (this.counters.get(name) ?? 0) + n);
  }
  time<T>(name: string, fn: () => T) {
    const t = performance.now();
    try {
      return fn();
    } finally {
      this.sample(name, performance.now() - t);
    }
  }
  reset() {
    this.series.clear();
    this.counters.clear();
  }
  attach(scene: Phaser.Scene) {
    this.scene = scene;
    const renderer = scene.game.renderer as unknown as Record<string, unknown>;
    const wrap = (
      obj: Record<string, unknown>,
      key: string,
      name: string,
      counter = false,
    ) => {
      const original = obj[key];
      if (typeof original !== "function") return;
      obj[key] = (...args: unknown[]) =>
        this.time(name, () => {
          if (counter) this.count(name);
          return original.apply(obj, args);
        });
      this.restores.push(() => {
        obj[key] = original;
      });
    };
    for (const key of ["preRender", "render", "postRender"])
      wrap(renderer, key, "renderer." + key);
    const gl = renderer.gl as
      (WebGLRenderingContext | WebGL2RenderingContext) | undefined;
    if (gl) {
      for (const key of [
        "drawArrays",
        "drawElements",
        "drawArraysInstanced",
        "drawElementsInstanced",
        "texImage2D",
        "texSubImage2D",
        "deleteTexture",
        "generateMipmap",
      ])
        wrap(gl as unknown as Record<string, unknown>, key, "gl." + key, true);
    } else {
      const context = renderer.currentContext as CanvasRenderingContext2D;
      if (context)
        wrap(
          context as unknown as Record<string, unknown>,
          "drawImage",
          "canvas.drawImage",
          true,
        );
    }
    if (PerformanceObserver.supportedEntryTypes.includes("longtask")) {
      this.observer = new PerformanceObserver((list) => {
        for (const e of list.getEntries())
          this.sample("browser.longtask", e.duration);
      });
      this.observer.observe({ type: "longtask", buffered: false });
    }
    scene.events.once("shutdown", () => {
      this.observer?.disconnect();
      this.restores.forEach((f) => f());
    });
  }
  trackImage(image: Phaser.GameObjects.Image, layer: string) {
    for (const key of ["renderWebGLStep", "renderCanvas"] as const) {
      const obj = image as unknown as Record<string, unknown>,
        original = obj[key];
      if (typeof original !== "function") continue;
      obj[key] = (...args: unknown[]) => {
        this.count(layer + ".submissions");
        return original.apply(image, args);
      };
    }
  }
  snapshot() {
    return {
      timings: Object.fromEntries(
        [...this.series].map(([k, v]) => [k, v.snapshot()]),
      ),
      counters: Object.fromEntries(this.counters),
      scope:
        "Opt-in CPU durations and API calls, not GPU completion, VRAM or physical-device acceptance",
    };
  }
}
