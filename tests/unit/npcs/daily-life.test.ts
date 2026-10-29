import { describe, it, expect } from "vitest";
import {
  NPCWorldClock,
  phaseAt,
  seededChoice,
  lifeClockKey,
} from "../../../src/npcs/clock";
import {
  dailySchedules,
  resolveActivity,
  validateSchedules,
} from "../../../src/npcs/schedules";
import { runtimeNPCCatalog } from "../../../src/npcs/history";
import { NPCActorModel } from "../../../src/npcs/actor";
import { NPCStateStore } from "../../../src/npcs/state";
const memory = () => {
  const data = new Map<string, string>();
  return {
    data,
    getItem: (k: string) => data.get(k) ?? null,
    setItem: (k: string, v: string) => {
      data.set(k, v);
    },
  };
};
describe("deterministic day and existing FSM", () => {
  it("has explicit phase boundaries and midnight rollover", () => {
    expect(
      [299, 300, 659, 660, 839, 840, 1079, 1080, 1319, 1320, 1440].map((m) =>
        phaseAt(m),
      ),
    ).toEqual([
      "night",
      "morning",
      "morning",
      "midday",
      "midday",
      "afternoon",
      "afternoon",
      "evening",
      "evening",
      "night",
      "night",
    ]);
    const c = new NPCWorldClock(undefined, 30000);
    c.setReviewTime(1439.9, 60);
    c.tick(200);
    expect(c.day).toBe(1);
    expect(c.minute).toBeLessThan(600);
  });
  it("clamps gaps, pauses and never persists QA acceleration", () => {
    const m = memory(),
      c = new NPCWorldClock(m);
    c.tick(86400000, true);
    expect(c.minute).toBe(540);
    c.tick(86400000, false, true);
    expect(c.minute).toBe(540);
    c.tick(86400000);
    expect(c.minute).toBeCloseTo(540.16);
    c.setReviewTime(1000, 60);
    c.save();
    const restored = new NPCWorldClock(m);
    expect(restored.minute).toBe(1000);
    expect(restored.rate).toBe(1);
  });
  it("tolerates malformed new records without touching old player/NPC data", () => {
    const m = memory();
    m.data.set("korean-arena-npc-world-v1", "KEEP");
    for (const raw of [
      "{",
      JSON.stringify({ version: 1, day: -1, minute: 1 }),
      JSON.stringify({ version: 99 }),
    ]) {
      m.data.set(lifeClockKey, raw);
      const c = new NPCWorldClock(m);
      expect(c.minute).toBe(540);
      c.save();
      expect(m.data.get("korean-arena-npc-world-v1")).toBe("KEEP");
    }
  });
  it("replays seeded choices and validates referenced anchors", () => {
    expect(seededChoice(42, 2, "work", 4)).toBe(seededChoice(42, 2, "work", 4));
    expect(validateSchedules(runtimeNPCCatalog.npcs)).toBe(26);
    for (const p of dailySchedules) {
      const n = runtimeNPCCatalog.get(p.npcId)!,
        c = new NPCWorldClock();
      expect(resolveActivity(n, c.snapshot())).toEqual(
        resolveActivity(n, c.snapshot()),
      );
    }
  });
  it("keeps TALK motionless and resumes the current task", () => {
    const d = runtimeNPCCatalog.get("npc-minseo")!,
      s = new NPCStateStore(undefined, [d]),
      a = new NPCActorModel(d, s.get(d.id)),
      c = new NPCWorldClock();
    a.setActivity(resolveActivity(d, c.snapshot()));
    const before = [...a.record.position];
    a.talk([600, 2630]);
    c.setReviewTime(720);
    a.setActivity(resolveActivity(d, c.snapshot()));
    a.step(
      100,
      () => true,
      () => false,
    );
    expect(a.record.position).toEqual(before);
    expect(a.state).toBe("TALK");
    a.finishTalk();
    for (let i = 0; i < 100; i++)
      a.step(
        50,
        () => true,
        () => false,
      );
    expect(a.activity?.id).toContain("midday-break");
    expect(a.record.position[0]).toBeGreaterThanOrEqual(650);
    expect(a.record.position[0]).toBeLessThanOrEqual(682);
  });
  it("provides exactly 20 distinct contemporary and six archive plans", () => {
    expect(
      dailySchedules.filter((p) => p.context === "present-day"),
    ).toHaveLength(20);
    expect(
      dailySchedules.filter((p) => p.context === "archive-story"),
    ).toHaveLength(6);
    expect(new Set(dailySchedules.map((p) => p.npcId)).size).toBe(26);
    expect(
      new Set(dailySchedules.map((p) => JSON.stringify(p.entries))).size,
    ).toBe(26);
  });
  it("ignores modern time/day for a selected era story while varying locally", () => {
    const n = runtimeNPCCatalog.get("npc-history-sejong")!,
      c = new NPCWorldClock(),
      first = resolveActivity(n, c.snapshot(), 1000);
    c.setReviewTime(1380);
    c.day = 100;
    expect(resolveActivity(n, c.snapshot(), 1000)).toEqual(first);
    expect(resolveActivity(n, c.snapshot(), 9000)?.id).not.toBe(first?.id);
  });
  it("uses unique visitor windows with deterministic quiet slots", async () => {
    const { visitorForGameTime } = await import("../../../src/npcs/visits");
    expect(visitorForGameTime("modern", 540, 20261029, 0)?.id).toBe(
      "npc-modern-daon",
    );
    expect(visitorForGameTime("modern", 10, 20261029, 0)).toBeUndefined();
    for (let m = 0; m < 1440; m += 15)
      expect(visitorForGameTime("station", m, 42, 3)).toEqual(
        visitorForGameTime("station", m, 42, 3),
      );
  });
  it("retains the visitor host slot during an out-of-window conversation", async () => {
    const { NPCVisitPolicy } = await import("../../../src/npcs/visits");
    const p = new NPCVisitPolicy(),
      ids = p.eligible(
        new Set(["modern"]),
        "npc-modern-daon",
        undefined,
        0,
        1400,
      );
    expect(ids.has("npc-modern-daon")).toBe(true);
    expect(ids.has("npc-minseo")).toBe(false);
  });
  it("runs a full configured day with bounded checkpoint storage", () => {
    const m = memory(),
      c = new NPCWorldClock(m);
    c.setReviewTime(0);
    for (let i = 0; i < 9001; i++) c.tick(200);
    expect(c.day).toBe(1);
    expect(c.minute).toBeLessThan(1);
    c.save(
      Object.fromEntries(
        Array.from({ length: 100 }, (_, i) => ["npc-test-" + i, "work"]),
      ),
    );
    expect(Object.keys(c.snapshot().scheduleCheckpoint)).toHaveLength(26);
  });
  it("backs off without tunneling, snapping or unbounded FSM history", () => {
    const d = runtimeNPCCatalog.get("npc-minseo")!,
      s = new NPCStateStore(undefined, [d]),
      a = new NPCActorModel(d, s.get(d.id)),
      c = new NPCWorldClock();
    c.setReviewTime(720);
    a.setActivity(resolveActivity(d, c.snapshot()));
    const before = [...a.record.position];
    for (let i = 0; i < 800; i++)
      a.step(
        50,
        () => false,
        () => false,
      );
    expect(a.record.position).toEqual(before);
    expect(a.blocked).toBeLessThan(30);
    expect(a.machine.history.length).toBeLessThanOrEqual(32);
  });
});
