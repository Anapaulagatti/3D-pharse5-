import { describe, it, expect } from "vitest";
import { plots, beds, freshEconomy } from "../../src/economy/catalog";
import { QuestManager, QUEST_STORAGE_KEY } from "../../src/quests/manager";
import { repairedHanokPassage } from "../../src/gate3/Accessibility";
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
describe("independent farm cells with legacy compatibility", () => {
  it("retains six IDs and stable points, provides36unique cells in6approved beds", () => {
    expect(beds).toHaveLength(6);
    expect(plots).toHaveLength(36);
    expect(new Set(plots.map((p) => p.id)).size).toBe(36);
    expect(plots.slice(0, 6).map((p) => p.id)).toEqual(
      Array.from({ length: 6 }, (_, i) => `NW-FARM-0${i + 1}`),
    );
    expect(plots[3].point).toEqual([470, 669]);
    for (const bed of beds)
      expect(plots.filter((p) => p.bedId === bed.id)).toHaveLength(6);
  });
  it("migrates old six states without cloning crops, changing money/progress or writing on read", () => {
    const s = store(),
      m = new QuestManager(s),
      v = m.snapshot();
    v.inventory = { "seed-radish": 3 };
    v.coins = 37;
    delete v.economy.farmCellSchema;
    for (const p of plots.slice(6)) delete v.economy.plots[p.id];
    v.economy.plots[plots[3].id] = {
      stage: "watered",
      cycle: 2,
      crop: "radish",
      plantedAt: 1000,
      wateredAt: 1100,
      growMs: 45000,
    };
    const raw = JSON.stringify(v);
    s.data.set(QUEST_STORAGE_KEY, raw);
    const loaded = new QuestManager(s).snapshot();
    expect(loaded.coins).toBe(37);
    expect(loaded.economy.plots[plots[3].id]).toEqual(
      v.economy.plots[plots[3].id],
    );
    expect(
      Object.values(loaded.economy.plots).filter((p) => p.crop),
    ).toHaveLength(1);
    expect(s.data.get(QUEST_STORAGE_KEY)).toBe(raw);
  });
  it("prepares and plants one cell only, spends once and cannot double harvest", () => {
    const s = store(),
      m = new QuestManager(s);
    const v = m.snapshot();
    v.inventory = { "seed-radish": 2 };
    s.data.set(QUEST_STORAGE_KEY, JSON.stringify(v));
    const a = new QuestManager(s),
      p = plots[3],
      other = plots.find((x) => x.bedId === p.bedId && x.id !== p.id)!;
    expect(
      a.farmAction(
        p.id,
        "till",
        undefined,
        "test:till",
        p.point,
        () => true,
        100,
      ),
    ).toBe(true);
    expect(a.snapshot().inventory["seed-radish"]).toBe(2);
    expect(
      a.farmAction(
        p.id,
        "plant",
        "radish",
        "test:plant",
        p.point,
        () => true,
        200,
      ),
    ).toBe(true);
    expect(
      a.farmAction(
        p.id,
        "plant",
        "radish",
        "test:plant",
        p.point,
        () => true,
        200,
      ),
    ).toBe(false);
    expect(a.snapshot().economy.plots[other.id].stage).toBe("empty");
    expect(
      a.farmAction(
        p.id,
        "water",
        undefined,
        "test:water",
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
        "test:harvest",
        p.point,
        () => true,
        45300,
      ),
    ).toBe(true);
    expect(
      a.farmAction(
        p.id,
        "harvest",
        undefined,
        "test:harvest2",
        p.point,
        () => true,
        45301,
      ),
    ).toBe(false);
    expect(a.snapshot().inventory.radish).toBe(2);
    expect(new QuestManager(s).snapshot()).toEqual(a.snapshot());
  });
});
describe("western hanok minimal anchor correction", () => {
  it("opens only the verified stone centre and preserves both sides", () => {
    for (const y of [1094, 1200, 1377])
      expect(repairedHanokPassage(534, y)).toBe(true);
    for (const p of [
      [519, 1200],
      [554, 1200],
      [600, 1200],
      [534, 1093],
      [534, 1378],
    ])
      expect(repairedHanokPassage(...(p as [number, number]))).toBe(false);
    expect(freshEconomy().plots).toHaveProperty("NW-FARM-04");
  });
});
