import Phaser from "phaser";
import { JuniScene } from "../refinement/JuniScene";
import { controls } from "../game/Plaza";
import world from "../../assets-src/full-world/map/world.json";
import bundle from "../../assets-src/full-world/map/outdoor-bundle.json";
import anchors from "../../public/review/full-world/world/anchors.json";
import room from "../../assets-src/living-seoul/room-world.json";
import roomBundle from "../../assets-src/full-world/room-bundle.json";
import roomAnchors from "../../public/review/living-seoul/room/anchors.json";
import water from "../../assets-src/full-world/water.json";
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
  namsan: "Namsan · Rừng & tháp",
  entertainment: "Bora Bloom · Vườn lễ hội",
  "busan-coast": "Blue Letter Coast · Ga & bờ biển",
  jeju: "Windstone · Vườn đá Jeju",
  commons: "Phố văn hóa · Lối đến các vùng",
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
const stops = [
  {
    id: "hall",
    x: 2176,
    y: 320,
    text: "궁궐 · Cung điện. 마당 · Sân. 문 · Cửa. Đại điện, cổng, vườn và đình nghỉ tạo chuỗi không gian cung hư cấu lấy cảm hứng kiến trúc Joseon.",
  },
  {
    id: "hanji",
    x: 2480,
    y: 384,
    text: "한지 · Giấy hanji. Bàn trưng bày giới thiệu sách đóng chỉ và nghệ thuật giấy. Artwork gốc; không sao chép hiện vật.",
  },
  {
    id: "pavilion",
    x: 1568,
    y: 528,
    text: "정자 · Đình nghỉ. Không gian mở trong vườn cung dành cho nghỉ chân, ngắm cây và đọc; lối đi chính luôn thông.",
  },
  {
    id: "science",
    x: 2656,
    y: 1472,
    text: "과학 · Khoa học. Sân phát minh có thiên cầu và dụng cụ đo; các vật liệu đồng/gỗ làm rõ chức năng của xưởng.",
  },
  {
    id: "museum",
    x: 3008,
    y: 2028,
    text: "역사 · Lịch sử. Hiên sử liệu và mô hình hàng hải mở ra phố, có lối qua riêng cách sân xưởng.",
  },
  {
    id: "bookshop",
    x: 2752,
    y: 2304,
    text: "서점 · Hiệu sách. 책 · Sách. 차 · Trà. Mặt tiền gạch, kính và mái vườn tiếp nối ngõ học truyền thống bằng một phố văn hóa hiện đại.",
  },
  {
    id: "tower",
    x: 832,
    y: 2912,
    text: "전망탑 · Tháp quan sát. 산 · Núi. 숲 · Rừng. Đây là điểm đến gợi Namsan trong thế giới du lịch giáo dục hư cấu.",
  },
  {
    id: "terrace",
    x: 1120,
    y: 3024,
    text: "전망 · Tầm nhìn. Đi lên bằng bậc đá thật; mặt giữ đất và lan can có va chạm. Quan sát con đường rừng đã đi qua.",
  },
  {
    id: "wheel",
    x: 3392,
    y: 2832,
    text: "관람차 · Vòng quay ngắm cảnh. Bora Bloom là công viên hoa hư cấu với artwork gốc, không phải Everland hay một thương hiệu thật. Các trò chơi là trưng bày trong bản review này.",
  },
  {
    id: "carousel",
    x: 4000,
    y: 2864,
    text: "회전목마 · Trò quay vòng. Mái hoa, ghế chim và khu vườn mang nhịp điệu lễ hội; đi theo vòng đường lát để trở về cổng hoa.",
  },
  {
    id: "arch",
    x: 3712,
    y: 3272,
    text: "꽃 · Hoa. 축제 · Lễ hội. Cổng giữa mở, hai chân cổng và bồn hoa có ranh giới vật lý; lối vườn phía tây là cửa vào thứ hai có chủ đích.",
  },
  {
    id: "station",
    x: 1824,
    y: 2816,
    text: "역 · Nhà ga. 기차 · Tàu. Ga ven biển gợi du lịch Busan, có đường ray liên tục và lối qua ray bằng gỗ riêng. Tàu trưng bày đang đứng yên, không phải tàu đang vận hành.",
  },
  {
    id: "bridge",
    x: 2320,
    y: 3160,
    text: "다리 · Cầu. 바다 · Biển. Cầu gỗ bắc qua một lòng nước thật; hãy ở trên mặt cầu và đường dạo. Không đi xuyên nước hay đường ray.",
  },
  {
    id: "guardian",
    x: 1920,
    y: 4432,
    text: "돌하르방 · Dol hareubang. Một diễn giải điêu khắc basalt nguyên gốc gợi Jeju; không phải bản sao hiện vật. 돌 · Đá. 바람 · Gió.",
  },
  {
    id: "oreum",
    x: 2240,
    y: 4144,
    text: "오름 · Đồi núi lửa. 귤 · Quýt. Vườn Windstone kết hợp đá núi lửa, cây quýt và cỏ ven biển; đường vòng đi quanh chân đồi.",
  },
  {
    id: "shelter",
    x: 2400,
    y: 4432,
    text: "쉼터 · Chỗ nghỉ. Gỗ và đá basalt tạo một mái nghỉ khác với kiến trúc cung điện. Jeju, Busan, Yongin và Seoul xa nhau ngoài đời; bản đồ này là hành trình hư cấu.",
  },
];
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
        : "review/full-world/world/",
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
        import.meta.env.BASE_URL + "review/full-world/world/rf-prod-doors.png",
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
      const phase = Math.floor(this.clock / 480) % 2;
      if (phase !== this.waterPhase && !controls.reduced) {
        this.waterPhase = phase;
        for (const child of this.children.list)
          if (
            child instanceof Phaser.Tilemaps.TilemapLayer &&
            child.layer.name === "Ground"
          ) {
            for (const rect of [water.region, water.inlet]) {
              const [x, y, w, h] = rect;
              for (
                let ty = Math.floor(y / 32);
                ty < Math.ceil((y + h) / 32);
                ty++
              )
                for (
                  let tx = Math.floor(x / 32);
                  tx < Math.ceil((x + w) / 32);
                  tx++
                ) {
                  const tile = child.getTileAt(tx, ty);
                  if (tile && water.tileIndices.includes(tile.index - 1))
                    tile.index = water.tileIndices[phase] + 1;
                }
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
