import Phaser from "phaser";
import { nativeCanvasOffset } from "./PixelGrid";
import { installPixelAudit } from "./PixelAudit";
import { Diagnostics } from "./Diagnostics";
import { JuniMotion, type JuniView } from "../engine/JuniMotion";
import { attachJoystick } from "../engine/Joystick";
import "../gate2/style.css";
import "./style.css";
import { FoundationCamera } from "./FoundationCamera";
import { SessionMetrics } from "../gate2/SessionMetrics";
import { WorldCache } from "./WorldCache";
import type { Manifest } from "./types";
type State = {
  renderer: string;
  ready: boolean;
  scene: string;
  x: number;
  y: number;
  frame: string;
  zoom: number;
  camera: ReturnType<FoundationCamera["snapshot"]>;
  chunks: ReturnType<WorldCache["pool"]["snapshot"]>;
  session: ReturnType<SessionMetrics["snapshot"]>;
  samplingMode: number;
  behind: string[];
  paused: boolean;
  textures: { key: string; width: number; height: number }[];
};
declare global {
  interface Window {
    __GATE3_PROFILE__?: {
      reset: () => void;
      layer: (mode: string) => void;
      snapshot: () => ReturnType<Diagnostics["snapshot"]>;
    };
    __GATE3__?: State;
    __GATE3_TEST__?: { walkable: (x: number, y: number) => boolean };
  }
}
const base = import.meta.env.BASE_URL,
  query = new URLSearchParams(location.search),
  native = query.has("native"),
  overview = query.has("overview");
const catalog = [
  {
    id: "recovery-pilots",
    label: "G3-D · three shared-style pilots / human review pending",
  },
  {
    id: "recovery-before",
    label: "G3-D BEFORE · rejected baseline / matching cameras",
  },
  {
    id: "production",
    label: "HISTORY · G3-B/C art REJECTED / engine retained",
  },
  {
    id: "registration-working-v3",
    label: "G3-A working V3 · accepted Maru / bakery deferred",
  },
  {
    id: "registration-review",
    label: "HISTORY · prior Q1 / forecourt review",
  },
  {
    id: "registration-forecourt",
    label: "Approved forecourt · Q1 context remains historical",
  },
  { id: "world", label: "G3-A · 4352×4864 world foundation" },
  {
    id: "registration",
    label: "HISTORY · W0 retired / original registrations",
  },
  {
    id: "registration-refined",
    label: "Q1 comparison only · quay allocation deferred",
  },
  { id: "district", label: "G3-A · approved district / isolated cache lab" },
];
const availableCatalog = query.has("pilotsOnly")
  ? catalog.filter((s) =>
      ["recovery-pilots", "recovery-before", "production"].includes(s.id),
    )
  : catalog;
const id = [
  "recovery-pilots",
  "recovery-before",
  "production",
  "district",
  "registration",
  "registration-refined",
  "registration-forecourt",
  "registration-review",
  "registration-working-v3",
].includes(query.get("scene") ?? "")
  ? query.get("scene")!
  : "production";
const data: Manifest = await fetch(
  base + "assets/gate3/" + id + "/manifest.json",
).then((r) => {
  if (!r.ok) throw Error("Missing G3 manifest");
  return r.json();
});
// Diagnostic stress profile only; normal review uses the manifest64MiB budget.
if (query.has("stress")) data.budgetBytes = 24 * 1024 * 1024;
const entries: Record<string, number[]> =
  data.reviewEntries ??
  (id === "world"
    ? { north: [1740, 1440], jeju: [3500, 4055] }
    : id.startsWith("registration")
      ? {
          station: [2598.5, 2760],
          bakery: [1814, 3900],
          retail: [1128, 2690],
          convenience: [368, 3220],
        }
      : { station: [2824, 857], alley: [1470, 850] });
if (entries[query.get("entry") ?? ""])
  data.spawn = entries[query.get("entry")!];
const label =
  id === "production" || id === "recovery-before"
    ? "HISTORY · full-world art rejected / engine retained"
    : id === "world"
      ? "G3-A foundation · engineering terrain is NOT final art"
      : id.startsWith("registration")
        ? "CANDIDATE ONLY · native registration / engineering routes · final approval pending"
        : id === "recovery-pilots"
          ? "G3-D three pilot regions only · unified art approval pending"
          : "Approved district · local coordinates · world registration pending";
const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><b>${id.startsWith("recovery-") ? "G3-D STYLE REVIEW" : "G3-C HISTORY PROTOTYPE"}</b><select id="scene-picker" aria-label="Review environment">${availableCatalog.map((s) => `<option value="${s.id}" ${s.id === id ? "selected" : ""}>${s.label}</option>`).join("")}</select><span id="camera-mode">Follow · native1:1</span><button id="scenic">Scenic</button><details id="settings"><summary aria-label="Options">···</summary><div><label><input type="checkbox" id="showcases"> Landmark moments</label><button id="pause">Pause</button><button id="export-session">Export test report</button></div></details></header><main id="stage"></main><div id="map-labels" aria-hidden="true"></div><div id="camera-tools"><span>Drag to look · pinch to zoom</span><button id="start-tour">Start Tour</button><span id="tour-caption" role="status" aria-live="polite"></span><button id="tour-pause">Pause</button><button id="tour-next">Skip landmark</button><button id="overview-mode">Full scene</button><button id="return-juni">Return to Juni</button></div><button id="tour-controls" aria-controls="camera-tools" aria-expanded="true">Tour controls</button><footer><span id="near">${label}</span><span>WASD / arrows · Shift run · E explore · Space greet</span></footer><div id="joystick" aria-label="Movement joystick"><span class="stick-knob"></span></div><div id="touch-actions"><button id="run">Run</button><button id="explore">Explore</button></div><aside id="dialog" hidden role="dialog" aria-label="Environment detail"><h2 id="title"></h2><p id="copy"></p><button id="close">Return</button></aside>`;
document.querySelector<HTMLSelectElement>("#scene-picker")!.onchange = (e) => {
  location.search =
    "?scene=" +
    (e.target as HTMLSelectElement).value +
    (query.has("pilotsOnly") ? "&pilotsOnly" : "");
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
  private reviewCamera!: FoundationCamera;
  private worldCache!: WorldCache;
  private overviewImage!: Phaser.GameObjects.Image;
  private diagnostics = query.has("profile") ? new Diagnostics() : undefined;
  private sessionMetrics = new SessionMetrics();
  private lastUpdateTime = performance.now();
  private lastMetrics = 0;
  private metrics = this.sessionMetrics.snapshot();
  private textureGeneration = -1;
  private textureInfo: State["textures"] = [];
  private legacy = query.has("baseline");
  private player!: Phaser.GameObjects.Sprite;
  private motion = new JuniMotion();
  private x = 0;
  private y = 0;
  private facing: JuniView = "front";
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private visited = new Set<string>();
  preload() {
    this.load.atlas(
      "juni",
      base + "assets/juni/juni.png",
      base + "assets/juni/juni.json",
    );
    this.load.image("overview", base + data.overview);
  }
  walkable(x: number, y: number) {
    return this.worldCache.walkable(x, y);
  }
  create() {
    this.worldCache = new WorldCache(this, data, base, this.diagnostics);
    if (this.diagnostics) {
      this.diagnostics.attach(this);
      window.__GATE3_PROFILE__ = {
        reset: () => this.diagnostics!.reset(),
        layer: (mode) => this.diagnostics!.layer(mode),
        snapshot: () => this.diagnostics!.snapshot(),
      };
    }
    this.overviewImage = this.add
      .image(0, 0, "overview")
      .setOrigin(0)
      .setDisplaySize(data.size[0], data.size[1])
      .setDepth(-101)
      .setVisible(false);
    [this.x, this.y] = data.spawn;
    // Initial movement waits for native chunk + local foreground + collision readiness.
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
    this.reviewCamera = new FoundationCamera(
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
      async () => {},
      data.stops,
    );
    if (
      native &&
      (id.startsWith("registration") ||
        id === "production" ||
        id.startsWith("recovery-"))
    ) {
      const centres: Record<string, [number, number]> = data.nativeFrames ?? {
        station: [2598.5, 2460],
        bakery: [1814, 3500],
        retail: [1128, 2360],
        convenience: [640, 2910],
      };
      const centre =
        centres[query.get("entry") ?? "station"] ?? centres.station;
      this.reviewCamera.frameNative(...centre);
    }
    document
      .querySelector("#joystick")!
      .addEventListener("pointerdown", () => this.reviewCamera.interruptTour());
    window.__GATE3_TEST__ = { walkable: (x, y) => this.walkable(x, y) };
    if (query.has("pixelAudit")) installPixelAudit(this);
    document
      .querySelector("#explore")!
      .addEventListener("click", () => this.inspect());
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
      : label;
    document.querySelector("#copy")!.textContent = close
      ? "Explore the architecture, materials and routes at Juni’s original scale."
      : "Walk toward an entrance or destination, then explore.";
    if (close) this.visited.add(nearest.id);
    document.querySelector<HTMLElement>("#dialog")!.hidden = false;
    paused = true;
    reset();
  }
  update(_t: number, delta: number) {
    if (!this.player) return;
    const updateStarted = performance.now();
    const collisionStarted = performance.now();
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
    // Sweep in <=1px increments: no wall tunnelling after a slow frame.
    const substeps = Math.max(1, Math.ceil(step));
    for (let i = 0; i < substeps; i++) {
      if (this.walkable(this.x + (dx * step) / substeps, this.y))
        this.x += (dx * step) / substeps;
      if (this.walkable(this.x, this.y + (dy * step) / substeps))
        this.y += (dy * step) / substeps;
    }
    this.diagnostics?.sample(
      "update.inputCollision",
      performance.now() - collisionStarted,
    );
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
    const cameraStarted = performance.now();
    this.reviewCamera.update(delta, this.x, this.y, dx, dy, paused);
    this.diagnostics?.sample(
      "update.camera",
      performance.now() - cameraStarted,
    );
    const cacheStarted = performance.now();
    const isOverview = this.reviewCamera.mode === "overview";
    this.overviewImage.setVisible(isOverview);
    const cameraSnapshot = this.reviewCamera.snapshot();
    this.worldCache.update(
      cameraSnapshot.worldView as [number, number, number, number],
      this.x,
      this.y,
      isOverview,
    );
    this.diagnostics?.sample("update.cache", performance.now() - cacheStarted);
    const behind = data.objects
      .filter(
        (o) =>
          this.x > o.x - 30 &&
          this.x < o.x + o.width + 30 &&
          this.y < o.sortY &&
          this.y > o.y,
      )
      .map((o) => o.id);
    const now = performance.now();
    this.sessionMetrics.add(now - this.lastUpdateTime);
    this.diagnostics?.sample("frame.interval", now - this.lastUpdateTime);
    this.lastUpdateTime = now;
    const stats = this.worldCache.pool.snapshot(),
      generation = stats.loads + stats.evictions;
    if (this.legacy || generation !== this.textureGeneration) {
      this.textureGeneration = generation;
      this.textureInfo = this.textures.getTextureKeys().map((key) => {
        const t = this.textures.get(key).getSourceImage() as HTMLImageElement;
        return { key, width: t.width, height: t.height };
      });
    }
    if (this.legacy || now - this.lastMetrics > 100) {
      this.lastMetrics = now;
      this.metrics = this.sessionMetrics.snapshot();
    }
    window.__GATE3__ = {
      renderer: this.game.renderer.type === Phaser.WEBGL ? "WebGL" : "Canvas",
      ready: this.walkable(this.x, this.y),
      scene: id,
      x: this.x,
      y: this.y,
      frame,
      zoom: this.cameras.main.zoom,
      camera: cameraSnapshot,
      chunks: stats,
      session: this.metrics,
      behind,
      paused,
      samplingMode: this.player.frame.source.scaleMode,
      textures: this.textureInfo,
    };
    const near = [...data.targets].sort(
      (a, b) =>
        Math.hypot(a.x - this.x, a.y - this.y) -
        Math.hypot(b.x - this.x, b.y - this.y),
    )[0];
    document.querySelector("#near")!.textContent =
      near && Math.hypot(near.x - this.x, near.y - this.y) < 120
        ? near.label
        : label;
    this.diagnostics?.sample("update.total", performance.now() - updateStarted);
  }
}
const stage = document.querySelector<HTMLElement>("#stage")!;
function dimensions() {
  return {
    width: native ? 1280 : Math.min(1280, stage.clientWidth),
    height: native ? 900 : Math.min(900, stage.clientHeight),
  };
}
const game = new Phaser.Game({
  type: query.get("renderer") === "canvas" ? Phaser.CANVAS : Phaser.AUTO,
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
function alignCanvas() {
  const s = dimensions();
  if (!native) game.scale.resize(s.width, s.height);
  game.canvas.style.left =
    nativeCanvasOffset(stage.clientWidth, s.width) + "px";
  game.canvas.style.top =
    nativeCanvasOffset(stage.clientHeight, s.height) + "px";
}
alignCanvas();
new ResizeObserver(alignCanvas).observe(stage);
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
    renderer: game.renderer.type === Phaser.WEBGL ? "WebGL" : "Canvas",
    foundationStatus: label,
    physicalDeviceVerification:
      "NOT AUTOMATICALLY VERIFIED / tester must record real model, OS and browser",
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    viewport: [innerWidth, innerHeight],
    screen: [screen.width, screen.height],
    dpr: devicePixelRatio,
    recordedAt: new Date().toISOString(),
    state: window.__GATE3__,
  };
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = "gate3a-test-report.json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
