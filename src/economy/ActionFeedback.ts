import Phaser from "phaser";
import type { WorldFeedback } from "../quests/ui";
type Point = readonly [number, number];
type View = "front" | "back" | "left" | "right";
/** Native world-space temporary tools. Never changes player art, anchor, collision or movement. */
export class ActionFeedback {
  private graphics: Phaser.GameObjects.Graphics;
  private tool: Phaser.GameObjects.Sprite;
  private gain: Phaser.GameObjects.Text;
  private action?: {
    kind: WorldFeedback;
    target: Point;
    start: Point;
    elapsed: number;
    view: View;
  };
  constructor(
    scene: Phaser.Scene,
    private player: () => Point,
    private view: () => View,
  ) {
    this.graphics = scene.add.graphics();
    this.tool = scene.add
      .sprite(0, 0, "world-actions", "seed-pouch")
      .setOrigin(0.5, 0.6)
      .setVisible(false);
    this.gain = scene.add
      .text(0, 0, "", {
        fontSize: "12px",
        fontFamily: "monospace",
        color: "#fff0b1",
        backgroundColor: "#294437",
        padding: { x: 4, y: 2 },
      })
      .setOrigin(0.5, 1)
      .setVisible(false);
  }
  play(kind: WorldFeedback, target: Point, label: string) {
    const p = this.player();
    this.action = {
      kind,
      target,
      start: [...p],
      elapsed: 0,
      view: this.view(),
    };
    this.gain
      .setText(label)
      .setPosition(Math.round(p[0]), Math.round(p[1]) - 98)
      .setDepth(p[1] + 2)
      .setVisible(true);
    this.tool
      .setFrame(
        kind === "water"
          ? "water-can"
          : kind === "plant"
            ? "seed-pouch"
            : kind === "harvest"
              ? "sickle"
              : kind === "deliver"
                ? "parcel"
                : kind === "collect" || kind === "handover"
                  ? "tangerine"
                  : "coin",
      )
      .setVisible(kind !== "report");
  }
  update(delta: number) {
    const a = this.action;
    this.graphics.clear();
    if (!a) return;
    a.elapsed += Math.min(100, delta);
    const t = Math.min(1, a.elapsed / 900),
      p = this.player(),
      offsets: Record<View, Point> = {
        front: [15, -38],
        back: [-14, -42],
        left: [-19, -39],
        right: [19, -39],
      },
      [ox, oy] = offsets[a.view],
      hand: Point = [p[0] + ox, p[1] + oy];
    this.tool
      .setPosition(
        Math.round(hand[0]),
        Math.round(hand[1] - Math.sin(t * Math.PI) * 2),
      )
      .setDepth(p[1] + (a.view === "back" ? -0.03 : 0.2))
      .setFlipX(a.view === "left");
    this.tool.setVisible(
      a.kind !== "report" &&
        t < 0.8 &&
        Math.hypot(p[0] - a.start[0], p[1] - a.start[1]) < 4,
    );
    if (a.kind === "water")
      this.tool.setFrame(t > 0.2 && t < 0.75 ? "water-can-pour" : "water-can");
    this.graphics.setDepth(Math.max(p[1], a.target[1]) + 0.3);
    for (
      let i = 0;
      i < (a.kind === "report" ? 0 : a.kind === "water" ? 8 : 4);
      i++
    ) {
      const v = (t + i * 0.09) % 1,
        collect = a.kind === "harvest" || a.kind === "collect",
        from = collect ? a.target : hand,
        to = collect ? [p[0], p[1] - 35] : a.target,
        x = Math.round(from[0] + (to[0] - from[0]) * v + ((i % 3) - 1) * 2),
        y = Math.round(
          from[1] +
            (to[1] - from[1]) * v -
            Math.sin(v * Math.PI) * (a.kind === "water" ? 6 : 16),
        );
      this.graphics
        .fillStyle(
          a.kind === "water"
            ? 0x8bced8
            : a.kind === "reward"
              ? 0xf0d28b
              : 0xdeb965,
          1,
        )
        .fillRect(x, y, 2, a.kind === "water" ? 3 : 2);
    }
    this.gain.setPosition(
      Math.round(a.start[0]),
      Math.round(a.start[1] - 94 - t * 12),
    );
    if (t >= 1) {
      this.action = undefined;
      this.tool.setVisible(false);
      this.gain.setVisible(false);
      this.graphics.clear();
    }
  }
  snapshot() {
    return {
      action: this.action?.kind ?? null,
      nativeToolScale: this.tool.scaleX,
      registration: [8, 12],
      sourceArtModified: false,
    };
  }
  dispose() {
    this.graphics.destroy();
    this.tool.destroy();
    this.gain.destroy();
  }
}
