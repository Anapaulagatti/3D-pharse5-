import { describe, it, expect } from "vitest";
import {
  quests,
  questRequirements,
  questAvailable,
  questStoryline,
  discoveryPoints,
} from "../../src/quests/content";
import { QuestManager, QUEST_STORAGE_KEY } from "../../src/quests/manager";
import { freshEconomy, validInventory, items } from "../../src/economy/catalog";
import {
  roomLayouts,
  roomWalkable,
  roomInteractionGround,
} from "../../src/interiors/registry";
const mem = () => {
  const m = new Map<string, string>();
  return {
    getItem: (k: string) => m.get(k) ?? null,
    setItem: (k: string, v: string) => {
      m.set(k, v);
    },
  };
};
function setup(completed: string[] = []) {
  const storage = mem(),
    records = Object.fromEntries(
      completed.map((id) => [
        id,
        {
          status: "completed",
          step: quests.find((q) => q.id === id)!.steps.length,
          attempts: 0,
        },
      ]),
    );
  storage.setItem(
    QUEST_STORAGE_KEY,
    JSON.stringify({
      schemaVersion: 1,
      records,
      coins: 40,
      xp: 0,
      inventory: { tangerine: 1 },
      transactions: completed.map((id) => `quest:${id}:base`),
      economy: freshEconomy(),
    }),
  );
  return { m: new QuestManager(storage), storage };
}
const finish = (m: QuestManager, id: string) => {
  const q = quests.find((q) => q.id === id)!;
  expect(m.returnToNPC(id, q.recipient ?? q.giver)).toBe(true);
  const a = m.question(id)!;
  expect(m.answerText(id, a.id, a.acceptedAnswers[0]).result).toBe("correct");
};
const service = (
  m: QuestManager,
  item: string,
  n: number,
  player: readonly [number, number] = [100, 200],
  target: readonly [number, number] = [100, 200],
) =>
  m.interiorEvent(
    "service",
    item,
    `test:${item}:${n}`,
    player,
    target,
    () => true,
  );
describe("V4 interwoven physical quest state and distinct room contracts", () => {
  it("12 unique real quests, five storylines, >=2branches and >=2joins with no cycle or dangling requirement", () => {
    expect(quests).toHaveLength(12);
    expect(new Set(quests.map((q) => q.id)).size).toBe(12);
    expect(new Set(quests.map(questStoryline)).size).toBeGreaterThanOrEqual(4);
    const out = new Map<string, number>();
    for (const q of quests)
      for (const pre of questRequirements(q)) {
        expect(quests.some((x) => x.id === pre)).toBe(true);
        out.set(pre, (out.get(pre) ?? 0) + 1);
      }
    expect(
      [...out.values()].filter((n) => n >= 2).length,
    ).toBeGreaterThanOrEqual(2);
    expect(
      quests.filter((q) => questRequirements(q).length >= 2).length,
    ).toBeGreaterThanOrEqual(2);
    const seen = new Set<string>(),
      active = new Set<string>();
    function visit(id: string) {
      if (seen.has(id)) return;
      expect(active.has(id), "cycle:" + id).toBe(false);
      active.add(id);
      for (const p of questRequirements(quests.find((q) => q.id === id)!))
        visit(p);
      active.delete(id);
      seen.add(id);
    }
    for (const q of quests) visit(q.id);
    expect(quests.find((q) => q.id === "farm-variety-v2")?.optional).toBe(true);
  });
  it("early discoveries persist before acceptance; all prereqs gate convergence; service distance/order enforced and rewards once", () => {
    const { m, storage } = setup([
      "farm-first-seed-v1",
      "shop-garden-market-v1",
      "jeju-orchard-v1",
      "town-first-delivery-v2",
    ]);
    for (const p of discoveryPoints)
      expect(m.observeWorld(p.point, () => true)).toBe(true);
    expect(m.accept("jeju-supply-v4", "npc-minseo")).toBe(false);
    expect(m.accept("culture-postcard-v4", "npc-seoyeon")).toBe(true);
    expect(m.snapshot().records["culture-postcard-v4"].step).toBe(2);
    finish(m, "culture-postcard-v4");
    expect(m.accept("workshop-imprint-v4", "npc-eunji")).toBe(true);
    expect(service(m, "workshop:packing", 0)).toBe(false);
    expect(service(m, "workshop:tools", 1, [0, 0], [100, 200])).toBe(false);
    expect(service(m, "workshop:tools", 2)).toBe(true);
    expect(service(m, "workshop:packing", 3)).toBe(true);
    finish(m, "workshop-imprint-v4");
    expect(m.accept("jeju-supply-v4", "npc-minseo")).toBe(true);
    expect(service(m, "seed-shop:packing", 4)).toBe(true);
    expect(m.snapshot().records["jeju-supply-v4"].step).toBe(3);
    finish(m, "jeju-supply-v4");
    expect(m.snapshot().inventory["supply-parcel"]).toBe(0);
    expect(m.accept("island-ledger-v4", "npc-harin")).toBe(true);
    expect(m.snapshot().records["island-ledger-v4"].step).toBe(1);
    expect(service(m, "seed-shop:packing", 5)).toBe(true);
    finish(m, "island-ledger-v4");
    expect(m.snapshot().inventory.tangerine).toBe(0);
    expect(m.accept("town-reunion-v4", "npc-jiho")).toBe(true);
    for (const [i, s] of [
      "workshop:packing",
      "seed-shop:packing",
      "bookshop:notice",
    ].entries())
      expect(service(m, s, 6 + i)).toBe(true);
    finish(m, "town-reunion-v4");
    const after = m.snapshot();
    expect(after.coins).toBe(152);
    expect(after.inventory["town-bookmark"]).toBe(1);
    expect(m.returnToNPC("town-reunion-v4", "npc-jiho")).toBe(false);
    expect(
      m.answerText("town-reunion-v4", "parcel-1", "책을 전해요"),
    ).toBeDefined();
    expect(m.snapshot().coins).toBe(after.coins);
    expect(new QuestManager(storage).snapshot()).toEqual(after);
    expect(after.trace!.some((t) => t.kind === "quest:accept")).toBe(true);
  });
  it("optional side quest never gates the required paths; quest papers do not consume the twelve crop/seed slots", () => {
    const records = Object.fromEntries(
      quests
        .filter((q) => q.id !== "farm-variety-v2")
        .map((q) => [q.id, { status: "completed" }]),
    );
    expect(quests.every((q) => questAvailable(q, records))).toBe(true);
    const inv = Object.fromEntries(
      Object.keys(items)
        .filter((id) => id.startsWith("seed-"))
        .slice(0, 12)
        .map((id) => [id, 1]),
    );
    expect(
      validInventory({ ...inv, "archive-note": 1, "packing-seal": 1 }),
    ).toBe(true);
    expect(validInventory({ ...inv, "archive-note": 100 })).toBe(false);
  });
  it("V2 save backed up byte exactly before first V4 write, old records and economic data preserved", () => {
    const { m, storage } = setup(["farm-first-seed-v1"]);
    const before = storage.getItem(QUEST_STORAGE_KEY);
    expect(m.toggleHints()).toBe(true);
    expect(storage.getItem(QUEST_STORAGE_KEY + ":backup:roadmap-v4")).toBe(
      before,
    );
    const saved = m.snapshot();
    expect(saved.coins).toBe(40);
    expect(saved.inventory.tangerine).toBe(1);
    m.toggleHints();
    expect(storage.getItem(QUEST_STORAGE_KEY + ":backup:roadmap-v4")).toBe(
      before,
    );
    expect(new QuestManager(storage).snapshot().storySchema).toBe(1);
  });
  it("rooms have distinct dimensions/furniture/approaches and all interaction anchors reachable without walking through counters", () => {
    expect(
      new Set(Object.values(roomLayouts).map((l) => JSON.stringify(l.props)))
        .size,
    ).toBe(3);
    for (const l of Object.values(roomLayouts)) {
      for (const p of [
        l.spawn,
        l.exit,
        l.fragment,
        l.sign,
        l.courier,
        l.service,
        l.actor,
      ])
        expect(roomWalkable(...p, l), JSON.stringify(p)).toBe(true);
      const [x, y, w, h] = l.counters[0];
      expect(roomWalkable(x + w / 2, y + h / 2, l)).toBe(false);
      expect(roomInteractionGround(x + w / 2, y + h / 2, l)).toBe(true);
      expect(roomInteractionGround(10, 100, l)).toBe(false);
    }
  });
});
