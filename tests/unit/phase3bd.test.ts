import { describe, it, expect } from "vitest";
import { QuestManager, QUEST_STORAGE_KEY } from "../../src/quests/manager";
import { crops, plots, ready, ECONOMY } from "../../src/economy/catalog";
const store = () => {
  const m = new Map<string, string>();
  return {
    getItem: (k: string) => m.get(k) ?? null,
    setItem: (k: string, v: string) => {
      m.set(k, v);
    },
    m,
  };
};
const shop = {
  npcId: "npc-minseo",
  player: [650, 2660] as const,
  actor: [650, 2620] as const,
  ground: () => true,
};
const plot = plots[0];
function funded(coins = 100, inventory: Record<string, number> = {}) {
  const s = store(),
    m = new QuestManager(s),
    v = m.snapshot();
  v.coins = coins;
  v.inventory = inventory;
  s.setItem(QUEST_STORAGE_KEY, JSON.stringify(v));
  return { s, m: new QuestManager(s) };
}
function grow(
  m: QuestManager,
  crop: "radish" | "scallion",
  prefix: string,
  now = 1000,
) {
  expect(
    m.farmAction(
      plot.id,
      "till",
      undefined,
      prefix + ":t",
      plot.point,
      () => true,
      now,
    ),
  ).toBe(true);
  expect(
    m.farmAction(
      plot.id,
      "plant",
      crop,
      prefix + ":p",
      plot.point,
      () => true,
      now,
    ),
  ).toBe(true);
  expect(
    m.farmAction(
      plot.id,
      "water",
      undefined,
      prefix + ":w",
      plot.point,
      () => true,
      now,
    ),
  ).toBe(true);
}
describe("atomic local farming/shop ledger", () => {
  it.each([0, -1, 1.5, NaN, Infinity, 100])(
    "rejects invalid quantity %s without wallet/stock/receipt mutations",
    (q) => {
      const { m } = funded();
      const before = m.snapshot();
      expect(m.trade("buy", "seed-radish", q, "bad:quantity", shop)).toBe(
        false,
      );
      expect(m.snapshot()).toEqual(before);
    },
  );
  it("buys and sells with exact accounting, persists and rejects replay", () => {
    const { s, m } = funded();
    expect(m.trade("buy", "seed-radish", 2, "buy:1", shop)).toBe(true);
    expect(m.snapshot().coins).toBe(92);
    expect(m.snapshot().inventory["seed-radish"]).toBe(2);
    expect(m.snapshot().economy.stock["seed-radish"]).toBe(48);
    expect(m.trade("buy", "seed-radish", 2, "buy:1", shop)).toBe(false);
    const r = new QuestManager(s);
    expect(r.snapshot()).toEqual(m.snapshot());
    expect(r.trade("sell", "seed-radish", 1, "seed:arbitrage", shop)).toBe(
      false,
    );
  });
  it("refuses insufficient coins, missing produce, invalid shop context and stock exhaustion", () => {
    const { m } = funded(0);
    expect(m.trade("buy", "seed-radish", 1, "no:funds", shop)).toBe(false);
    expect(m.trade("sell", "radish", 1, "no:produce", shop)).toBe(false);
    expect(
      m.trade("buy", "seed-radish", 1, "wrong:npc", {
        ...shop,
        npcId: "npc-jiho",
      }),
    ).toBe(false);
    const r = funded(1000).m;
    expect(r.trade("buy", "seed-radish", 51, "no:stock", shop)).toBe(false);
    expect(
      r.trade("buy", "seed-radish", 1, "no:remote", {
        ...shop,
        player: [0, 0],
      }),
    ).toBe(false);
  });
  it("preserves whole transaction on full inventory/stack and quota failure", () => {
    const inv = Object.fromEntries(
      Array.from({ length: ECONOMY.slots }, (_, i) => ["legacy-" + i, 1]),
    );
    const { m } = funded(100, inv),
      before = m.snapshot();
    expect(m.trade("buy", "seed-radish", 1, "full:bag", shop)).toBe(false);
    expect(m.snapshot()).toEqual(before);
    const full = funded(100, { "seed-radish": 99 }).m;
    expect(full.trade("buy", "seed-radish", 1, "full:stack", shop)).toBe(false);
    const bad = new QuestManager({
      getItem: () => null,
      setItem: () => {
        throw Error("quota");
      },
    });
    expect(bad.accept("farm-radish-harvest-v1", "npc-nayeon")).toBe(false);
    expect(bad.snapshot().inventory).toEqual({});
  });
  it("twenty simultaneous duplicate UI requests consume funds exactly once", async () => {
    const { m } = funded();
    const r = await Promise.all(
      Array.from({ length: 20 }, () =>
        Promise.resolve(m.trade("buy", "seed-radish", 1, "same:request", shop)),
      ),
    );
    expect(r.filter(Boolean)).toHaveLength(1);
    expect(m.snapshot().coins).toBe(96);
    expect(m.snapshot().transactions).toEqual(["trade:same:request"]);
  });
  it.each(["radish", "scallion"] as const)(
    "%s persists growth and harvests only once after genuine elapsed time",
    (crop) => {
      const { s, m } = funded(100, { [crops[crop].seed]: 1 });
      grow(m, crop, crop);
      expect(
        m.farmAction(
          plot.id,
          "harvest",
          undefined,
          "early:crop",
          plot.point,
          () => true,
          1000,
        ),
      ).toBe(false);
      const r = new QuestManager(s);
      expect(ready(r.snapshot().economy.plots[plot.id], 999)).toBe(false);
      const when = 1000 + crops[crop].growMs;
      expect(
        r.farmAction(
          plot.id,
          "harvest",
          undefined,
          "harvest:" + crop,
          plot.point,
          () => true,
          when,
        ),
      ).toBe(true);
      expect(r.snapshot().inventory[crop]).toBe(crops[crop].yield);
      expect(
        r.farmAction(
          plot.id,
          "harvest",
          undefined,
          "harvest:duplicate",
          plot.point,
          () => true,
          when + 1,
        ),
      ).toBe(false);
      expect(r.trade("sell", crop, 1, "sell:" + crop, shop)).toBe(true);
      expect(r.snapshot().coins).toBe(103);
    },
  );
  it("never plants/harvests remotely or through walls and rolls back a full-bag harvest", () => {
    const { m } = funded(100, { "seed-radish": 1 });
    expect(
      m.farmAction(
        "fake",
        "till",
        undefined,
        "fake:plot",
        plot.point,
        () => true,
      ),
    ).toBe(false);
    expect(
      m.farmAction(plot.id, "till", undefined, "far:plot", [0, 0], () => true),
    ).toBe(false);
    expect(
      m.farmAction(
        plot.id,
        "till",
        undefined,
        "wall:plot",
        plot.point,
        () => false,
      ),
    ).toBe(false);
    grow(m, "radish", "real");
    const v = m.snapshot();
    v.inventory = Object.fromEntries(
      Array.from({ length: 12 }, (_, i) => ["legacy" + i, 1]),
    );
    const s = store();
    s.setItem(QUEST_STORAGE_KEY, JSON.stringify(v));
    const r = new QuestManager(s),
      before = r.snapshot();
    expect(
      r.farmAction(
        plot.id,
        "harvest",
        undefined,
        "full:harvest",
        plot.point,
        () => true,
        100000,
      ),
    ).toBe(false);
    expect(r.snapshot()).toEqual(before);
  });
  it("migrates only additive economy fields and leaves old player/progress/saves intact", () => {
    const s = store();
    s.setItem("player", "KEEP");
    const value = {
      schemaVersion: 1,
      records: {},
      inventory: { seed: 2 },
      coins: 25,
      xp: 10,
      transactions: [],
    };
    s.setItem(QUEST_STORAGE_KEY, JSON.stringify(value));
    const before = s.getItem(QUEST_STORAGE_KEY);
    const m = new QuestManager(s);
    expect(m.snapshot().coins).toBe(25);
    expect(m.snapshot().economy.plots).toHaveProperty(plot.id);
    expect(s.getItem(QUEST_STORAGE_KEY)).toBe(before);
    expect(s.getItem("player")).toBe("KEEP");
  });
  it("advances two new actual economy quests only on valid activity events, with Korean gating and finite intro boost", () => {
    const { s, m } = funded();
    expect(m.accept("farm-radish-harvest-v1", "npc-nayeon")).toBe(true);
    expect(
      m.worldAction("farm-radish-harvest-v1", "till", plot.point, () => true),
    ).toBe(false);
    grow(m, "radish", "tutorial", 1000);
    expect(m.snapshot().economy.plots[plot.id].growMs).toBe(6000);
    expect(
      m.farmAction(
        plot.id,
        "harvest",
        undefined,
        "tutorial:h",
        plot.point,
        () => true,
        7000,
      ),
    ).toBe(true);
    expect(m.snapshot().records["farm-radish-harvest-v1"].step).toBe(4);
    expect(m.returnToNPC("farm-radish-harvest-v1", "npc-nayeon")).toBe(true);
    const q = m.question("farm-radish-harvest-v1")!;
    expect(m.answer("farm-radish-harvest-v1", q.id, 0).result).toBe(
      "incorrect",
    );
    expect(m.question("farm-radish-harvest-v1")!.id).not.toBe(q.id);
    const q2 = m.question("farm-radish-harvest-v1")!;
    expect(m.answer("farm-radish-harvest-v1", q2.id, q2.correct).result).toBe(
      "correct",
    );
    expect(m.accept("shop-garden-market-v1", "npc-minseo")).toBe(true);
    expect(m.trade("buy", "seed-scallion", 1, "market:buy", shop)).toBe(true);
    grow(m, "scallion", "market", 2000);
    expect(m.snapshot().economy.plots[plot.id].growMs).toBe(10000);
    expect(
      m.farmAction(
        plot.id,
        "harvest",
        undefined,
        "market:h",
        plot.point,
        () => true,
        12000,
      ),
    ).toBe(true);
    expect(m.trade("sell", "scallion", 1, "market:sell", shop)).toBe(true);
    expect(m.returnToNPC("shop-garden-market-v1", "npc-minseo")).toBe(true);
    const question = m.question("shop-garden-market-v1")!;
    expect(
      m.answer("shop-garden-market-v1", question.id, question.correct).result,
    ).toBe("correct");
    const r = new QuestManager(s);
    expect(r.snapshot()).toEqual(m.snapshot());
    expect(
      r.answer("shop-garden-market-v1", question.id, question.correct).result,
    ).toBe("invalid");
  });
});
