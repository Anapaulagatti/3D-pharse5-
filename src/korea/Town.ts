import Phaser from "phaser";
import { JuniScene } from "../refinement/JuniScene";
import { controls } from "../game/Plaza";
import outdoor from "../../assets-src/living-korea/north/world.json";
import bundle from "../../assets-src/living-korea/north/outdoor-bundle.json";
import anchors from "../../public/review/living-korea/north/anchors.json";
import room from "../../assets-src/living-seoul/room-world.json";
import roomBundle from "../../assets-src/world-refinement/room-bundle.json";
import roomAnchors from "../../public/review/living-seoul/room/anchors.json";
let returning = false,
  gateOpen = false,
  transitions = 0;
export class KoreaTown extends JuniScene {
  private transitioning = false;
  private door?: Phaser.GameObjects.Image;
  private leafBody?: Phaser.Physics.Arcade.StaticBody;
  private leaves: Phaser.GameObjects.Image[] = [];
  private lamps: Phaser.GameObjects.Image[] = [];
  private scenery: Phaser.GameObjects.Image[] = [];
  private ambient = 0;
  private activeScenery = 0;
  private cullX = NaN;
  private cullY = NaN;
  private cullWidth = NaN;
  private cullHeight = NaN;
  private overview = new URLSearchParams(location.search).has("overview");
  constructor(private inside = false) {
    super({
      key: inside ? "korea-room" : "plaza",
      layout: inside ? room : outdoor,
      bundle: inside ? roomBundle : bundle,
      anchors: inside ? roomAnchors : anchors,
      assetRoot: inside
        ? "review/living-seoul/room/"
        : "review/living-korea/north/",
      ambience: false,
    });
  }
  override preload() {
    if (this.textures.exists("tiles")) this.textures.remove("tiles");
    super.preload();
    const base = import.meta.env.BASE_URL;
    if (this.inside)
      this.load.image(
        "refined-room-base",
        `${base}review/living-seoul/room/room-base.png`,
      );
    else
      this.load.image(
        "rf-prod-doors",
        `${base}review/living-korea/north/rf-prod-doors.png`,
      );
  }
  override create() {
    super.create();
    this.transitioning = false;
    this.leaves = [];
    this.lamps = [];
    this.scenery = [];
    this.ambient = 0;
    this.cullX = NaN;
    this.cullY = NaN;
    if (this.inside)
      this.add.image(0, 0, "refined-room-base").setOrigin(0).setDepth(-95);
    else {
      if (returning) {
        this.player.setPosition(544, 1152);
        this.player.body?.reset(544, 1152);
        this.lastPosition.x = 544;
        this.lastPosition.y = 1152;
        returning = false;
      }
      this.door = this.add
        .image(1152, 743, "rf-prod-doors")
        .setOrigin(0.5, 1)
        .setDepth(760)
        .setVisible(!gateOpen);
      this.registerOccluder(this.door);
      for (const x of [1033, 1271]) {
        const leaf = this.add
          .image(x, 743, "rf-prod-doors")
          .setOrigin(0.5, 1)
          .setScale(0.72)
          .setDepth(760);
        this.registerOccluder(leaf);
      }
      const zone = this.add.zone(1152, 640, 80, 192);
      this.physics.add.existing(zone, true);
      this.leafBody = zone.body as Phaser.Physics.Arcade.StaticBody;
      this.leafBody.enable = !gateOpen;
      this.physics.add.collider(this.player, zone);
      for (let i = 0; i < 8; i++)
        this.leaves.push(
          this.add
            .image(760 + i * 110, 920 + (i % 3) * 80, "leaf-review")
            .setDepth(8000),
        );
      for (const o of this.children.list)
        if (
          o instanceof Phaser.GameObjects.Image &&
          bundle.props[o.texture.key as keyof typeof bundle.props]
        ) {
          this.scenery.push(o);
          if (
            o.texture.key === "rf-prod-lantern" ||
            o.texture.key === "rf-stone-lantern"
          )
            this.lamps.push(o);
        }
    }
    const labels = this.inside
      ? [
          [385, 350, "✦ Bàn học · E"],
          [384, 530, "↓ Ra sân · E"],
        ]
      : [
          [1152, 816, "광화문 · Vào cung · E"],
          [1152, 328, "궁궐 · Đại điện · E"],
          [1456, 394, "한지 · Trưng bày · E"],
          [544, 1144, "배움터 · Phòng đọc · E"],
          [944, 1408, "↔ Lối vườn Học viện"],
          [1632, 1488, "과학 · Sân phát minh · E"],
          [1984, 1968, "역사 · Hiên sử liệu · E"],
          [1152, 2104, "남산 · Hành trình công viên · E"],
          [512, 1856, "책과 차 · Sách & trà · E"],
        ];
    for (const [x, y, text] of labels)
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
        .on("pointerdown", () => this.interact());
    this.game.canvas.setAttribute(
      "aria-label",
      "Living Seoul — cung điện, Học viện, phố sử liệu và góc sách hiện đại. WASD/mũi tên đi, Shift chạy, E khám phá; có điều khiển cảm ứng.",
    );
    if (new URLSearchParams(location.search).has("qa"))
      window.__SEOUL_TEST__ = {
        place: (x, y) => {
          this.player.setPosition(x, y);
          this.player.body?.reset(x, y);
          this.lastPosition.x = x;
          this.lastPosition.y = y;
          this.activeScenery = this.scenery.reduce(
            (n, o) => n + Number(o.visible),
            0,
          );
          this.invalidateCue();
        },
      };
    this.events.once("shutdown", () => {
      delete window.__SEOUL__;
      delete window.__SEOUL_TEST__;
    });
  }
  private near(x: number, y: number, r = 100) {
    return Phaser.Math.Distance.Between(this.player.x, this.player.y, x, y) < r;
  }
  private say(text: string) {
    this.interactions++;
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
      this.scene.start(this.inside ? "plaza" : "korea-room");
    };
    if (controls.reduced) go();
    else {
      this.cameras.main.fadeOut(80, 35, 53, 47);
      this.time.delayedCall(80, go);
    }
  }
  private toggleGate() {
    if (
      gateOpen &&
      this.player.x > 1096 &&
      this.player.x < 1208 &&
      this.player.y > 528 &&
      this.player.y < 756
    ) {
      this.say("Juni đang ở ngưỡng cửa. Bước hẳn ra ngoài rồi khép cổng nhé.");
      return;
    }
    gateOpen = !gateOpen;
    this.door?.setVisible(!gateOpen);
    if (this.leafBody) this.leafBody.enable = !gateOpen;
    this.invalidateCue();
    this.say(
      gateOpen
        ? "문을 열어요 · Mở cổng. Theo lối đá qua cổng trong để đến đại điện và trưng bày hanji."
        : "문을 닫아요 · Khép cổng. Cửa phụ của cung vẫn đóng.",
    );
  }
  override interact() {
    if (controls.paused || document.hidden || this.transitioning) return;
    if (this.inside) {
      if (this.near(384, 510, 56)) this.changeArea();
      else if (this.near(385, 354, 100))
        window.dispatchEvent(new Event("academy-lesson"));
      else this.say("Đến bàn viết để học ba tên chữ Hangul. Cửa ra phía nam.");
      return;
    }
    if (this.near(1152, 2080, 120)) {
      window.dispatchEvent(new Event("korea-travel"));
      return;
    }
    if (this.near(1152, 752, 180)) {
      this.toggleGate();
      return;
    }
    if (this.near(544, 1120, 64)) {
      this.changeArea();
      return;
    }
    if (this.near(1456, 384, 90)) {
      this.say(
        "한지 · Hanji — giấy truyền thống Hàn Quốc. Bàn trưng bày diễn giải sách đóng chỉ, bản khắc in và hoa văn dệt. Đây là artwork gốc trong cung hư cấu, không phải hiện vật lịch sử được sao chép.",
      );
      return;
    }
    if (this.near(1152, 320, 100)) {
      this.say(
        "궁궐 · Cung điện. 마당 · Sân. 문 · Cửa. Đại điện, cổng và vườn tạo chuỗi không gian lấy cảm hứng Gyeongbokgung và Changdeokgung; đây không phải bản tái dựng lịch sử.",
      );
      return;
    }
    if (this.near(1152, 448, 64)) {
      this.say(
        "문 · Cửa. Cổng trong đang mở. Đi tiếp về bắc để xem đại điện; hai lối bên dẫn vào vườn yên tĩnh.",
      );
      return;
    }
    if (this.near(1632, 1472, 120) || this.near(2144, 1174, 110)) {
      this.say(
        "과학 · Khoa học. Quan sát thiên cầu, đồng hồ mặt trời và mô hình đồng hồ nước. Bảng sao, dụng cụ đo và cửa dịch vụ làm rõ chức năng của sân phát minh; đây là diễn giải giáo dục nguyên gốc.",
      );
      return;
    }
    if (this.near(1984, 1920, 160)) {
      this.say(
        "역사 · Lịch sử. Bàn chiến thuật, mô hình thuyền rùa và bia biểu tượng giới thiệu văn hóa hàng hải. Hiên mở ra phố, không tạo một bến cảng tưởng tượng.",
      );
      return;
    }
    if (this.near(512, 1840, 112)) {
      this.say(
        "책 · Sách. 차 · Trà. 커피 · Cà phê. Một góc sách hiện đại gợi văn hóa café và đọc sách ở Seoul, nối tiếp ngõ hanok qua phố văn hóa. Chỉ một góc prototype; chưa xây cả khu hiện đại.",
      );
      return;
    }
    if (this.near(1344, 1208, 112)) {
      this.say(
        "세종 · Sejong. Dấu mốc học chữ ở quảng trường; đây là tượng đã duyệt, không phải NPC mới.",
      );
      return;
    }
    this.say(
      "Bắc: mở cổng để thăm đại điện và vườn. Tây: Học viện có cổng nam và lối tắt phía đông. Đông: sân phát minh, hiên sử liệu. Tây nam: góc sách & trà hiện đại.",
    );
  }
  override interactProp(kind: string) {
    if (controls.paused || document.hidden) return;
    if (kind === "rf-prod-gate") {
      this.toggleGate();
      return;
    }
    if (kind === "rf-exhibit") {
      this.say(
        "한지 · Giấy hanji, sách đóng chỉ và bản khắc. Trưng bày văn hóa nguyên gốc, không sao chép hiện vật.",
      );
      return;
    }
    if (kind === "rf-cafe") {
      this.say(
        "책과 차 · Sách và trà. Góc đọc hiện đại mở ra phố, nối tiếp khu hanok qua ngõ văn hóa.",
      );
      return;
    }
    this.interact();
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.player?.body) return;
    const camera = this.cameras.main;
    if (this.overview && !this.inside) {
      camera.stopFollow();
      camera.setZoom(
        Math.min(this.scale.width / 2304, this.scale.height / 2240),
      );
      camera.centerOn(1152, 1120);
    }
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
    if (this.transitioning) this.player.setVelocity(0);
    if (!this.inside) {
      if (!controls.reduced && !controls.paused && !document.hidden) {
        this.ambient += Math.min(delta, 40);
        for (let i = 0; i < this.leaves.length; i++)
          this.leaves[i].setPosition(
            Math.round(720 + i * 110 + Math.sin(this.ambient / 1900 + i) * 14),
            Math.round(900 + ((i * 67 + this.ambient / 85) % 560)),
          );
        for (let i = 0; i < this.lamps.length; i++)
          this.lamps[i].setTint(
            Phaser.Display.Color.GetColor(
              255,
              248 + Math.round(7 * Math.sin(this.ambient / 500 + i)),
              235 + Math.round(20 * Math.sin(this.ambient / 700 + i)),
            ),
          );
      }
      for (const l of this.leaves) l.setVisible(!controls.reduced);
      const cx = Math.floor(camera.worldView.x / 32),
        cy = Math.floor(camera.worldView.y / 32);
      if (
        cx !== this.cullX ||
        cy !== this.cullY ||
        camera.worldView.width !== this.cullWidth ||
        camera.worldView.height !== this.cullHeight
      ) {
        this.cullX = cx;
        this.cullY = cy;
        this.cullWidth = camera.worldView.width;
        this.cullHeight = camera.worldView.height;
        const v = camera.worldView;
        this.activeScenery = 0;
        for (const o of this.scenery) {
          const left = o.x - o.displayWidth * o.originX,
            top = o.y - o.displayHeight * o.originY;
          o.setVisible(
            this.overview ||
              (left + o.displayWidth > v.x - 256 &&
                left < v.right + 256 &&
                top + o.displayHeight > v.y - 256 &&
                top < v.bottom + 256),
          );
        }
        this.activeScenery = this.scenery.reduce(
          (n, o) => n + Number(o.visible),
          0,
        );
        this.invalidateCue();
      }
    }
    const location = this.inside
      ? "Phòng đọc Học viện"
      : this.player.y < 736
        ? "Cung điện & vườn"
        : this.player.y > 1960
          ? "Vườn chuyển tiếp du lịch"
          : this.player.x < 1000 && this.player.y > 1560
            ? "Góc sách hiện đại"
            : this.player.x < 1000 && this.player.y > 900
              ? "Sân Học viện"
              : this.player.x > 1650 && this.player.y > 1550
                ? "Hiên sử liệu"
                : this.player.x > 1450
                  ? "Sân phát minh"
                  : "Quảng trường & ngõ văn hóa";
    window.__SEOUL__ = {
      ready: true,
      area: this.inside ? "room" : "outdoor",
      x: this.player.x,
      y: this.player.y,
      world: this.inside ? [768, 576] : [2304, 2240],
      gateOpen,
      transitions,
      activeProps: this.activeScenery,
      totalProps: this.inside ? 3 : outdoor.objects.length,
      ambientClock: this.ambient,
      reservedNPCs: ["sejong", "jang", "yi"],
      view: [
        camera.worldView.x,
        camera.worldView.y,
        camera.worldView.width,
        camera.worldView.height,
      ],
    };
    if (window.__PLAZA_REVIEW__)
      window.__PLAZA_REVIEW__.environmentClock = this.ambient;
    window.dispatchEvent(
      new CustomEvent("district-position", {
        detail: {
          area: this.inside ? "room" : "outdoor",
          x: this.player.x,
          y: this.player.y,
          location,
        },
      }),
    );
  }
}
