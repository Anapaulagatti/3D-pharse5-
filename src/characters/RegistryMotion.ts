import type { CharacterDefinition, Direction } from "./types";
import type { JuniGesture } from "../engine/JuniMotion";
/** Generic pose playback for future completed atlases. World movement remains
 * entirely in the original scene controller, shared by every avatar. */
export class RegistryMotion {
  action = "idle";
  view: Direction = "front";
  frame: string;
  phase = 0;
  private elapsed = 0;
  private requested: JuniGesture | null = null;
  constructor(private def: CharacterDefinition) {
    this.frame = def.animations["idle-front"].frames[0];
  }
  gesture(action: JuniGesture) {
    this.requested = action;
  }
  step(
    dt: number,
    travelled: number,
    input: boolean,
    running: boolean,
    view: Direction,
    reduced: boolean,
    paused: boolean,
  ) {
    if (paused) return this.frame;
    this.elapsed += Math.min(dt, 100);
    const gait = running ? "run" : "walk";
    if (travelled > 0)
      this.phase =
        (this.phase +
          travelled /
            (running
              ? this.def.movement.runStride
              : this.def.movement.walkStride)) %
        1;
    if (input) {
      this.action = gait;
      this.view = view;
      this.requested = null;
    } else if (this.requested) {
      this.action = this.requested;
      this.requested = null;
      this.view = "front";
      this.elapsed = 0;
    } else if (this.action === "walk" || this.action === "run") {
      this.action = "idle";
      this.elapsed = 0;
    }
    let clip =
      this.def.animations[`${this.action}-${this.view}`] ??
      this.def.animations[`idle-${this.view}`];
    const total = clip.durationsMs.reduce((a, b) => a + b, 0);
    if (!clip.loop && this.elapsed >= total) {
      this.action = "idle";
      this.elapsed = 0;
      clip = this.def.animations[`idle-${this.view}`];
    }
    let index = 0;
    if (input)
      index = Math.floor(this.phase * clip.frames.length) % clip.frames.length;
    else if (!reduced) {
      let t = this.elapsed % clip.durationsMs.reduce((a, b) => a + b, 0);
      while (index < clip.frames.length - 1 && t >= clip.durationsMs[index])
        t -= clip.durationsMs[index++];
    }
    this.frame = clip.frames[index];
    return this.frame;
  }
  get snapshot() {
    return {
      action: this.action,
      view: this.view,
      frame: this.frame,
      phase: this.phase,
      heading: this.view,
    };
  }
}
