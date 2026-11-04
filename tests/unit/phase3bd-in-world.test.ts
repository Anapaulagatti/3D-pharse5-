import { describe, it, expect } from "vitest";
import {
  QuestManager,
  QUEST_STORAGE_KEY,
  type InteractionContext,
} from "../../src/quests/manager";
import { plots, ready } from "../../src/economy/catalog";
import { plotPresentation } from "../../src/economy/presentation";
const store = () => {
  const data = new Map<string, string>();
  return {
    data,
    getItem: (k: string) => data.get(k) ?? null,
    setItem: (k: string, v: string) => {
      data.set(k, v);
    },
  };
};
const farm = "farm-first-seed-v1",
  plot = plots[3],
  ctx: InteractionContext = {
    npcId: "npc-cheolsu",
    player: [500, 850],
    actor: [500, 810],
    ground: () => true,
  };
describe("physical world interactions reuse the atomic quest/economy ledger", () => {
  it("runs actual planting/watering/growing/harvest, validates NPC range and rewards once after a different retry question", () => {
    const s = store(),
      m = new QuestManager(s);
    expect(m.acceptInWorld(farm, ctx.npcId, { ...ctx, player: [0, 0] })).toBe(
      false,
    );
    expect(m.acceptInWorld(farm, ctx.npcId, ctx)).toBe(true);
    expect(m.snapshot().inventory["seed-radish"]).toBe(1);
    expect(
      m.farmAction(
        plot.id,
        "plant",
        "radish",
        "real:plant",
        plot.point,
        () => true,
        1000,
      ),
    ).toBe(true);
    expect(m.snapshot().records[farm].step).toBe(1);
    expect(m.snapshot().inventory["seed-radish"]).toBe(0);
    expect(
      m.farmAction(
        plot.id,
        "water",
        undefined,
        "real:water",
        plot.point,
        () => true,
        1100,
      ),
    ).toBe(true);
    expect(plotPresentation(m.snapshot().economy.plots[plot.id], 3000)).toBe(
      "GROWING",
    );
    expect(
      m.farmAction(
        plot.id,
        "harvest",
        undefined,
        "too:soon",
        plot.point,
        () => true,
        3000,
      ),
    ).toBe(false);
    const loaded = new QuestManager(s);
    expect(
      loaded.farmAction(
        plot.id,
        "harvest",
        undefined,
        "real:harvest",
        plot.point,
        () => true,
        7100,
      ),
    ).toBe(true);
    expect(loaded.snapshot().records[farm].step).toBe(3);
    expect(loaded.snapshot().inventory.radish).toBe(2);
    expect(
      loaded.farmAction(
        plot.id,
        "harvest",
        undefined,
        "repeat:harvest",
        plot.point,
        () => true,
        7100,
      ),
    ).toBe(false);
    expect(
      loaded.returnInWorld(farm, ctx.npcId, { ...ctx, ground: () => false }),
    ).toBe(false);
    expect(loaded.returnInWorld(farm, ctx.npcId, ctx)).toBe(true);
    const q = loaded.question(farm)!;
    expect(
      loaded.answerInWorld(farm, q.id, q.correct, { ...ctx, player: [0, 0] })
        .result,
    ).toBe("invalid");
    expect(
      loaded.answerInWorld(farm, q.id, (q.correct + 1) % q.options.length, ctx)
        .result,
    ).toBe("incorrect");
    const next = loaded.question(farm)!;
    expect(next.id).not.toBe(q.id);
    expect(next.difficulty).toBe(q.difficulty);
    expect(loaded.snapshot().coins).toBe(0);
    expect(loaded.answerInWorld(farm, next.id, next.correct, ctx).result).toBe(
      "correct",
    );
    const final = new QuestManager(s);
    expect(final.snapshot().coins).toBe(20);
    expect(final.snapshot().xp).toBe(20);
    expect(final.snapshot().inventory["seed-radish"]).toBe(2);
    expect(final.answerInWorld(farm, next.id, next.correct, ctx).result).toBe(
      "invalid",
    );
  });
  it("migrates old completed tray receipts and seeds additively without read-only storage rewrite or repeated rewards", () => {
    const s = store(),
      v = new QuestManager().snapshot();
    delete v.economy.interactionSchema;
    v.inventory = { seed: 2 };
    v.coins = 20;
    v.records[farm] = { status: "completed", step: 4, attempts: 1 };
    v.transactions = [`quest:${farm}:base`];
    const raw = JSON.stringify(v);
    s.setItem(QUEST_STORAGE_KEY, raw);
    const m = new QuestManager(s);
    expect(m.storageWarning).toBe("");
    expect(m.snapshot().records[farm].status).toBe("completed");
    expect(m.snapshot().records[farm].step).toBe(3);
    expect(m.snapshot().inventory["seed-radish"]).toBe(2);
    expect(m.snapshot().coins).toBe(20);
    expect(s.getItem(QUEST_STORAGE_KEY)).toBe(raw);
    expect(m.accept(farm, ctx.npcId)).toBe(false);
  });
  it("explicitly restarts unfinished tray objectives but preserves unrelated wallet; growth starts only when watered", () => {
    const s = store(),
      v = new QuestManager().snapshot();
    delete v.economy.interactionSchema;
    v.records[farm] = { status: "challenge", step: 4, attempts: 0 };
    v.coins = 37;
    s.setItem(QUEST_STORAGE_KEY, JSON.stringify(v));
    const m = new QuestManager(s);
    expect(m.migrationNotice).toContain("luống thật");
    expect(m.snapshot().records[farm]).toMatchObject({
      status: "active",
      step: 0,
    });
    expect(m.snapshot().inventory["seed-radish"]).toBe(1);
    expect(m.snapshot().coins).toBe(37);
    expect(
      m.farmAction(
        plot.id,
        "plant",
        "radish",
        "new:plant",
        plot.point,
        () => true,
        1000,
      ),
    ).toBe(true);
    expect(ready(m.snapshot().economy.plots[plot.id], 900000)).toBe(false);
  });
  it("rolls back implicit till, seed consumption and quest progression together on storage failure", () => {
    const s = store(),
      m = new QuestManager(s);
    expect(m.acceptInWorld(farm, ctx.npcId, ctx)).toBe(true);
    const before = m.snapshot();
    s.setItem = () => {
      throw Error("quota");
    };
    expect(
      m.farmAction(
        plot.id,
        "plant",
        "radish",
        "bad:quota",
        plot.point,
        () => true,
        1000,
      ),
    ).toBe(false);
    expect(m.snapshot()).toEqual(before);
  });
  it("collects3distinct real orchard objects in any order; refuses remote/replay and requires actual return clearance", () => {
    const m = new QuestManager();
    expect(m.accept("jeju-orchard-v1", "npc-harin")).toBe(true);
    for (const [id, x, y] of [
      ["fruit-c", 3960, 4080],
      ["fruit-a", 3900, 4070],
      ["fruit-b", 3930, 4080],
    ] as const) {
      expect(m.worldAction("jeju-orchard-v1", id, [0, 0], () => true)).toBe(
        false,
      );
      expect(m.worldAction("jeju-orchard-v1", id, [x, y], () => true)).toBe(
        true,
      );
      expect(m.worldAction("jeju-orchard-v1", id, [x, y], () => true)).toBe(
        false,
      );
    }
    expect(m.snapshot().inventory.tangerine).toBe(3);
    const c: InteractionContext = {
      npcId: "npc-harin",
      player: [3740, 4070],
      actor: [3740, 4082],
      ground: () => true,
    };
    expect(
      m.returnInWorld("jeju-orchard-v1", c.npcId, {
        ...c,
        ground: () => false,
      }),
    ).toBe(false);
    expect(m.returnInWorld("jeju-orchard-v1", c.npcId, c)).toBe(true);
    expect(m.snapshot().inventory.tangerine).toBe(0);
  });
});
