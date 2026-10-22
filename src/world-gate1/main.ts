import Phaser from "phaser";
import { plan, walkable } from "./geometry";
import { attachJoystick } from "../engine/Joystick";
import "./style.css";
const q = new URLSearchParams(location.search),
  overview = q.has("overview"),
  native = q.has("native");
const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><b>KOREAN ARENA · GATE 1</b><span>ART PROVISIONAL · PLAN PENDING · GATE 2 LOCKED</span><a href="?overview">Toàn cảnh</a><a href="?">Đi bộ 1:1</a><a href="./docs/world-gate1/style-bible.html">Quy chuẩn hình ảnh</a></header><main id="stage"></main><footer><span id="status">Đang tải…</span><span>WASD / mũi tên · Shift chạy · E xem điểm đến</span></footer><aside id="card" hidden></aside><div id="joystick" aria-label="Cần di chuyển"><span class="stick-knob"></span></div><button id="inspect">E · Khám phá</button>`;
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
  distanceWalked: 0,
  simulationMs: 0,
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
    // Planning symbols only: contours, orchard rows and rail reservations, no production art.
    for (const f of plan.features) {
      const colors: Record<string, number> = {
        oreum: 0xb1a58a,
        basalt: 0x7f8e8a,
        orchard: 0xb6c481,
        culture: 0xb9b29a,
      };
      g.fillStyle(colors[f.kind]).fillRoundedRect(
        ...(f.rect as [number, number, number, number]),
        24,
      );
      this.add
        .text(
          f.rect[0] + 10,
          f.rect[1] + (f.kind === "oreum" ? 60 : 10),
          f.label,
          {
            fontFamily: "monospace",
            fontSize: 18,
            color: "#263d3b",
            wordWrap: { width: f.rect[2] - 20 },
          },
        )
        .setDepth(6);
      if (f.kind === "oreum")
        for (let n = 0; n < 4; n++)
          g.lineStyle(3, 0x7e7766).strokeEllipse(
            3750,
            3520,
            380 - n * 60,
            340 - n * 55,
          );
    }
    for (const obstacle of plan.landscapeSolids) {
      const [x, y, w, h] = obstacle.rect;
      if (obstacle.id.startsWith("orchard-tree")) {
        g.fillStyle(0x71895e).fillCircle(x + w / 2, y + h / 2, 23);
        g.fillStyle(0xd6a363).fillCircle(x + w / 2, y + h / 2, 6);
      } else
        g.fillStyle(
          obstacle.id === "oreum-core" ? 0x938574 : 0x536663,
        ).fillRoundedRect(x, y, w, h, 16);
    }
    for (const r of plan.railKeepouts)
      g.fillStyle(0x7c8581).fillRect(
        ...(r as [number, number, number, number]),
      );
    for (const track of plan.station.tracks) {
      const pts = new Phaser.Curves.Spline(
        track.points.map(([x, y]) => new Phaser.Math.Vector2(x, y)),
      ).getPoints(180);
      for (let i = 1; i < pts.length; i++) {
        const a = pts[i - 1],
          b = pts[i],
          d = b.clone().subtract(a).normalize(),
          nx = -d.y,
          ny = d.x;
        if (i % 3 === 0) {
          g.lineStyle(5, 0x415052).lineBetween(
            b.x + nx * 26,
            b.y + ny * 26,
            b.x - nx * 26,
            b.y - ny * 26,
          );
        }
        for (const side of [-1, 1])
          g.lineStyle(3, 0xe3e0cf).lineBetween(
            a.x + nx * 14 * side,
            a.y + ny * 14 * side,
            b.x + nx * 14 * side,
            b.y + ny * 14 * side,
          );
      }
      const last = track.points.at(-1)!;
      g.lineStyle(9, 0x603f3a).lineBetween(
        last[0] - 30,
        last[1],
        last[0] + 30,
        last[1],
      );
    }
    for (const platform of plan.station.platforms) {
      g.fillStyle(0xd7d3ba).fillRect(
        ...(platform.rect as [number, number, number, number]),
      );
      g.lineStyle(5, 0xe7c47a).strokeRect(
        ...(platform.rect as [number, number, number, number]),
      );
      this.add.text(
        platform.rect[0] + 10,
        platform.rect[1] + 15,
        platform.id + "\n100 × 400",
        { fontFamily: "monospace", fontSize: 16, color: "#31464a" },
      );
    }
    g.fillStyle(0xa9c1bd).fillRect(
      ...(plan.station.entrancePlaza as [number, number, number, number]),
    );
    for (const r of plan.overpasses) {
      g.fillStyle(0xd5d1bb).fillRect(
        ...(r as [number, number, number, number]),
      );
      g.lineStyle(4, 0xf3e8bd).strokeRect(
        ...(r as [number, number, number, number]),
      );
    }
    this.add
      .text(2980, 2650, "PEDESTRIAN OVERPASS", {
        fontFamily: "monospace",
        fontSize: 16,
        color: "#304f51",
      })
      .setDepth(6);
    this.add.text(
      3490,
      2320,
      "RAIL APPROACH → OFF MAP\nReserved engineering corridor · no train operation",
      { fontFamily: "monospace", fontSize: 18, color: "#ffffff" },
    );
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
    for (const reserve of plan.facadeReserves) {
      g.lineStyle(3, 0xf3e5bb).strokeRect(
        ...(reserve.rect as [number, number, number, number]),
      );
      g.lineStyle(3, 0xffd180).strokeRect(
        ...(reserve.door as [number, number, number, number]),
      );
      this.add.text(
        reserve.rect[0] + 8,
        reserve.rect[1] + 10,
        "500px FACADE RESERVE · NO ART",
        { fontFamily: "monospace", fontSize: 15, color: "#31494b" },
      );
    }
    for (const link of plan.seaLinks) {
      const [a, b] = link.points;
      g.lineStyle(8, 0xf4d39b);
      for (let t = 0; t < 1; t += 0.06) {
        g.beginPath();
        g.moveTo(Phaser.Math.Linear(a[0], b[0], t), a[1]);
        g.lineTo(Phaser.Math.Linear(a[0], b[0], Math.min(1, t + 0.03)), b[1]);
        g.strokePath();
      }
    }
    for (const n of plan.accessNodes) {
      g.fillStyle(0xf7dc97).fillCircle(...(n.point as [number, number]), 14);
      this.add.text(n.point[0] - 90, n.point[1] + 25, n.label, {
        fontFamily: "monospace",
        fontSize: 18,
        wordWrap: { width: 180 },
        color: "#ffffff",
      });
    }
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
    // Door guides must remain visible above the ground-footprint fill.
    for (const reserve of plan.facadeReserves) {
      g.lineStyle(3, 0xffd180).strokeRect(
        ...(reserve.door as [number, number, number, number]),
      );
      this.add.text(reserve.door[0] + 4, reserve.door[1] + 5, "100px", {
        fontFamily: "monospace",
        fontSize: 15,
        color: "#ffe5aa",
      });
    }
    for (const b of plan.boundaries)
      g.fillStyle(0x8b795c).fillRect(
        ...(b.rect as [number, number, number, number]),
      );
    this.add.text(
      320,
      4050,
      "JEJU · bridge at y3480 · separate ferry piers at y4100\nDashed sea link = proposal only; no operational ferry",
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
    if (!overview && q.has("scale")) this.cameras.main.setFollowOffset(0, 180);
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
    const places = [
      ...plan.buildings.map((b) => ({
        id: b.id,
        label: b.label,
        entry: b.entry,
        note: "Planned building / entrance; no interior or finished art.",
      })),
      ...plan.accessNodes.map((n) => ({
        id: n.id,
        label: n.label,
        entry: n.point,
        note:
          "note" in n
            ? String(n.note)
            : "Planned exploration or transport access point.",
      })),
    ];
    const b = places.sort(
      (a, b) =>
        Math.hypot(this.juni.x - a.entry[0], this.juni.y - a.entry[1]) -
        Math.hypot(this.juni.x - b.entry[0], this.juni.y - b.entry[1]),
    )[0];
    const close =
      Math.hypot(this.juni.x - b.entry[0], this.juni.y - b.entry[1]) < 150;
    const card = document.querySelector<HTMLElement>("#card")!;
    card.hidden = false;
    card.textContent = close
      ? `${b.label} · ${b.note}`
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
    const beforeX = this.juni.x,
      beforeY = this.juni.y;
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
      distanceWalked:
        snapshot.distanceWalked +
        Math.hypot(this.juni.x - beforeX, this.juni.y - beforeY),
      simulationMs: snapshot.simulationMs + Math.min(delta, 50),
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
