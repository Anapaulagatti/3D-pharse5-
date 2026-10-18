import Phaser from "phaser";
import { JuniScene } from "../refinement/JuniScene";
import { controls } from "../game/Plaza";
import { travelState } from "./travel";
import world from "../../assets-src/living-korea/park/world.json";
import bundle from "../../assets-src/living-korea/park/outdoor-bundle.json";
import anchors from "../../public/review/living-korea/park/anchors.json";
export class NamsanPark extends JuniScene {
  private scenery: Phaser.GameObjects.Image[] = [];
  private leaves: Phaser.GameObjects.Image[] = [];
  private clock = 0;
  private cull = "";
  private scenicStops = 0;
  private leaving = false;
  private readonly overview = new URLSearchParams(location.search).has(
    "overview",
  );
  constructor() {
    super({
      key: "namsan",
      layout: world,
      bundle,
      anchors,
      assetRoot: "review/living-korea/park/",
      ambience: false,
    });
  }
  override preload() {
    if (this.textures.exists("tiles")) this.textures.remove("tiles");
    super.preload();
  }
  override create() {
    super.create();
    this.scenery = [];
    this.leaves = [];
    this.clock = 0;
    this.cull = "";
    this.leaving = false;
    for (const o of this.children.list)
      if (
        o instanceof Phaser.GameObjects.Image &&
        bundle.props[o.texture.key as keyof typeof bundle.props]
      )
        this.scenery.push(o);
    for (let i = 0; i < 6; i++)
      this.leaves.push(
        this.add.image(360 + i * 120, 800, "leaf-review").setDepth(8000),
      );
    for (const [x, y, text] of [
      [832, 696, "전망탑 · Tháp quan sát · E"],
      [1120, 848, "전망 · Đài ngắm cảnh · E"],
      [384, 864, "숲 · Rừng thông · E"],
      [704, 1176, "문화 거리 · Về phố văn hóa · E"],
    ] as const)
      this.add
        .text(x, y, text, {
          fontFamily: "sans-serif",
          fontSize: "12px",
          color: "#fff1cd",
          backgroundColor: "#294b42",
          padding: { x: 6, y: 4 },
        })
        .setOrigin(0.5, 0)
        .setDepth(9500)
        .setInteractive()
        .on("pointerdown", () => this.interact());
    if (new URLSearchParams(location.search).has("qa"))
      window.__SEOUL_TEST__ = {
        place: (x, y) => {
          this.player.setPosition(x, y);
          this.player.body?.reset(x, y);
          this.lastPosition = { x, y };
          this.invalidateCue();
        },
      };
    this.game.canvas.setAttribute(
      "aria-label",
      "Namsan — công viên tháp quan sát hư cấu. Đi theo đường rừng, lên bậc đá đài ngắm cảnh; E khám phá hoặc trở về khu di sản.",
    );
    this.events.once("shutdown", () => {
      delete window.__SEOUL__;
      delete window.__SEOUL_TEST__;
      delete window.__KOREA__;
    });
  }
  private near(x: number, y: number, r = 100) {
    return Phaser.Math.Distance.Between(this.player.x, this.player.y, x, y) < r;
  }
  private say(text: string) {
    this.interactions++;
    this.scenicStops++;
    window.dispatchEvent(new CustomEvent("town-dialog", { detail: text }));
  }
  public returnToHeritage() {
    if (this.leaving) return;
    this.leaving = true;
    this.player.setVelocity(0);
    controls.x = controls.y = 0;
    controls.run = false;
    travelState.returnNorth = true;
    travelState.transitions++;
    this.scene.start("plaza");
  }
  override interact() {
    if (controls.paused || document.hidden || this.leaving) return;
    if (this.near(704, 1120, 128)) {
      window.dispatchEvent(
        new CustomEvent("korea-travel", { detail: "heritage" }),
      );
      return;
    }
    if (this.near(1120, 784, 120)) {
      this.say(
        "전망 · Tầm nhìn. 산 · Núi. 숲 · Rừng. Từ đài cao, thử tìm mái nhà, rừng và con đường đã đi qua. Đài quan sát này lấy cảm hứng Namsan; đây là điểm đến trong thế giới du lịch hư cấu, không phải bản tái dựng địa lý Seoul.",
      );
      window.dispatchEvent(new Event("korea-scenic-view"));
      return;
    }
    if (this.near(832, 672, 120)) {
      this.say(
        "전망탑 · Tháp quan sát. Một tháp truyền phát và quan sát gợi Namsan, với sảnh khách, vườn trên đồi và tháp ngắm cảnh. Artwork gốc; không đại diện cho một cơ sở du lịch thật. Đi về phía đông để lên đài ngắm cảnh qua bậc đá.",
      );
      return;
    }
    if (this.near(384, 816, 120)) {
      this.say(
        "숲 · Rừng. 소나무 · Cây thông. Namsan là ngọn đồi giữa Seoul; các điểm Busan, Yongin và Jeju ở những vùng xa nhau ngoài đời. Hành trình của Korean Arena nối các vùng bằng chuyển cảnh du lịch, không gộp chúng thành một khu phố thật.",
      );
      return;
    }
    this.say(
      "Theo đường đất lên sảnh tháp; nhánh phía đông dẫn đến đài ngắm cảnh có bậc đá. Vườn đến phía nam đưa bạn trở về phố văn hóa. Công viên giải trí, bờ biển Busan và vườn Jeju hiện mới ở quy hoạch.",
    );
  }
  override interactProp(kind: string) {
    if (controls.paused || document.hidden) return;
    if (kind === "kr-directory" && this.near(512, 1168, 200)) {
      window.dispatchEvent(
        new CustomEvent("korea-travel", { detail: "heritage" }),
      );
      return;
    }
    this.interact();
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.player?.body) return;
    const camera = this.cameras.main;
    camera.setFollowOffset(0, Math.min(96, this.scale.height / 4));
    const w = this.scale.width / controls.zoom,
      h = this.scale.height / controls.zoom;
    camera.setBounds(
      Math.min(0, (1408 - w) / 2),
      Math.min(0, (1280 - h) / 2),
      Math.max(w, 1408),
      Math.max(h, 1280),
    );
    if (this.overview) {
      camera.stopFollow();
      camera.setZoom(
        Math.min(this.scale.width / 1408, this.scale.height / 1280),
      );
      camera.centerOn(704, 640);
    }
    if (!controls.paused && !controls.reduced && !document.hidden) {
      this.clock += Math.min(delta, 40);
      for (let i = 0; i < this.leaves.length; i++)
        this.leaves[i].setPosition(
          Math.round(320 + i * 144 + Math.sin(this.clock / 1800 + i) * 14),
          Math.round(720 + ((i * 47 + this.clock / 90) % 340)),
        );
    }
    for (const leaf of this.leaves) leaf.setVisible(!controls.reduced);
    const v = camera.worldView,
      key = [
        Math.floor(v.x / 32),
        Math.floor(v.y / 32),
        v.width,
        v.height,
      ].join(":");
    if (key !== this.cull) {
      this.cull = key;
      for (const o of this.scenery) {
        const l = o.x - o.displayWidth * o.originX,
          t = o.y - o.displayHeight * o.originY;
        o.setVisible(
          this.overview ||
            (l + o.displayWidth > v.x - 192 &&
              l < v.right + 192 &&
              t + o.displayHeight > v.y - 192 &&
              t < v.bottom + 192),
        );
      }
      this.invalidateCue();
    }
    window.__SEOUL__ = {
      ready: true,
      area: "outdoor",
      x: this.player.x,
      y: this.player.y,
      world: [1408, 1280],
      gateOpen: false,
      transitions: travelState.transitions,
      activeProps: this.scenery.filter((o) => o.visible).length,
      totalProps: world.objects.length,
      ambientClock: this.clock,
      reservedNPCs: [],
      view: [v.x, v.y, v.width, v.height],
    };
    window.__KOREA__ = {
      district: "namsan",
      travelTransitions: travelState.transitions,
      scenicStops: this.scenicStops,
      world: [1408, 1280],
    };
    if (window.__PLAZA_REVIEW__)
      window.__PLAZA_REVIEW__.environmentClock = this.clock;
    window.dispatchEvent(
      new CustomEvent("district-position", {
        detail: {
          area: "outdoor",
          district: "namsan",
          x: this.player.x,
          y: this.player.y,
          location:
            this.player.y > 1000
              ? "Namsan · Vườn đến"
              : this.player.x > 1000
                ? "Namsan · Đài ngắm cảnh"
                : "Namsan · Đường rừng & tháp",
        },
      }),
    );
  }
}
