import Phaser from "phaser";
import { Plaza, controls } from "../game/Plaza";
import { JuniMotion, type JuniView } from "./JuniMotion";
import type { Emote } from "../game/ActorMotion";
import type { ReviewWorld } from "./types";
import animation from "../../assets-src/juni-animation/runtime.json";

type Alpha = { width: number; height: number; pixels: Uint8Array };
type Occluder = {
  image: Phaser.GameObjects.Image;
  alpha: Alpha;
  left: number;
  top: number;
  right: number;
  bottom: number;
  stamp: number;
};
declare global {
  interface Window {
    __REFINEMENT__?: {
      cueMode: string;
      cueUpdates: number;
      cueUploads: number;
      maskReadsAtLoad: number;
      candidates: number;
      area: string;
      frameCount: number;
    };
  }
}

/** Same Plaza movement/physics/UI and approved JuniMotion; cached alpha replaces GPU readback. */
export class JuniScene extends Plaza {
  protected juniMotion = new JuniMotion();
  protected lastPosition = { x: 0, y: 0 };
  protected juni!: Phaser.GameObjects.Sprite;
  protected cue!: Phaser.GameObjects.Image;
  private cueTexture!: Phaser.Textures.CanvasTexture;
  private frameMasks = new Map<string, Alpha>();
  private sourceMasks = new Map<string, Alpha>();
  private grid = new Map<string, Occluder[]>();
  private candidates: Occluder[] = [];
  private stamp = 0;
  private cueX = NaN;
  private cueY = NaN;
  private cueFrame = "";
  private cueEpoch = 0;
  private priorEpoch = -1;
  private followZoom = NaN;
  private covered = 0;
  private imageData!: ImageData;
  private referenceMask = document.createElement("canvas");
  private updates = 0;
  private uploads = 0;
  private reads = 0;
  protected referenceCue =
    new URLSearchParams(location.search).has("qa") &&
    new URLSearchParams(location.search).get("occlusion") === "reference";
  constructor(protected review: ReviewWorld) {
    super({
      key: review.key,
      layout: review.layout,
      assetRoot: review.assetRoot,
      anchors: review.anchors,
      guests: false,
      ambience: false,
    });
  }
  override preload() {
    super.preload();
    const base = import.meta.env.BASE_URL;
    this.load.atlas(
      "juni-review",
      `${base}assets/juni/juni.png`,
      `${base}assets/juni/juni.json`,
    );
    this.load.image("leaf-review", `${base}assets/shared/leaf.png`);
  }
  override create() {
    this.juniMotion = new JuniMotion();
    this.grid.clear();
    this.sourceMasks.clear();
    this.frameMasks.clear();
    this.candidates.length = 0;
    this.stamp = 0;
    this.cueX = NaN;
    this.cueFrame = "";
    this.priorEpoch = -1;
    this.covered = 0;
    this.updates = 0;
    this.uploads = 0;
    this.reads = 0;
    super.create();
    this.lastPosition = { x: this.player.x, y: this.player.y };
    this.player.body?.setOffset(16, 60);
    this.juni = this.add
      .sprite(this.player.x, this.player.y, "juni-review", "idle-front-0")
      .setOrigin(0.5, 100 / 112);
    const key = `refined-cue-${this.sys.settings.key}`;
    if (this.textures.exists(key)) this.textures.remove(key);
    this.cueTexture = this.textures.createCanvas(key, 96, 112)!;
    this.imageData = this.cueTexture.context.createImageData(96, 112);
    for (let i = 0; i < this.imageData.data.length; i += 4) {
      this.imageData.data[i] = 255;
      this.imageData.data[i + 1] = 240;
      this.imageData.data[i + 2] = 184;
    }
    this.cue = this.add
      .image(this.player.x, this.player.y, key)
      .setOrigin(0.5, 100 / 112)
      .setDepth(9000)
      .setAlpha(0.48)
      .setVisible(false);
    this.referenceMask.width = 96;
    this.referenceMask.height = 112;
    // Decode the actual atlas once. No getImageData in the default frame path.
    const atlas = this.readSource("juni-review");
    for (const name of this.textures.get("juni-review").getFrameNames()) {
      const f = this.textures.getFrame("juni-review", name);
      const pixels = new Uint8Array(96 * 112);
      for (let y = 0; y < 112; y++)
        for (let x = 0; x < 96; x++)
          pixels[y * 96 + x] =
            atlas.pixels[(f.cutY + y) * atlas.width + f.cutX + x];
      this.frameMasks.set(name, { width: 96, height: 112, pixels });
    }
    const depths = new Map(
      this.review.bundle.objects.map((o) => [
        `${o.prop}:${o.x}:${o.y}`,
        o.sortY,
      ]),
    );
    for (const child of this.children.list) {
      if (
        child instanceof Phaser.GameObjects.Image &&
        this.review.bundle.props[child.texture.key]
      ) {
        child.setDepth(
          depths.get(`${child.texture.key}:${child.x}:${child.y}`) ?? child.y,
        );
        this.registerOccluder(child);
      }
    }
    // Follow the SAME rounded root that is rendered, rather than a post-physics fractional root.
    const follow = () => {
      this.followZoom = controls.zoom;
      return this.cameras.main.startFollow(
        this.juni,
        true,
        1,
        1,
        0,
        this.scale.width < 600 ? 60 : 48,
      );
    };
    follow();
    this.scale.on("resize", follow);
    this.events.once("shutdown", () => {
      this.scale.off("resize", follow);
      delete window.__PLAZA_REVIEW__;
      delete window.__REFINEMENT__;
    });
  }
  private readSource(key: string): Alpha {
    const cached = this.sourceMasks.get(key);
    if (cached) return cached;
    const image = this.textures.get(key).getSourceImage() as HTMLImageElement;
    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    const ctx = canvas.getContext("2d", { willReadFrequently: true })!;
    ctx.drawImage(image, 0, 0);
    const rgba = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    this.reads++;
    const pixels = new Uint8Array(canvas.width * canvas.height);
    for (let i = 0; i < pixels.length; i++) pixels[i] = rgba[i * 4 + 3];
    const mask = { width: canvas.width, height: canvas.height, pixels };
    this.sourceMasks.set(key, mask);
    return mask;
  }
  protected registerOccluder(image: Phaser.GameObjects.Image) {
    let alpha = this.readSource(image.texture.key);
    const width = Math.round(image.displayWidth),
      height = Math.round(image.displayHeight);
    if (width !== alpha.width || height !== alpha.height) {
      const pixels = new Uint8Array(width * height);
      for (let y = 0; y < height; y++)
        for (let x = 0; x < width; x++)
          pixels[y * width + x] =
            alpha.pixels[
              Math.min(
                alpha.height - 1,
                Math.floor(((y + 0.5) * alpha.height) / height),
              ) *
                alpha.width +
                Math.min(
                  alpha.width - 1,
                  Math.floor(((x + 0.5) * alpha.width) / width),
                )
            ];
      alpha = { width, height, pixels };
    }
    const left = Math.round(image.x - image.originX * image.displayWidth),
      top = Math.round(image.y - image.originY * image.displayHeight);
    const item = {
      image,
      alpha,
      left,
      top,
      right: left + width,
      bottom: top + height,
      stamp: 0,
    };
    for (
      let row = Math.floor(top / 256);
      row <= Math.floor(item.bottom / 256);
      row++
    )
      for (
        let col = Math.floor(left / 256);
        col <= Math.floor(item.right / 256);
        col++
      ) {
        const key = `${col},${row}`;
        let cell = this.grid.get(key);
        if (!cell) {
          cell = [];
          this.grid.set(key, cell);
        }
        cell.push(item);
      }
    this.invalidateCue();
  }
  protected invalidateCue() {
    this.cueEpoch++;
  }
  private updateCue(frame: string) {
    const x = Math.round(this.player.x),
      y = Math.round(this.player.y);
    if (
      x === this.cueX &&
      y === this.cueY &&
      frame === this.cueFrame &&
      this.priorEpoch === this.cueEpoch
    )
      return;
    this.cueX = x;
    this.cueY = y;
    this.cueFrame = frame;
    this.priorEpoch = this.cueEpoch;
    this.updates++;
    const left = x - 48,
      top = y - 100;
    this.candidates.length = 0;
    this.stamp++;
    for (
      let row = Math.floor(top / 256);
      row <= Math.floor((top + 112) / 256);
      row++
    )
      for (
        let col = Math.floor(left / 256);
        col <= Math.floor((left + 96) / 256);
        col++
      ) {
        const cell = this.grid.get(`${col},${row}`);
        if (!cell) continue;
        for (const o of cell) {
          if (o.stamp === this.stamp) continue;
          o.stamp = this.stamp;
          if (
            o.image.depth <= y ||
            !o.image.visible ||
            o.left >= left + 96 ||
            o.top >= top + 112 ||
            o.right <= left ||
            o.bottom <= top
          )
            continue;
          this.candidates.push(o);
        }
      }
    if (this.referenceCue) {
      this.updateReference(frame, left, top);
      return;
    }
    const actor = this.frameMasks.get(frame)!;
    let covered = 0;
    const rgba = this.imageData.data;
    // Only96x112 CPU bytes; no canvas read, no GPU synchronization or fresh frame buffers.
    for (let ay = 0; ay < 112; ay++)
      for (let ax = 0; ax < 96; ax++) {
        const index = ay * 96 + ax;
        let visible = 0;
        if (actor.pixels[index])
          for (const o of this.candidates) {
            const px = left + ax - o.left,
              py = top + ay - o.top;
            if (
              px >= 0 &&
              py >= 0 &&
              px < o.alpha.width &&
              py < o.alpha.height &&
              o.alpha.pixels[py * o.alpha.width + px]
            ) {
              visible = actor.pixels[index];
              break;
            }
          }
        rgba[index * 4 + 3] = visible;
        if (visible) covered++;
      }
    this.covered = covered;
    this.cue.setVisible(covered > 0);
    if (covered) {
      this.cueTexture.context.putImageData(this.imageData, 0, 0);
      this.cueTexture.refresh();
      this.uploads++;
    }
  }
  /** Opt-in QA reference ONLY: previous eager canvas/readback algorithm on this exact same scene. */
  private updateReference(frame: string, left: number, top: number) {
    const mask = this.referenceMask.getContext("2d")!;
    mask.clearRect(0, 0, 96, 112);
    for (const o of this.candidates)
      mask.drawImage(
        this.textures
          .get(o.image.texture.key)
          .getSourceImage() as HTMLImageElement,
        0,
        0,
        o.image.width,
        o.image.height,
        o.left - left,
        o.top - top,
        o.alpha.width,
        o.alpha.height,
      );
    const f = this.textures.getFrame("juni-review", frame),
      ctx = this.cueTexture.context;
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
    ctx.drawImage(this.referenceMask, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    const rgba = ctx.getImageData(0, 0, 96, 112).data;
    this.covered = 0;
    for (let i = 3; i < rgba.length; i += 4) if (rgba[i]) this.covered++;
    this.cueTexture.refresh();
    this.uploads++;
    this.cue.setVisible(this.covered > 0);
  }
  override emote(action: Emote) {
    if (!controls.paused && !document.hidden)
      this.juniMotion.gesture(
        action === "pose" || action === "think" ? "social" : action,
      );
  }
  override update(time: number, delta: number) {
    super.update(time, delta);
    if (!this.juni) return;
    if (this.followZoom !== controls.zoom) {
      this.followZoom = controls.zoom;
      this.cameras.main.startFollow(
        this.juni,
        true,
        1,
        1,
        0,
        this.scale.width < 600 ? 60 : 48,
      );
    }
    this.player.setVisible(false);
    for (const layer of this.layers) layer.setVisible(false);
    const m = window.__PIXEL_METRICS__!;
    const view: JuniView =
      m.direction === "down"
        ? "front"
        : m.direction === "up"
          ? "back"
          : m.direction;
    const distance = Math.hypot(
      m.x - this.lastPosition.x,
      m.y - this.lastPosition.y,
    );
    this.lastPosition.x = m.x;
    this.lastPosition.y = m.y;
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
    m.avatarVersion = "Juni-imagegen-actions-v1";
    m.frame = frame;
    m.layerFrames = [frame];
    m.heroCssHeight = 80 * controls.zoom;
    m.animationFrames = animation.frameCount;
    window.__PLAZA_REVIEW__ = {
      ready: true,
      district: "Living Seoul compact refinement",
      player: "Juni / approved144frames",
      direction: this.juniMotion.view,
      action: this.juniMotion.action,
      frame,
      phase: this.juniMotion.phase,
      nativeBodyHeight: 80,
      staticCharacter: false,
      environmentClock: 0,
      occludedPixels: this.covered,
      userApproval: "PENDING",
    };
    const stats = (window.__REFINEMENT__ ??= {
      cueMode: this.referenceCue
        ? "QA canvas-readback reference"
        : "cached-alpha",
      cueUpdates: 0,
      cueUploads: 0,
      maskReadsAtLoad: 0,
      candidates: 0,
      area: this.sys.settings.key,
      frameCount: 0,
    });
    stats.cueUpdates = this.updates;
    stats.cueUploads = this.uploads;
    stats.maskReadsAtLoad = this.reads;
    stats.candidates = this.candidates.length;
    stats.frameCount = m.frameCount;
    stats.area = this.sys.settings.key;
  }
}
