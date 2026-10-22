import Phaser from "phaser";
import { JuniMotion, type JuniView } from "../engine/JuniMotion";
import { attachJoystick } from "../engine/Joystick";
import "./style.css";
import { ReviewCamera } from "./ReviewCamera";
import { SessionMetrics } from "./SessionMetrics";
import { ChunkCache, type GroundChunk } from "./ChunkCache";
type Obj = {
  id: string;
  image: string;
  x: number;
  y: number;
  width: number;
  height: number;
  sortY: number;
  alphaSoftening: number;
};
type Target = { id: string; x: number; y: number; label: string };
type Data = {
  id: string;
  label: string;
  size: number[];
  spawn: number[];
  camera: number[];
  ground: string;
  grounds?: GroundChunk[];
  chunkLoading?: boolean;
  engineering?: {
    rect?: number[];
    points?: number[][];
    width?: number;
    color: number;
    label?: string;
  }[];
  mask: string;
  objects: Obj[];
  targets: Target[];
  routes: { id: string; points: number[][]; width: number }[];
  reservation?: string;
};
type State = {
  ready: boolean;
  scene: string;
  x: number;
  y: number;
  frame: string;
  zoom: number;
  visited: string[];
  behind: string[];
  samplingMode: number;
  paused: boolean;
  occluders: { id: string; depth: number; alpha: number }[];
  camera?: ReturnType<ReviewCamera["snapshot"]>;
  frameTimes?: number[];
  heap?: { used: number; total: number };
  chunks?: ReturnType<ChunkCache["snapshot"]>;
  session?: ReturnType<SessionMetrics["snapshot"]>;
  textures?: { key: string; width: number; height: number }[];
};
declare global {
  interface Window {
    __GATE2__?: State;
    __GATE2_TEST__?: {
      place: (x: number, y: number) => void;
      walkable: (x: number, y: number) => boolean;
    };
  }
}
const base = import.meta.env.BASE_URL,
  query = new URLSearchParams(location.search),
  overview = query.has("overview"),
  native = query.has("native"),
  asset = base + "assets/gate2/";
const catalog: { id: string; label: string }[] = await fetch(
  asset + "catalog.json",
).then((r) => {
  if (!r.ok) throw Error("Missing review catalog");
  return r.json();
});
const id = catalog.some((s) => s.id === query.get("scene"))
  ? query.get("scene")!
  : catalog[0].id;
const data: Data = await fetch(asset + id + "/scene.json").then((r) =>
  r.json(),
);
const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><b>KOREAN ARENA</b><select id="scene-picker" aria-label="Review environment">${catalog.map((s) => `<option value="${s.id}" ${s.id === id ? "selected" : ""}>${s.label}</option>`).join("")}</select><span id="camera-mode">Follow · native1:1</span><button id="scenic">Scenic</button><details id="settings"><summary aria-label="Options">···</summary><div><label><input type="checkbox" id="showcases"> Landmark moments</label><button id="pause">Pause</button><button id="export-session">Export test report</button></div></details></header><main id="stage"></main><div id="map-labels" aria-hidden="true"></div><div id="camera-tools"><span>Drag to look · pinch to zoom</span><button id="start-tour">Start Tour</button><span id="tour-caption" role="status" aria-live="polite"></span><button id="tour-pause">Pause</button><button id="tour-next">Skip landmark</button><button id="overview-mode">Full scene</button><button id="return-juni">Return to Juni</button></div><footer><span id="near">${data.label}</span><span>WASD / arrows · Shift run · E explore · Space greet</span></footer><div id="joystick" aria-label="Movement joystick"><span class="stick-knob"></span></div><div id="touch-actions"><button id="run">Run</button><button id="explore">Explore</button></div><aside id="dialog" hidden role="dialog" aria-label="Environment detail"><h2 id="title"></h2><p id="copy"></p><button id="close">Return</button></aside>`;
document.querySelector<HTMLSelectElement>("#scene-picker")!.onchange = (e) => {
  location.search = "?scene=" + (e.target as HTMLSelectElement).value;
};
if (native) document.body.dataset.native = "true";
let scenicLocked = false;
let paused = false,
  heldRun = false,
  analog = { x: 0, y: 0 };
const reset = attachJoystick(
  document.querySelector<HTMLElement>("#joystick")!,
  (x, y) => {
    analog = { x, y };
  },
  () => paused || scenicLocked,
);
class Slice extends Phaser.Scene {
  private reviewCamera!: ReviewCamera;
  private chunkCache?: ChunkCache;
  private frameTimes: number[] = [];
  private sessionMetrics = new SessionMetrics();
  private lastUpdateTime = performance.now();
  private player!: Phaser.GameObjects.Sprite;
  private motion = new JuniMotion();
  private mask!: Uint8ClampedArray;
  private x = 0;
  private y = 0;
  private facing: JuniView = "front";
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private occluders: { data: Obj; image: Phaser.GameObjects.Image }[] = [];
  private visited = new Set<string>();
  preload() {
    if (data.grounds)
      data.grounds.forEach((g, i) => {
        if (!data.chunkLoading || native || i < 2)
          this.load.image("ground-" + i, asset + g.image);
      });
    else this.load.image("foundation", asset + data.ground);
    this.load.image("walk", asset + data.mask);
    this.load.atlas(
      "juni",
      base + "assets/juni/juni.png",
      base + "assets/juni/juni.json",
    );
    for (const o of data.objects) this.load.image(o.id, asset + o.image);
  }
  walkable(x: number, y: number) {
    return (
      (!this.chunkCache || this.chunkCache.readyAt(x, y)) &&
      x >= 8 &&
      y >= 8 &&
      x < data.size[0] - 8 &&
      y < data.size[1] - 8 &&
      this.mask[(Math.round(y) * data.size[0] + Math.round(x)) * 4] > 127
    );
  }
  create() {
    if (data.chunkLoading && data.grounds)
      this.chunkCache = new ChunkCache(
        this,
        data.grounds,
        asset,
        native ? [0, 1, 2] : [0, 1],
      );
    else if (data.grounds)
      data.grounds.forEach((g, i) =>
        this.add
          .image(g.x, g.y, "ground-" + i)
          .setOrigin(0)
          .setDepth(-100),
      );
    else this.add.image(0, 0, "foundation").setOrigin(0).setDepth(-100);
    if (data.engineering) {
      const g = this.add.graphics().setDepth(-99);
      for (const e of data.engineering) {
        g.fillStyle(e.color, 1);
        if (e.rect) g.fillRect(e.rect[0], e.rect[1], e.rect[2], e.rect[3]);
        if (e.points) {
          g.lineStyle(e.width ?? 4, e.color);
          g.beginPath();
          e.points.forEach((p, i) =>
            i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]),
          );
          g.strokePath();
        }
        if (e.label) {
          const p = e.rect ?? e.points![0];
          this.add
            .text(p[0] + 8, p[1] + 8, e.label, {
              fontSize: "15px",
              color: "#ffffff",
              backgroundColor: "#20383c",
            })
            .setDepth(-98);
        }
      }
    }
    const raw = this.textures.get("walk").getSourceImage() as HTMLImageElement,
      c = document.createElement("canvas");
    c.width = data.size[0];
    c.height = data.size[1];
    const ctx = c.getContext("2d", { willReadFrequently: true })!;
    ctx.drawImage(raw, 0, 0);
    this.mask = ctx.getImageData(0, 0, c.width, c.height).data;
    for (const o of data.objects) {
      const image = this.add
        .image(o.x, o.y, o.id)
        .setOrigin(0)
        .setDepth(o.sortY);
      this.occluders.push({ data: o, image });
    }
    [this.x, this.y] = data.spawn;
    if (!this.walkable(this.x, this.y)) throw Error("Blocked initial spawn");
    this.player = this.add
      .sprite(this.x, this.y, "juni", "idle-front-0")
      .setOrigin(0.5, 100 / 112)
      .setDepth(this.y + 0.1);
    this.keys = this.input.keyboard!.addKeys(
      "W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT,E,SPACE",
    ) as typeof this.keys;
    this.input.keyboard!.addCapture(["SPACE", "UP", "DOWN", "LEFT", "RIGHT"]);
    this.input.keyboard!.on("keydown-E", () => this.inspect());
    this.input.keyboard!.on("keydown-SPACE", () => this.motion.gesture("wave"));
    this.reviewCamera = new ReviewCamera(
      this,
      data.size,
      data.targets,
      id,
      (on) => {
        scenicLocked = on;
        reset();
        heldRun = false;
      },
      native,
      overview,
      this.x,
      this.y,
      () => this.chunkCache?.prepareAll() ?? Promise.resolve(),
    );
    document
      .querySelector("#joystick")!
      .addEventListener("pointerdown", () => this.reviewCamera.interruptTour());
    if (query.has("qa"))
      window.__GATE2_TEST__ = {
        place: (x, y) => {
          if (!this.walkable(x, y)) throw Error(`Blocked QA start ${x},${y}`);
          this.x = x;
          this.y = y;
          this.player.setPosition(x, y);
        },
        walkable: (x, y) => this.walkable(x, y),
      };
    document
      .querySelector("#explore")!
      .addEventListener("click", () => this.inspect());
    window.__GATE2__ = {
      ready: true,
      scene: id,
      x: this.x,
      y: this.y,
      frame: "idle-front-0",
      zoom: 1,
      visited: [],
      behind: [],
      samplingMode: 1,
      paused: false,
      occluders: [],
    };
  }
  inspect() {
    if (paused || scenicLocked) return;
    const nearest = [...data.targets].sort(
      (a, b) =>
        Math.hypot(a.x - this.x, a.y - this.y) -
        Math.hypot(b.x - this.x, b.y - this.y),
    )[0];
    const close =
      nearest && Math.hypot(nearest.x - this.x, nearest.y - this.y) < 120;
    document.querySelector("#title")!.textContent = close
      ? nearest.label
      : data.label;
    document.querySelector("#copy")!.textContent = close
      ? "Explore the architecture, materials and route at Juni’s original scale. This review scene awaits your artistic approval."
      : "Walk toward an entrance or destination, then explore.";
    if (close) this.visited.add(nearest.id);
    document.querySelector<HTMLElement>("#dialog")!.hidden = false;
    paused = true;
    reset();
  }
  update(_t: number, delta: number) {
    if (!this.player || !window.__GATE2__) return;
    let dx =
        Number(this.keys.D.isDown || this.keys.RIGHT.isDown) -
        Number(this.keys.A.isDown || this.keys.LEFT.isDown) +
        analog.x,
      dy =
        Number(this.keys.S.isDown || this.keys.DOWN.isDown) -
        Number(this.keys.W.isDown || this.keys.UP.isDown) +
        analog.y;
    if (Math.hypot(dx, dy) > 0.01) this.reviewCamera.interruptTour();
    if (paused || scenicLocked || document.hidden) {
      dx = 0;
      dy = 0;
    }
    const n = Math.max(1, Math.hypot(dx, dy));
    dx /= n;
    dy /= n;
    const running = heldRun || this.keys.SHIFT.isDown,
      speed = running ? 100 : 60,
      step = (Math.min(delta, 50) * speed) / 1000,
      oldX = this.x,
      oldY = this.y;
    if (this.walkable(this.x + dx * step, this.y)) this.x += dx * step;
    if (this.walkable(this.x, this.y + dy * step)) this.y += dy * step;
    const distance = Math.hypot(this.x - oldX, this.y - oldY);
    if (distance > 0.01)
      this.facing =
        Math.abs(dx) > Math.abs(dy)
          ? dx > 0
            ? "right"
            : "left"
          : dy > 0
            ? "front"
            : "back";
    const frame = this.motion.step(
      delta,
      distance,
      distance > 0.01,
      running,
      this.facing,
      matchMedia("(prefers-reduced-motion: reduce)").matches,
      paused,
    );
    this.player
      .setPosition(Math.round(this.x), Math.round(this.y))
      .setFrame(frame)
      .setDepth(Math.round(this.y) + 0.1);
    const behind: string[] = [];
    for (const o of this.occluders) {
      const near =
        this.x > o.data.x - 30 &&
        this.x < o.data.x + o.data.width + 30 &&
        this.y < o.data.sortY &&
        this.y > o.data.y &&
        this.y - 100 < o.data.y + o.data.height;
      const soften = near;
      o.image.setAlpha(soften ? o.data.alphaSoftening : 1);
      if (near) behind.push(o.data.id);
    }
    this.reviewCamera.update(delta, this.x, this.y, dx, dy, paused);
    this.chunkCache?.update(
      this.x,
      this.reviewCamera.snapshot().worldView,
      this.reviewCamera.mode === "overview",
    );
    const now = performance.now();
    this.sessionMetrics.add(now - this.lastUpdateTime);
    this.frameTimes.push(now - this.lastUpdateTime);
    this.lastUpdateTime = now;
    const memory = (
      performance as Performance & {
        memory?: { usedJSHeapSize: number; totalJSHeapSize: number };
      }
    ).memory;
    if (this.frameTimes.length > 300) this.frameTimes.shift();
    window.__GATE2__ = {
      session: this.sessionMetrics.snapshot(),
      chunks: this.chunkCache?.snapshot(),
      camera: this.reviewCamera.snapshot(),
      frameTimes: this.frameTimes,
      heap: memory
        ? { used: memory.usedJSHeapSize, total: memory.totalJSHeapSize }
        : undefined,
      textures: this.textures.getTextureKeys().map((key) => {
        const t = this.textures.get(key).getSourceImage() as HTMLImageElement;
        return { key, width: t.width, height: t.height };
      }),
      ready: true,
      scene: id,
      x: this.x,
      y: this.y,
      frame,
      zoom: this.cameras.main.zoom,
      visited: [...this.visited],
      behind,
      samplingMode: this.player.frame.source.scaleMode,
      paused,
      occluders: this.occluders.map((o) => ({
        id: o.data.id,
        depth: o.image.depth,
        alpha: o.image.alpha,
      })),
    };
    const near = [...data.targets].sort(
      (a, b) =>
        Math.hypot(a.x - this.x, a.y - this.y) -
        Math.hypot(b.x - this.x, b.y - this.y),
    )[0];
    document.querySelector("#near")!.textContent =
      near && Math.hypot(near.x - this.x, near.y - this.y) < 120
        ? near.label
        : data.label;
  }
}
const stage = document.querySelector<HTMLElement>("#stage")!;
function dimensions() {
  return {
    width: native ? data.size[0] : Math.min(1280, stage.clientWidth),
    height: native ? data.size[1] : Math.min(900, stage.clientHeight),
  };
}
const game = new Phaser.Game({
  type: Phaser.CANVAS,
  parent: stage,
  ...dimensions(),
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  backgroundColor: "#33494a",
  scene: Slice,
  audio: { noAudio: true },
  banner: false,
  input: { activePointers: 4 },
});
if (!native)
  new ResizeObserver(() => {
    const s = dimensions();
    game.scale.resize(s.width, s.height);
  }).observe(stage);
document.querySelector("#pause")!.addEventListener("click", () => {
  paused = !paused;
  reset();
  document.querySelector("#pause")!.textContent = paused ? "Resume" : "Pause";
});
document.querySelector("#close")!.addEventListener("click", () => {
  document.querySelector<HTMLElement>("#dialog")!.hidden = true;
  paused = false;
});
const run = document.querySelector<HTMLButtonElement>("#run")!;
run.onpointerdown = (e) => {
  run.setPointerCapture(e.pointerId);
  heldRun = !scenicLocked;
};
run.onpointerup =
  run.onpointercancel =
  run.onlostpointercapture =
    () => {
      heldRun = false;
    };
window.addEventListener("blur", () => {
  reset();
  heldRun = false;
});

document.querySelector("#export-session")!.addEventListener("click", () => {
  const report = {
    physicalDeviceVerification:
      "NOT AUTOMATICALLY VERIFIED / tester must record real model, OS and browser",
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    viewport: [innerWidth, innerHeight],
    screen: [screen.width, screen.height],
    dpr: devicePixelRatio,
    recordedAt: new Date().toISOString(),
    state: window.__GATE2__,
  };
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = "gate25-test-report.json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
