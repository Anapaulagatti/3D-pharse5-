import Phaser from "phaser";
import { JuniMotion, type JuniView } from "./JuniMotion";
import type { Emote } from "../game/ActorMotion";
import animation from "../../assets-src/juni-animation/runtime.json";
import { Plaza, controls } from "../game/Plaza";
import layout from "../../assets-src/gwanghwamun/world.json";
import bundle from "../../assets-src/gwanghwamun/map-bundle.json";
import anchors from "../../public/review/gwanghwamun/anchors.json";

type View = JuniView;
export type ReviewWorld = {
  layout: typeof layout;
  bundle: {
    objects: { sortY: number; prop: string; x: number; y: number }[];
    props: Record<string, { anchor_px: number[]; size: number[] }>;
  };
  anchors: Record<string, number[]>;
  assetRoot: string;
  key?: string;
  ambience?: boolean;
};
declare global {
  interface Window {
    __PLAZA_REVIEW__?: {
      ready: boolean;
      district: string;
      player: string;
      direction: View;
      nativeBodyHeight: number;
      staticCharacter: false;
      action: string;
      frame: string;
      phase: number;
      environmentClock: number;
      occludedPixels: number;
      userApproval: "PENDING";
    };
  }
}

// Only artwork/layout differ. Movement, acceleration, keyboard/touch, pause,
// visibility and UI remain the existing Plaza controller's implementation.
export class Gwanghwamun extends Plaza {
  private juniMotion = new JuniMotion();
  protected lastPosition = { x: 512, y: 600 };
  private juni!: Phaser.GameObjects.Sprite;
  private cue!: Phaser.GameObjects.Image;
  private cueTexture!: Phaser.Textures.CanvasTexture;
  private mask = document.createElement("canvas");
  private leaves: Phaser.GameObjects.Image[] = [];
  private water?: Phaser.GameObjects.TileSprite;
  private lamps: Phaser.GameObjects.Image[] = [];
  private clock = 0;
  private cueKey = "";
  private covered = 0;
  constructor(private review?: ReviewWorld) {
    super({
      key: review?.key,
      layout: review?.layout ?? layout,
      assetRoot: review?.assetRoot ?? "review/gwanghwamun/",
      anchors: review?.anchors ?? anchors,
      guests: false,
      ambience: false,
    });
  }
  preload() {
    super.preload();
    const base = import.meta.env.BASE_URL;
    this.load.atlas(
      "juni-review",
      `${base}review/juni-animation/juni.png`,
      `${base}review/juni-animation/juni.json`,
    );
    this.load.image("water-review", `${base}review/gwanghwamun/water.png`);
    this.load.image("leaf-review", `${base}review/gwanghwamun/leaf.png`);
  }
  create() {
    this.leaves = [];
    this.lamps = [];
    this.cueKey = "";
    this.juniMotion = new JuniMotion();
    super.create();
    this.lastPosition = { x: this.player.x, y: this.player.y };
    // Centre the existing16x8 foot collider on Juni's recorded root; default game unchanged.
    this.player.body?.setOffset(16, 60);
    this.juni = this.add
      .sprite(this.player.x, this.player.y, "juni-review", "idle-front-0")
      .setOrigin(0.5, 100 / 112);
    this.mask.width = 96;
    this.mask.height = 112;
    const cueTextureKey = `juni-occlusion-cue-${this.sys.settings.key}`;
    if (this.textures.exists(cueTextureKey))
      this.textures.remove(cueTextureKey);
    this.cueTexture = this.textures.createCanvas(cueTextureKey, 96, 112)!;
    this.cue = this.add
      .image(this.player.x, this.player.y, cueTextureKey)
      .setOrigin(0.5, 100 / 112)
      .setDepth(9000)
      .setAlpha(0.48);
    if (this.review?.ambience !== false)
      this.water = this.add
        .tileSprite(704, 576, 64, 320, "water-review")
        .setDepth(-80);
    // Keep the walkable deck below Juni instead of sorting by its south edge.
    this.children.list.forEach((o) => {
      if (o instanceof Phaser.GameObjects.Image && o.texture.key === "bridge")
        o.setDepth(-60);
      if (o instanceof Phaser.GameObjects.Image && o.texture.key === "lantern")
        this.lamps.push(o);
    });
    for (let i = 0; i < (this.review?.ambience === false ? 0 : 6); i++)
      this.leaves.push(
        this.add
          .image(130 + i * 139, 200 + i * 65, "leaf-review")
          .setDepth(8000),
      );
    this.game.canvas.setAttribute(
      "aria-label",
      "Gwanghwamun Plaza — Juni có hoạt ảnh bốn hướng. WASD/mũi tên đi bộ, Shift chạy, E khám phá; nút Chào, Vui mừng và Biểu cảm.",
    );
    this.events.once("shutdown", () => {
      delete window.__PLAZA_REVIEW__;
    });
  }
  override interactProp(kind: string) {
    this.interactions++;
    const text: Record<string, string> = {
      gate: "광화문 · Gwanghwamun — cổng hai tầng trên bệ đá ba vòm, lấy cảm hứng kiến trúc Joseon. Đây là bản diễn giải RPG gốc, không phải bản tái dựng lịch sử.",
      sejong:
        "세종대왕 · Sejong — tượng học giả ngồi với sách. Dấu mốc học tập của quảng trường; đây là tượng, chưa phải NPC mới hay nhiệm vụ hoàn chỉnh.",
      pavilion:
        "책 · Sách — đình đọc sách bằng gỗ, nơi gặp gỡ và học trong tương lai. Bản này chỉ duyệt nghệ thuật môi trường.",
      hall: "한지 · Hanji — nhà trà/sách với cửa giấy và lưới gỗ. Chưa mở nội thất.",
      bridge:
        "다리 · Cầu — cầu đá qua rãnh nước trang trí trong quảng trường. Chưa xây khu Cheonggyecheon.",
      ginkgo:
        "은행나무 · Bạch quả — tán vàng, thân cây có va chạm; bạn có thể đi sau tán lá.",
      tree: "나무 · Cây — tán lá được phân lớp theo vị trí chân Juni, không làm mờ cả cây.",
      lantern:
        "등불 · Đèn — đèn hanji ấm; chuyển động nhẹ dừng khi giảm chuyển động hoặc tạm dừng.",
    };
    window.dispatchEvent(
      new CustomEvent("town-dialog", {
        detail:
          text[kind] ??
          "Một chi tiết sân vườn gốc của Ginkgo Commons. Hình ảnh đang chờ bạn duyệt.",
      }),
    );
  }
  override interact() {
    const nearest = (this.review?.layout ?? layout).objects
      .map((o) => ({
        o,
        d: Phaser.Math.Distance.Between(this.player.x, this.player.y, o.x, o.y),
      }))
      .sort((a, b) => a.d - b.d)[0];
    if (nearest && nearest.d < 140) this.interactProp(nearest.o.kind);
    else
      window.dispatchEvent(
        new CustomEvent("town-dialog", {
          detail:
            "Đến gần cổng, tượng Sejong, đình đọc sách hoặc cây; nhấn E hay chạm vào địa điểm. Dùng Chào, Vui mừng hoặc Biểu cảm để Juni đáp lại.",
        }),
      );
  }
  override emote(action: Emote) {
    if (!controls.paused && !document.hidden)
      this.juniMotion.gesture(
        action === "pose" || action === "think" ? "social" : action,
      );
  }
  private updateCue(frame: string) {
    const x = Math.round(this.player.x),
      y = Math.round(this.player.y);
    const key = `${x},${y},${frame}`;
    if (key === this.cueKey) return;
    this.cueKey = key;
    const mask = this.mask.getContext("2d")!;
    mask.clearRect(0, 0, 96, 112);
    const left = x - 48,
      top = y - 100;
    const map = this.review?.bundle ?? bundle;
    for (const o of map.objects) {
      if (o.sortY <= y || o.prop === "bridge") continue;
      const p = (map.props as ReviewWorld["bundle"]["props"])[o.prop];
      const ox = o.x - p.anchor_px[0] - left,
        oy = o.y - p.anchor_px[1] - top;
      if (ox >= 96 || oy >= 112 || ox + p.size[0] <= 0 || oy + p.size[1] <= 0)
        continue;
      mask.drawImage(
        this.textures.get(o.prop).getSourceImage() as HTMLImageElement,
        ox,
        oy,
      );
    }
    const f = this.textures.getFrame("juni-review", frame);
    const ctx = this.cueTexture.context;
    ctx.clearRect(0, 0, 96, 112);
    ctx.globalCompositeOperation = "source-over";
    ctx.drawImage(
      f.source.image as HTMLImageElement,
      f.cutX,
      f.cutY,
      f.cutWidth,
      f.cutHeight,
      0,
      0,
      96,
      112,
    );
    ctx.globalCompositeOperation = "source-in";
    ctx.fillStyle = "#fff0b8";
    ctx.fillRect(0, 0, 96, 112);
    ctx.globalCompositeOperation = "destination-in";
    ctx.drawImage(this.mask, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    const pixels = ctx.getImageData(0, 0, 96, 112).data;
    this.covered = 0;
    for (let i = 3; i < pixels.length; i += 4)
      if (pixels[i] > 0) this.covered++;
    this.cueTexture.refresh();
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.juni) return;
    this.player.setVisible(false);
    this.layers.forEach((l) => l.setVisible(false));
    const m = window.__PIXEL_METRICS__!;
    const view: View =
      m.direction === "down"
        ? "front"
        : m.direction === "up"
          ? "back"
          : m.direction;
    const distance = Math.hypot(
      m.x - this.lastPosition.x,
      m.y - this.lastPosition.y,
    );
    this.lastPosition = { x: m.x, y: m.y };
    const frame = this.juniMotion.step(
      delta,
      distance,
      m.moving,
      m.speed === 100,
      view,
      controls.reduced,
      m.paused,
    );
    this.juni
      .setPosition(Math.round(m.x), Math.round(m.y))
      .setFrame(frame)
      .setDepth(Math.round(m.y) + 0.1);
    this.cue.setPosition(Math.round(m.x), Math.round(m.y));
    this.updateCue(frame);
    if (!m.paused && !controls.reduced) {
      this.clock += Math.min(delta, 50);
      if (this.water) this.water.tilePositionY = Math.floor(this.clock / 230);
      this.leaves.forEach((leaf, i) =>
        leaf.setPosition(
          Math.round(90 + i * 144 + Math.sin(this.clock / 2100 + i) * 12),
          Math.round(190 + ((i * 79 + this.clock / 64) % 480)),
        ),
      );
      this.lamps.forEach((lamp, i) =>
        lamp.setTint(
          Phaser.Display.Color.GetColor(
            255,
            248 + Math.round(7 * Math.sin(this.clock / 430 + i)),
            235 + Math.round(20 * Math.sin(this.clock / 650 + i)),
          ),
        ),
      );
    }
    this.leaves.forEach((l) => l.setVisible(!controls.reduced));
    if (this.scale.width < 600 && controls.zoom === 1)
      this.cameras.main.startFollow(this.player, true, 1, 1, 0, 60);
    m.avatarVersion = "Juni-imagegen-actions-v1";
    m.frame = frame;
    m.layerFrames = [frame];
    m.heroCssHeight = 80 * controls.zoom;
    m.animationFrames = animation.frameCount;
    window.__PLAZA_REVIEW__ = {
      ready: true,
      district: "Gwanghwamun Plaza · B Ginkgo Commons",
      player: "Juni · provisional B",
      direction: this.juniMotion.view,
      action: this.juniMotion.action,
      frame,
      phase: this.juniMotion.phase,
      nativeBodyHeight: 80,
      staticCharacter: false,
      environmentClock: this.clock,
      occludedPixels: this.covered,
      userApproval: "PENDING",
    };
  }
}
