import Phaser from "phaser";
import type { ContactSpec } from "./NativeContact";
import { entranceRepairs } from "./Accessibility";
/** Read-only QA overlay samples the SAME readiness-aware player anchor query, never opens terrain. */
export class CollisionDebug {
  private graphics: Phaser.GameObjects.Graphics;
  private elapsed = 0;
  constructor(
    private scene: Phaser.Scene,
    private contact?: ContactSpec,
  ) {
    this.graphics = scene.add.graphics().setDepth(100000);
  }
  update(
    delta: number,
    x: number,
    y: number,
    walkable: (x: number, y: number) => boolean,
    frame = "idle-front-0",
  ) {
    this.elapsed += delta;
    if (this.elapsed < 250) return;
    this.elapsed = 0;
    const g = this.graphics.clear(),
      v = this.scene.cameras.main.worldView;
    for (let sy = Math.floor(v.y / 8) * 8; sy < v.bottom; sy += 8)
      for (let sx = Math.floor(v.x / 8) * 8; sx < v.right; sx += 8) {
        const free = walkable(sx, sy),
          narrow =
            free &&
            (!walkable(sx - 8, sy) ||
              !walkable(sx + 8, sy) ||
              !walkable(sx, sy - 8) ||
              !walkable(sx, sy + 8));
        g.fillStyle(
          !free ? 0xff3535 : narrow ? 0xffc344 : 0x35df96,
          0.22,
        ).fillRect(sx, sy, 8, 8);
      }
    // Global collision is an anchor sample; only the local contact field adds native foot pixels.
    g.fillStyle(0xffffff, 1).fillRect(Math.round(x), Math.round(y), 1, 1);
    const parts = frame.split("-");
    const offsets =
      this.contact?.footprints[
        `${parts[0] === "run" ? "run" : "walk"}-${parts[1]}`
      ] ?? [];
    if (
      this.contact &&
      x >= this.contact.rect[0] &&
      y >= this.contact.rect[1] &&
      x < this.contact.rect[0] + this.contact.rect[2] &&
      y < this.contact.rect[1] + this.contact.rect[3]
    )
      for (const [dx, dy] of offsets)
        g.fillRect(Math.round(x) + dx, Math.round(y) + dy, 1, 1);
    for (const p of entranceRepairs) {
      const [a, b, w, h] = p.rect;
      g.lineStyle(1, 0x45bfff, 1).strokeRect(a, b, w, h);
    }
  }
  dispose() {
    this.graphics.destroy();
  }
}
