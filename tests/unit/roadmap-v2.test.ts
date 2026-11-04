import { describe, it, expect, vi } from "vitest";
import { crops, items, cropUnlocked, plots } from "../../src/economy/catalog";
import { QuestManager, QUEST_STORAGE_KEY } from "../../src/quests/manager";
import { quests } from "../../src/quests/content";
import {
  interiors,
  roomWalkable,
  ROOM,
  readInterior,
  INTERIOR_SAVE,
} from "../../src/interiors/registry";
import {
  LIVE_FEATURES,
  noAds,
  disabledRoom,
  LocalRoomSimulation,
} from "../../src/roadmap/contracts";
const storage = () => {
  const map = new Map<string, string>();
  return {
    map,
    getItem: (k: string) => map.get(k) ?? null,
    setItem: (k: string, v: string) => {
      map.set(k, v);
    },
  };
};
function fixture(completed: string[] = []) {
  const s = storage(),
    q = new QuestManager(s).snapshot();
  q.coins = 100;
  for (const id of completed) {
    q.records[id] = {
      status: "completed",
      step: quests.find((q) => q.id === id)!.steps.length,
      attempts: 0,
    };
    q.transactions.push(`quest:${id}:base`);
  }
  s.map.set(QUEST_STORAGE_KEY, JSON.stringify(q));
  return { store: s, manager: new QuestManager(s) };
}
describe("Roadmap V2 local content and transaction gates", () => {
  it("twelve real distinct native crop definitions; all prices and progression maps valid", () => {
    expect(Object.keys(crops)).toHaveLength(12);
    for (const c of Object.values(crops)) {
      expect(items[c.seed].buy).toBeGreaterThan(0);
      expect(items[c.produce].sell * c.yield).toBeGreaterThanOrEqual(
        items[c.seed].buy,
      );
      expect(c.growMs).toBeGreaterThanOrEqual(c.introMs);
    }
    expect(new Set(Object.values(crops).map((c) => c.frame)).size).toBe(12);
  });
  it("two explicit quest unlock chains, no purchase bypass or locked sowing", () => {
    expect(cropUnlocked("carrot", {})).toBe(false);
    expect(
      cropUnlocked("rice", { "farm-first-seed-v1": { status: "completed" } }),
    ).toBe(false);
    const { manager } = fixture();
    const c = {
      npcId: "npc-minseo",
      player: [0, 0] as const,
      actor: [0, 0] as const,
      ground: () => true,
    };
    const before = manager.snapshot();
    expect(manager.trade("buy", "seed-carrot", 1, "locked:buy", c)).toBe(false);
    expect(manager.snapshot()).toEqual(before);
    const { manager: a } = fixture(["farm-first-seed-v1"]);
    expect(a.trade("buy", "seed-carrot", 1, "open:buy", c)).toBe(true);
    expect(a.trade("buy", "seed-rice", 1, "locked:rice", c)).toBe(false);
    expect(
      cropUnlocked("rice", {
        "shop-garden-market-v1": { status: "completed" },
      }),
    ).toBe(true);
  });
  it("three crop lifecycles independent, real duration bounds, reload, exactly-once harvesting", () => {
    const { manager: m, store } = fixture(["farm-first-seed-v1"]);
    const v = m.snapshot();
    v.inventory = { "seed-radish": 1, "seed-scallion": 1, "seed-carrot": 1 };
    store.map.set(QUEST_STORAGE_KEY, JSON.stringify(v));
    const a = new QuestManager(store);
    for (const [id, index] of [
      ["radish", 0],
      ["scallion", 1],
      ["carrot", 2],
    ] as const) {
      const p = plots[index];
      expect(
        a.farmAction(
          p.id,
          "till",
          undefined,
          `${id}:till`,
          p.point,
          () => true,
          100,
        ),
      ).toBe(true);
      expect(
        a.farmAction(
          p.id,
          "plant",
          id,
          `${id}:plant`,
          p.point,
          () => true,
          200,
        ),
      ).toBe(true);
      expect(
        a.farmAction(
          p.id,
          "water",
          undefined,
          `${id}:water`,
          p.point,
          () => true,
          300,
        ),
      ).toBe(true);
      expect(
        a.farmAction(
          p.id,
          "harvest",
          undefined,
          `${id}:early`,
          p.point,
          () => true,
          301,
        ),
      ).toBe(false);
    }
    const restored = new QuestManager(store);
    for (const [id, index] of [
      ["radish", 0],
      ["scallion", 1],
      ["carrot", 2],
    ] as const) {
      const p = plots[index];
      expect(
        restored.farmAction(
          p.id,
          "harvest",
          undefined,
          `${id}:harvest`,
          p.point,
          () => true,
          500000,
        ),
      ).toBe(true);
      expect(
        restored.farmAction(
          p.id,
          "harvest",
          undefined,
          `${id}:again`,
          p.point,
          () => true,
          500001,
        ),
      ).toBe(false);
      expect(restored.snapshot().inventory[id]).toBe(crops[id].yield);
    }
    expect(
      Object.values(restored.snapshot().economy.plots).filter((p) => p.crop),
    ).toHaveLength(0);
  });
  it("rejects corrupt growth-speed saves without overwriting original", () => {
    const { store, manager } = fixture();
    const v = manager.snapshot();
    v.economy.plots[plots[0].id] = {
      stage: "watered",
      cycle: 1,
      crop: "radish",
      plantedAt: 100,
      wateredAt: 200,
      growMs: 1,
    };
    const raw = JSON.stringify(v);
    store.map.set(QUEST_STORAGE_KEY, raw);
    expect(new QuestManager(store).storageWarning).toBeTruthy();
    expect(store.getItem(QUEST_STORAGE_KEY)).toBe(raw);
  });
  it("bounded starter recovery cannot repeat or mint crops/coins", () => {
    const { manager } = fixture();
    expect(manager.recoverStarter()).toBe(true);
    expect(manager.recoverStarter()).toBe(false);
    expect(manager.snapshot().coins).toBe(100);
    expect(manager.snapshot().inventory["seed-radish"]).toBe(1);
  });
  it("eight physical first-delivery steps ordered, through-wall and receipt replay denied", () => {
    const { manager: m } = fixture(["farm-first-seed-v1"]);
    expect(m.accept("town-first-delivery-v2", "npc-eunji")).toBe(true);
    const q = quests.find((x) => x.id === "town-first-delivery-v2")!;
    expect(
      m.interiorEvent(
        "repair",
        "workshop",
        "wrong:order",
        [320, 300],
        [320, 300],
        () => true,
      ),
    ).toBe(false);
    for (const [o, i] of q.economyObjectives!.map((o, i) => [o, i] as const)) {
      expect(
        m.interiorEvent(
          o.event,
          o.item!,
          `wall:${i}`,
          [320, 300],
          [321, 300],
          () => false,
        ),
      ).toBe(false);
      expect(
        m.interiorEvent(
          o.event,
          o.item!,
          `story:${i}`,
          [320, 300],
          [320, 300],
          () => true,
        ),
      ).toBe(true);
      expect(
        m.interiorEvent(
          o.event,
          o.item!,
          `story:${i}`,
          [320, 300],
          [320, 300],
          () => true,
        ),
      ).toBe(false);
    }
    expect(m.snapshot().records[q.id].step).toBe(8);
    expect(m.returnToNPC(q.id, "npc-jiho")).toBe(true);
    const question = m.question(q.id)!;
    expect(m.answer(q.id, question.id, (question.correct + 1) % 3).result).toBe(
      "incorrect",
    );
    expect(m.question(q.id)!.id).not.toBe(question.id);
    const next = m.question(q.id)!;
    expect(m.answer(q.id, next.id, next.correct).result).toBe("correct");
    expect(m.answer(q.id, next.id, next.correct).result).toBe("invalid");
    expect(m.snapshot().coins).toBe(136);
  });
  it("backs up pre-upgrade saves and restores validated progress without replacing the corrupt original silently", () => {
    const s = storage(),
      old = new QuestManager(s).snapshot();
    delete old.economy.stock["seed-carrot"];
    const raw = JSON.stringify(old);
    s.map.set(QUEST_STORAGE_KEY, raw);
    const m = new QuestManager(s);
    expect(s.getItem(QUEST_STORAGE_KEY + ":backup:roadmap-v2")).toBe(null);
    expect(m.accept("farm-first-seed-v1", "npc-cheolsu")).toBe(true);
    expect(s.getItem(QUEST_STORAGE_KEY + ":backup:roadmap-v2")).toBe(raw);
    s.map.set(QUEST_STORAGE_KEY, "{broken");
    const broken = new QuestManager(s);
    expect(broken.storageWarning).toBeTruthy();
    expect(broken.restoreMigrationBackup()).toBe(true);
    expect(s.getItem(QUEST_STORAGE_KEY + ":corrupt-backup:roadmap-v2")).toBe(
      "{broken",
    );
    expect(broken.snapshot().coins).toBe(old.coins);
  });
  it("does not resume a room from coercible string coordinates or corrupt local positions", () => {
    const s = storage();
    vi.stubGlobal("localStorage", s);
    try {
      s.setItem(
        INTERIOR_SAVE,
        JSON.stringify({
          version: 1,
          id: "seed-shop",
          world: [717, 2605],
          position: ["320", "414"],
        }),
      );
      expect(readInterior()).toBeUndefined();
      s.setItem(
        INTERIOR_SAVE,
        JSON.stringify({
          version: 1,
          id: "seed-shop",
          world: [717, 2605],
          position: [320, 414],
        }),
      );
      expect(readInterior()?.position).toEqual([320, 414]);
    } finally {
      vi.unstubAllGlobals();
    }
  });
  it("three registered canonical entrances, safe spawn and bounded solid counters", () => {
    expect(interiors).toHaveLength(3);
    expect(new Set(interiors.map((x) => x.buildingId)).size).toBe(3);
    expect(roomWalkable(...ROOM.spawn)).toBe(true);
    expect(roomWalkable(...ROOM.actor)).toBe(true);
    expect(roomWalkable(300, 200)).toBe(false);
    expect(roomWalkable(0, 0)).toBe(false);
    for (const p of [ROOM.fragment, ROOM.sign, ROOM.courier, ROOM.exit])
      expect(roomWalkable(p[0], p[1])).toBe(true);
  });
  it("live adapters disabled, local simulation explicit; speed/replay/rate limits enforced", async () => {
    expect(Object.values(LIVE_FEATURES).every((x) => x === false)).toBe(true);
    expect(await noAds.show(true)).toEqual({ status: "disabled", granted: 0 });
    expect(await disabledRoom.join()).toEqual({
      status: "disabled",
      actors: [],
    });
    const r = new LocalRoomSimulation();
    expect((await r.join()).status).toBe("local-simulation");
    expect(r.move("TEST_ACTOR_A", 10, 10, 100)).toBe(true);
    expect(r.move("TEST_ACTOR_A", 3000, 3000, 200)).toBe(false);
    expect(r.move("TEST_ACTOR_A", 11, 10, 110)).toBe(false);
    expect(r.cosmeticReceipt("test:reward")).toBe(true);
    expect(r.cosmeticReceipt("test:reward")).toBe(false);
  });
});
