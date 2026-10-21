import Phaser from "phaser";
import { JuniScene } from "../engine/JuniScene";
import { controls } from "../game/Plaza";
import world from "../../assets-src/gate1/map/world.json";
import bundle from "../../assets-src/gate1/map/bundle.json";
import anchors from "../../assets-src/gate1/map/anchors.json";
import venues from "../../assets-src/gate1/map/venues.json";

declare global {
  interface Window {
    __GATE1__?: {
      ready: boolean;
      x: number;
      y: number;
      frame: string;
      venues: string[];
      activeVenue: string | null;
      userApproval: "PENDING";
      source: string;
    };
    __GATE1_TEST__?: { place: (x: number, y: number) => void };
  }
}
export class Street extends JuniScene {
  private visited = new Set<string>();
  private activeVenue: string | null = null;
  constructor() {
    super({
      key: "gate1",
      layout: world,
      bundle,
      anchors,
      assetRoot: "assets/gate1/",
      ambience: false,
    });
  }
  override create() {
    super.create();
    // Shared Plaza's old schematic shadow boxes are not artwork in this slice.
    for (const child of [...this.children.list])
      if (child instanceof Phaser.GameObjects.Rectangle && child.depth === -50)
        child.destroy();
    this.game.canvas.setAttribute(
      "aria-label",
      "Phố Muneum: mũi tên hoặc WASD để đi, Shift chạy, E khám phá, Space chào.",
    );
    if (new URLSearchParams(location.search).has("qa"))
      window.__GATE1_TEST__ = {
        place: (x, y) => {
          this.player.setPosition(x, y).setVelocity(0);
          this.lastPosition = { x, y };
        },
      };
    this.events.once("shutdown", () => {
      delete window.__GATE1__;
      delete window.__GATE1_TEST__;
    });
  }
  override interactProp() {
    this.interact();
  }
  override interact() {
    const close = venues
      .map((v) => ({
        v,
        d: Math.hypot(this.player.x - v.x, this.player.y - v.y),
      }))
      .sort((a, b) => a.d - b.d)[0];
    if (close && close.d < 96) {
      this.visited.add(close.v.id);
      this.interactions++;
      window.dispatchEvent(
        new CustomEvent("street-dialog", {
          detail: { title: close.v.label, text: close.v.text },
        }),
      );
    } else
      window.dispatchEvent(
        new CustomEvent("street-dialog", {
          detail: {
            title: "Phố Muneum",
            text: "Dạo theo mặt phố. Đến gần một cửa tiệm hoặc sân gặp gỡ rồi nhấn E để khám phá.",
          },
        }),
      );
  }
  override update(time: number, delta: number) {
    const vx = this.player?.body?.velocity.x ?? 0,
      vy = this.player?.body?.velocity.y ?? 0;
    super.update(time, delta);
    if (!this.player?.body) return;
    const magnitude = Math.min(1, Math.hypot(controls.x, controls.y));
    if (magnitude > 0 && !controls.paused && !document.hidden) {
      const speed = controls.run ? 100 : 60,
        step = Math.min(delta, 100) * 0.85;
      const approach = (v: number, t: number) =>
        v + Math.sign(t - v) * Math.min(Math.abs(t - v), step);
      this.player.setVelocity(
        approach(vx, controls.x * speed),
        approach(vy, controls.y * speed),
      );
    }
    const cam = this.cameras.main;
    cam.setFollowOffset(0, Math.min(160, this.scale.height * 0.22));
    if (new URLSearchParams(location.search).has("overview")) {
      cam.stopFollow();
      cam.setZoom(1);
      cam.centerOn(world.width / 2, world.height / 2);
    }
    const nearest = venues
      .map((v) => ({
        v,
        d: Math.hypot(this.player.x - v.x, this.player.y - v.y),
      }))
      .sort((a, b) => a.d - b.d)[0];
    const id = nearest && nearest.d < 96 ? nearest.v.id : null;
    if (id !== this.activeVenue) {
      this.activeVenue = id;
      window.dispatchEvent(
        new CustomEvent("street-near", {
          detail: id ? nearest.v.label : "Dạo phố · sân gặp gỡ ở bên kia đường",
        }),
      );
    }
    window.__GATE1__ = {
      ready: true,
      x: this.player.x,
      y: this.player.y,
      frame: window.__PLAZA_REVIEW__?.frame ?? "",
      venues: [...this.visited],
      activeVenue: this.activeVenue,
      userApproval: "PENDING",
      source: "Gate1 new original street + protected Juni/shared foundation",
    };
  }
}
