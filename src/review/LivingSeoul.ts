import Phaser from "phaser";
import { Gwanghwamun } from "./Gwanghwamun";
import { controls } from "../game/Plaza";
import outdoor from "../../assets-src/living-seoul/outdoor-world.json";
import outsideBundle from "../../assets-src/living-seoul/outdoor-bundle.json";
import room from "../../assets-src/living-seoul/room-world.json";
import roomBundle from "../../assets-src/living-seoul/room-bundle.json";
import outdoorAnchors from "../../public/review/living-seoul/outdoor/anchors.json";
import roomAnchors from "../../public/review/living-seoul/room/anchors.json";

declare global {
  interface Window {
    __DISTRICT__?: {
      ready: boolean;
      area: "outdoor" | "room";
      location: string;
      x: number;
      y: number;
      world: number[];
      visibleProps: number;
      totalProps: number;
      roomLoaded: boolean;
      transitions: number;
      camera: { x: number; y: number };
    };
  }
}
let transitions = 0;
let roomLoaded = false;
let returnFromRoom = false;

export class LivingSeoul extends Gwanghwamun {
  private transitioning = false;
  private lastHud = "";
  private landmarks: Phaser.GameObjects.Text[] = [];
  constructor(private inside = false) {
    super({
      key: inside ? "reading-room" : "plaza",
      layout: inside ? room : outdoor,
      bundle: inside ? roomBundle : outsideBundle,
      anchors: inside ? roomAnchors : outdoorAnchors,
      assetRoot: `review/living-seoul/${inside ? "room" : "outdoor"}/`,
      ambience: !inside,
    });
  }
  override preload() {
    super.preload();
    if (this.inside)
      this.load.image(
        "reading-room-base",
        `${import.meta.env.BASE_URL}review/living-seoul/room/room-base.png`,
      );
  }
  override create() {
    super.create();
    this.transitioning = false;
    this.lastHud = "";
    this.landmarks = [];
    if (this.inside) {
      roomLoaded = true;
      this.cameras.main.setBackgroundColor("#263f37");
      this.add.image(0, 0, "reading-room-base").setOrigin(0).setDepth(-95);
    } else if (returnFromRoom) {
      this.player.setPosition(1536, 475);
      this.lastPosition = { x: 1536, y: 475 };
      returnFromRoom = false;
    }
    const labels = this.inside
      ? [
          { x: 385, y: 350, text: "✦ Bàn học · E" },
          { x: 384, y: 530, text: "↓ Ra sân · E" },
        ]
      : [
          { x: 1536, y: 448, text: "✦ Học viện Hangul · E" },
          { x: 1850, y: 560, text: "Quầy đổi sách" },
          { x: 1080, y: 640, text: "→ Ngõ sách" },
        ];
    for (const l of labels)
      this.landmarks.push(
        this.add
          .text(l.x, l.y, l.text, {
            fontFamily: "sans-serif",
            fontSize: "12px",
            color: "#fff4d0",
            backgroundColor: "#294b42",
            padding: { x: 6, y: 4 },
          })
          .setOrigin(0.5, 0)
          .setDepth(9500)
          .setInteractive()
          .on("pointerdown", () => this.interact()),
      );
    this.game.canvas.setAttribute(
      "aria-label",
      "Living Seoul: WASD/mũi tên đi, Shift chạy; E gần cửa để vào/ra Học viện hoặc mở bài học. Điều khiển cảm ứng bên dưới.",
    );
    this.events.once("shutdown", () => {
      delete window.__DISTRICT__;
    });
  }
  private near(x: number, y: number, r: number) {
    return Phaser.Math.Distance.Between(this.player.x, this.player.y, x, y) < r;
  }
  private changeArea() {
    if (this.transitioning || controls.paused || document.hidden) return;
    this.transitioning = true;
    this.player.setVelocity(0);
    controls.x = 0;
    controls.y = 0;
    this.input.keyboard?.resetKeys();
    const next = this.inside ? "plaza" : "reading-room";
    if (this.inside) returnFromRoom = true;
    const go = () => {
      transitions++;
      this.scene.start(next);
    };
    if (controls.reduced) go();
    else {
      this.cameras.main.fadeOut(180, 35, 49, 45);
      this.cameras.main.once("camerafadeoutcomplete", go);
    }
  }
  override interact() {
    if (controls.paused || document.hidden || this.transitioning) return;
    if (!this.inside && this.near(1536, 434, 88)) {
      this.changeArea();
      return;
    }
    if (this.inside && this.near(384, 510, 56)) {
      this.changeArea();
      return;
    }
    if (this.inside && this.near(385, 354, 100)) {
      window.dispatchEvent(new Event("academy-lesson"));
      return;
    }
    window.dispatchEvent(
      new CustomEvent("town-dialog", {
        detail: this.inside
          ? "Phòng đọc Học viện · Đến gần bàn viết ở giữa, nhấn E để ghép tên ba chữ Hangul. Cửa ra ở phía nam. Đây là không gian thử đầu tiên; Sejong và ba vị khách lịch sử mới chưa được sản xuất."
          : this.player.x > 1024
            ? "Ngõ sách → Học viện Hangul. Đến bậc cửa giữa tòa nhà, nhấn E để vào. Quầy đổi sách và vườn đọc là nơi nghỉ; các khu khoa học, nghệ thuật và bảo tàng hiện mới ở bản quy hoạch."
            : "Gwanghwamun được giữ nguyên. Qua cầu đá, theo đường phía đông rồi ngõ sách để đến Học viện. Xem chấm vị trí trên bản đồ nhỏ.",
      }),
    );
  }
  override interactProp(kind: string) {
    if (this.inside || kind === "academy") {
      this.interact();
      return;
    }
    if (["kiosk", "sign", "shelf", "desk"].includes(kind)) {
      window.dispatchEvent(
        new CustomEvent("town-dialog", {
          detail:
            "Quầy sách của Học viện · 책 nghĩa là sách. Lối vào phòng đọc nằm ở cửa giữa Học viện, phía tây quầy. Hãy đến gần rồi nhấn E.",
        }),
      );
      return;
    }
    super.interactProp(kind);
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.player?.body) return;
    if (this.transitioning) this.player.setVelocity(0);
    const camera = this.cameras.main;
    if (this.inside) {
      const width = this.scale.width / controls.zoom;
      const height = this.scale.height / controls.zoom;
      camera.setBounds(
        Math.min(0, (768 - width) / 2),
        Math.min(0, (576 - height) / 2),
        Math.max(768, width),
        Math.max(576, height),
      );
    }
    if (!new URLSearchParams(location.search).has("overview"))
      camera.startFollow(this.player, true, 1, 1, 0, this.inside ? 25 : 55);
    const b = this.inside ? roomBundle : outsideBundle;
    const images = this.children.list.filter(
      (o): o is Phaser.GameObjects.Image =>
        o instanceof Phaser.GameObjects.Image &&
        o.type === "Image" &&
        o.depth < 8000,
    );
    const view = camera.worldView;
    let visible = 0;
    for (const image of images) {
      const bounds = image.getBounds();
      const show = Phaser.Geom.Intersects.RectangleToRectangle(view, bounds);
      image.setVisible(show);
      if (show) visible++;
    }
    const name = this.inside
      ? "Phòng đọc Học viện"
      : this.player.x > 1300
        ? "Sân Học viện"
        : this.player.x > 1024
          ? "Ngõ sách"
          : "Gwanghwamun Plaza";
    window.__DISTRICT__ = {
      ready: true,
      area: this.inside ? "room" : "outdoor",
      location: name,
      x: this.player.x,
      y: this.player.y,
      world: this.inside ? [768, 576] : [2048, 768],
      visibleProps: visible,
      totalProps: b.objects.length,
      roomLoaded,
      transitions,
      camera: { x: camera.scrollX, y: camera.scrollY },
    };
    const hud = `${name}:${Math.round(this.player.x / 4)},${Math.round(this.player.y / 4)}`;
    if (hud !== this.lastHud) {
      this.lastHud = hud;
      window.dispatchEvent(
        new CustomEvent("district-position", { detail: window.__DISTRICT__ }),
      );
    }
    this.landmarks.forEach((l) =>
      l.setAlpha(this.near(l.x, l.y, 180) ? 1 : 0.8),
    );
    if (window.__PLAZA_REVIEW__) window.__PLAZA_REVIEW__.district = name;
  }
}
