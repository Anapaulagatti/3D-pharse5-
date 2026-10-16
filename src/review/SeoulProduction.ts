import Phaser from "phaser";
import { Gwanghwamun } from "./Gwanghwamun";
import { controls } from "../game/Plaza";
import outdoor from "../../assets-src/seoul-production/world.json";
import bundle from "../../assets-src/seoul-production/outdoor-bundle.json";
import anchors from "../../public/review/seoul-production/anchors.json";
import room from "../../assets-src/living-seoul/room-world.json";
import roomBundle from "../../assets-src/living-seoul/room-bundle.json";
import roomAnchors from "../../public/review/living-seoul/room/anchors.json";

declare global {
  interface Window {
    __SEOUL_TEST__?: { place: (x: number, y: number) => void };
    __SEOUL__?: {
      ready: boolean;
      area: string;
      x: number;
      y: number;
      world: number[];
      gateOpen: boolean;
      transitions: number;
      activeProps: number;
      totalProps: number;
      ambientClock: number;
      reservedNPCs: string[];
      view: number[];
    };
  }
}
let returning = false;
let transitions = 0;
let gateOpen = false;

export class SeoulProduction extends Gwanghwamun {
  private transitioning = false;
  private door?: Phaser.GameObjects.Image;
  private leafBody?: Phaser.Physics.Arcade.StaticBody;
  private foliage: Phaser.GameObjects.Image[] = [];
  private productionLamps: Phaser.GameObjects.Image[] = [];
  private ambientClock = 0;
  private labels: Phaser.GameObjects.Text[] = [];
  constructor(private inside = false) {
    super({
      key: inside ? "production-room" : "plaza",
      layout: inside ? room : outdoor,
      bundle: inside ? roomBundle : bundle,
      anchors: inside ? roomAnchors : anchors,
      assetRoot: inside
        ? "review/living-seoul/room/"
        : "review/seoul-production/",
      ambience: false,
    });
  }
  override preload() {
    super.preload();
    if (this.inside)
      this.load.image(
        "production-room-base",
        `${import.meta.env.BASE_URL}review/living-seoul/room/room-base.png`,
      );
    else
      this.load.image(
        "production-door",
        `${import.meta.env.BASE_URL}review/seoul-production/prod-doors.png`,
      );
  }
  override create() {
    super.create();
    this.transitioning = false;
    this.foliage = [];
    this.productionLamps = [];
    this.labels = [];
    this.ambientClock = 0;
    if (this.inside) {
      this.add.image(0, 0, "production-room-base").setOrigin(0).setDepth(-95);
    } else {
      if (returning) {
        this.player.setPosition(672, 832);
        this.lastPosition = { x: 672, y: 832 };
        returning = false;
      }
      this.door = this.add
        .image(2048, 743, "production-door")
        .setOrigin(0.5, 1)
        .setDepth(760)
        .setVisible(!gateOpen);
      const zone = this.add.zone(2048, 640, 80, 192);
      this.physics.add.existing(zone, true);
      this.leafBody = zone.body as Phaser.Physics.Arcade.StaticBody;
      this.leafBody.enable = !gateOpen;
      this.physics.add.collider(this.player, zone);
      for (let i = 0; i < 8; i++)
        this.foliage.push(
          this.add
            .image(1536 + i * 144, 1000 + (i % 3) * 80, "leaf-review")
            .setDepth(8000),
        );
      this.children.list.forEach((o) => {
        if (
          o instanceof Phaser.GameObjects.Image &&
          o.texture.key === "prod-lantern"
        )
          this.productionLamps.push(o);
      });
    }
    const labels = this.inside
      ? [
          [385, 350, "✦ Bàn học · E"],
          [384, 530, "↓ Ra sân · E"],
        ]
      : [
          [2048, 816, "광화문 · Cổng cung điện · E"],
          [672, 824, "한글 배움터 · Phòng đọc · E"],
          [3168, 1152, "과학 · Sân phát minh · E"],
          [3552, 1312, "역사 · Hiên lịch sử · E"],
          [2280, 1240, "세종 · Dấu mốc Hangul · E"],
          [1280, 1632, "↓ Khu tiếp theo · Chờ duyệt"],
          [2780, 1632, "↓ Khu tiếp theo · Chờ duyệt"],
        ];
    for (const [x, y, text] of labels)
      this.labels.push(
        this.add
          .text(Number(x), Number(y), String(text), {
            fontFamily: "sans-serif",
            fontSize: "12px",
            color: "#fff2d2",
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
      "Living Seoul — WASD/mũi tên đi, Shift chạy, E mở cổng / vào phòng đọc / khám phá; có điều khiển cảm ứng.",
    );
    if (new URLSearchParams(location.search).has("qa"))
      window.__SEOUL_TEST__ = {
        place: (x, y) => {
          this.player.setPosition(x, y);
          this.player.body?.reset(x, y);
          this.lastPosition = { x, y };
        },
      };
    this.events.once("shutdown", () => {
      delete window.__SEOUL__;
      delete window.__SEOUL_TEST__;
    });
  }
  private near(x: number, y: number, r = 104) {
    return Phaser.Math.Distance.Between(this.player.x, this.player.y, x, y) < r;
  }
  private say(text: string) {
    window.dispatchEvent(new CustomEvent("town-dialog", { detail: text }));
  }
  private changeArea() {
    if (this.transitioning || controls.paused || document.hidden) return;
    this.transitioning = true;
    this.player.setVelocity(0);
    controls.x = 0;
    controls.y = 0;
    this.input.keyboard?.resetKeys();
    if (this.inside) returning = true;
    const go = () => {
      transitions++;
      this.scene.start(this.inside ? "plaza" : "production-room");
    };
    if (controls.reduced) go();
    else {
      this.cameras.main.fadeOut(180, 35, 49, 45);
      this.cameras.main.once("camerafadeoutcomplete", go);
    }
  }
  private toggleGate() {
    if (!this.near(2048, 752, 180)) {
      this.say(
        "광화문 · Đến gần bậc cổng rồi nhấn E. Cổng chỉ mở sân ngoài; cung trong còn khép.",
      );
      return;
    }
    if (
      gateOpen &&
      this.player.x > 1992 &&
      this.player.x < 2104 &&
      this.player.y > 528 &&
      this.player.y < 756
    ) {
      this.say("Hãy bước ra khỏi ngưỡng cửa trước khi khép cổng.");
      return;
    }
    gateOpen = !gateOpen;
    this.door?.setVisible(!gateOpen);
    if (this.leafBody) this.leafBody.enable = !gateOpen;
    this.say(
      gateOpen
        ? "문을 열어요 · Mở cổng. Bạn có thể thăm sân ngoài; tường phía bắc giữ cung trong ở trạng thái đóng."
        : "문을 닫아요 · Khép cổng. Lối ngưỡng cửa hiện có va chạm trở lại.",
    );
  }
  override interact() {
    if (controls.paused || document.hidden || this.transitioning) return;
    if (this.inside) {
      if (this.near(384, 510, 56)) this.changeArea();
      else if (this.near(385, 354, 100))
        window.dispatchEvent(new Event("academy-lesson"));
      else
        this.say("Đến bàn viết để học ba tên chữ Hangul. Cửa ra ở phía nam.");
      return;
    }
    if (this.near(672, 800, 64)) {
      this.changeArea();
      return;
    }
    if (this.near(2048, 752, 180)) {
      this.toggleGate();
      return;
    }
    if (
      this.near(3168, 1120, 160) ||
      this.near(3680, 880, 160) ||
      this.near(3112, 988, 120)
    ) {
      this.say(
        "과학 · Khoa học. Xem hỗn thiên nghi, đồng hồ mặt trời dạng bán cầu và mô hình đồng hồ nước. Lấy cảm hứng thiết bị thời Joseon; đây là bản diễn giải giáo dục gốc, không phải bản phục dựng chính xác. Jang Yeong-sil sẽ đến sau vòng duyệt này.",
      );
      return;
    }
    if (this.near(3552, 1392, 260)) {
      this.say(
        "역사 · Lịch sử. Mô hình thuyền rùa và bàn chiến thuật giúp khám phá lịch sử hàng hải; bảo tàng ở phố nội địa, không có bến cảng giả. Yi Sun-sin mới được giữ chỗ, chưa có NPC mới.",
      );
      return;
    }
    if (this.near(2280, 1248, 160)) {
      this.say(
        "한글 · Hangul. Tượng Sejong là điểm hẹn của quảng trường. Đi theo đường cong về tây tới sân Học viện, vào phòng đọc để ghép ㄱ, ㄴ và ㅁ.",
      );
      return;
    }
    this.say(
      "Cổng cung điện ở phía bắc; Học viện ở phía tây, xưởng khoa học và bảo tàng ở phía đông. E gần cửa phòng đọc để học. Khu phía nam, suối và nhà ở chờ bạn duyệt Stage B trước khi xây.",
    );
  }
  override interactProp(kind: string) {
    if (controls.paused || document.hidden) return;
    if (kind === "prod-gate") {
      this.toggleGate();
      return;
    }
    if (kind === "prod-hall" || this.inside) {
      this.interact();
      return;
    }
    if (
      [
        "prod-armillary",
        "prod-sundial",
        "prod-clock",
        "prod-workshop",
      ].includes(kind)
    ) {
      this.say(
        "Sân phát minh · Ba mô hình thiên văn và đo thời gian, diễn giải gốc dựa trên bối cảnh khoa học Joseon. Điểm đặt Jang Yeong-sil được giữ thoáng ở sân đông; chưa tạo NPC mới.",
      );
      return;
    }
    if (["prod-strategy", "prod-ship", "prod-museum"].includes(kind)) {
      this.say(
        "Hiên lịch sử · Bàn chiến thuật và mô hình thuyền rùa là hiện vật thu nhỏ. Tòa trưng bày dài có tiền sảnh lệch tây, khác biệt với Học viện và xưởng.",
      );
      return;
    }
    if (kind === "prod-lantern") {
      this.productionLamps.forEach((l) => l.setTint(0xffdc94));
      this.say(
        "등불 · Đèn hanji đánh dấu lối vào. Ánh đèn nhẹ dừng khi tạm dừng hoặc giảm chuyển động.",
      );
      return;
    }
    if (kind === "prod-writing") {
      this.say(
        "책 · Sách; 붓 · Bút lông. Đi qua sân đến cửa giữa giảng đường, nhấn E để vào phòng đọc hiện có.",
      );
      return;
    }
    this.interact();
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.player?.body) return;
    if (this.transitioning) this.player.setVelocity(0);
    const camera = this.cameras.main;
    if (new URLSearchParams(location.search).has("overview")) {
      camera.stopFollow();
      camera.setZoom(
        Math.min(this.scale.width / 4096, this.scale.height / 1728),
      );
      camera.centerOn(2048, 864);
    }
    if (!new URLSearchParams(location.search).has("overview"))
      camera.startFollow(this.player, true, 1, 1, 0, this.inside ? 25 : 55);
    if (this.inside) {
      const w = this.scale.width / controls.zoom,
        h = this.scale.height / controls.zoom;
      camera.setBounds(
        Math.min(0, (768 - w) / 2),
        Math.min(0, (576 - h) / 2),
        Math.max(768, w),
        Math.max(576, h),
      );
    }
    if (!controls.reduced && !controls.paused && !document.hidden) {
      this.ambientClock += Math.min(delta, 40);
      this.foliage.forEach((l, i) =>
        l.setPosition(
          Math.round(
            1500 + i * 150 + Math.sin(this.ambientClock / 1800 + i) * 18,
          ),
          Math.round(900 + ((i * 61 + this.ambientClock / 75) % 450)),
        ),
      );
      this.productionLamps.forEach((l, i) =>
        l.setTint(
          Phaser.Display.Color.GetColor(
            255,
            245 + Math.round(10 * Math.sin(this.ambientClock / 800 + i)),
            226 + Math.round(20 * Math.sin(this.ambientClock / 650 + i)),
          ),
        ),
      );
    }
    this.foliage.forEach((l) => l.setVisible(!controls.reduced));
    let active = 0;
    const view = camera.worldView;
    this.children.list.forEach((o) => {
      if (
        o instanceof Phaser.GameObjects.Image &&
        o.type === "Image" &&
        o.depth < 8000 &&
        o !== this.door
      ) {
        const show = Phaser.Geom.Intersects.RectangleToRectangle(
          view,
          o.getBounds(),
        );
        o.setVisible(show);
        if (show) active++;
      }
    });
    this.labels.forEach((l) => l.setAlpha(this.near(l.x, l.y, 200) ? 1 : 0.65));
    const locationName = this.inside
      ? "Phòng đọc Học viện"
      : this.player.x < 1200
        ? "Sân Học viện"
        : this.player.x > 3000
          ? this.player.y < 1150
            ? "Sân phát minh"
            : "Hiên lịch sử"
          : this.player.y < 840
            ? "Cổng cung điện"
            : "Gwanghwamun Plaza";
    window.__SEOUL__ = {
      ready: true,
      area: this.inside ? "room" : "outdoor",
      x: this.player.x,
      y: this.player.y,
      world: this.inside ? [768, 576] : [4096, 1728],
      gateOpen,
      transitions,
      activeProps: active,
      totalProps: this.inside
        ? roomBundle.objects.length
        : bundle.objects.length,
      ambientClock: this.ambientClock,
      reservedNPCs: ["sejong", "jang", "yi", "saimdang (future south)"],
      view: [view.x, view.y, view.width, view.height],
    };
    window.dispatchEvent(
      new CustomEvent("district-position", {
        detail: { ...window.__SEOUL__, location: locationName },
      }),
    );
    if (window.__PLAZA_REVIEW__)
      window.__PLAZA_REVIEW__.district = locationName;
  }
}
