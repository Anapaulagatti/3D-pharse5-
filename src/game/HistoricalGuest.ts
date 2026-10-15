import Phaser from "phaser";
import { ActorMotion, type Emote } from "./ActorMotion";
import { facing } from "../domains/state";
import type { historicalGuests } from "../content/historicalGuests";
type Definition = (typeof historicalGuests)[number];
export class HistoricalGuest {
  readonly body: Phaser.Physics.Arcade.Sprite;
  private label: Phaser.GameObjects.Text;
  readonly motion = new ActorMotion();
  private previous: { x: number; y: number };
  private rest = 2400;
  private target = 0;
  private nextGesture: Emote | null = null;
  private gestureWait = 0;
  private route: { x: number; y: number }[];
  constructor(
    scene: Phaser.Scene,
    readonly definition: Definition,
    solids: Phaser.Physics.Arcade.StaticGroup,
    onInteract: () => void,
  ) {
    const [x, y] = definition.home;
    this.body = scene.physics.add
      .sprite(x, y, `guest-${definition.id}`, "idle-down-0")
      .setOrigin(0.5, 64 / 68)
      .setDepth(y)
      .setInteractive({ pixelPerfect: true });
    this.body.body?.setSize(16, 8);
    this.body.body?.setOffset(16, 55);
    scene.physics.add.collider(this.body, solids);
    this.body.on("pointerdown", onInteract);
    this.label = scene.add
      .text(x, y - 68, definition.name, {
        fontFamily: "system-ui",
        fontSize: "8px",
        color: "#fff2d0",
        backgroundColor: "#303e47",
        padding: { x: 3, y: 2 },
      })
      .setOrigin(0.5, 1)
      .setDepth(y + 0.1);
    this.previous = { x, y };
    this.route = [
      { x: x - 10, y },
      { x: x + 10, y },
      { x: x + 10, y: y + 12 },
      { x: x - 10, y: y + 12 },
    ];
  }
  greet() {
    this.rest = 2600;
    this.body.setVelocity(0);
    this.motion.emote("wave");
    this.nextGesture =
      this.definition.gesture === "wave"
        ? null
        : (this.definition.gesture as Emote);
    this.gestureWait = 900;
  }
  step(dt: number, paused: boolean, reduced: boolean) {
    const b = this.body;
    const actual = Math.hypot(b.x - this.previous.x, b.y - this.previous.y);
    this.previous = { x: b.x, y: b.y };
    let moving = false,
      dx = 0,
      dy = 0;
    if (!paused) {
      this.rest = Math.max(0, this.rest - dt);
      if (this.nextGesture) {
        this.gestureWait -= dt;
        if (this.gestureWait <= 0) {
          this.motion.emote(this.nextGesture);
          this.nextGesture = null;
        }
      }
      if (!reduced && !this.rest) {
        const t = this.route[this.target];
        dx = t.x - b.x;
        dy = t.y - b.y;
        if (Math.hypot(dx, dy) < 1.5) {
          this.target = (this.target + 1) % this.route.length;
          this.rest = 1600;
        } else moving = true;
      }
      const l = Math.hypot(dx, dy) || 1;
      b.setVelocity(moving ? (dx / l) * 18 : 0, moving ? (dy / l) * 18 : 0);
    } else b.setVelocity(0);
    const dr = facing(moving ? dx : 0, moving ? dy : 0, this.motion.direction);
    b.setFrame(
      this.motion.step(dt, actual, moving, false, dr, reduced, paused),
    ).setDepth(Math.round(b.y));
    this.label
      .setPosition(Math.round(b.x), Math.round(b.y) - 68)
      .setDepth(Math.round(b.y) + 0.1);
  }
  get metrics() {
    return {
      id: this.definition.id,
      x: this.body.x,
      y: this.body.y,
      frame: this.body.frame.name,
      mood: this.motion.mood ?? "neutral",
      direction: this.motion.direction,
    };
  }
}
