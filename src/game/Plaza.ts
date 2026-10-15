import Phaser from "phaser";
import layout from "../../assets-src/layout.json";
import { facing, inputVector, type Direction } from "../domains/state";
export type ArtStyle = "A" | "B" | "C";
export const controls = {
  x: 0,
  y: 0,
  run: false,
  reduced: matchMedia("(prefers-reduced-motion: reduce)").matches,
  paused: false,
  night: false,
  zoom: 1,
};
export type Metrics = {
  ready: boolean;
  style: ArtStyle;
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
  animationFrames: number;
};
declare global {
  interface Window {
    __PIXEL_METRICS__?: Metrics;
  }
}
export class Plaza extends Phaser.Scene {
  private style: ArtStyle;
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
  constructor(style: ArtStyle) {
    super("plaza");
    this.style = style;
  }
  preload() {
    const base = import.meta.env.BASE_URL + "assets/";
    for (const kind of [
      "house",
      "tiles",
      "tree",
      "lamp",
      "mailbox",
      "bench",
      "market",
      "bridge",
      "flowers",
      "fence",
    ])
      this.load.image(kind, `${base}${this.style}/${kind}.png`);
    this.load.atlas(
      "avatar",
      `${base}${this.style}/avatar.png`,
      `${base}${this.style}/avatar.json`,
    );
    this.load.tilemapTiledJSON("plaza", base + "plaza.json");
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
    map.createLayer("GardenBorders", tiles, 0, 0)?.setDepth(-90);
    this.physics.world.setBounds(32, 32, 704, 544);
    this.cameras.main.setBounds(0, 0, 768, 576);
    this.cameras.main.roundPixels = true;
    this.add
      .image(layout.house[0], layout.house[1], "house")
      .setOrigin(0.5, 1)
      .setDepth(layout.house[1]);
    for (const p of layout.props) {
      const image = this.add
        .image(p.x, p.y, p.kind)
        .setOrigin(0.5, 1)
        .setDepth(p.y);
      if (p.kind === "lamp" || p.kind === "mailbox")
        image
          .setInteractive({ pixelPerfect: true })
          .on("pointerdown", () => this.interactProp(p.kind));
    }
    for (const [x, y] of [
      [217, 252],
      [548, 240],
      [238, 453],
      [500, 460],
      [178, 286],
      [612, 375],
      [318, 455],
      [448, 455],
    ])
      this.add.image(x, y, "flowers").setOrigin(0.5, 1).setDepth(y);
    for (const x of [36, 100, 164, 548, 612, 676])
      this.add.image(x, 95, "fence").setOrigin(0, 1).setDepth(95);
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
        ["idle", 2, 1],
        ["walk", 6, 10],
        ["run", 6, 15],
        ["wave", 4, 7],
      ] as const)
        this.anims.create({
          key: `${action}-${dr}`,
          frames: Array.from({ length: n }, (_, i) => ({
            key: "avatar",
            frame: `${action === "run" ? "walk" : action}-${dr}-${i}`,
          })),
          frameRate: fps,
          repeat: action === "wave" ? 0 : -1,
          repeatDelay: action === "idle" ? 2600 : 0,
        });
    this.player = this.physics.add
      .sprite(layout.spawn[0], layout.spawn[1], "avatar", "idle-down-0")
      .setOrigin(0.5, 1)
      .setCollideWorldBounds(true);
    this.player.body?.setSize(16, 10);
    this.player.body?.setOffset(16, 49);
    this.physics.add.collider(this.player, this.solids);
    this.npc = this.add
      .sprite(layout.npc[0], layout.npc[1], "avatar", "idle-left-0")
      .setOrigin(0.5, 1)
      .setTint(0xf3dfb0)
      .setDepth(layout.npc[1]);
    this.add
      .text(layout.npc[0] - 4, layout.npc[1] - 72, "Mira", {
        fontFamily: "system-ui",
        fontSize: "12px",
        color: "#343c51",
        backgroundColor: "#fff0cd",
        padding: { x: 5, y: 2 },
      })
      .setOrigin(0.5, 1)
      .setDepth(800);
    this.overlay = this.add
      .rectangle(384, 288, 768, 576, 0x263b65, 0)
      .setDepth(900);
    this.cursors = this.input.keyboard!.createCursorKeys();
    this.keys = this.input.keyboard!.addKeys("W,A,S,D,E,SHIFT,SPACE") as Record<
      string,
      Phaser.Input.Keyboard.Key
    >;
    this.input.keyboard!.addCapture(["UP", "DOWN", "LEFT", "RIGHT", "SPACE"]);
    this.input.keyboard!.on("keydown-E", () => this.interact());
    this.input.keyboard!.on("keydown-SPACE", () => this.wave());
    this.cameras.main.startFollow(this.player, true, 1, 1, 0, 76);
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
  }
  interactProp(kind: string) {
    this.interactions++;
    this.wave();
    window.dispatchEvent(
      new CustomEvent("town-dialog", {
        detail:
          kind === "mailbox"
            ? "Hòm thư đang đợi một tấm bưu thiếp. Mira có biết ai gửi nó không?"
            : "Một đốm sáng ấm đáp lại bạn. Lễ hội đèn lồng sẽ được mở ở milestone sau.",
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
          detail:
            "Mira · Trưởng bưu cục\nChào người đưa thư mới! Có ai đó đã làm biến mất tên trên những lá thư…\n우체국 — Bưu điện. Hẹn gặp bạn trong “Chuyến giao thư đầu tiên” sau khi duyệt mỹ thuật.",
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
    this.waveUntil = this.time.now + 900;
    this.player.anims.play(`wave-${this.direction}`, true);
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
        layout.npc[0] + Math.round(Math.sin(this.elapsed / 3200) * 6);
      for (let i = 0; i < this.particles.length; i++) {
        const p = this.particles[i];
        p.x = Math.round(100 + ((i * 89 + this.elapsed / 60) % 570));
        p.y = Math.round(200 + ((i * 53 + this.elapsed / 150) % 230));
      }
    } else this.npc.anims.pause();
    this.overlay.setAlpha(controls.night ? 0.34 : 0);
    for (const p of this.particles) p.setVisible(!controls.reduced);
    if (this.cameras.main.zoom !== controls.zoom) this.resize();
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
      animationFrames: this.textures.get("avatar").getFrameNames().length,
    };
  }
}
