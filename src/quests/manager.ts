import {
  LocalLearningProgress,
  quests,
  type LearningProgressAdapter,
} from "./content";
export const QUEST_STORAGE_KEY = "korean-arena-quests-v1";
export type QuestStatus = "active" | "challenge" | "completed";
export interface QuestRecord {
  status: QuestStatus;
  step: number;
  attempts: number;
}
export interface QuestSave {
  schemaVersion: 1;
  records: Record<string, QuestRecord>;
  inventory: Record<string, number>;
  coins: number;
  xp: number;
  transactions: string[];
}
const fresh = (): QuestSave => ({
  schemaVersion: 1,
  records: {},
  inventory: {},
  coins: 0,
  xp: 0,
  transactions: [],
});
const integer = (v: unknown): v is number =>
  Number.isSafeInteger(v) && Number(v) >= 0 && Number(v) <= 1000000;
/** Local demo authority. Single atomic save contains progress AND reward receipts. No mastery/account claims. */
export class QuestManager {
  private value = fresh();
  storageWarning = "";
  constructor(
    private storage?: Pick<Storage, "getItem" | "setItem">,
    readonly learning: LearningProgressAdapter = new LocalLearningProgress(),
  ) {
    try {
      const raw = storage?.getItem(QUEST_STORAGE_KEY);
      if (!raw) return;
      const v = JSON.parse(raw) as QuestSave;
      if (
        v.schemaVersion !== 1 ||
        !integer(v.coins) ||
        !integer(v.xp) ||
        !v.records ||
        !v.inventory ||
        !Array.isArray(v.transactions)
      )
        throw Error("invalid");
      if (
        !Object.values(v.inventory).every(integer) ||
        v.transactions.some((t) => typeof t !== "string")
      )
        throw Error("invalid");
      for (const [id, record] of Object.entries(v.records)) {
        const def = quests.find((q) => q.id === id);
        if (
          !def ||
          !["active", "challenge", "completed"].includes(record.status) ||
          !integer(record.step) ||
          record.step > def.steps.length ||
          !integer(record.attempts)
        )
          throw Error("invalid");
        if (
          (record.status === "completed") !==
          v.transactions.includes(`quest:${id}:base`)
        )
          throw Error("invalid receipt");
      }
      this.value = v;
    } catch {
      this.storageWarning =
        "Dữ liệu nhiệm vụ không hợp lệ; dữ liệu gốc chưa bị ghi đè.";
    }
  }
  snapshot(): QuestSave {
    return structuredClone(this.value);
  }
  private commit(change: (next: QuestSave) => boolean) {
    if (this.storageWarning) return false;
    const next = this.snapshot();
    if (!change(next)) return false;
    try {
      this.storage?.setItem(QUEST_STORAGE_KEY, JSON.stringify(next));
    } catch {
      this.storageWarning =
        "Không lưu được nhiệm vụ. Chưa cấp phần thưởng; hãy kiểm tra bộ nhớ trình duyệt.";
      return false;
    }
    this.value = next;
    return true;
  }
  accept(id: string, npcId: string) {
    const def = quests.find((q) => q.id === id && q.giver === npcId);
    if (!def) return false;
    return this.commit((s) => {
      if (s.records[id]) return false;
      s.records[id] = { status: "active", step: 0, attempts: 0 };
      if (def.topic === "farm") s.inventory.seed = (s.inventory.seed ?? 0) + 1;
      if (def.recipient) s.inventory.parcel = (s.inventory.parcel ?? 0) + 1;
      return true;
    });
  }
  worldAction(
    id: string,
    action: string,
    position: readonly [number, number],
    ground: (x: number, y: number) => boolean,
  ) {
    const def = quests.find((q) => q.id === id),
      record = this.value.records[id];
    const step = def?.steps[record?.step ?? -1];
    if (
      !def ||
      !record ||
      record.status !== "active" ||
      !step ||
      step.id !== action ||
      Math.hypot(position[0] - step.point[0], position[1] - step.point[1]) > 30
    )
      return false;
    // Exact canonical floor samples; no through-wall or remote collection.
    for (let i = 0; i <= 30; i++)
      if (
        !ground(
          position[0] + ((step.point[0] - position[0]) * i) / 30,
          position[1] + ((step.point[1] - position[1]) * i) / 30,
        )
      )
        return false;
    return this.commit((s) => {
      if (def.topic === "farm" && action === "plant") {
        if (!(s.inventory.seed > 0)) return false;
        s.inventory.seed--;
      }
      if (def.topic === "orchard")
        s.inventory.tangerine = (s.inventory.tangerine ?? 0) + 1;
      s.records[id].step++;
      return true;
    });
  }
  returnToNPC(id: string, npcId: string) {
    const def = quests.find((q) => q.id === id),
      r = this.value.records[id];
    if (
      !def ||
      !r ||
      r.status !== "active" ||
      npcId !== (def.recipient ?? def.giver) ||
      r.step !== def.steps.length
    )
      return false;
    return this.commit((s) => {
      if (def.recipient) {
        if (!(s.inventory.parcel > 0)) return false;
        s.inventory.parcel--;
      }
      if (def.topic === "orchard") {
        if ((s.inventory.tangerine ?? 0) < 3) return false;
        s.inventory.tangerine -= 3;
      }
      s.records[id].status = "challenge";
      return true;
    });
  }
  question(id: string) {
    const def = quests.find((q) => q.id === id),
      r = this.value.records[id];
    const pool = def && this.learning.questions(def.topic);
    return r?.status === "challenge" && pool?.length
      ? pool[r.attempts % pool.length]
      : undefined;
  }
  answer(id: string, questionId: string, choice: number) {
    const q = this.question(id),
      def = quests.find((d) => d.id === id);
    if (
      !q ||
      !def ||
      q.id !== questionId ||
      !Number.isInteger(choice) ||
      choice < 0 ||
      choice >= q.options.length
    )
      return { result: "invalid", explanation: "Câu hỏi đã thay đổi." };
    const correct = choice === q.correct;
    const saved = this.commit((s) => {
      if (!correct) {
        s.records[id].attempts++;
        return true;
      }
      const tx = `quest:${id}:base`;
      if (s.transactions.includes(tx)) return false;
      s.transactions.push(tx);
      s.records[id].status = "completed";
      s.coins += def.reward.coins;
      s.xp += def.reward.xp;
      for (const [item, amount] of Object.entries(def.reward.items))
        s.inventory[item] = (s.inventory[item] ?? 0) + amount;
      return true;
    });
    return {
      result: saved ? (correct ? "correct" : "incorrect") : "unsaved",
      explanation: q.explanation,
    };
  }
}
/** Disabled contract only. No simulated view grants a real bonus. */
export interface RewardedAdAdapter {
  readonly enabled: false;
  requestBonus(transactionId: string): Promise<{ status: "disabled" }>;
}
export const disabledRewardedAds: RewardedAdAdapter = {
  enabled: false,
  requestBonus: async () => ({ status: "disabled" }),
};
