import type { NPCState, NPCDirection, Point, NPCDefinition } from "./types";
import { onDeclaredRoute } from "./navigation";
export const transitions: Record<NPCState, readonly NPCState[]> = {
  IDLE: ["LOOK_AROUND", "PATROL", "GREET", "TALK"],
  LOOK_AROUND: ["IDLE", "PATROL", "GREET", "TALK"],
  PATROL: ["MOVE_TO_WAYPOINT", "WAIT", "GREET", "TALK"],
  MOVE_TO_WAYPOINT: ["WAIT", "IDLE", "GREET", "TALK"],
  WAIT: ["PATROL", "IDLE", "GREET", "TALK"],
  GREET: ["RETURN_TO_ACTIVITY", "TALK"],
  TALK: ["RETURN_TO_ACTIVITY"],
  RETURN_TO_ACTIVITY: ["IDLE", "PATROL", "MOVE_TO_WAYPOINT", "GREET", "TALK"],
};
export class NPCStateMachine {
  state: NPCState = "IDLE";
  history: { from: NPCState; to: NPCState }[] = [];
  transition(to: NPCState) {
    if (to === this.state) return;
    if (!transitions[this.state].includes(to))
      throw Error(`Invalid NPC transition ${this.state}→${to}`);
    this.history.push({ from: this.state, to });
    if (this.history.length > 32) this.history.shift();
    this.state = to;
  }
}
export interface NPCRecord {
  position: Point;
  direction: NPCDirection;
  waypoint: number;
  conversations: number;
  distance: number;
}
export class NPCStateStore {
  private records = new Map<string, NPCRecord>();
  constructor(
    private storage: Pick<Storage, "getItem" | "setItem"> | undefined,
    defs: readonly NPCDefinition[],
  ) {
    let input: Record<string, unknown> = {};
    try {
      const raw = JSON.parse(
        storage?.getItem("korean-arena-npc-world-v1") ?? "null",
      );
      if (raw?.version === 1) input = raw.records ?? {};
    } catch {
      /* Storage is optional. */
    }
    for (const d of defs) {
      const q = input[d.id] as Partial<NPCRecord> | undefined;
      const p = q?.position;
      const valid =
        Array.isArray(p) &&
        p.length === 2 &&
        p.every((v) => typeof v === "number" && Number.isFinite(v)) &&
        onDeclaredRoute(d, p as Point);
      this.records.set(d.id, {
        position: valid ? [p![0], p![1]] : [...d.spawn],
        direction:
          q?.direction &&
          ["front", "back", "left", "right"].includes(q.direction)
            ? q.direction
            : d.direction,
        waypoint:
          Number.isInteger(q?.waypoint) &&
          q!.waypoint! >= 0 &&
          q!.waypoint! < d.route.length
            ? q!.waypoint!
            : 1,
        conversations:
          typeof q?.conversations === "number" &&
          Number.isFinite(q.conversations)
            ? Math.max(0, Math.min(10000, Math.floor(q.conversations)))
            : 0,
        distance:
          typeof q?.distance === "number" && Number.isFinite(q.distance)
            ? Math.max(0, q.distance) % 44
            : 0,
      });
    }
  }
  get(id: string) {
    return this.records.get(id)!;
  }
  save() {
    try {
      this.storage?.setItem(
        "korean-arena-npc-world-v1",
        JSON.stringify({
          version: 1,
          records: Object.fromEntries(this.records),
        }),
      );
    } catch {
      /* Never reset player stores on quota errors. */
    }
  }
}
export function facing(
  dx: number,
  dy: number,
  fallback: NPCDirection,
): NPCDirection {
  if (Math.hypot(dx, dy) < 0.01) return fallback;
  return Math.abs(dx) > Math.abs(dy)
    ? dx > 0
      ? "right"
      : "left"
    : dy > 0
      ? "front"
      : "back";
}
export function animationFrame(
  def: NPCDefinition,
  state: NPCState,
  direction: NPCDirection,
  elapsed: number,
  distance: number,
  activity: boolean,
) {
  const kind =
    state === "MOVE_TO_WAYPOINT"
      ? "walk"
      : state === "GREET" || state === "TALK"
        ? "greet"
        : activity
          ? "activity"
          : "idle";
  const clip = def.animations[`${kind}-${direction}`];
  if (kind === "walk")
    return clip.frames[Math.floor(((distance % 44) / 44) * 8)];
  const duration = clip.durationsMs.reduce((a, b) => a + b, 0);
  let t = elapsed % duration;
  for (let i = 0; i < clip.frames.length; i++) {
    if (t < clip.durationsMs[i]) return clip.frames[i];
    t -= clip.durationsMs[i];
  }
  return clip.frames[0];
}
