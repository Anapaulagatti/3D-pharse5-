import { describe, it, expect } from "vitest";
import {
  QuestManager,
  QUEST_STORAGE_KEY,
  disabledRewardedAds,
} from "../../src/quests/manager";
import { quests } from "../../src/quests/content";
import {
  compatibleItems,
  normalizeAppearance,
  retiredHairAccessories,
} from "../../src/characters/appearance";
import { characterRegistry } from "../../src/characters/registry";
import {
  repairedEntrance,
  entranceRepairs,
} from "../../src/gate3/Accessibility";
const memory = () => {
  const data = new Map<string, string>();
  return {
    getItem: (k: string) => data.get(k) ?? null,
    setItem: (k: string, v: string) => {
      data.set(k, v);
    },
    data,
  };
};
describe("Phase3BC quest transactions", () => {
  it.each(quests.map((q) => [q.id, q]))(
    "%s requires real objectives, contextual return and Korean answer; reload cannot duplicate reward",
    (_id, def) => {
      const storage = memory(),
        m = new QuestManager(storage);
      expect(m.accept(def.id, "npc-not-giver")).toBe(false);
      expect(m.accept(def.id, def.giver)).toBe(true);
      expect(m.accept(def.id, def.giver)).toBe(false);
      expect(m.answer(def.id, "unknown", 0).result).toBe("invalid");
      for (const step of def.steps) {
        expect(m.worldAction(def.id, step.id, [0, 0], () => true)).toBe(false);
        expect(m.worldAction(def.id, step.id, step.point, () => false)).toBe(
          false,
        );
        expect(m.worldAction(def.id, step.id, step.point, () => true)).toBe(
          true,
        );
        expect(m.worldAction(def.id, step.id, step.point, () => true)).toBe(
          false,
        );
      }
      expect(m.returnToNPC(def.id, "npc-wrong")).toBe(false);
      expect(m.returnToNPC(def.id, def.recipient ?? def.giver)).toBe(true);
      const q = m.question(def.id)!;
      expect(
        m.answer(def.id, q.id, (q.correct + 1) % q.options.length).result,
      ).toBe("incorrect");
      expect(m.question(def.id)!.id).not.toBe(q.id);
      expect(m.question(def.id)!.difficulty).toBe(q.difficulty);
      expect(m.snapshot().coins).toBe(0);
      const restored = new QuestManager(storage),
        next = restored.question(def.id)!;
      expect(next.id).toBe(m.question(def.id)!.id);
      expect(restored.answer(def.id, next.id, next.correct).result).toBe(
        "correct",
      );
      const final = new QuestManager(storage);
      expect(final.snapshot().coins).toBe(def.reward.coins);
      expect(final.answer(def.id, next.id, next.correct).result).toBe(
        "invalid",
      );
      expect(final.snapshot().transactions).toEqual([`quest:${def.id}:base`]);
      expect(final.snapshot().xp).toBe(def.reward.xp);
    },
  );
  it("does not reset unrelated preferences, world checkpoint or invalid raw save", () => {
    const storage = memory();
    storage.setItem("world", "protected");
    storage.setItem("korean-arena-player-preferences-v1", "legacy");
    storage.setItem(QUEST_STORAGE_KEY, "{bad");
    const m = new QuestManager(storage);
    expect(m.accept(quests[0].id, quests[0].giver)).toBe(false);
    expect(storage.getItem(QUEST_STORAGE_KEY)).toBe("{bad");
    expect(storage.getItem("world")).toBe("protected");
  });
  it("refuses rewards when storage commit fails", () => {
    const m = new QuestManager({
      getItem: () => null,
      setItem: () => {
        throw Error("quota");
      },
    });
    expect(m.accept(quests[0].id, quests[0].giver)).toBe(false);
    expect(m.snapshot().coins).toBe(0);
  });
  it("has no real ads or mastery multiplication", async () => {
    expect(disabledRewardedAds.enabled).toBe(false);
    expect(await disabledRewardedAds.requestBonus("x")).toEqual({
      status: "disabled",
    });
  });
});
it("retires head accessories for every player and saved preset without removing other categories", () => {
  for (const def of characterRegistry.all) {
    const items = compatibleItems(def.id);
    expect(items.some((i) => retiredHairAccessories.has(i.id))).toBe(false);
    const look = normalizeAppearance(def.id, {
      schemaVersion: 2,
      characterId: def.id,
      hairstyleId: null,
      outfitId: null,
      accessoryIds: [...retiredHairAccessories],
    });
    expect(look.accessoryIds).toEqual([]);
  }
  expect(compatibleItems("juni").some((i) => i.category === "hairstyle")).toBe(
    true,
  );
});
it("opens only four documented paved entrance lanes and preserves footprints", () => {
  expect(entranceRepairs).toHaveLength(4);
  expect(repairedEntrance(717, 2595)).toBe(true);
  expect(repairedEntrance(717, 2589)).toBe(false);
  expect(repairedEntrance(2598, 2450)).toBe(false);
  expect(repairedEntrance(3500, 3610)).toBe(false);
});
