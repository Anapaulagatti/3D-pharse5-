import Phaser from "phaser";
import { ActorMotion, type Emote } from "./ActorMotion";
import { HistoricalGuest } from "./HistoricalGuest";
import {
  historicalGuests,
  historicalDisclaimer,
} from "../content/historicalGuests";
import world from "../../assets-src/world/world.json";
type World = typeof world;
type PlazaOptions = {
  key?: string;
  layout?: World;
  assetRoot?: string;
  anchors?: Record<string, number[]>;
  guests?: boolean;
  ambience?: boolean;
};
import { facing, inputVector, type Direction } from "../domains/state";

export const controls = {
  x: 0,
  y: 0,
  run: false,
  reduced: matchMedia("(prefers-reduced-motion: reduce)").matches,
  paused: false,
  night: false,
  zoom: 2,
  hair: 0,
  outfit: 0,
  accessory: true,
  expression: "neutral",
};
export type Metrics = {
  ready: boolean;
  style: string;
  x: number;
  y: number;
  frame: string;
  direction: Direction;
  moving: boolean;
  speed: number;
  reduced: boolean;
  paused: boolean;
  interactions: number;
  renderer: string;
  width: number;
  height: number;
  fps: number;
  frameCount: number;
  environmentFrame: number;
  colliders: number;
  cameraZoom: number;
  role: string;
  mapSha: string;
  worldProps: number;
  heroCssHeight: number;
  animationFrames: number;
  hair: number;
  outfit: number;
  accessory: boolean;
  layerFrames: string[];
  expression: string;
  avatarVersion: string;
  screenFoot: { x: number; y: number };
  guests: HistoricalGuest["metrics"][];
};
declare global {
  interface Window {
    __PIXEL_METRICS__?: Metrics;
  }
}
export class Plaza extends Phaser.Scene {
  private style = "unified";
  private layout: World;
  protected layers: Phaser.GameObjects.Sprite[] = [];
  private guests: HistoricalGuest[] = [];
  protected player!: Phaser.Physics.Arcade.Sprite;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private direction: Direction = "down";
  private solids!: Phaser.Physics.Arcade.StaticGroup;
  private particles: Phaser.GameObjects.Rectangle[] = [];
  private elapsed = 0;
  protected interactions = 0;
  private motion = new ActorMotion();
  private lastFoot = { x: 512, y: 560 };
  private active = true;
  private overlay!: Phaser.GameObjects.Rectangle;
  constructor(private options: PlazaOptions = {}) {
    super(options.key ?? "plaza");
    this.layout = options.layout ?? world;
  }
  preload() {
    const base =
      import.meta.env.BASE_URL + (this.options.assetRoot ?? "assets/world/");
    const kinds = this.options.assetRoot
      ? [...new Set(this.layout.objects.map((p) => p.kind)), "tiles"]
      : [
          "wall",
          "jars",
          "gardenbed",
          "parcel",
          "table",
          "courier",
          "cafe",
          "hanok",
          "academy",
          "tree",
          "pine",
          "plum",
          "fountain",
          "board",
          "puzzle",
          "portal",
          "outfit",
          "stall",
          "bench",
          "planter",
          "lantern",
          "tiles",
        ];
    for (const kind of kinds) this.load.image(kind, `${base}${kind}.png`);
    const heroBase = import.meta.env.BASE_URL + "assets/actors/hero/";
    for (const layer of [
      "body",
      "outfit0",
      "outfit1",
      "hair0",
      "hair1",
      "satchel",
      "face-neutral",
      "face-happy",
      "face-focused",
      "face-surprised",
      "hands",
    ])
      this.load.atlas(
        `hero-${layer}`,
        `${heroBase}${layer}.png`,
        `${heroBase}atlas.json`,
      );
    for (const guest of this.options.guests === false ? [] : historicalGuests) {
      const guestBase = import.meta.env.BASE_URL + `assets/actors/${guest.id}/`;
      this.load.atlas(
        `guest-${guest.id}`,
        `${guestBase}sprite.png`,
        `${guestBase}atlas.json`,
      );
    }
    this.load.tilemapTiledJSON(
      this.options.key ?? "plaza",
      `${base}plaza.json`,
    );
    this.load.on("loaderror", (file: Phaser.Loader.File) =>
      window.dispatchEvent(
        new CustomEvent("game-error", {
          detail: `Không tải được ${file.key}. Hãy mở qua HTTP và tải lại.`,
        }),
      ),
    );
  }
  create() {
    const map = this.make.tilemap({ key: this.options.key ?? "plaza" });
    const tiles = map.addTilesetImage("town", "tiles", 32, 32, 0, 0);
    if (!tiles) throw Error("Tiled tileset missing");
    map.createLayer("Ground", tiles, 0, 0)?.setDepth(-100);
    map.createLayer("Edging", tiles, 0, 0)?.setDepth(-90);
    this.physics.world.setBounds(
      32,
      32,
      this.layout.width - 64,
      this.layout.height - 64,
    );
    this.cameras.main.setBounds(0, 0, this.layout.width, this.layout.height);
    this.cameras.main.roundPixels = true;
    for (const p of this.layout.objects) {
      this.add
        .rectangle(
          p.x + 5,
          p.y - 2,
          p.width + 6,
          Math.max(4, p.height / 3),
          0x423c35,
          0.18,
        )
        .setDepth(-50);
      const image = this.add
        .image(p.x, p.y, p.kind)
        .setOrigin(0.5, 1)
        .setDepth(p.y);
      const anchor = this.options.anchors?.[p.kind];
      if (anchor)
        image.setOrigin(anchor[0] / image.width, anchor[1] / image.height);
      image
        .setInteractive({ pixelPerfect: true })
        .on("pointerdown", () => this.interactProp(p.kind));
    }
    this.solids = this.physics.add.staticGroup();
    for (const o of map.getObjectLayer("Collision")?.objects ?? []) {
      const rect = this.add.rectangle(
        (o.x ?? 0) + (o.width ?? 0) / 2,
        (o.y ?? 0) + (o.height ?? 0) / 2,
        o.width ?? 1,
        o.height ?? 1,
        0,
        0,
      );
      this.solids.add(rect);
    }
    this.player = this.physics.add
      .sprite(
        this.layout.spawn[0],
        this.layout.spawn[1],
        "hero-body",
        "idle-down-0",
      )
      .setOrigin(0.5, 64 / 68)
      .setCollideWorldBounds(true);
    this.player.body?.setSize(16, 8);
    this.player.body?.setOffset(16, 55);
    this.physics.add.collider(this.player, this.solids);
    this.layers = [
      "hero-outfit0",
      "hero-hair0",
      "hero-satchel",
      "hero-face-neutral",
      "hero-hands",
    ].map((k) =>
      this.add
        .sprite(this.player.x, this.player.y, k, "idle-down-0")
        .setOrigin(0.5, 64 / 68),
    );
    for (const guest of this.options.guests === false ? [] : historicalGuests)
      this.guests.push(
        new HistoricalGuest(this, guest, this.solids, () =>
          this.interactGuest(guest.id),
        ),
      );
    this.overlay = this.add
      .rectangle(
        this.layout.width / 2,
        this.layout.height / 2,
        this.layout.width,
        this.layout.height,
        0x263b65,
        1,
      )
      .setDepth(10000)
      .setAlpha(0);
    this.cursors = this.input.keyboard!.createCursorKeys();
    this.keys = this.input.keyboard!.addKeys("W,A,S,D,E,SHIFT,SPACE") as Record<
      string,
      Phaser.Input.Keyboard.Key
    >;
    this.input.keyboard!.addCapture(["UP", "DOWN", "LEFT", "RIGHT", "SPACE"]);
    this.input.keyboard!.on("keydown-E", () => this.interact());
    this.input.keyboard!.on("keydown-SPACE", () => this.wave());
    this.cameras.main.startFollow(
      this.player,
      true,
      1,
      1,
      0,
      this.layout.follow,
    );
    this.resize();
    this.scale.on("resize", this.resize, this);
    for (let i = 0; i < (this.options.ambience === false ? 0 : 7); i++)
      this.particles.push(
        this.add
          .rectangle(150 + i * 73, 180 + i * 37, 3, 2, 0xffe0c0)
          .setDepth(700),
      );
    const visibility = () => {
      this.active = document.visibilityState === "visible";
      if (!this.active) {
        controls.x = 0;
        controls.y = 0;
        this.player.setVelocity(0);
      }
    };
    const blur = () => {
      controls.x = 0;
      controls.y = 0;
      this.input.keyboard?.resetKeys();
    };
    document.addEventListener("visibilitychange", visibility);
    window.addEventListener("blur", blur);
    this.events.once("shutdown", () => {
      document.removeEventListener("visibilitychange", visibility);
      window.removeEventListener("blur", blur);
      this.scale.off("resize", this.resize, this);
    });
    window.dispatchEvent(new CustomEvent("game-ready"));
    this.game.canvas.setAttribute(
      "aria-label",
      "Quảng trường pixel: WASD hoặc mũi tên để đi, Shift chạy, E trò chuyện, Space vẫy tay.",
    );
    this.game.canvas.tabIndex = 0;
  }
  private resize() {
    this.cameras.main.setZoom(controls.zoom);
    if (controls.zoom === 1) {
      this.cameras.main.stopFollow();
      this.cameras.main.centerOn(this.layout.width / 2, this.layout.height / 2);
    } else {
      this.cameras.main.startFollow(
        this.player,
        true,
        1,
        1,
        0,
        Math.min(
          this.layout.follow,
          96,
          Math.max(0, this.scale.height / (2 * controls.zoom) - 24),
        ),
      );
    }
  }
  interactProp(kind: string) {
    this.interactions++;
    const messages: Record<string, string> = {
      courier:
        "Trạm thư · Những lá thư thất lạc sẽ mở thành nhiệm vụ ở Gate 3.",
      cafe: "Café Dal · Một nơi để gặp gỡ. Hiện chỉ có NPC demo cục bộ.",
      board:
        "Bảng chuyện · The Lost Letters. Nhiệm vụ chưa mở trong bản duyệt hình ảnh.",
      puzzle: "Ghép âm · Sign Repair sẽ được xây sau khi duyệt hình ảnh.",
      academy:
        "TOPIK I / II và EPS-TOPIK · Lối học trực tiếp đang được lên kế hoạch; chưa có khóa học trong bản này.",
      portal: "Đấu trường · PvP công bằng theo trình độ, chưa kết nối máy chủ.",
      outfit: "Góc trang phục · Thử tóc và áo trong bảng điều khiển bên cạnh.",
      fountain: "Giếng thư · Những câu chuyện của phố bắt đầu từ một lá thư.",
    };
    this.wave();
    window.dispatchEvent(
      new CustomEvent("town-dialog", {
        detail:
          messages[kind] ??
          "Một góc nhỏ của quảng trường. Chào mừng bạn đến Living Pixel Seoul.",
      }),
    );
  }
  interactGuest(id: string) {
    const guest = this.guests.find((g) => g.definition.id === id);
    if (!guest) return;
    guest.greet();
    this.interactions++;
    window.dispatchEvent(
      new CustomEvent("town-dialog", {
        detail: `${guest.definition.name} · ${guest.definition.ko}
${guest.definition.dialogue}

${guest.definition.hook}

${historicalDisclaimer}`,
      }),
    );
  }
  interact() {
    const nearest = this.guests
      .map((g) => ({
        g,
        d: Phaser.Math.Distance.Between(
          this.player.x,
          this.player.y,
          g.body.x,
          g.body.y,
        ),
      }))
      .sort((a, b) => a.d - b.d)[0];
    if (nearest && nearest.d < 100) this.interactGuest(nearest.g.definition.id);
    else
      window.dispatchEvent(
        new CustomEvent("town-dialog", {
          detail:
            "Đến gần một vị khách lịch sử rồi nhấn E, hoặc chạm vào nhân vật để nghe lời chào.",
        }),
      );
  }
  wave() {
    this.emote("wave");
  }
  emote(action: Emote) {
    if (!controls.paused) this.motion.emote(action);
  }
  update(_time: number, delta: number) {
    if (!this.player?.body) return;
    const blocked = controls.paused || !this.active;
    const keyboard = this.game.canvas === document.activeElement;
    const x =
      controls.x +
      (keyboard
        ? Number(this.cursors.right.isDown || this.keys.D.isDown) -
          Number(this.cursors.left.isDown || this.keys.A.isDown)
        : 0);
    const y =
      controls.y +
      (keyboard
        ? Number(this.cursors.down.isDown || this.keys.S.isDown) -
          Number(this.cursors.up.isDown || this.keys.W.isDown)
        : 0);
    const v = inputVector(x, y);
    const moving = !blocked && (!!v.x || !!v.y);
    const speed = controls.run || this.keys.SHIFT.isDown ? 100 : 60;
    const travelled = Math.hypot(
      this.player.x - this.lastFoot.x,
      this.player.y - this.lastFoot.y,
    );
    this.lastFoot = { x: this.player.x, y: this.player.y };
    this.direction = facing(moving ? v.x : 0, moving ? v.y : 0, this.direction);
    const frame = this.motion.step(
      delta,
      travelled,
      moving,
      speed === 100,
      this.direction,
      controls.reduced,
      blocked,
    );
    this.player.setFrame(frame);
    const targetX = moving ? v.x * speed * this.motion.moveScale : 0;
    const targetY = moving ? v.y * speed * this.motion.moveScale : 0;
    const step = Math.min(delta, 100) * (moving ? 0.85 : 1.2);
    const approach = (current: number, target: number) =>
      current +
      Math.sign(target - current) * Math.min(Math.abs(target - current), step);
    if (blocked) {
      this.physics.world.pause();
      this.player.setVelocity(0);
    } else {
      this.physics.world.resume();
      this.player.setVelocity(
        approach(this.player.body.velocity.x, targetX),
        approach(this.player.body.velocity.y, targetY),
      );
    }
    this.player.setDepth(Math.round(this.player.y));
    if (!blocked && !controls.reduced) {
      this.elapsed += Math.min(delta, 50);
      for (let i = 0; i < this.particles.length; i++) {
        const p = this.particles[i];
        p.x = Math.round(100 + ((i * 89 + this.elapsed / 60) % 570));
        p.y = Math.round(200 + ((i * 53 + this.elapsed / 150) % 230));
      }
    }
    for (const guest of this.guests)
      guest.step(delta, blocked, controls.reduced);
    this.overlay.setAlpha(controls.night ? 0.34 : 0);
    for (const p of this.particles) p.setVisible(!controls.reduced);
    if (this.cameras.main.zoom !== controls.zoom) this.resize();
    this.layers[0].setTexture(
      `hero-outfit${controls.outfit}`,
      this.player.frame.name,
    );
    this.layers[1].setTexture(
      `hero-hair${controls.hair}`,
      this.player.frame.name,
    );
    const emotion = this.motion.mood ?? controls.expression;
    this.layers[3].setTexture(`hero-face-${emotion}`, this.player.frame.name);
    this.layers[2].setVisible(controls.accessory);
    for (let i = 0; i < this.layers.length; i++)
      this.layers[i]
        .setPosition(Math.round(this.player.x), Math.round(this.player.y))
        .setDepth(Math.round(this.player.y) + [0.01, 0.03, 0.05, 0.02, 0.04][i])
        .setFrame(this.player.frame.name);
    window.__PIXEL_METRICS__ = {
      ready: true,
      style: this.style,
      x: this.player.x,
      y: this.player.y,
      frame: this.player.frame.name,
      direction: this.direction,
      moving,
      speed: moving ? speed : 0,
      reduced: controls.reduced,
      paused: blocked,
      interactions: this.interactions,
      renderer: this.game.renderer.type === Phaser.CANVAS ? "Canvas" : "WebGL",
      width: this.scale.width,
      height: this.scale.height,
      fps: this.game.loop.actualFps,
      frameCount: this.game.loop.frame,
      environmentFrame: this.elapsed,
      colliders: this.solids.getLength(),
      cameraZoom: this.cameras.main.zoom,
      role: this.layout.role,
      mapSha: this.layout.mapSha256,
      worldProps: this.layout.objects.length,
      heroCssHeight: 56 * this.cameras.main.zoom,
      hair: controls.hair,
      outfit: controls.outfit,
      accessory: controls.accessory,
      layerFrames: this.layers.map((l) => l.frame.name),
      expression: emotion,
      avatarVersion: "chibi-motion-v2",
      screenFoot: {
        x: Math.round(
          (this.player.x - this.cameras.main.worldView.x) * controls.zoom,
        ),
        y: Math.round(
          (this.player.y - this.cameras.main.worldView.y) * controls.zoom,
        ),
      },
      guests: this.guests.map((g) => g.metrics),
      animationFrames: this.textures.get("hero-body").getFrameNames().length,
    };
  }
}
