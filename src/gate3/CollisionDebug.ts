import Phaser from "phaser";
import type { ContactSpec } from "./NativeContact";
import { entranceRepairs } from "./Accessibility";
/** Read-only QA overlay samples the SAME readiness-aware player anchor query, never opens terrain. */
export class CollisionDebug {
  private graphics: Phaser.GameObjects.Graphics;
  private elapsed = 0;
  private readout: Phaser.GameObjects.Text;
  constructor(
    private scene: Phaser.Scene,
    private contact?: ContactSpec,
    private points: readonly (readonly [number, number])[] = [],
    private solids: readonly { rect: readonly number[] }[] = [],
  ) {
    this.graphics = scene.add.graphics().setDepth(100000);
    this.readout = scene.add
      .text(8, 8, "", {
        fontFamily: "monospace",
        fontSize: "11px",
        color: "#fff6ce",
        backgroundColor: "#182921",
      })
      .setScrollFactor(0)
      .setDepth(100001);
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
    const camera = this.scene.cameras.main;
    const zones = this.scene.children.list.filter(
      (o): o is Phaser.GameObjects.Zone => o instanceof Phaser.GameObjects.Zone,
    );
    this.readout.setText(
      `QA ground collision | x${x.toFixed(2)} y${y.toFixed(2)} | camera ${camera.scrollX.toFixed(2)},${camera.scrollY.toFixed(2)}\nFoot native envelope [-27,-4]..[24,-1]; grid8px; blockers red; walkable green; zones purple\nCustom anchor-mask controller; Arcade/Matter bodies: NONE; frame ${frame}`,
    );
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
    for (const zone of zones)
      g.lineStyle(1, 0xc58eff, 0.6).strokeRect(
        zone.x - zone.displayWidth * zone.originX,
        zone.y - zone.displayHeight * zone.originY,
        zone.displayWidth,
        zone.displayHeight,
      );
    // Read-only native ground-foot envelope; no Arcade/Matter body exists here.
    g.lineStyle(1, 0x57eaff, 1).strokeRect(
      Math.round(x) - 27 + 0.5,
      Math.round(y) - 4 + 0.5,
      52,
      4,
    );
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
    // Declared entrance/exit landmarks and actual continuous solid reservations.
    for (const {
      rect: [sx, sy, w, h],
    } of this.solids)
      g.lineStyle(1, 0xff5555, 1).strokeRect(sx, sy, w, h);
    for (const [px, py] of this.points) {
      if (px < v.x || px > v.right || py < v.y || py > v.bottom) continue;
      g.lineStyle(1, walkable(px, py) ? 0x43e5ff : 0xff77dd, 1).strokeCircle(
        px,
        py,
        5,
      );
    }
    for (const p of entranceRepairs) {
      const [a, b, w, h] = p.rect;
      g.lineStyle(1, 0x45bfff, 1).strokeRect(a, b, w, h);
    }
  }
  dispose() {
    this.readout.destroy();
    this.graphics.destroy();
  }
}
