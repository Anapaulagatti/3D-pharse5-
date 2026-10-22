import Phaser from "phaser";
import { JuniMotion, type JuniView } from "../engine/JuniMotion";
import { attachJoystick } from "../engine/Joystick";
import "./style.css";
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
root.innerHTML = `<header><b>KOREAN ARENA · GATE 2</b><nav>${catalog.map((s) => `<a ${s.id === id ? 'aria-current="page"' : ""} href="?scene=${s.id}">${s.label}</a>`).join("")}</nav><button id="pause">Pause</button></header><div id="scope">${id === "c" ? "Jeju native-size reservation proposal · approved planning map unchanged" : "Native-scale art review · awaiting human artistic approval"}</div><main id="stage"></main><footer><span id="near">${data.label}</span><span>WASD / arrows · Shift run · E explore · Space greet · 1:1 native</span></footer><div id="joystick" aria-label="Movement joystick"><span class="stick-knob"></span></div><div id="touch-actions"><button id="run">Hold to run</button><button id="explore">Explore</button></div><aside id="dialog" hidden role="dialog" aria-label="Environment detail"><h2 id="title"></h2><p id="copy"></p><button id="close">Return</button></aside>`;
let paused = false,
  heldRun = false,
  analog = { x: 0, y: 0 };
const reset = attachJoystick(
  document.querySelector<HTMLElement>("#joystick")!,
  (x, y) => {
    analog = { x, y };
  },
  () => paused,
);
class Slice extends Phaser.Scene {
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
    this.load.image("foundation", asset + data.ground);
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
      x >= 8 &&
      y >= 8 &&
      x < data.size[0] - 8 &&
      y < data.size[1] - 8 &&
      this.mask[(Math.round(y) * data.size[0] + Math.round(x)) * 4] > 127
    );
  }
  create() {
    this.add.image(0, 0, "foundation").setOrigin(0).setDepth(-100);
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
    const cam = this.cameras.main;
    cam.setBounds(0, 0, ...(data.size as [number, number])).setZoom(1);
    if (overview) cam.centerOn(data.size[0] / 2, data.size[1] / 2);
    else
      cam.startFollow(
        this.player,
        true,
        1,
        1,
        0,
        Math.min(160, this.scale.height * 0.2),
      );
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
    if (paused) return;
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
    if (paused || document.hidden) {
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
    window.__GATE2__ = {
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
    width: native
      ? data.size[0]
      : Math.min(data.size[0], 1024, stage.clientWidth),
    height: native
      ? data.size[1]
      : Math.min(data.size[1], 768, stage.clientHeight),
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
  heldRun = true;
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
