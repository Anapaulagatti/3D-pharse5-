import Phaser from "phaser";
import { quests } from "./content";
import type { QuestSave } from "./manager";
/** Temporary gameplay indicators, separate from immutable world art and collision.
 * Practice tray sits beside cultivated bed4; no planted world plot is relabeled empty.
 */
export class QuestWorldIndicators {
  private graphics: Phaser.GameObjects.Graphics;
  private label: Phaser.GameObjects.Text;
  private key = "";
  constructor(scene: Phaser.Scene) {
    this.graphics = scene.add.graphics().setDepth(670);
    this.label = scene.add
      .text(0, 0, "", {
        fontSize: "11px",
        color: "#fff2ce",
        backgroundColor: "#263e39",
        padding: { x: 4, y: 3 },
      })
      .setOrigin(0.5, 1)
      .setDepth(674);
  }
  update(save: QuestSave) {
    const key = JSON.stringify(save.records);
    if (key === this.key) return;
    this.key = key;
    const g = this.graphics.clear();
    this.label.setVisible(false);
    for (const def of quests) {
      const record = save.records[def.id];
      if (!record) continue;
      if (def.topic === "orchard" && record.status === "active") {
        for (let i = record.step; i < def.steps.length; i++) {
          const [x, y] = def.steps[i].point;
          g.fillStyle(0x704a2f, 1).fillRect(x - 6, y - 2, 12, 5);
          g.fillStyle(0xefac3c, 1)
            .fillRect(x - 4, y - 5, 3, 3)
            .fillRect(x + 1, y - 4, 3, 3);
          g.lineStyle(1, 0xffe3a3, 1).strokeRect(x - 7, y - 7, 14, 11);
        }
      }
      if (def.topic === "farm") {
        // Native pixel gameplay tray, not a replacement painted farming landscape.
        const [x, y] = def.steps[0].point;
        g.fillStyle(0x78634a, 1).fillRect(x - 10, y - 8, 20, 10);
        g.fillStyle(record.step > 0 ? 0x704b36 : 0xb39a6b, 1).fillRect(
          x - 8,
          y - 7,
          16,
          7,
        );
        if (record.step >= 2)
          g.fillStyle(0xd4b56b, 1)
            .fillRect(x - 5, y - 4, 2, 2)
            .fillRect(x + 3, y - 4, 2, 2);
        if (record.step >= 3)
          g.fillStyle(0x557d43, 1)
            .fillRect(x - 5, y - 7, 2, 5)
            .fillRect(x - 7, y - 6, 5, 2)
            .fillRect(x + 3, y - 7, 2, 5)
            .fillRect(x + 1, y - 6, 5, 2);
        this.label
          .setPosition(x, y - 14)
          .setText("Khay thực hành · 연습")
          .setVisible(true);
      }
    }
  }
  dispose() {
    this.graphics.destroy();
    this.label.destroy();
  }
}
