import Phaser from "phaser";
import { Plaza, controls } from "../game/Plaza";
import layout from "../../assets-src/gwanghwamun/world.json";
import bundle from "../../assets-src/gwanghwamun/map-bundle.json";
import anchors from "../../public/review/gwanghwamun/anchors.json";

type View = "front" | "back" | "left" | "right";
declare global {
  interface Window {
    __PLAZA_REVIEW__?: {
      ready: boolean;
      district: string;
      player: string;
      direction: View;
      nativeBodyHeight: number;
      staticCharacter: true;
      environmentClock: number;
      occludedPixels: number;
      userApproval: "PENDING";
    };
  }
}

// Only artwork/layout differ. Movement, acceleration, keyboard/touch, pause,
// visibility and UI remain the existing Plaza controller's implementation.
export class Gwanghwamun extends Plaza {
  private juni!: Phaser.GameObjects.Image;
  private cue!: Phaser.GameObjects.Image;
  private cueTexture!: Phaser.Textures.CanvasTexture;
  private mask = document.createElement("canvas");
  private leaves: Phaser.GameObjects.Image[] = [];
  private water!: Phaser.GameObjects.TileSprite;
  private lamps: Phaser.GameObjects.Image[] = [];
  private clock = 0;
  private cueKey = "";
  private covered = 0;
  constructor() {
    super({
      layout,
      assetRoot: "review/gwanghwamun/",
      anchors,
      guests: false,
      ambience: false,
    });
  }
  preload() {
    super.preload();
    const base = import.meta.env.BASE_URL;
    this.load.atlas(
      "juni-review",
      `${base}review/characters/B/direction-stills-atlas-00.png`,
      `${base}review/characters/B/atlas.json`,
    );
    this.load.image("water-review", `${base}review/gwanghwamun/water.png`);
    this.load.image("leaf-review", `${base}review/gwanghwamun/leaf.png`);
  }
  create() {
    super.create();
    // Centre the existing16x8 foot collider on Juni's recorded root; default game unchanged.
    this.player.body?.setOffset(16, 60);
    this.juni = this.add
      .image(this.player.x, this.player.y, "juni-review", "front")
      .setOrigin(0.5, 96 / 104);
    this.mask.width = 80;
    this.mask.height = 104;
    this.cueTexture = this.textures.createCanvas(
      "juni-occlusion-cue",
      80,
      104,
    )!;
    this.cue = this.add
      .image(this.player.x, this.player.y, "juni-occlusion-cue")
      .setOrigin(0.5, 96 / 104)
      .setDepth(9000)
      .setAlpha(0.48);
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
    for (let i = 0; i < 6; i++)
      this.leaves.push(
        this.add
          .image(130 + i * 139, 200 + i * 65, "leaf-review")
          .setDepth(8000),
      );
    this.game.canvas.setAttribute(
      "aria-label",
      "Gwanghwamun Plaza — Juni bốn hướng tĩnh. WASD/mũi tên, Shift chạy, E khám phá địa điểm. Chưa có hoạt ảnh nhân vật mới.",
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
    const nearest = layout.objects
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
            "Đến gần cổng, tượng Sejong, đình đọc sách hoặc cây; nhấn E hay chạm vào địa điểm. Juni đang dùng bốn hướng tĩnh, chưa có bộ hoạt ảnh mới.",
        }),
      );
  }
  override emote() {
    // Four static Juni views are not action clips; no hidden legacy emote is played.
  }
  private updateCue(view: View) {
    const x = Math.round(this.player.x),
      y = Math.round(this.player.y);
    const key = `${x},${y},${view}`;
    if (key === this.cueKey) return;
    this.cueKey = key;
    const mask = this.mask.getContext("2d")!;
    mask.clearRect(0, 0, 80, 104);
    const left = x - 40,
      top = y - 96;
    for (const o of bundle.objects) {
      if (o.sortY <= y || o.prop === "bridge") continue;
      const p = bundle.props[o.prop as keyof typeof bundle.props];
      const ox = o.x - p.anchor_px[0] - left,
        oy = o.y - p.anchor_px[1] - top;
      if (ox >= 80 || oy >= 104 || ox + p.size[0] <= 0 || oy + p.size[1] <= 0)
        continue;
      mask.drawImage(
        this.textures.get(o.prop).getSourceImage() as HTMLImageElement,
        ox,
        oy,
      );
    }
    const f = this.textures.getFrame("juni-review", view);
    const ctx = this.cueTexture.context;
    ctx.clearRect(0, 0, 80, 104);
    ctx.globalCompositeOperation = "source-over";
    ctx.drawImage(
      f.source.image as HTMLImageElement,
      f.cutX,
      f.cutY,
      f.cutWidth,
      f.cutHeight,
      0,
      0,
      80,
      104,
    );
    ctx.globalCompositeOperation = "source-in";
    ctx.fillStyle = "#fff0b8";
    ctx.fillRect(0, 0, 80, 104);
    ctx.globalCompositeOperation = "destination-in";
    ctx.drawImage(this.mask, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    const pixels = ctx.getImageData(0, 0, 80, 104).data;
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
    this.juni
      .setPosition(Math.round(m.x), Math.round(m.y))
      .setFrame(view)
      .setDepth(Math.round(m.y) + 0.1);
    this.cue.setPosition(Math.round(m.x), Math.round(m.y));
    this.updateCue(view);
    if (!m.paused && !controls.reduced) {
      this.clock += Math.min(delta, 50);
      this.water.tilePositionY = Math.floor(this.clock / 230);
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
    m.avatarVersion = "Juni-provisional-static-directions";
    m.heroCssHeight = 80 * controls.zoom;
    m.animationFrames = 0;
    window.__PLAZA_REVIEW__ = {
      ready: true,
      district: "Gwanghwamun Plaza · B Ginkgo Commons",
      player: "Juni · provisional B",
      direction: view,
      nativeBodyHeight: 80,
      staticCharacter: true,
      environmentClock: this.clock,
      occludedPixels: this.covered,
      userApproval: "PENDING",
    };
  }
}
