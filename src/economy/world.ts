import Phaser from "phaser";
import { plots, ready } from "./catalog";
import type { QuestSave } from "../quests/manager";
/** Additive front-row gameplay objects inside approved cultivated rectangles; no ground texture writes. */
export class FarmWorld {
  private entries: {
    id: string;
    graphics: Phaser.GameObjects.Graphics;
    label: Phaser.GameObjects.Text;
    plants: Phaser.GameObjects.Sprite[];
  }[];
  private last = "";
  constructor(scene: Phaser.Scene) {
    this.entries = plots.map((plot) => {
      const [x, y, w] = plot.row;
      const graphics = scene.add.graphics().setDepth(y + 1);
      const label = scene.add
        .text(x + w / 2, y + 17, plot.id.replace("NW-FARM-", "Luống "), {
          fontSize: "10px",
          fontFamily: "system-ui",
          color: "#fff2d2",
          backgroundColor: "#3c4c37",
          padding: { x: 3, y: 1 },
        })
        .setOrigin(0.5, 0)
        .setDepth(y + 18);
      const plants = Array.from({ length: 6 }, (_, i) =>
        scene.add
          .sprite(x + i * 20 + 8, y + 9, "farm-crops", "radish-sown")
          .setOrigin(0.5, 0.85)
          .setDepth(y + 10)
          .setVisible(false),
      );
      return { id: plot.id, graphics, label, plants };
    });
  }
  update(save: QuestSave) {
    const view = this.entries.map((e) => {
      const p = save.economy.plots[e.id];
      return { ...p, ready: ready(p, Date.now()) };
    });
    const key = JSON.stringify(view);
    if (key === this.last) return;
    this.last = key;
    this.entries.forEach((e, i) => {
      const p = view[i],
        def = plots[i],
        [x, y, w, h] = def.row;
      const g = e.graphics.clear();
      g.lineStyle(1, 0xa9a26d, 0.7).strokeRect(x - 1, y - 1, w + 2, h + 2);
      if (p.stage !== "empty") {
        g.lineStyle(1, p.stage === "watered" ? 0x635442 : 0x967b50, 0.9);
        for (let j = 1; j < 4; j++)
          g.lineBetween(x, y + j * 3, x + w, y + j * 3);
      }
      const frame = p.crop
        ? `${p.crop}-${p.ready ? "ready" : p.stage === "watered" ? "sprout" : "sown"}`
        : "radish-sown";
      for (const plant of e.plants)
        plant
          .setVisible(p.stage === "planted" || p.stage === "watered")
          .setFrame(frame);
      e.label.setText(
        `${def.id.slice(-2)} · ${p.ready ? "Thu hoạch" : p.stage === "empty" ? "Hàng trống" : p.stage === "tilled" ? "Đã xới" : p.stage === "planted" ? "Cần tưới" : "Đang lớn"}`,
      );
    });
  }
  dispose() {
    for (const e of this.entries) {
      e.graphics.destroy();
      e.label.destroy();
      for (const p of e.plants) p.destroy();
    }
  }
}
