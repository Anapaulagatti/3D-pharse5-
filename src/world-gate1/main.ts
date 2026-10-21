import Phaser from "phaser";
import { plan, walkable } from "./geometry";
import { attachJoystick } from "../engine/Joystick";
import "./style.css";
const q = new URLSearchParams(location.search),
  overview = q.has("overview"),
  native = q.has("native");
const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><b>KOREAN ARENA · GATE 1</b><span>STYLE + MASTERPLAN · GRAYBOX · CHƯA DUYỆT</span><a href="?overview">Toàn cảnh</a><a href="?">Đi bộ 1:1</a><a href="./docs/world-gate1/style-bible.html">Quy chuẩn hình ảnh</a></header><main id="stage"></main><footer><span id="status">Đang tải…</span><span>WASD / mũi tên · Shift chạy · E xem điểm đến</span></footer><aside id="card" hidden></aside><div id="joystick" aria-label="Cần di chuyển"><span class="stick-knob"></span></div><button id="inspect">E · Khám phá</button>`;
let analog = { x: 0, y: 0 };
attachJoystick(
  document.querySelector<HTMLElement>("#joystick")!,
  (x, y) => {
    analog = { x, y };
  },
  () => false,
);
const palette: Record<string, number> = {
  heritage: 0xb49a75,
  transition: 0xd3c7a2,
  main: 0x697a80,
  secondary: 0xaabfc2,
  local: 0xbecbc8,
  scenic: 0xd7cead,
};
let snapshot = {
  ready: false,
  samplingMode: -1,
  x: 0,
  y: 0,
  zoom: 1,
  frame: "",
  visited: [] as string[],
  stage: plan.stage,
};
Object.defineProperty(window, "__WORLD_PLAN__", {
  get: () => ({ ...snapshot }),
});
class Masterplan extends Phaser.Scene {
  private juni!: Phaser.GameObjects.Sprite;
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private facing = "front";
  private ticks = 0;
  private moving = false;
  private visited = new Set<string>();
  preload() {
    this.load.atlas("juni", "assets/juni/juni.png", "assets/juni/juni.json");
  }
  create() {
    const g = this.add.graphics();
    g.fillStyle(0x548d9e).fillRect(0, 0, ...(plan.size as [number, number]));
    for (const r of plan.land)
      g.fillStyle(0xced1b8).fillRect(
        ...(r as [number, number, number, number]),
      );
    // Zoning colors and blocks are planning symbols, never claimed as final pixel artwork.
    for (const z of plan.zones) {
      g.fillStyle(
        Phaser.Display.Color.HexStringToColor(z.color).color,
      ).fillRoundedRect(...(z.rect as [number, number, number, number]), 36);
      this.add
        .text(z.rect[0] + 24, z.rect[1] + 16, z.label, {
          fontFamily: "monospace",
          fontSize: 24,
          color: "#283e40",
          backgroundColor: "#edf0da",
        })
        .setDepth(5);
    }
    for (const p of plan.paths) {
      g.lineStyle(p.width, palette[p.kind], 1);
      const pts = p.points.map(([x, y]) => new Phaser.Math.Vector2(x, y));
      if (p.kind === "scenic") {
        const curve = new Phaser.Curves.Spline(pts);
        g.strokePoints(curve.getPoints(120), false);
      } else {
        g.beginPath();
        g.moveTo(pts[0].x, pts[0].y);
        for (const pt of pts.slice(1)) g.lineTo(pt.x, pt.y);
        g.strokePath();
      }
      if (p.kind === "main") {
        g.lineStyle(3, 0xe7d5a3, 1);
        g.strokePoints(pts, false);
      }
    }
    const routeAudit = plan.paths.map((p) => {
      const points = p.points.map(([x, y]) => new Phaser.Math.Vector2(x, y));
      const samples =
        p.kind === "scenic"
          ? new Phaser.Curves.Spline(points).getPoints(500)
          : ([] as Phaser.Math.Vector2[]);
      if (p.kind !== "scenic")
        for (let i = 1; i < points.length; i++)
          for (let k = 0; k <= 100; k++)
            samples.push(
              new Phaser.Math.Vector2(
                Phaser.Math.Linear(points[i - 1].x, points[i].x, k / 100),
                Phaser.Math.Linear(points[i - 1].y, points[i].y, k / 100),
              ),
            );
      return {
        id: p.id,
        samples: samples.length,
        blocked: samples
          .filter((v) => !walkable(v.x, v.y))
          .map((v) => [Math.round(v.x), Math.round(v.y)]),
      };
    });
    Object.defineProperty(window, "__WORLD_PATH_AUDIT__", {
      value: routeAudit,
      configurable: true,
    });
    for (const b of plan.buildings) {
      const [x, y, w, h] = b.rect;
      g.fillStyle(
        b.kind === "heritage"
          ? 0x775e51
          : b.kind === "modern"
            ? 0x456773
            : 0x668267,
      ).fillRoundedRect(x, y, w, h, 12);
      g.lineStyle(4, 0xeff1d5).strokeRoundedRect(x, y, w, h, 12);
      this.add.text(x + 16, y + 20, b.label, {
        fontFamily: "monospace",
        fontSize: 22,
        color: "#ffffff",
        wordWrap: { width: w - 24 },
      });
      g.fillStyle(0xf7dc97).fillCircle(...(b.entry as [number, number]), 14);
    }
    for (const b of plan.boundaries)
      g.fillStyle(0x8b795c).fillRect(
        ...(b.rect as [number, number, number, number]),
      );
    this.add.text(
      320,
      4050,
      "WATER · mainland quay → pedestrian bridge → island garden\nFerry terminal = planned shore facility; no playable ferry claimed",
      { fontFamily: "monospace", fontSize: 28, color: "#ffffff" },
    );
    this.juni = this.add
      .sprite(...(plan.spawn as [number, number]), "juni", "idle-front-0")
      .setOrigin(0.5, 0.9)
      .setDepth(20);
    this.keys = this.input.keyboard!.addKeys(
      "W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT,E",
    ) as typeof this.keys;
    this.input.keyboard!.on("keydown-E", () => this.inspect());
    document
      .querySelector("#inspect")!
      .addEventListener("click", () => this.inspect());
    this.cameras.main.setBounds(0, 0, ...(plan.size as [number, number]));
    if (overview) {
      const zoom = native
        ? 1
        : Math.min(
            this.scale.width / plan.size[0],
            this.scale.height / plan.size[1],
          );
      this.cameras.main
        .setZoom(zoom)
        .centerOn(plan.size[0] / 2, plan.size[1] / 2);
    } else {
      this.cameras.main.setZoom(1).startFollow(this.juni, true, 1, 1);
    }
    if (q.has("qa"))
      Object.defineProperty(window, "__WORLD_PLAN_TEST__", {
        value: {
          place: (x: number, y: number) => {
            if (!walkable(x, y)) throw Error("Blocked placement");
            this.juni.setPosition(x, y);
          },
        },
        configurable: true,
      });
    snapshot.ready = true;
  }
  private inspect() {
    const b = [...plan.buildings].sort(
      (a, b) =>
        Math.hypot(this.juni.x - a.entry[0], this.juni.y - a.entry[1]) -
        Math.hypot(this.juni.x - b.entry[0], this.juni.y - b.entry[1]),
    )[0];
    const close =
      Math.hypot(this.juni.x - b.entry[0], this.juni.y - b.entry[1]) < 150;
    const card = document.querySelector<HTMLElement>("#card")!;
    card.hidden = false;
    card.textContent = close
      ? `${b.label} · Điểm đến quy hoạch, chưa có nội thất hoặc mỹ thuật sản xuất.`
      : "Đến gần chấm vàng để xem điểm đến.";
    if (close) this.visited.add(b.id);
    card.onclick = () => {
      card.hidden = true;
    };
  }
  update(_time: number, delta: number) {
    if (!this.juni) return;
    let dx =
        Number(this.keys.D.isDown || this.keys.RIGHT.isDown) -
        Number(this.keys.A.isDown || this.keys.LEFT.isDown) +
        analog.x,
      dy =
        Number(this.keys.S.isDown || this.keys.DOWN.isDown) -
        Number(this.keys.W.isDown || this.keys.UP.isDown) +
        analog.y;
    const norm = Math.max(1, Math.hypot(dx, dy));
    dx /= norm;
    dy /= norm;
    const speed = this.keys.SHIFT.isDown ? 100 : 60,
      step = (speed * Math.min(delta, 50)) / 1000;
    this.moving = Math.hypot(dx, dy) > 0.1;
    if (this.moving) {
      this.facing =
        Math.abs(dx) > Math.abs(dy)
          ? dx > 0
            ? "right"
            : "left"
          : dy > 0
            ? "front"
            : "back";
      const nx = this.juni.x + dx * step,
        ny = this.juni.y + dy * step;
      if (walkable(nx, this.juni.y)) this.juni.x = nx;
      if (walkable(this.juni.x, ny)) this.juni.y = ny;
    }
    this.ticks += Math.min(delta, 50);
    const frame = `${this.moving ? "walk" : "idle"}-${this.facing}-${Math.floor(this.ticks / 110) % (this.moving ? 8 : 6)}`;
    if (this.textures.get("juni").has(frame)) this.juni.setFrame(frame);
    snapshot = {
      ...snapshot,
      x: this.juni.x,
      y: this.juni.y,
      zoom: this.cameras.main.zoom,
      frame,
      samplingMode: this.juni.frame.source.scaleMode,
      visited: [...this.visited],
    };
    document.querySelector("#status")!.textContent =
      `${overview ? "SƠ ĐỒ QUY HOẠCH · thu nhỏ có ghi rõ" : "GRAYBOX 1:1 · Juni giữ nguyên kích thước"} · ${Math.round(this.juni.x)}, ${Math.round(this.juni.y)}`;
  }
}
const stage = document.querySelector<HTMLElement>("#stage")!;
const dimensions = () =>
  native
    ? { width: plan.size[0], height: plan.size[1] }
    : { width: stage.clientWidth, height: stage.clientHeight };
const game = new Phaser.Game({
  type: Phaser.CANVAS,
  parent: stage,
  ...dimensions(),
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  backgroundColor: "#548d9e",
  scene: Masterplan,
  audio: { noAudio: true },
  banner: false,
  input: { activePointers: 3 },
});
if (!native)
  new ResizeObserver(() => {
    const { width, height } = dimensions();
    game.scale.resize(width, height);
    if (overview) {
      game.scene.scenes[0]?.cameras.main
        .setZoom(Math.min(width / plan.size[0], height / plan.size[1]))
        .centerOn(plan.size[0] / 2, plan.size[1] / 2);
    }
  }).observe(stage);
