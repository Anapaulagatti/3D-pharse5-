import Phaser from "phaser";
import world from "../../assets-src/unified-v4/world.json";
type World = typeof world;
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
};
declare global {
  interface Window {
    __PIXEL_METRICS__?: Metrics;
  }
}
export class Plaza extends Phaser.Scene {
  private style = "unified";
  private layout: World;
  private layers: Phaser.GameObjects.Sprite[] = [];
  private npcLayers: Phaser.GameObjects.Sprite[] = [];
  private player!: Phaser.Physics.Arcade.Sprite;
  private npc!: Phaser.GameObjects.Sprite;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private direction: Direction = "down";
  private solids!: Phaser.Physics.Arcade.StaticGroup;
  private particles: Phaser.GameObjects.Rectangle[] = [];
  private elapsed = 0;
  private interactions = 0;
  private waveUntil = 0;
  private active = true;
  private overlay!: Phaser.GameObjects.Rectangle;
  constructor() {
    super("plaza");
    this.layout = world;
  }
  preload() {
    const base = import.meta.env.BASE_URL + "assets/unified-v4/";
    for (const kind of [
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
    ])
      this.load.image(kind, `${base}${kind}.png`);
    for (const layer of [
      "body",
      "outfit0",
      "outfit1",
      "hair0",
      "hair1",
      "satchel",
    ])
      this.load.atlas(layer, `${base}${layer}.png`, `${base}avatar.json`);
    this.load.tilemapTiledJSON("plaza", `${base}plaza.json`);
    this.load.on("loaderror", (file: Phaser.Loader.File) =>
      window.dispatchEvent(
        new CustomEvent("game-error", {
          detail: `Không tải được ${file.key}. Hãy mở qua HTTP và tải lại.`,
        }),
      ),
    );
  }
  create() {
    const map = this.make.tilemap({ key: "plaza" });
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
          0x536457,
        )
        .setDepth(-50);
      const image = this.add
        .image(p.x, p.y, p.kind)
        .setOrigin(0.5, 1)
        .setDepth(p.y);
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
    for (const dr of ["down", "left", "right", "up"])
      for (const [action, n, fps] of [
        ["idle", 4, 10],
        ["walk", 8, 10],
        ["run", 8, 13],
        ["wave", 6, 9],
        ["celebrate", 8, 10],
        ["pose", 4, 5],
      ] as const)
        this.anims.create({
          key: `${action}-${dr}`,
          frames: Array.from({ length: n }, (_, i) => ({
            key: "body",
            frame: `${action}-${dr}-${i}`,
            ...(action === "idle"
              ? { duration: [1800, 120, 350, 1100][i] }
              : {}),
          })),
          frameRate: fps,
          repeat: ["wave", "celebrate", "pose"].includes(action) ? 0 : -1,
          repeatDelay: 0,
        });
    this.player = this.physics.add
      .sprite(this.layout.spawn[0], this.layout.spawn[1], "body", "idle-down-0")
      .setOrigin(0.5, 1)
      .setCollideWorldBounds(true);
    this.player.body?.setSize(16, 8);
    this.player.body?.setOffset(8, 39);
    this.physics.add.collider(this.player, this.solids);
    this.npc = this.add
      .sprite(this.layout.npc[0], this.layout.npc[1], "body", "idle-left-0")
      .setOrigin(0.5, 1)
      .setTint(0xf3dfb0)
      .setDepth(this.layout.npc[1]);
    this.layers = ["outfit0", "hair0", "satchel"].map((k) =>
      this.add
        .sprite(this.player.x, this.player.y, k, "idle-down-0")
        .setOrigin(0.5, 1),
    );
    this.npcLayers = ["outfit1", "hair1"].map((k) =>
      this.add
        .sprite(this.npc.x, this.npc.y, k, "idle-left-0")
        .setOrigin(0.5, 1)
        .setDepth(this.npc.y + 0.1),
    );
    this.add
      .text(this.layout.npc[0], this.layout.npc[1] - 53, "Mira · demo NPC", {
        fontFamily: "system-ui",
        fontSize: "8px",
        color: "#f4e6ba",
        backgroundColor: "#303945",
        padding: { x: 3, y: 2 },
      })
      .setOrigin(0.5, 1)
      .setDepth(900);
    this.overlay = this.add
      .rectangle(
        this.layout.width / 2,
        this.layout.height / 2,
        this.layout.width,
        this.layout.height,
        0x263b65,
        0,
      )
      .setDepth(10000);
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
    for (let i = 0; i < 7; i++)
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
  interact() {
    if (
      Phaser.Math.Distance.Between(
        this.player.x,
        this.player.y,
        this.npc.x,
        this.npc.y,
      ) < 88
    ) {
      this.interactions++;
      this.wave();
      window.dispatchEvent(
        new CustomEvent("town-dialog", {
          detail: `Mira · NPC demo cục bộ\nChào bạn! ${this.layout.mood}\nVai nhân vật: ${this.layout.role}.\n우체국 — Bưu điện. Chuyến phiêu lưu đầu tiên sẽ chờ sau khi duyệt bản hình ảnh thống nhất.`,
        }),
      );
    } else
      window.dispatchEvent(
        new CustomEvent("town-dialog", {
          detail: "Hãy đến gần Mira bên bưu điện, rồi nhấn E.",
        }),
      );
  }
  wave() {
    this.emote("wave");
  }
  emote(action: "wave" | "celebrate" | "pose") {
    if (controls.paused) return;
    this.waveUntil = this.time.now + (action === "wave" ? 720 : 880);
    this.player.anims.play(`${action}-${this.direction}`, false);
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
    const speed = controls.run || this.keys.SHIFT.isDown ? 126 : 78;
    this.player.setVelocity(moving ? v.x * speed : 0, moving ? v.y * speed : 0);
    this.direction = facing(moving ? v.x : 0, moving ? v.y : 0, this.direction);
    this.player.setDepth(Math.round(this.player.y));
    if (blocked) {
      this.physics.world.pause();
      this.player.anims.pause();
      this.npc.anims.pause();
    } else {
      this.physics.world.resume();
      this.player.anims.resume();
      if (moving) {
        this.waveUntil = 0;
        this.player.anims.play(
          `${speed === 126 ? "run" : "walk"}-${this.direction}`,
          true,
        );
      } else if (this.time.now > this.waveUntil) {
        if (controls.reduced) {
          this.player.anims.stop();
          this.player.setFrame(`idle-${this.direction}-0`);
        } else this.player.anims.play(`idle-${this.direction}`, true);
      }
    }
    if (!blocked && !controls.reduced) {
      this.elapsed += Math.min(delta, 50);
      this.npc.anims.play("idle-left", true);
      this.npc.anims.resume();
      this.npc.x =
        this.layout.npc[0] + Math.round(Math.sin(this.elapsed / 3200) * 6);
      for (let i = 0; i < this.particles.length; i++) {
        const p = this.particles[i];
        p.x = Math.round(100 + ((i * 89 + this.elapsed / 60) % 570));
        p.y = Math.round(200 + ((i * 53 + this.elapsed / 150) % 230));
      }
    } else this.npc.anims.pause();
    this.overlay.setAlpha(controls.night ? 0.34 : 0);
    for (const p of this.particles) p.setVisible(!controls.reduced);
    if (this.cameras.main.zoom !== controls.zoom) this.resize();
    this.layers[0].setTexture(
      `outfit${controls.outfit}`,
      this.player.frame.name,
    );
    this.layers[1].setTexture(`hair${controls.hair}`, this.player.frame.name);
    this.layers[2].setVisible(controls.accessory);
    for (let i = 0; i < this.layers.length; i++)
      this.layers[i]
        .setPosition(Math.round(this.player.x), Math.round(this.player.y))
        .setDepth(Math.round(this.player.y) + (i + 1) * 0.01)
        .setFrame(this.player.frame.name);
    for (let i = 0; i < this.npcLayers.length; i++)
      this.npcLayers[i]
        .setPosition(Math.round(this.npc.x), Math.round(this.npc.y))
        .setDepth(this.npc.y + (i + 1) * 0.01)
        .setFrame(this.npc.frame.name);
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
      heroCssHeight: 48 * this.cameras.main.zoom,
      hair: controls.hair,
      outfit: controls.outfit,
      accessory: controls.accessory,
      layerFrames: this.layers.map((l) => l.frame.name),
      animationFrames: this.textures.get("body").getFrameNames().length,
    };
  }
}
