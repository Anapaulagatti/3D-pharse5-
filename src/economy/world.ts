import Phaser from "phaser";
import { cropVisual } from "./presentation";
import { plots } from "./catalog";
import type { QuestSave } from "../quests/manager";
/** Reversible managed beds cover only baked crop interiors, never fences or public aisles. */
export class FarmWorld {
  private entries: {
    id: string;
    soil: Phaser.GameObjects.Sprite;
    graphics: Phaser.GameObjects.Graphics;
    label: Phaser.GameObjects.Text;
    plants: Phaser.GameObjects.Sprite[];
    hit: Phaser.GameObjects.Zone;
  }[];
  private last = "";
  constructor(scene: Phaser.Scene, onPick: (id: string) => void) {
    this.entries = plots.map((plot) => {
      const [x, y, , h] = plot.bed;
      const soil = scene.add
        .sprite(x, y, "farm-soil", 0)
        .setOrigin(0)
        .setDepth(y);
      const graphics = scene.add.graphics().setDepth(y + h + 1);
      const label = scene.add
        .text(x, y + h + 18, "", {
          fontSize: "10px",
          fontFamily: "system-ui",
          color: "#fff2d2",
          backgroundColor: "#3c4c37",
          padding: { x: 3, y: 1 },
        })
        .setDepth(y + h + 19);
      const plants = Array.from({ length: 18 }, (_, i) => {
        const py = y + 20 + Math.floor(i / 6) * 27;
        return scene.add
          .sprite(x + 14 + (i % 6) * 22, py, "farm-crops", "radish-sown")
          .setOrigin(0.5, 0.85)
          .setDepth(py + 1)
          .setVisible(false);
      });
      const r = plot.sourceRect;
      const hit = scene.add
        .zone(r[0], r[1], r[2], r[3])
        .setOrigin(0)
        .setDepth(y - 1)
        .setInteractive({ useHandCursor: true });
      hit.on("pointerup", (pointer: Phaser.Input.Pointer) => {
        if (pointer.getDistance() < 12) onPick(plot.id);
      });
      return { id: plot.id, soil, graphics, label, plants, hit };
    });
  }
  update(save: QuestSave, selected?: string) {
    const view = this.entries.map((e) =>
      cropVisual(save.economy.plots[e.id], Date.now()),
    );
    const key = JSON.stringify([view, selected]);
    if (key === this.last) return;
    this.last = key;
    this.entries.forEach((e, i) => {
      const visual = view[i],
        def = plots[i],
        [x, y, w, h] = def.bed;
      e.soil.setFrame(visual.wet ? 1 : 0);
      const g = e.graphics.clear();
      if (visual.stage === "empty") {
        // Unworked soil: interrupt furrows with native clods, no fake pre-grown crops.
        for (let j = 0; j < 30; j++)
          g.fillStyle(j % 2 ? 0x70583e : 0xa1865b).fillRect(
            x + 3 + ((j * 37) % (w - 8)),
            y + 3 + ((j * 19) % (h - 8)),
            4,
            2,
          );
      }
      if (selected === e.id) g.lineStyle(1, 0xf3d58e).strokeRect(x, y, w, h);
      // Wet-soil sheen is native pixels and remains behind plant silhouettes.
      if (visual.wet)
        for (let j = 0; j < 9; j++)
          g.fillStyle(0x718d8d, 0.7).fillRect(
            x + 6 + ((j * 31) % (w - 16)),
            y + 24 + ((j * 17) % (h - 30)),
            3,
            1,
          );
      for (const plant of e.plants) {
        plant.setVisible(!["empty", "tilled"].includes(visual.stage));
        if (visual.frame && !["empty", "tilled"].includes(visual.stage))
          plant.setFrame(visual.frame);
      }
      const name = {
        empty: "Đất trống",
        tilled: "Đất đã làm",
        sown: "Đã gieo",
        sprout: "Nảy mầm",
        young: "Cây non",
        growing: "Đang lớn",
        ready: "Thu hoạch",
      }[visual.stage];
      e.label
        .setText(
          `Luống ${Number(def.id.slice(-2))} · ${name}${visual.stage === "sown" && !visual.wet ? " · cần tưới" : visual.wet ? " · đất ẩm" : ""}`,
        )
        .setVisible(selected === e.id);
    });
  }
  dispose() {
    for (const e of this.entries) {
      e.soil.destroy();
      e.graphics.destroy();
      e.hit.destroy();
      e.label.destroy();
      for (const p of e.plants) p.destroy();
    }
  }
}
