import type { NPCDefinition, Point, NPCState } from "./types";
import {
  NPCStateMachine,
  facing,
  animationFrame,
  type NPCRecord,
} from "./state";
import { moveOnRoute, type GroundQuery } from "./navigation";
export class NPCActorModel {
  readonly machine = new NPCStateMachine();
  timer = 2200;
  elapsed = 0;
  cooldown = 0;
  blocked = 0;
  cycles = 0;
  private resume: NPCState = "IDLE";
  constructor(
    readonly def: NPCDefinition,
    readonly record: NPCRecord,
  ) {}
  get state() {
    return this.machine.state;
  }
  private enter(state: NPCState, ms = 0) {
    this.machine.transition(state);
    this.elapsed = 0;
    this.timer = ms;
  }
  greet(player: Point) {
    if (
      this.cooldown > 0 ||
      ["GREET", "TALK", "RETURN_TO_ACTIVITY"].includes(this.state)
    )
      return;
    this.resume = this.state;
    this.record.direction = facing(
      player[0] - this.record.position[0],
      player[1] - this.record.position[1],
      this.record.direction,
    );
    this.cooldown = 12000;
    this.enter("GREET", 900);
  }
  talk(player: Point) {
    if (this.state !== "GREET") this.resume = this.state;
    this.record.direction = facing(
      player[0] - this.record.position[0],
      player[1] - this.record.position[1],
      this.record.direction,
    );
    this.enter("TALK");
  }
  finishTalk() {
    if (this.state !== "TALK") return;
    this.record.conversations = Math.min(10000, this.record.conversations + 1);
    this.enter("RETURN_TO_ACTIVITY", 550);
    this.cooldown = 12000;
  }
  step(dt: number, ground: GroundQuery, occupied: (p: Point) => boolean) {
    this.elapsed += dt;
    this.cooldown = Math.max(0, this.cooldown - dt);
    this.timer = Math.max(0, this.timer - dt);
    if (this.state === "TALK") return;
    if (this.state === "GREET") {
      if (!this.timer) this.enter("RETURN_TO_ACTIVITY", 500);
      return;
    }
    if (this.state === "RETURN_TO_ACTIVITY") {
      if (!this.timer)
        this.enter(
          this.resume === "MOVE_TO_WAYPOINT" ? "MOVE_TO_WAYPOINT" : "IDLE",
          this.resume === "MOVE_TO_WAYPOINT" ? 0 : 2200,
        );
      return;
    }
    if (this.state === "IDLE") {
      if (!this.timer)
        this.enter(this.cycles % 3 === 0 ? "LOOK_AROUND" : "PATROL", 800);
      return;
    }
    if (this.state === "LOOK_AROUND") {
      if (this.elapsed < dt + 1) {
        const ds = ["front", "left", "back", "right"] as const;
        this.record.direction = ds[(ds.indexOf(this.record.direction) + 1) % 4];
      }
      if (!this.timer) this.enter("PATROL");
      return;
    }
    if (this.state === "WAIT") {
      if (!this.timer)
        this.enter(this.cycles % 4 === 0 ? "IDLE" : "PATROL", 2200);
      return;
    }
    if (this.state === "PATROL") {
      this.enter("MOVE_TO_WAYPOINT");
      return;
    }
    const target = this.def.route[this.record.waypoint];
    this.record.direction = facing(
      target[0] - this.record.position[0],
      target[1] - this.record.position[1],
      this.record.direction,
    );
    const next = moveOnRoute(
      this.def,
      this.record.position,
      target,
      (this.def.walkSpeed * dt) / 1000,
      ground,
      occupied,
    );
    this.record.position = next.position;
    this.record.distance = (this.record.distance + next.distance) % 44;
    if (next.arrived) {
      this.record.waypoint = (this.record.waypoint + 1) % this.def.route.length;
      this.cycles++;
      this.enter("WAIT", 850 + (this.cycles % 3) * 130);
    } else if (next.blocked) {
      this.blocked++;
      this.enter("WAIT", 650);
    }
  }
  frame() {
    return animationFrame(
      this.def,
      this.state,
      this.record.direction,
      this.elapsed,
      this.record.distance,
      (this.state === "IDLE" && this.elapsed > 400) ||
        (this.state === "WAIT" && this.cycles % 3 === 0),
    );
  }
  snapshot() {
    return {
      id: this.def.id,
      zone: this.def.homeZone,
      position: [...this.record.position],
      direction: this.record.direction,
      state: this.state,
      frame: this.frame(),
      waypoint: this.record.waypoint,
      conversations: this.record.conversations,
      blocked: this.blocked,
      history: [...this.machine.history],
    };
  }
}
