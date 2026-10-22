import Phaser from "phaser";
export type CameraMode = "follow" | "scenic" | "overview" | "showcase";
type Destination = { id: string; x: number; y: number; label: string };
const levels = [0.25, 1 / 3, 0.5, 1];
export function fittedZoom(width: number, height: number, world: number[]) {
  const fit = Math.min(width / world[0], height / world[1], 1);
  return levels.filter((z) => z <= fit + 1e-6).at(-1) ?? fit;
}
export function constrainedCenter(
  center: number,
  extent: number,
  visible: number,
) {
  return visible >= extent
    ? extent / 2
    : Math.max(visible / 2, Math.min(extent - visible / 2, center));
}
/** Native follow; pixel-aligned reciprocal scenic zoom; actual Phaser camera throughout. */
export class ReviewCamera {
  mode: CameraMode = "follow";
  private cx = 0;
  private cy = 0;
  private lookX = 0;
  private lookY = 0;
  private zoom = 1;
  private pointers = new Map<number, { x: number; y: number }>();
  private pinchDistance = 0;
  private pinchZoom = 1;
  private lastMean = { x: 0, y: 0 };
  private idle = 0;
  private showcaseUntil = 0;
  private showcased = new Set<string>();
  private showcaseTarget?: Destination;
  private followView = [0, 0, 0, 0];
  private followCenter = [0, 0];
  private graphics: Phaser.GameObjects.Graphics;
  private labels = document.querySelector<HTMLElement>("#map-labels")!;
  private reduce = matchMedia("(prefers-reduced-motion: reduce)");
  private returning = false;
  constructor(
    private scene: Phaser.Scene,
    private world: number[],
    private targets: Destination[],
    private sceneId: string,
    private lock: (on: boolean) => void,
    private native: boolean,
    overview: boolean,
    x: number,
    y: number,
  ) {
    this.graphics = scene.add.graphics().setDepth(100000);
    this.cx = x;
    this.cy = y - Math.min(160, scene.scale.height * 0.18);
    if (native && overview) {
      this.cx = world[0] / 2;
      this.cy = world[1] / 2;
    }
    this.apply();
    this.followCenter = [this.cx, this.cy];
    this.followView = this.view();
    if (native) return;
    document
      .querySelector("#scenic")!
      .addEventListener("click", () => this.enter("scenic"));
    document
      .querySelector("#overview-mode")!
      .addEventListener("click", () => this.enter("overview"));
    document
      .querySelector("#return-juni")!
      .addEventListener("click", () => this.returnToJuni());
    const enabled = document.querySelector<HTMLInputElement>("#showcases")!;
    const accessibility = () => {
      enabled.disabled = this.reduce.matches;
      if (this.reduce.matches) {
        enabled.checked = false;
        if (this.mode === "showcase") this.enter("follow");
      }
    };
    accessibility();
    this.reduce.addEventListener("change", accessibility);
    const canvas = scene.game.canvas;
    const local = (e: PointerEvent) => {
      const r = canvas.getBoundingClientRect();
      return {
        x: ((e.clientX - r.left) * canvas.width) / r.width,
        y: ((e.clientY - r.top) * canvas.height) / r.height,
      };
    };
    canvas.addEventListener("pointerdown", (e) => {
      if (this.mode === "showcase") {
        this.returnToJuni();
        return;
      }
      if (!["scenic", "overview"].includes(this.mode)) return;
      e.preventDefault();
      canvas.setPointerCapture(e.pointerId);
      if (this.mode === "overview") {
        this.mode = "scenic";
        this.updateHud();
      }
      this.pointers.set(e.pointerId, local(e));
      this.seedGesture();
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!this.pointers.has(e.pointerId)) return;
      e.preventDefault();
      this.pointers.set(e.pointerId, local(e));
      const pts = [...this.pointers.values()];
      const mean = {
        x: pts.reduce((v, p) => v + p.x, 0) / pts.length,
        y: pts.reduce((v, p) => v + p.y, 0) / pts.length,
      };
      this.cx -= (mean.x - this.lastMean.x) / this.zoom;
      this.cy -= (mean.y - this.lastMean.y) / this.zoom;
      if (pts.length >= 2) {
        const distance = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
        const wanted =
          (this.pinchZoom * distance) / Math.max(1, this.pinchDistance);
        const chosen = levels.reduce((a, b) =>
          Math.abs(Math.log(b / wanted)) < Math.abs(Math.log(a / wanted))
            ? b
            : a,
        );
        this.setZoom(chosen, mean);
      }
      this.lastMean = mean;
      this.apply();
    });
    const release = (e: PointerEvent) => {
      this.pointers.delete(e.pointerId);
      this.seedGesture();
    };
    canvas.addEventListener("pointerup", release);
    canvas.addEventListener("pointercancel", release);
    canvas.addEventListener("lostpointercapture", release);
    canvas.addEventListener(
      "wheel",
      (e) => {
        if (this.mode !== "scenic") return;
        e.preventDefault();
        const index = levels.indexOf(this.zoom);
        this.setZoom(
          levels[
            Math.max(
              0,
              Math.min(levels.length - 1, index + (e.deltaY < 0 ? 1 : -1)),
            )
          ],
        );
        this.apply();
      },
      { passive: false },
    );
    this.updateHud();
  }
  private seedGesture() {
    const p = [...this.pointers.values()];
    if (!p.length) return;
    this.lastMean = {
      x: p.reduce((v, q) => v + q.x, 0) / p.length,
      y: p.reduce((v, q) => v + q.y, 0) / p.length,
    };
    this.pinchZoom = this.zoom;
    this.pinchDistance =
      p.length > 1 ? Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y) : 0;
  }
  private setZoom(z: number, point?: { x: number; y: number }) {
    if (z === this.zoom) return;
    const c = this.scene.cameras.main;
    const anchor = point
      ? {
          x: this.cx + (point.x - c.x - c.width / 2) / this.zoom,
          y: this.cy + (point.y - c.y - c.height / 2) / this.zoom,
        }
      : undefined;
    this.zoom = z;
    this.apply();
    if (anchor && point) {
      this.cx = anchor.x - (point.x - c.x - c.width / 2) / z;
      this.cy = anchor.y - (point.y - c.y - c.height / 2) / z;
    }
    this.updateHud();
  }
  enter(mode: CameraMode) {
    if (this.native) return;
    if (this.returning) return;
    if (this.mode === "follow") {
      this.followCenter = [this.cx, this.cy];
      this.followView = this.view();
    }
    this.pointers.clear();
    this.mode = mode;
    this.lock(mode === "scenic" || mode === "overview");
    if (mode === "overview") {
      this.zoom = fittedZoom(
        this.scene.scale.width,
        this.scene.scale.height,
        this.world,
      );
      this.cx = this.world[0] / 2;
      this.cy = this.world[1] / 2;
    }
    if (mode === "follow") {
      this.zoom = 1;
      this.cx = this.followCenter[0];
      this.cy = this.followCenter[1];
    }
    this.apply();
    this.updateHud();
  }
  returnToJuni() {
    if (this.mode === "follow" || this.returning) return;
    if (this.reduce.matches) {
      this.enter("follow");
      return;
    }
    this.returning = true;
    const cam = this.scene.cameras.main;
    cam.fadeOut(90, 14, 32, 39);
    this.scene.time.delayedCall(100, () => {
      this.returning = false;
      this.enter("follow");
      cam.fadeIn(160, 14, 32, 39);
    });
  }
  private apply() {
    const c = this.scene.cameras.main,
      z = this.zoom;
    const w = Math.min(this.scene.scale.width, this.world[0] * z),
      h = Math.min(this.scene.scale.height, this.world[1] * z);
    c.removeBounds();
    c.setViewport(
      Math.round((this.scene.scale.width - w) / 2),
      Math.round((this.scene.scale.height - h) / 2),
      w,
      h,
    ).setZoom(z);
    const vw = c.width / z,
      vh = c.height / z;
    this.cx = constrainedCenter(this.cx, this.world[0], vw);
    this.cy = constrainedCenter(this.cy, this.world[1], vh);
    // Phaser scroll is measured before its centered zoom transform.
    // Snap the actual visible world edge, then account for that zoom origin.
    const left = Math.round((this.cx - vw / 2) * z) / z;
    const top = Math.round((this.cy - vh / 2) * z) / z;
    c.setScroll(left + (vw - c.width) / 2, top + (vh - c.height) / 2);
    c.roundPixels = true;
  }
  private view() {
    const c = this.scene.cameras.main;
    return [
      c.scrollX + (c.width - c.width / this.zoom) / 2,
      c.scrollY + (c.height - c.height / this.zoom) / 2,
      c.width / this.zoom,
      c.height / this.zoom,
    ];
  }
  private updateHud() {
    document.body.dataset.camera = this.mode;
    document.querySelector<HTMLElement>("#camera-mode")!.textContent =
      this.mode === "follow"
        ? "Follow · native1:1"
        : this.mode === "overview"
          ? `Full scene · ${Math.round(this.zoom * 100)}%`
          : this.mode === "showcase"
            ? "Landmark moment"
            : `Scenic · ${Math.round(this.zoom * 100)}%`;
    document.querySelector<HTMLElement>("#return-juni")!.textContent =
      this.mode === "showcase" ? "Skip" : "Return to Juni";
  }
  update(
    delta: number,
    x: number,
    y: number,
    dx: number,
    dy: number,
    paused: boolean,
  ) {
    if (this.native) return;
    const moving = Math.hypot(dx, dy) > 0.01;
    if (
      this.mode === "showcase" &&
      (moving ||
        paused ||
        this.reduce.matches ||
        this.scene.time.now > this.showcaseUntil)
    ) {
      this.mode = "follow";
      this.updateHud();
    }
    if (this.mode === "follow") {
      const k = this.reduce.matches
        ? 1
        : 1 - Math.exp(-Math.min(delta, 50) / 220);
      this.lookX += (dx * 60 - this.lookX) * k;
      this.lookY += (dy * 42 - this.lookY) * k;
      const leadY = Math.min(
        160,
        this.scene.scale.height *
          (this.scene.scale.width / this.scene.scale.height > 2.1
            ? 0.13
            : 0.18),
      );
      const a = this.reduce.matches
        ? 1
        : 1 - Math.exp(-Math.min(delta, 50) / 140);
      this.cx += (x + this.lookX - this.cx) * a;
      this.cy += (y - leadY + this.lookY - this.cy) * a;
      this.idle = !moving && !paused ? this.idle + delta : 0;
      const enabled =
        document.querySelector<HTMLInputElement>("#showcases")!.checked;
      const target = this.targets.find(
        (t) =>
          Math.hypot(t.x - x, t.y - y) < 150 &&
          !this.showcased.has(t.id) &&
          !sessionStorage.getItem(`gate2-showcase:${this.sceneId}:${t.id}`),
      );
      if (enabled && !this.reduce.matches && this.idle > 1100 && target) {
        this.showcased.add(target.id);
        sessionStorage.setItem(
          `gate2-showcase:${this.sceneId}:${target.id}`,
          "1",
        );
        this.followCenter = [this.cx, this.cy];
        this.showcaseTarget = target;
        this.mode = "showcase";
        this.showcaseUntil = this.scene.time.now + 2600;
        this.updateHud();
      }
    } else if (this.mode === "showcase" && this.showcaseTarget) {
      const a = 1 - Math.exp(-Math.min(delta, 50) / 500);
      this.cx += (this.showcaseTarget.x - this.cx) * a;
      this.cy +=
        (this.showcaseTarget.y -
          Math.min(200, this.scene.scale.height * 0.3) -
          this.cy) *
        a;
    }
    this.apply();
    if (this.mode === "follow") {
      this.followCenter = [this.cx, this.cy];
      this.followView = this.view();
    }
    const camera = this.scene.cameras.main;
    const playerScreenY = camera.y + (y - this.view()[1]) * this.zoom;
    // At the northern clamp, protect Juni's head from the floating HUD.
    document.body.dataset.edgeFocus = String(
      this.mode === "follow" &&
        this.scene.scale.height < 500 &&
        playerScreenY - 80 < 58,
    );
    this.graphics.clear();
    this.labels.replaceChildren();
    const canvasBounds = this.scene.game.canvas.getBoundingClientRect();
    this.labels.style.left = canvasBounds.left + "px";
    this.labels.style.top = canvasBounds.top + "px";
    if (this.mode === "overview") {
      const c = this.scene.cameras.main,
        z = this.zoom;
      this.graphics
        .lineStyle(2 / z, 0xffd083, 1)
        .strokeRect(
          this.followView[0],
          this.followView[1],
          this.followView[2],
          this.followView[3],
        );
      for (const t of [...this.targets, { id: "juni", x, y, label: "Juni" }]) {
        this.graphics
          .fillStyle(t.id === "juni" ? 0xffd083 : 0x8ce2cd)
          .fillCircle(t.x, t.y, 4 / z);
        const label = document.createElement("span");
        label.textContent = t.label.split(" · ")[0].slice(0, 22);
        label.style.left = `${c.x + (t.x - this.view()[0]) * z + 8}px`;
        label.style.top = `${c.y + (t.y - this.view()[1]) * z + (t.id === "juni" ? 10 : -15)}px`;
        if (t.id === "juni") label.style.color = "#ffd083";
        this.labels.append(label);
      }
    }
  }
  snapshot() {
    const c = this.scene.cameras.main;
    return {
      mode: this.mode,
      zoom: this.zoom,
      viewport: [c.x, c.y, c.width, c.height],
      canvas: [this.scene.scale.width, this.scene.scale.height],
      worldView: this.view(),
      renderedWorldView: [
        c.worldView.x,
        c.worldView.y,
        c.worldView.width,
        c.worldView.height,
      ],
      center: [this.cx, this.cy],
      lookAhead: [this.lookX, this.lookY],
      pointers: this.pointers.size,
      levels,
      showcased: [...this.showcased],
      reducedMotion: this.reduce.matches,
    };
  }
}
