import Phaser from "phaser";
import { JuniScene } from "../refinement/JuniScene";
import { controls } from "../game/Plaza";
import world from "../../assets-src/v3-final/map/world.json";
import bundle from "../../assets-src/v3-final/map/outdoor-bundle.json";
import anchors from "../../public/review/v3-final/world/anchors.json";
import room from "../../assets-src/living-seoul/room-world.json";
import roomBundle from "../../assets-src/v3-final/room-bundle.json";
import roomAnchors from "../../public/review/living-seoul/room/anchors.json";
import water from "../../assets-src/v3-final/water.json";
import stops from "../../assets-src/v3-final/stops.json";
const waterByTile = new Map<number, number[]>();
for (const frames of water.frames)
  for (const id of frames) waterByTile.set(id, frames);
let basaltFound = false;
declare global {
  interface Window {
    __V3_WORLD__?: { discoveryFound: boolean; candidate: string };
  }
}

let gateOpen = false,
  returning = false,
  transitions = 0;
export const worldSize = [4352, 4800] as const;
export type FullDistrict =
  | "heritage"
  | "namsan"
  | "entertainment"
  | "busan-coast"
  | "jeju"
  | "commons"
  | "room";
export const names: Record<FullDistrict, string> = {
  heritage: "Di sản · Cung điện & phố học",
  namsan: "Namsan · Đài quan sát",
  entertainment: "Bora Bloom · Công viên khám phá",
  "busan-coast": "Blue Letter Coast · Ga & bờ biển",
  jeju: "Windstone · Đảo đá & làng Jeju",
  commons: "Phố văn hóa · Cửa ngõ hiện đại",
  room: "Học viện · Phòng đọc",
};
export function districtAt(x: number, y: number): FullDistrict {
  if (y >= 3648 && x >= 1536 && x <= 2944) return "jeju";
  if (y >= 2496 && y < 3648 && x >= 1536 && x <= 3072) return "busan-coast";
  if (y >= 2240 && x < 1408) return "namsan";
  if (y >= 2240 && x >= 3072) return "entertainment";
  if (y < 2240 && x >= 1024 && x < 3328) return "heritage";
  return "commons";
}
declare global {
  interface Window {
    __FULL_WORLD__?: {
      district: FullDistrict;
      world: number[];
      activeProps: number;
      totalProps: number;
      transitions: number;
      gateOpen: boolean;
      analogMagnitude: number;
      velocity: number[];
      softwareRendererFallback?: boolean;
      camera: number[];
    };
  }
}
export class FullWorld extends JuniScene {
  private door?: Phaser.GameObjects.Image;
  private leafBody?: Phaser.Physics.Arcade.StaticBody;
  private scenery: Phaser.GameObjects.Image[] = [];
  private labels: Phaser.GameObjects.Text[] = [];
  private leafParticles: Phaser.GameObjects.Image[] = [];
  private clock = 0;
  private waterPhase = -1;
  private lastCull = "";
  private leaving = false;
  private lastEvent = 0;
  private overview = new URLSearchParams(location.search).has("overview");
  constructor(private inside = false) {
    super({
      key: inside ? "full-room" : "plaza",
      layout: inside ? room : world,
      bundle: inside ? roomBundle : bundle,
      anchors: inside ? roomAnchors : anchors,
      assetRoot: inside
        ? "review/living-seoul/room/"
        : "review/v3-final/world/",
      ambience: false,
    });
  }
  override preload() {
    if (this.textures.exists("tiles")) this.textures.remove("tiles");
    super.preload();
    if (this.inside)
      this.load.image(
        "full-room-base",
        import.meta.env.BASE_URL + "review/living-seoul/room/room-base.png",
      );
    else
      this.load.image(
        "rf-prod-doors",
        import.meta.env.BASE_URL + "review/v3-final/world/rf-prod-doors.png",
      );
  }
  override create() {
    super.create();
    this.scenery = [];
    this.labels = [];
    this.leafParticles = [];
    this.lastCull = "";
    this.clock = 0;
    this.waterPhase = -1;
    this.leaving = false;
    this.lastEvent = 0;
    if (this.inside) {
      this.add.image(0, 0, "full-room-base").setOrigin(0).setDepth(-95);
      for (const [x, y, text] of [
        [385, 350, "✦ Bàn học · E"],
        [384, 530, "↓ Ra phố · E"],
      ] as const)
        this.add
          .text(x, y, text, {
            fontFamily: "sans-serif",
            fontSize: "12px",
            color: "#fff0cd",
            backgroundColor: "#23493e",
            padding: { x: 5, y: 3 },
          })
          .setOrigin(0.5, 0)
          .setDepth(9500);
    } else {
      if (returning) {
        this.place(1568, 1152);
        returning = false;
      }
      this.door = this.add
        .image(2176, 743, "rf-prod-doors")
        .setOrigin(0.5, 1)
        .setDepth(760)
        .setVisible(!gateOpen);
      this.registerOccluder(this.door);
      for (const x of [2057, 2295]) {
        const l = this.add
          .image(x, 743, "rf-prod-doors")
          .setOrigin(0.5, 1)
          .setScale(0.72)
          .setDepth(760);
        this.registerOccluder(l);
      }
      const z = this.add.zone(2176, 640, 80, 192);
      this.physics.add.existing(z, true);
      this.leafBody = z.body as Phaser.Physics.Arcade.StaticBody;
      this.leafBody.enable = !gateOpen;
      this.physics.add.collider(this.player, z);
      for (const child of this.children.list)
        if (
          child instanceof Phaser.GameObjects.Image &&
          bundle.props[child.texture.key as keyof typeof bundle.props]
        )
          this.scenery.push(child);
      for (const s of stops)
        this.labels.push(
          this.add
            .text(s.x, s.y + 20, s.text.split(".")[0] + " · E", {
              fontFamily: "sans-serif",
              fontSize: "12px",
              color: "#fff0cd",
              backgroundColor: "#23493ed9",
              padding: { x: 5, y: 3 },
            })
            .setOrigin(0.5, 0)
            .setDepth(9500),
        );
      for (let i = 0; i < 8; i++)
        this.leafParticles.push(
          this.add.image(0, 0, "leaf-review").setDepth(8000),
        );
    }
    if (new URLSearchParams(location.search).has("qa"))
      window.__SEOUL_TEST__ = { place: (x, y) => this.place(x, y) };
    this.game.canvas.setAttribute(
      "aria-label",
      "Korean Arena — toàn thế giới: WASD hoặc joystick để đi, giữ chạy, E khám phá; cung điện, rừng tháp, lễ hội, ga ven biển và vườn Jeju.",
    );
    this.events.once("shutdown", () => {
      delete window.__SEOUL__;
      delete window.__SEOUL_TEST__;
      delete window.__FULL_WORLD__;
    });
  }
  private place(x: number, y: number) {
    this.player.setPosition(x, y);
    this.player.body?.reset(x, y);
    this.lastPosition = { x, y };
    this.invalidateCue();
  }
  private near(x: number, y: number, r = 96) {
    return Phaser.Math.Distance.Between(this.player.x, this.player.y, x, y) < r;
  }
  private say(text: string) {
    this.interactions++;
    window.dispatchEvent(new CustomEvent("town-dialog", { detail: text }));
  }
  private changeRoom() {
    if (this.leaving) return;
    this.leaving = true;
    this.player.setVelocity(0);
    controls.x = controls.y = 0;
    controls.run = false;
    window.dispatchEvent(new Event("full-reset-input"));
    if (this.inside) returning = true;
    window.dispatchEvent(new Event("full-loading"));
    transitions++;
    this.scene.start(this.inside ? "plaza" : "full-room");
  }
  public ferry(to: "jeju" | "busan-coast") {
    if (this.inside || this.leaving) return;
    this.leaving = true;
    this.player.setVelocity(0);
    this.input.keyboard?.resetKeys();
    window.dispatchEvent(new Event("full-reset-input"));
    const arrive = () => {
      const p = to === "jeju" ? [1760, 4544] : [2848, 3136];
      this.place(p[0], p[1]);
      this.juni.setPosition(p[0], p[1]);
      this.cameras.main.centerOn(p[0], p[1]);
      transitions++;
      this.leaving = false;
      if (!controls.reduced) this.cameras.main.fadeIn(120, 23, 46, 43);
    };
    if (controls.reduced) arrive();
    else {
      this.cameras.main.fadeOut(120, 23, 46, 43);
      this.time.delayedCall(120, arrive);
    }
  }
  public completeDiscovery() {
    basaltFound = true;
  }
  override interact() {
    if (controls.paused || document.hidden || this.leaving) return;
    if (this.inside) {
      if (this.near(384, 510, 56)) this.changeRoom();
      else if (this.near(385, 354, 100))
        window.dispatchEvent(new Event("academy-lesson"));
      else
        this.say("Đến bàn học để khám phá ba tên chữ Hangul; cửa ra phía nam.");
      return;
    }
    if (this.near(2848, 3184, 112) || this.near(1760, 4608, 112)) {
      const to = this.player.y > 3600 ? "busan-coast" : "jeju";
      window.dispatchEvent(new CustomEvent("full-ferry", { detail: to }));
      return;
    }
    if (this.near(1568, 1120, 64)) {
      this.changeRoom();
      return;
    }
    if (this.near(2176, 752, 180)) {
      if (
        gateOpen &&
        this.player.x > 2120 &&
        this.player.x < 2232 &&
        this.player.y > 528 &&
        this.player.y < 756
      ) {
        this.say(
          "Juni đang ở ngưỡng cửa. Bước hẳn ra ngoài trước khi khép cổng.",
        );
        return;
      }
      gateOpen = !gateOpen;
      this.door?.setVisible(!gateOpen);
      if (this.leafBody) this.leafBody.enable = !gateOpen;
      this.invalidateCue();
      this.say(
        gateOpen
          ? "문을 열어요 · Mở cổng. Theo lối qua cổng trong đến đại điện, vườn và đình nghỉ."
          : "문을 닫아요 · Khép cổng. Ranh giới cung vẫn liền mạch.",
      );
      return;
    }
    if (this.near(2144, 4560, 112)) {
      window.dispatchEvent(new Event("v3-discovery"));
      return;
    }
    const stop = stops
      .map((s) => ({
        s,
        d: Phaser.Math.Distance.Between(this.player.x, this.player.y, s.x, s.y),
      }))
      .sort((a, b) => a.d - b.d)[0];
    if (stop && stop.d < 140) this.say(stop.s.text);
    else
      this.say(
        "Theo đường lát và bảng chỉ dẫn: phía bắc là cung/học viện, phía tây là rừng Namsan, phía đông là công viên hoa. Qua lối gỗ của ga để xuống bờ biển; từ bến phà có chuyến đến vườn Jeju hư cấu. Mở bản đồ để xem toàn hành trình.",
      );
  }
  override interactProp() {
    this.interact();
  }
  override update(time: number, delta: number) {
    const vx = this.player?.body?.velocity.x ?? 0,
      vy = this.player?.body?.velocity.y ?? 0;
    super.update(time, delta);
    if (!this.player?.body) return;
    const magnitude = Math.min(1, Math.hypot(controls.x, controls.y));
    // Isolated analog adapter; approved shared controller and144image frames are unchanged.
    if (
      magnitude > 0 &&
      !controls.paused &&
      !document.hidden &&
      !this.leaving
    ) {
      const speed = controls.run ? 100 : 60,
        step = Math.min(delta, 100) * 0.85;
      const approach = (v: number, t: number) =>
        v + Math.sign(t - v) * Math.min(Math.abs(t - v), step);
      this.player.setVelocity(
        approach(vx, controls.x * speed),
        approach(vy, controls.y * speed),
      );
    }
    if (this.leaving) this.player.setVelocity(0);
    const cam = this.cameras.main;
    cam.setFollowOffset(0, Math.min(60, this.scale.height / 6));
    if (this.overview && !this.inside) {
      cam.stopFollow();
      cam.setZoom(1);
      cam.centerOn(2176, 2400);
    }
    if (this.inside) {
      const w = this.scale.width / controls.zoom,
        h = this.scale.height / controls.zoom;
      cam.setBounds(
        Math.min(0, (768 - w) / 2),
        Math.min(0, (576 - h) / 2),
        Math.max(w, 768),
        Math.max(h, 576),
      );
    } else {
      if (!controls.paused && !controls.reduced && !document.hidden) {
        this.clock += Math.min(delta, 40);
        for (let i = 0; i < this.leafParticles.length; i++) {
          const p = this.leafParticles[i];
          p.setPosition(
            Math.round(
              (
                {
                  heritage: 2176,
                  namsan: 832,
                  entertainment: 3712,
                  "busan-coast": 2400,
                  jeju: 2240,
                  commons: 2176,
                  room: 384,
                } as const
              )[districtAt(this.player.x, this.player.y)] -
                320 +
                i * 96 +
                Math.sin(this.clock / 2100 + i) * 12,
            ),
            Math.round(
              (
                {
                  heritage: 1120,
                  namsan: 2912,
                  entertainment: 2960,
                  "busan-coast": 3120,
                  jeju: 4384,
                  commons: 2368,
                  room: 384,
                } as const
              )[districtAt(this.player.x, this.player.y)] -
                240 +
                ((i * 61 + this.clock / 80) % 420),
            ),
          );
        }
      }
      const phase = Math.floor(this.clock / water.periodMs) % 6;
      if (phase !== this.waterPhase && !controls.reduced) {
        this.waterPhase = phase;
        const view = cam.worldView;
        for (const child of this.children.list)
          if (
            child instanceof Phaser.Tilemaps.TilemapLayer &&
            child.layer.name === "Ground"
          ) {
            const fromX = Math.max(0, Math.floor(view.x / 32) - 1),
              fromY = Math.max(0, Math.floor(view.y / 32) - 1);
            const toX = Math.min(136, Math.ceil(view.right / 32) + 1),
              toY = Math.min(150, Math.ceil(view.bottom / 32) + 1);
            for (let y = fromY; y < toY; y++)
              for (let x = fromX; x < toX; x++) {
                const tile = child.getTileAt(x, y);
                if (!tile) continue;
                const frames = waterByTile.get(tile.index - 1);
                if (frames) tile.index = frames[phase] + 1;
              }
          }
      }
      for (const p of this.leafParticles)
        p.setVisible(!controls.reduced && !this.overview);
      const v = cam.worldView,
        key = [
          Math.floor(v.x / 64),
          Math.floor(v.y / 64),
          v.width,
          v.height,
        ].join(":");
      if (key !== this.lastCull) {
        this.lastCull = key;
        for (const o of this.scenery) {
          const left = o.x - o.displayWidth * o.originX,
            top = o.y - o.displayHeight * o.originY;
          o.setVisible(
            this.overview ||
              (left + o.displayWidth > v.x - 160 &&
                left < v.right + 160 &&
                top + o.displayHeight > v.y - 160 &&
                top < v.bottom + 160),
          );
        }
        for (const l of this.labels)
          l.setVisible(
            !this.overview &&
              l.x > v.x - 160 &&
              l.x < v.right + 160 &&
              l.y > v.y - 160 &&
              l.y < v.bottom + 160,
          );
        this.invalidateCue();
      }
    }
    const district = this.inside
      ? "room"
      : districtAt(this.player.x, this.player.y);
    const v = cam.worldView;
    window.__SEOUL__ = {
      ready: true,
      area: this.inside ? "room" : "outdoor",
      x: this.player.x,
      y: this.player.y,
      world: this.inside ? [768, 576] : [4352, 4800],
      gateOpen,
      transitions,
      activeProps: this.scenery.filter((o) => o.visible).length,
      totalProps: this.inside ? 3 : world.objects.length,
      ambientClock: this.clock,
      reservedNPCs: [],
      view: [v.x, v.y, v.width, v.height],
    };
    window.__FULL_WORLD__ = {
      district,
      world: this.inside ? [768, 576] : [4352, 4800],
      activeProps: window.__SEOUL__.activeProps,
      totalProps: window.__SEOUL__.totalProps,
      transitions,
      gateOpen,
      analogMagnitude: magnitude,
      velocity: [this.player.body.velocity.x, this.player.body.velocity.y],
      camera: [cam.scrollX, cam.scrollY, cam.zoom],
    };
    window.__V3_WORLD__ = {
      discoveryFound: basaltFound,
      candidate: "v3-final",
    };
    if (window.__PLAZA_REVIEW__)
      window.__PLAZA_REVIEW__.environmentClock = this.clock;
    if (time - this.lastEvent > 100) {
      this.lastEvent = time;
      window.dispatchEvent(
        new CustomEvent("district-position", {
          detail: {
            area: this.inside ? "room" : "outdoor",
            x: this.player.x,
            y: this.player.y,
            location: names[district],
          },
        }),
      );
    }
  }
}
