import Phaser from "phaser";
import { quests } from "./content";
import type { QuestSave } from "./manager";
/** Three native harvestable objects at existing canonical fruit anchors. No scenery writes. */
export class QuestWorldIndicators {
  private entries: { step: string; sprite: Phaser.GameObjects.Sprite }[];
  constructor(scene: Phaser.Scene, onPick: (step: string) => void) {
    this.entries = quests
      .find((q) => q.topic === "orchard")!
      .steps.map((p) => {
        const sprite = scene.add
          .sprite(p.point[0], p.point[1] - 2, "world-actions", "basket")
          .setOrigin(0.5, 0.85)
          .setDepth(p.point[1] + 0.1)
          .setVisible(false)
          .setInteractive(
            new Phaser.Geom.Rectangle(-14, -8, 44, 44),
            Phaser.Geom.Rectangle.Contains,
          );
        sprite.on("pointerup", (pointer: Phaser.Input.Pointer) => {
          if (pointer.getDistance() < 12) onPick(p.id);
        });
        return { step: p.id, sprite };
      });
  }
  update(save: QuestSave) {
    const r = save.records["jeju-orchard-v1"],
      collected =
        r?.collected ?? this.entries.slice(0, r?.step ?? 0).map((e) => e.step);
    for (const e of this.entries)
      e.sprite.setVisible(
        r?.status === "active" && !collected.includes(e.step),
      );
  }
  dispose() {
    for (const e of this.entries) e.sprite.destroy();
  }
}
