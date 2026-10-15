import animation from "../../assets-src/juni-animation/runtime.json";
export type JuniView = "front" | "back" | "left" | "right";
export type JuniGesture = "wave" | "celebrate" | "social";
type Action = "idle" | "walk" | "run" | "start" | "stop" | "turn" | JuniGesture;

const headings: Record<JuniView, number> = {
  front: 0,
  left: 2,
  back: 4,
  right: 6,
};
const inverse: JuniView[] = [
  "front",
  "front",
  "left",
  "left",
  "back",
  "back",
  "right",
  "right",
];
const durations = animation.durations;

/** Frames are genuine retained imagegen art. This class selects poses only;
 * physics owns position and scale. No mirroring, squash shader or image tween.
 * The gait clock advances by ACTUAL collision-resolved travel, not input/time.
 */
export class JuniMotion {
  action: Action = "idle";
  view: JuniView = "front";
  frame = "idle-front-0";
  phase = 0;
  private elapsed = 0;
  private moving = false;
  private turnFrames: number[] = [];
  private turnTarget: JuniView = "front";
  private afterTurn: Action = "idle";
  private requested: JuniGesture | null = null;
  private reducedPose: string | null = null;
  private heading = 0;

  gesture(action: JuniGesture) {
    this.requested = action;
  }

  private begin(action: Action) {
    this.action = action;
    this.elapsed = 0;
    this.reducedPose = null;
  }

  private turn(target: JuniView, after: Action) {
    let heading = this.heading;
    const end = headings[target];
    const forward = (end - heading + 8) % 8;
    const step = forward <= 4 ? 1 : -1;
    this.turnFrames = [];
    while (heading !== end) {
      heading = (heading + step + 8) % 8;
      this.turnFrames.push(heading);
    }
    this.turnTarget = target;
    this.afterTurn = after;
    this.begin("turn");
  }

  step(
    dt: number,
    travelled: number,
    input: boolean,
    running: boolean,
    view: JuniView,
    reduced: boolean,
    paused: boolean,
  ): string {
    if (paused) return this.frame;
    this.elapsed += Math.min(dt, 100);
    const gait = running ? "run" : "walk";
    // Declared/tuned stride, not an alleged mocap measurement. Retain phase on
    // direction/run changes so a planted contact doesn't restart on every key.
    if (travelled > 0)
      this.phase =
        (this.phase +
          travelled /
            (running ? animation.strides.run : animation.strides.walk)) %
        1;
    if (this.requested && !input) {
      const action = this.requested;
      this.requested = null;
      if (!reduced && this.view !== "front") this.turn("front", action);
      else {
        this.view = "front";
        this.heading = 0;
        this.begin(action);
      }
    } else if (input) {
      this.requested = null;
      if (
        this.action === "turn" ? view !== this.turnTarget : view !== this.view
      ) {
        if (reduced) {
          this.view = view;
          this.heading = headings[view];
          this.begin(gait);
        } else if (this.heading === headings[view]) {
          this.view = view;
          this.begin(this.moving ? gait : "start");
        } else this.turn(view, this.moving ? gait : "start");
      } else if (!this.moving && this.action !== "turn") this.begin("start");
      else if (!["start", "turn"].includes(this.action)) this.action = gait;
    } else if (this.moving) this.begin("stop");
    this.moving = input;

    if (this.action === "turn") {
      if (this.elapsed >= this.turnFrames.length * 50) {
        this.view = this.turnTarget;
        this.heading = headings[this.view];
        this.begin(
          input
            ? this.afterTurn === "start"
              ? "start"
              : gait
            : this.afterTurn,
        );
      } else {
        const heading =
          this.turnFrames[
            Math.min(this.turnFrames.length - 1, Math.floor(this.elapsed / 50))
          ];
        this.frame = `turn-${heading}`;
        this.heading = heading;
        return this.frame;
      }
    }
    if (this.action === "walk" || this.action === "run") {
      // Essential user-controlled locomotion remains articulated in reduced
      // motion; idle/environment/unsolicited motion is simplified instead.
      this.frame = `${this.action}-${this.view}-${Math.floor(this.phase * 8) % 8}`;
      return this.frame;
    }
    if (reduced && this.action === "idle") {
      this.frame = `idle-${this.view}-0`;
      return this.frame;
    }
    const times = durations[this.action as keyof typeof durations];
    const total = times.reduce((a, b) => a + b, 0);
    if (this.action !== "idle" && this.elapsed >= total) {
      this.begin(input ? gait : "idle");
      return this.step(0, 0, input, running, view, reduced, false);
    }
    let clock = this.elapsed % total;
    let index = 0;
    while (index < times.length - 1 && clock >= times[index])
      clock -= times[index++];
    if (reduced && ["wave", "celebrate", "social"].includes(this.action)) {
      this.reducedPose ??= `${this.action}-front-${this.action === "celebrate" ? 7 : 4}`;
      this.frame = this.reducedPose;
    } else this.frame = `${this.action}-${this.view}-${index}`;
    return this.frame;
  }

  get snapshot() {
    return {
      action: this.action,
      view: this.view,
      frame: this.frame,
      phase: this.phase,
      heading:
        this.action === "turn"
          ? inverse[Number(this.frame.split("-")[1])]
          : this.view,
    };
  }
}
