import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { NPCRegistry, npcRegistry } from "../../../src/npcs/registry";
import { npcSchema, validateNPCAtlas } from "../../../src/npcs/types";
import {
  NPCStateMachine,
  NPCStateStore,
  animationFrame,
} from "../../../src/npcs/state";
import { NPCActorModel } from "../../../src/npcs/actor";
import {
  moveOnRoute,
  routeSegmentAllows,
  clearInteractionLine,
  onDeclaredRoute,
} from "../../../src/npcs/navigation";
import { chooseTarget } from "../../../src/npcs/interaction";
import { npcReviewSpawn } from "../../../src/npcs/review";
const data = () => structuredClone(npcRegistry.npcs),
  nodes = () => structuredClone([...npcRegistry.nodes.values()]);
const memory = (initial: Record<string, string> = {}) => ({
  data: new Map(Object.entries(initial)),
  getItem(k: string) {
    return this.data.get(k) ?? null;
  },
  setItem(k: string, v: string) {
    this.data.set(k, v);
  },
});
const ground = () => true;
describe("native NPC registry, content and ownership", () => {
  it("has unique non-player IDs, all regional roles, complete native directional animation", () => {
    expect(npcRegistry.npcs.length).toBeGreaterThanOrEqual(4);
    expect(new Set(npcRegistry.npcs.map((n) => n.id)).size).toBe(
      npcRegistry.npcs.length,
    );
    for (const d of npcRegistry.npcs) {
      expect(d.names.ko).toMatch(/[가-힣]/);
      expect(d.names.vi.length).toBeGreaterThan(2);
      expect(d.assets.key).toBe(d.id);
      for (const direction of ["front", "back", "left", "right"]) {
        expect(new Set(d.animations["walk-" + direction].frames).size).toBe(8);
        expect(d.animations["idle-" + direction].frames.length).toBe(2);
        expect(d.animations["activity-" + direction].frames.length).toBe(8);
      }
      const atlas = JSON.parse(
        readFileSync("public/" + d.assets.atlas, "utf8"),
      );
      expect(() => validateNPCAtlas(d, atlas, 768, 1456)).not.toThrow();
    }
  });
  it("rejects duplicate IDs, unavailable cells and malformed timing", () => {
    const ds = data();
    expect(() => new NPCRegistry([...ds, ds[0]], nodes())).toThrow();
    const d = structuredClone(ds[0]);
    d.animations["walk-front"].frames[1] = d.animations["walk-front"].frames[0];
    expect(npcSchema.safeParse(d).success).toBe(false);
    const atlas = JSON.parse(
      readFileSync("public/" + ds[0].assets.atlas, "utf8"),
    );
    delete atlas.frames["walk-front-0"];
    expect(() => validateNPCAtlas(ds[0], atlas, 768, 1456)).toThrow();
  });
  it("rejects missing links, cycles, cross-owner references, orphans and out-of-world placement", () => {
    const ds = data();
    let ns = nodes();
    ns[0].next = "missing";
    expect(() => new NPCRegistry(ds, ns)).toThrow();
    ns = nodes();
    ns[1].next = ns[0].id;
    expect(() => new NPCRegistry(ds, ns)).toThrow();
    ns = nodes();
    ns[0].choices[0].next = ns.find((n) => n.npcId !== ns[0].npcId)!.id;
    expect(() => new NPCRegistry(ds, ns)).toThrow();
    ns = nodes();
    ns.push({ ...ns[0], id: "orphan" });
    expect(() => new NPCRegistry(ds, ns)).toThrow();
    ds[0].spawn = [-1, 0];
    expect(() => new NPCRegistry(ds, nodes())).toThrow();
  });
  it("keeps Korean/Vietnamese authored text complete and future providers inactive", () => {
    for (const n of npcRegistry.nodes.values()) {
      expect(n.content.ko).toMatch(/[가-힣]/);
      expect(n.content.vi).not.toMatch(/�|undefined|lorem/i);
      expect(n.content.vi.length).toBeGreaterThan(20);
      expect(n.futureQuestHook).toBeNull();
    }
    for (const n of npcRegistry.npcs) {
      expect(n.future.shopProviderId).toBeNull();
      expect(n.future.questProviderId).toBeNull();
    }
  });
  it("allows a review spawn only for an explicit known NPC QA URL", () => {
    expect(
      npcReviewSpawn(new URLSearchParams("npcReview=" + data()[0].id)),
    ).toBeUndefined();
    expect(
      npcReviewSpawn(new URLSearchParams("qa&npcReview=missing")),
    ).toBeUndefined();
    expect(
      npcReviewSpawn(new URLSearchParams("qa&npcReview=" + data()[0].id)),
    ).toEqual(data()[0].reviewSpawn);
  });
});
describe("native routes, proximity and state machine", () => {
  it("uses the canonical ground query across a complete registered footprint and swept route", () => {
    const d = data()[0];
    const a: [number, number] = [100, 100],
      b: [number, number] = [150, 100];
    expect(routeSegmentAllows(d, a, b, ground)).toBe(true);
    expect(
      routeSegmentAllows(d, a, b, (x, y) => !(x === 125 && y === 100)),
    ).toBe(false);
    expect(clearInteractionLine(a, b, (x) => x < 124)).toBe(false);
    const result = moveOnRoute(
      d,
      a,
      b,
      200,
      (x) => x < 120,
      () => false,
    );
    expect(result.blocked).toBe(true);
    expect(result.position[0]).toBeLessThan(120);
  });
  it("stops for occupancy without teleporting or exceeding declared step distance", () => {
    const d = data()[0];
    const r = moveOnRoute(
      d,
      [100, 100],
      [150, 100],
      18,
      ground,
      (p) => p[0] > 108,
    );
    expect(r.position[0]).toBe(108);
    expect(r.distance).toBe(8);
    expect(r.blocked).toBe(true);
    expect(onDeclaredRoute(d, d.spawn)).toBe(true);
    expect(onDeclaredRoute(d, [0, 0])).toBe(false);
  });
  it("selects closest deterministically, retains a near-equal eligible target and clears stale IDs", () => {
    expect(
      chooseTarget([
        { id: "npc-b", distance: 20 },
        { id: "npc-a", distance: 20 },
      ]),
    ).toBe("npc-a");
    expect(
      chooseTarget(
        [
          { id: "npc-b", distance: 30 },
          { id: "npc-a", distance: 20 },
        ],
        "npc-b",
      ),
    ).toBe("npc-b");
    expect(
      chooseTarget(
        [
          { id: "npc-b", distance: 40 },
          { id: "npc-a", distance: 20 },
        ],
        "npc-b",
      ),
    ).toBe("npc-a");
    expect(chooseTarget([], "stale")).toBeUndefined();
  });
  it("rejects forbidden FSM jumps and bounds transition history", () => {
    const m = new NPCStateMachine();
    expect(() => m.transition("RETURN_TO_ACTIVITY")).toThrow();
    for (let i = 0; i < 40; i++) {
      m.transition("GREET");
      m.transition("RETURN_TO_ACTIVITY");
      m.transition("IDLE");
    }
    expect(m.history).toHaveLength(32);
  });
  it("greets, pins talk, closes safely and returns to the same valid route", () => {
    const d = data()[0],
      store = new NPCStateStore(undefined, [d]),
      a = new NPCActorModel(d, store.get(d.id));
    a.greet([d.spawn[0], d.spawn[1] + 70]);
    expect(a.state).toBe("GREET");
    a.talk([d.spawn[0], d.spawn[1] + 60]);
    const p = [...a.record.position];
    for (let i = 0; i < 30; i++) a.step(100, ground, () => false);
    expect(a.state).toBe("TALK");
    expect(a.record.position).toEqual(p);
    a.finishTalk();
    expect(a.record.conversations).toBe(1);
    for (let i = 0; i < 90; i++) a.step(100, ground, () => false);
    expect(a.state).not.toBe("TALK");
    expect(onDeclaredRoute(d, a.record.position)).toBe(true);
  });
  it("maintains matching four-direction gait phases without editing a player controller", () => {
    const d = data()[0];
    for (const dir of ["front", "back", "left", "right"] as const) {
      const names = Array.from({ length: 8 }, (_, i) =>
        animationFrame(d, "MOVE_TO_WAYPOINT", dir, 0, (i * 44) / 8, false),
      );
      expect(names).toEqual(d.animations["walk-" + dir].frames);
    }
    expect(animationFrame(d, "TALK", "front", 0, 0, false)).toMatch(
      /^greet-front/,
    );
  });
  it("makes bounded progress on the full route, waits for obstructions and never enters blocked ground", () => {
    const d = data()[0],
      store = new NPCStateStore(undefined, [d]),
      a = new NPCActorModel(d, store.get(d.id));
    for (let i = 0; i < 500; i++) a.step(50, ground, () => false);
    expect(a.cycles).toBeGreaterThan(0);
    expect(onDeclaredRoute(d, a.record.position)).toBe(true);
    const before = [...a.record.position];
    for (let i = 0; i < 100; i++)
      a.step(
        50,
        () => false,
        () => false,
      );
    expect(a.record.position).toEqual(before);
    expect(a.blocked).toBeGreaterThan(0);
  });
});
describe("additive NPC persistence", () => {
  it("preserves deterministic position/phase across zone reactivation and independent reload", () => {
    const d = data()[0],
      storage = memory({
        "korean-arena-player-preferences-v1": "KEEP",
        "lesson-progress": "KEEP",
      }),
      store = new NPCStateStore(storage, [d]);
    const r = store.get(d.id);
    r.position = [...d.route[1]];
    r.waypoint = 2;
    r.distance = 22;
    r.conversations = 2;
    store.save();
    const next = new NPCStateStore(storage, [d]).get(d.id);
    expect(next).toEqual(r);
    expect(storage.getItem("korean-arena-player-preferences-v1")).toBe("KEEP");
    expect(storage.getItem("lesson-progress")).toBe("KEEP");
  });
  it("recovers corrupt/off-route state and denied storage without touching player data", () => {
    const d = data()[0];
    for (const records of [
      { [d.id]: { position: "xx" } },
      { [d.id]: { position: [0, 0], waypoint: 999, conversations: Infinity } },
    ]) {
      const s = memory({
        "korean-arena-npc-world-v1": JSON.stringify({ version: 1, records }),
      });
      expect(new NPCStateStore(s, [d]).get(d.id).position).toEqual(d.spawn);
    }
    expect(() =>
      new NPCStateStore(
        {
          getItem() {
            throw Error("denied");
          },
          setItem() {
            throw Error("denied");
          },
        },
        [d],
      ).save(),
    ).not.toThrow();
  });
});
