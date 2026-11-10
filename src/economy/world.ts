import Phaser from "phaser";
import { cropVisual } from "./presentation";
import groundOwnership from "../../public/assets/roadmap-v4/farm/ownership.json";
import { plots } from "./catalog";
import type { QuestSave } from "../quests/manager";
/** Small native material components and independently owned crop cells; no bed-sized image. */
export class FarmWorld {
  private grounds: Phaser.GameObjects.Image[] = [];
  private entries: {
    id: string;
    tiles: Phaser.GameObjects.Image[];
    plant: Phaser.GameObjects.Sprite;
    debris: Phaser.GameObjects.Image;
    hint: Phaser.GameObjects.Graphics;
    hit: Phaser.GameObjects.Zone;
  }[];
  private last = "";
  constructor(scene: Phaser.Scene, onPick: (id: string) => void) {
    for (const bed of groundOwnership.beds)
      this.grounds.push(
        scene.add
          .image(bed.x, bed.y, "farm-ground-" + bed.id)
          .setOrigin(0)
          .setDepth(bed.y - 1),
      );
    for (const bed of groundOwnership.beds)
      for (const layer of ["rim-back", "rim-front"] as const) {
        const rim = bed[layer];
        this.grounds.push(
          scene.add
            .image(
              rim.position[0],
              rim.position[1],
              "farm-" + layer + "-" + bed.id,
            )
            .setOrigin(0)
            .setDepth(rim.depth),
        );
      }
    this.entries = plots.map((p, i) => {
      const [x, y, w, h] = p.sourceRect,
        tiles: Phaser.GameObjects.Image[] = [];
      for (let dy = 0; dy < h; dy += 16)
        for (let dx = 0; dx < w; dx += 16)
          tiles.push(
            scene.add
              .image(
                x + dx,
                y + dy,
                "farm-materials",
                `tilled-${(i + dx + dy) % 12}`,
              )
              .setOrigin(0)
              .setCrop(0, 0, Math.min(16, w - dx), Math.min(16, h - dy))
              .setDepth(y)
              .setVisible(false),
          );
      const plant = scene.add
        .sprite(...p.root, "farm-crops", "radish-sown")
        .setOrigin(0.5, 40 / 44)
        .setDepth(p.root[1] + 1)
        .setVisible(false);
      const hint = scene.add.graphics().setDepth(p.root[1] + 2);
      const hit = scene.add
        .zone(x, y, w, h)
        .setOrigin(0)
        .setDepth(p.root[1] - 1)
        .setInteractive({ useHandCursor: true });
      hit.on("pointerup", (pointer: Phaser.Input.Pointer) => {
        if (pointer.getDistance() < 12) onPick(p.id);
      });
      const debris = scene.add
        .image(
          x + 8 + ((i * 7) % 14),
          y + 8 + ((i * 11) % 16),
          "farm-materials",
          ["debris-stone", "debris-straw", "debris-rim"][i % 3],
        )
        .setOrigin(0.5)
        .setDepth(y + 1)
        .setVisible(i % 2 === 0);
      return { id: p.id, tiles, plant, debris, hint, hit };
    });
  }
  update(save: QuestSave, selected?: string) {
    const views = this.entries.map((e) =>
      cropVisual(save.economy.plots[e.id], Date.now()),
    );
    const key = JSON.stringify([views, selected]);
    if (key === this.last) return;
    this.last = key;
    this.entries.forEach((e, i) => {
      const v = views[i],
        p = plots[i],
        visible = !["empty", "tilled"].includes(v.stage);
      e.tiles.forEach((tile, j) =>
        tile
          .setFrame(`${v.wet ? "wet" : "tilled"}-${(i * 7 + j * 5) % 12}`)
          .setVisible(v.stage !== "empty"),
      );
      e.debris.setVisible(v.stage === "empty" && i % 2 === 0);
      e.plant.setVisible(visible);
      if (visible && v.frame) e.plant.setFrame(v.frame);
      const g = e.hint.clear();
      if (e.id === selected) {
        const [x, y, w, h] = p.sourceRect;
        g.fillStyle(0xf3dc9a, 1)
          .fillRect(x + 2, y + h - 2, 5, 1)
          .fillRect(x + w - 7, y + h - 2, 5, 1);
      }
    });
  }
  dispose() {
    for (const o of this.grounds) o.destroy();
    for (const e of this.entries) {
      e.debris.destroy();
      e.hit.destroy();
      e.hint.destroy();
      e.plant.destroy();
      for (const t of e.tiles) t.destroy();
    }
  }
}
