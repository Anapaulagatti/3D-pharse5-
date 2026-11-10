import Phaser from "phaser";
import { quests } from "./content";
import type { QuestSave } from "./manager";
/** Three native harvestable objects at existing canonical fruit anchors. No scenery writes. */
export class QuestWorldIndicators {
  private beacon: Phaser.GameObjects.Graphics;
  private entries: { step: string; sprite: Phaser.GameObjects.Sprite }[];
  constructor(scene: Phaser.Scene, onPick: (step: string) => void) {
    this.beacon = scene.add.graphics().setDepth(9000);
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
    this.beacon.clear();
    const active = quests
        .filter((q) => save.records[q.id]?.status === "active")
        .sort(
          (a, b) =>
            Number(b.id === save.trackedQuest) -
            Number(a.id === save.trackedQuest),
        ),
      q = active[0],
      step = q?.steps[save.records[q.id]?.step ?? -1];
    if (step && save.hints !== false) {
      const [x, y] = step.point;
      this.beacon
        .lineStyle(1, 0xf5db85, 1)
        .strokeCircle(x, y, 9)
        .fillStyle(0xf5db85, 1)
        .fillTriangle(x - 4, y - 21, x + 4, y - 21, x, y - 15);
    }
    const r = save.records["jeju-orchard-v1"],
      collected =
        r?.collected ?? this.entries.slice(0, r?.step ?? 0).map((e) => e.step);
    for (const e of this.entries)
      e.sprite.setVisible(
        r?.status === "active" && !collected.includes(e.step),
      );
  }
  dispose() {
    this.beacon.destroy();
    for (const e of this.entries) e.sprite.destroy();
  }
}
