import { describe, expect, it } from "vitest";
import {
  hangulQuestions,
  isCorrectHangul,
  normalizeHangulAnswer,
} from "../../src/quests/learning";
import { translationQuestions } from "../../src/quests/translations";
import { PracticeProgress } from "../../src/quests/PracticeProgress";
import { QuestManager, QUEST_STORAGE_KEY } from "../../src/quests/manager";
import { freshEconomy } from "../../src/economy/catalog";
const memory = () => {
  const m = new Map<string, string>();
  return {
    getItem: (k: string) => m.get(k) ?? null,
    setItem: (k: string, v: string) => m.set(k, v),
  };
};
function challenge() {
  const store = memory();
  store.setItem(
    QUEST_STORAGE_KEY,
    JSON.stringify({
      schemaVersion: 1,
      records: {
        "farm-first-seed-v1": { status: "challenge", step: 3, attempts: 0 },
      },
      inventory: {},
      coins: 0,
      xp: 0,
      transactions: [],
      economy: freshEconomy(),
    }),
  );
  return new QuestManager(store);
}
describe("V4 Hangul assessment direction and local rights/content contracts", () => {
  it("36 unique original items span4topics/3grades; every assessment answer isHangul and not claimed human approved", () => {
    expect(hangulQuestions).toHaveLength(36);
    expect(new Set(hangulQuestions.map((q) => q.id)).size).toBe(36);
    for (const q of hangulQuestions) {
      expect(q.direction).toBe("vi-ko");
      expect(q.answerLanguage).toBe("ko");
      expect(q.review).toBe("PENDING_HUMAN_REVIEW");
      expect(q.choiceIds.length).toBe(q.options.length);
      expect(q.distractorRationale.length).toBe(q.options.length);
      expect(new Set(q.options.map(normalizeHangulAnswer)).size).toBe(
        q.options.length,
      );
      expect(
        q.options.every(
          (v) => /\p{Script=Hangul}/u.test(v) && !/[A-Za-z]/.test(v),
        ),
      ).toBe(true);
      expect(isCorrectHangul(q, q.options[q.correct])).toBe(true);
    }
    for (const topic of ["farm", "shop", "delivery", "orchard"])
      for (const grade of ["alphabet", "basic", "intermediate"])
        expect(
          hangulQuestions.filter((q) => q.topic === topic && q.grade === grade),
        ).toHaveLength(3);
  });
  it("retains12 explicitly separate Korean→Vietnamese translation items without leaking into assessment pools", () => {
    const rows = Object.values(translationQuestions).flat();
    expect(rows).toHaveLength(12);
    expect(
      rows.every(
        (q) =>
          q.direction === "ko-vi" &&
          q.answerLanguage === "vi" &&
          q.id.startsWith("translation:"),
      ),
    ).toBe(true);
  });
  it("NFC/NFD, whitespace and optional terminal punctuation accept the same valid Hangul; Latin or wrong syllables do not", () => {
    const q = hangulQuestions.find((q) => q.id === "farm-1")!;
    expect(isCorrectHangul(q, q.options[q.correct].normalize("NFD"))).toBe(
      true,
    );
    expect(isCorrectHangul(q, "  씨앗을   심어요 ！ ")).toBe(true);
    expect(isCorrectHangul(q, "gieo hạt")).toBe(false);
    expect(isCorrectHangul(q, "씨앗을 팔아요.")).toBe(false);
  });
  it("wrongtyped answer preserves coins/inventory and retries atsamegrade; correctNFD awards once and replay is rejected", () => {
    const m = challenge(),
      id = "farm-first-seed-v1",
      first = m.question(id)!;
    expect(m.answerText(id, first.id, "gieo hạt").result).toBe("incorrect");
    const second = m.question(id)!;
    expect(second.id).not.toBe(first.id);
    expect(second.grade).toBe(first.grade);
    expect(m.snapshot().coins).toBe(0);
    expect(
      m.answerText(
        id,
        second.id,
        second.options[second.correct].normalize("NFD"),
      ).result,
    ).toBe("correct");
    expect(m.snapshot().coins).toBe(20);
    expect(m.snapshot().inventory["seed-radish"]).toBe(2);
    expect(
      m.answerText(id, second.id, second.options[second.correct]).result,
    ).toBe("invalid");
    expect(m.snapshot().coins).toBe(20);
  });
  it("typedquest response still requires genuine NPC interaction range", () => {
    const m = challenge(),
      id = "farm-first-seed-v1",
      q = m.question(id)!;
    expect(
      m.answerTextInWorld(id, q.id, q.options[q.correct], {
        npcId: "npc-cheolsu",
        player: [1000, 1000],
        actor: [500, 810],
        ground: () => true,
      }).result,
    ).toBe("invalid");
    expect(m.snapshot().coins).toBe(0);
  });
  it("practice persists bounded history withdirection but cannot mutatequest/currency/player stores", () => {
    const s = memory();
    s.setItem(QUEST_STORAGE_KEY, "PROTECTED");
    const practice = new PracticeProgress(s),
      q = hangulQuestions[0];
    for (let i = 0; i < 120; i++) practice.answer(q, q.correct);
    expect(practice.snapshot()).toHaveLength(100);
    expect(new PracticeProgress(s).snapshot()).toHaveLength(100);
    expect(s.getItem(QUEST_STORAGE_KEY)).toBe("PROTECTED");
    expect(
      practice
        .snapshot()
        .every((x) => x.direction === "vi-ko" && x.mode === "choice"),
    ).toBe(true);
  });
});
