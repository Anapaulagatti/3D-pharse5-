import Phaser from "phaser";
import { growthProgress } from "./presentation";
import { plots, ready } from "./catalog";
import type { QuestSave } from "../quests/manager";
/** Additive front-row gameplay objects inside approved cultivated rectangles; no ground texture writes. */
export class FarmWorld {
  private entries: {
    id: string;
    graphics: Phaser.GameObjects.Graphics;
    label: Phaser.GameObjects.Text;
    plants: Phaser.GameObjects.Sprite[];
    hit: Phaser.GameObjects.Zone;
  }[];
  private last = "";
  constructor(scene: Phaser.Scene, onPick: (id: string) => void) {
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
      const r = plot.sourceRect;
      const hit = scene.add
        .zone(r[0], r[1], r[2], r[3])
        .setOrigin(0)
        .setDepth(y - 1)
        .setInteractive({ useHandCursor: true });
      hit.on("pointerup", (pointer: Phaser.Input.Pointer) => {
        if (pointer.getDistance() < 12) onPick(plot.id);
      });
      return { id: plot.id, graphics, label, plants, hit };
    });
  }
  update(save: QuestSave, selected?: string) {
    const view = this.entries.map((e) => {
      const p = save.economy.plots[e.id];
      return {
        ...p,
        ready: ready(p, Date.now()),
        sprouting: growthProgress(p, Date.now()) >= 0.25,
      };
    });
    const key = JSON.stringify([view, selected]);
    if (key === this.last) return;
    this.last = key;
    this.entries.forEach((e, i) => {
      const p = view[i],
        def = plots[i],
        [x, y, w, h] = def.row;
      const g = e.graphics.clear();
      // Reversible managed native front row within the approved cultivated rectangle.
      g.fillStyle(p.stage === "watered" ? 0x6c6047 : 0x947d53, 1).fillRect(
        x,
        y,
        w,
        h,
      );
      for (let n = 0; n < 20; n++)
        g.fillStyle(n % 3 ? 0xb49c6c : 0x705c41, 1).fillRect(
          x + ((n * 37 + i * 11) % (w - 2)),
          y + ((n * 7 + i * 3) % (h - 1)),
          2,
          1,
        );
      g.fillStyle(selected === e.id ? 0xf3d58e : 0x897c51, 1)
        .fillRect(x - 1, y - 1, w + 2, 1)
        .fillRect(x - 1, y + h, w + 2, 1)
        .fillRect(x - 1, y, 1, h)
        .fillRect(x + w, y, 1, h);
      if (p.stage !== "empty")
        for (let j = 1; j < 4; j++)
          g.fillStyle(p.stage === "watered" ? 0x635442 : 0x967b50, 1).fillRect(
            x,
            y + j * 3,
            w,
            1,
          );
      const frame = p.crop
        ? `${p.crop}-${p.ready ? "ready" : p.stage === "watered" && p.sprouting ? "sprout" : "sown"}`
        : "radish-sown";
      for (const plant of e.plants)
        plant
          .setVisible(p.stage === "planted" || p.stage === "watered")
          .setFrame(frame);
      e.label
        .setOrigin(0, 0)
        .setPosition(def.sourceRect[0] + 5, y + 18)
        .setText(`Luống ${Number(def.id.slice(-2))}`)
        .setVisible(selected === e.id);
    });
  }
  dispose() {
    for (const e of this.entries) {
      e.graphics.destroy();
      e.hit.destroy();
      e.label.destroy();
      for (const p of e.plants) p.destroy();
    }
  }
}
