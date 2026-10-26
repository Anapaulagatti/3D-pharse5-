import type { CharacterDefinition, Direction } from "./types";
import type { JuniGesture } from "../engine/JuniMotion";
/** Playback only: world travel/collision/camera remain in the accepted controller.
 * Native locomotion phase follows actual distance, never wall-clock input time. */
export class RegistryMotion {
  action = "idle";
  view: Direction = "front";
  frame: string;
  phase = 0;
  private elapsed = 0;
  private requested: JuniGesture | null = null;
  private moving = false;
  private transition: string | null = null;
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
    const enter = (action: string, transition: string | null = null) => {
      this.action = action;
      this.transition = transition;
      this.elapsed = 0;
    };
    if (input) {
      this.requested = null;
      const turn = `turn-${this.view}-${view}`;
      if (this.view !== view && this.def.animations[turn]) enter("turn", turn);
      else if (!this.moving && this.def.animations[`start-${view}`])
        enter("start", `start-${view}`);
      else if (!this.transition) this.action = gait;
      this.view = view;
    } else if (this.requested) {
      enter(this.requested);
      this.requested = null;
      this.view = "front";
    } else if (this.moving) {
      if (this.def.animations[`stop-${this.view}`])
        enter("stop", `stop-${this.view}`);
      else enter("idle");
    }
    this.moving = input;
    const current = () =>
      this.def.animations[this.transition ?? `${this.action}-${this.view}`] ??
      this.def.animations[`idle-${this.view}`];
    let clip = current();
    const duration = () => clip.durationsMs.reduce((a, b) => a + b, 0);
    if (!clip.loop && this.elapsed >= duration()) {
      enter(input ? gait : "idle");
      clip = current();
    }
    let index = 0;
    if (input && !this.transition)
      index = Math.floor(this.phase * clip.frames.length) % clip.frames.length;
    else if (!reduced || !clip.loop) {
      let t = this.elapsed % duration();
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
