import type { Direction } from "../domains/state";
import manifest from "../../assets-src/actors/hero/manifest.json";
export type Emote = "wave" | "celebrate" | "pose" | "think";
type Action = keyof typeof manifest.actions;
/** Crisp hand-authored transitions; locomotion advances only on real travel. */
export class ActorMotion {
  private action: Action = "idle";
  private elapsed = 0;
  private phase = 0;
  private wasMoving = false;
  direction: Direction = "down";
  frame = "idle-down-0";
  private duration(action: Action) {
    const times = manifest.durations_ms as Record<string, number[]>;
    return (times[action] ?? []).reduce((a, b) => a + b, 0);
  }
  emote(action: Emote) {
    this.action = action;
    this.elapsed = 0;
  }
  get moveScale() {
    return this.action === "start"
      ? this.elapsed < 40
        ? 0
        : this.elapsed < 80
          ? 0.5
          : 1
      : 1;
  }
  get mood() {
    return this.action === "celebrate" || this.action === "wave"
      ? "happy"
      : this.action === "think" || this.action === "pose"
        ? "focused"
        : null;
  }
  step(
    dt: number,
    travelled: number,
    moving: boolean,
    running: boolean,
    direction: Direction,
    reduced: boolean,
    paused: boolean,
  ) {
    if (paused) return this.frame;
    this.elapsed += Math.min(dt, 150);
    const changed = direction !== this.direction;
    this.direction = direction;
    if (moving && !this.wasMoving) {
      this.action = "start";
      this.elapsed = 0;
    } else if (moving && changed) {
      this.action = "turn";
      this.elapsed = 0;
    } else if (!moving && this.wasMoving) {
      this.action = "stop";
      this.elapsed = 0;
    }
    this.wasMoving = moving;
    const transition = ["start", "stop", "turn"].includes(this.action);
    const emote = ["wave", "celebrate", "pose", "think"].includes(this.action);
    if ((transition || emote) && this.elapsed >= this.duration(this.action)) {
      this.action = moving ? (running ? "run" : "walk") : "idle";
      this.elapsed = 0;
    } else if (!transition && !emote)
      this.action = moving ? (running ? "run" : "walk") : "idle";
    let index = 0;
    if (moving)
      this.phase = (this.phase + travelled / (running ? 44 : 26.6666667)) % 1;
    if (this.action === "walk" || this.action === "run")
      index =
        Math.floor(this.phase * manifest.actions[this.action]) %
        manifest.actions[this.action];
    else if (!(this.action === "idle" && reduced)) {
      const times = (manifest.durations_ms as Record<string, number[]>)[
        this.action
      ];
      let clock =
        this.action === "idle"
          ? this.elapsed % this.duration("idle")
          : this.elapsed;
      for (; index < times.length - 1 && clock >= times[index]; index++)
        clock -= times[index];
    }
    this.frame = `${this.action}-${direction}-${index}`;
    return this.frame;
  }
}
