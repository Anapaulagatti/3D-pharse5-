import {
  crops,
  cropUnlocked,
  items,
  plots,
  freshEconomy,
  ready,
  validInventory,
  nearGround,
  SHOPKEEPER,
  ECONOMY,
  type EconomyState,
  type CropId,
  type FarmAction,
} from "../economy/catalog";
import {
  LocalLearningProgress,
  quests,
  type LearningProgressAdapter,
} from "./content";
export interface InteractionContext {
  npcId: string;
  player: readonly [number, number];
  actor: readonly [number, number];
  ground: (x: number, y: number) => boolean;
}
export const QUEST_STORAGE_KEY = "korean-arena-quests-v1";
export type QuestStatus = "active" | "challenge" | "completed";
export interface QuestRecord {
  status: QuestStatus;
  step: number;
  attempts: number;
  boundPlot?: string;
  collected?: string[];
}
export interface QuestSave {
  schemaVersion: 1;
  records: Record<string, QuestRecord>;
  inventory: Record<string, number>;
  coins: number;
  xp: number;
  transactions: string[];
  economy: EconomyState;
}
const fresh = (): QuestSave => ({
  schemaVersion: 1,
  records: {},
  inventory: {},
  coins: 0,
  xp: 0,
  transactions: [],
  economy: freshEconomy(),
});
const integer = (v: unknown): v is number =>
  Number.isSafeInteger(v) && Number(v) >= 0 && Number(v) <= 1000000;
/** Local demo authority. Single atomic save contains progress AND reward receipts. No mastery/account claims. */
export class QuestManager {
  private value = fresh();
  storageWarning = "";
  migrationNotice = "";
  private lastRaw: string | null = null;
  private migrationBackupNeeded = false;
  constructor(
    private storage?: Pick<Storage, "getItem" | "setItem">,
    readonly learning: LearningProgressAdapter = new LocalLearningProgress(),
  ) {
    try {
      const raw = storage?.getItem(QUEST_STORAGE_KEY);
      if (!raw) return;
      const v = JSON.parse(raw) as QuestSave;
      const legacy = v.economy?.interactionSchema !== 2;
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
          record.step >
            (legacy && id === "farm-first-seed-v1" ? 4 : def.steps.length) ||
          !integer(record.attempts)
        )
          throw Error("invalid");
        if (
          (record.status === "completed") !==
          v.transactions.includes(`quest:${id}:base`)
        )
          throw Error("invalid receipt");
      }
      for (const def of quests.filter((q) => q.topic === "orchard")) {
        const r = v.records[def.id];
        if (!r) continue;
        r.collected ??= def.steps.slice(0, r.step).map((s) => s.id);
        if (
          !Array.isArray(r.collected) ||
          new Set(r.collected).size !== r.collected.length ||
          r.collected.some((id) => !def.steps.some((s) => s.id === id)) ||
          r.collected.length !== r.step
        )
          throw Error("invalid collected objects");
      }
      if (legacy) {
        const n = Math.min(
          v.inventory.seed ?? 0,
          Math.max(0, 99 - (v.inventory["seed-radish"] ?? 0)),
        );
        const slots = Object.values(v.inventory).filter((n) => n > 0).length;
        if (
          n > 0 &&
          ((v.inventory["seed-radish"] ?? 0) > 0 ||
            slots < ECONOMY.slots ||
            n === v.inventory.seed)
        ) {
          v.inventory.seed -= n;
          v.inventory["seed-radish"] = (v.inventory["seed-radish"] ?? 0) + n;
        }
        const r = v.records["farm-first-seed-v1"];
        if (r?.status === "completed") r.step = 3;
        else if (r) {
          r.status = "active";
          r.step = 0;
          delete r.boundPlot;
          if (
            !(v.inventory["seed-radish"] > 0) &&
            Object.values(v.inventory).filter((n) => n > 0).length <
              ECONOMY.slots
          )
            v.inventory["seed-radish"] = 1;
          this.migrationNotice =
            "Hướng dẫn cũ chuyển sang luống thật; xu và phần thưởng đã nhận vẫn giữ nguyên.";
        }
      }
      v.economy ??= freshEconomy();
      v.economy.interactionSchema = 2;
      if (
        !integer(v.economy.revision) ||
        !v.economy.plots ||
        !v.economy.stock ||
        !v.economy.harvests ||
        !v.economy.sales
      )
        throw Error("invalid economy");
      if (
        v.economy.farmCellSchema !== undefined &&
        v.economy.farmCellSchema !== 1
      )
        throw Error("unknown farm cell schema");
      const legacyCells = v.economy.farmCellSchema === undefined;
      // Additive migration: existing six states retain the exact crop/timer/cycle.
      // New cells start empty; never clone a planted legacy crop or its reward.
      for (const plot of plots) {
        if (legacyCells && plot.id !== plot.bedId && !v.economy.plots[plot.id])
          v.economy.plots[plot.id] = { stage: "empty", cycle: 0 };
        const state = v.economy.plots[plot.id];
        if (
          !state ||
          !["empty", "tilled", "planted", "watered"].includes(state.stage) ||
          !integer(state.cycle)
        )
          throw Error("invalid plot");
        if (state.crop && !(state.crop in crops)) throw Error("invalid crop");
        if (
          (state.stage === "planted" || state.stage === "watered") &&
          (!state.crop ||
            !Number.isFinite(state.plantedAt) ||
            !Number.isFinite(state.growMs))
        )
          throw Error("invalid plant");
        if (
          state.crop &&
          state.growMs !== undefined &&
          ![crops[state.crop].growMs, crops[state.crop].introMs].includes(
            state.growMs as never,
          )
        )
          throw Error("untrusted growth duration");
        if (state.plantedAt !== undefined && state.plantedAt < 0)
          throw Error("invalid planting date");
        if (
          state.wateredAt !== undefined &&
          state.wateredAt < (state.plantedAt ?? 0)
        )
          throw Error("water before planting");
        if (state.stage === "watered" && !Number.isFinite(state.wateredAt))
          throw Error("invalid water");
      }
      // Preserve the original pre-upgrade snapshot before the first successful write.
      this.migrationBackupNeeded = v.economy.stock["seed-carrot"] === undefined;
      // Add only genuinely new stock IDs; never refill an existing exhausted item.
      for (const [id, item] of Object.entries(items))
        if (item.stock > 0 && v.economy.stock[id] === undefined)
          v.economy.stock[id] = item.stock;
      v.economy.farmCellSchema = 1;
      if (!Object.values(v.economy.stock).every(integer))
        throw Error("invalid stock");
      this.value = v;
      this.lastRaw = raw;
    } catch {
      this.storageWarning =
        "Dữ liệu nhiệm vụ không hợp lệ; dữ liệu gốc chưa bị ghi đè.";
    }
  }
  exportRawSave() {
    try {
      return this.storage?.getItem(QUEST_STORAGE_KEY) ?? null;
    } catch {
      return null;
    }
  }
  restoreMigrationBackup() {
    try {
      const raw = this.storage?.getItem(
        QUEST_STORAGE_KEY + ":backup:roadmap-v2",
      );
      if (!raw || !this.storage) return false;
      const parsed = new QuestManager({
        getItem: (key) => (key === QUEST_STORAGE_KEY ? raw : null),
        setItem: () => {},
      });
      if (parsed.storageWarning) return false;
      const current = this.storage.getItem(QUEST_STORAGE_KEY);
      if (current)
        this.storage.setItem(
          QUEST_STORAGE_KEY + ":corrupt-backup:roadmap-v2",
          current,
        );
      const next = parsed.snapshot(),
        serialized = JSON.stringify(next);
      this.storage.setItem(QUEST_STORAGE_KEY, serialized);
      this.value = next;
      this.lastRaw = serialized;
      this.storageWarning = "";
      this.migrationBackupNeeded = false;
      return true;
    } catch {
      return false;
    }
  }
  snapshot(): QuestSave {
    return structuredClone(this.value);
  }
  private commit(change: (next: QuestSave) => boolean) {
    if (this.storageWarning) return false;
    try {
      const raw = this.storage?.getItem(QUEST_STORAGE_KEY) ?? null;
      if (this.storage && raw !== this.lastRaw) {
        const latest = new QuestManager(this.storage, this.learning);
        if (latest.storageWarning) {
          this.storageWarning = latest.storageWarning;
          return false;
        }
        this.value = latest.snapshot();
        this.lastRaw = raw;
      }
    } catch {
      return false;
    }
    const next = this.snapshot();
    if (!change(next)) return false;
    if (
      !validInventory(next.inventory) ||
      !integer(next.coins) ||
      !integer(next.xp) ||
      next.transactions.length > ECONOMY.maxReceipts
    )
      return false;
    next.economy.revision++;
    const serialized = JSON.stringify(next);
    try {
      if (
        this.migrationBackupNeeded &&
        this.lastRaw &&
        !this.storage?.getItem(QUEST_STORAGE_KEY + ":backup:roadmap-v2")
      )
        this.storage?.setItem(
          QUEST_STORAGE_KEY + ":backup:roadmap-v2",
          this.lastRaw,
        );
      this.storage?.setItem(QUEST_STORAGE_KEY, serialized);
      this.migrationBackupNeeded = false;
    } catch {
      this.storageWarning =
        "Không lưu được nhiệm vụ. Chưa cấp phần thưởng; hãy kiểm tra bộ nhớ trình duyệt.";
      return false;
    }
    this.value = next;
    this.lastRaw = serialized;
    return true;
  }
  private validContext(id: string, npcId: string, c: InteractionContext) {
    return (
      c.npcId === npcId &&
      nearGround(c.player, c.actor, c.ground, 112) &&
      quests.some((q) => q.id === id)
    );
  }
  acceptInWorld(id: string, npcId: string, c: InteractionContext) {
    return this.validContext(id, npcId, c) && this.accept(id, npcId);
  }
  returnInWorld(id: string, npcId: string, c: InteractionContext) {
    return this.validContext(id, npcId, c) && this.returnToNPC(id, npcId);
  }
  answerInWorld(
    id: string,
    questionId: string,
    choice: number,
    c: InteractionContext,
  ) {
    const q = quests.find((q) => q.id === id);
    return q && this.validContext(id, q.recipient ?? q.giver, c)
      ? this.answer(id, questionId, choice)
      : { result: "invalid", explanation: "Hãy trở lại người bạn để trả lời." };
  }
  accept(id: string, npcId: string) {
    const def = quests.find((q) => q.id === id && q.giver === npcId);
    if (!def) return false;
    return this.commit((s) => {
      if (
        def.prerequisite &&
        s.records[def.prerequisite]?.status !== "completed"
      )
        return false;
      if (s.records[id]) return false;
      s.records[id] = { status: "active", step: 0, attempts: 0 };
      if (def.id === "farm-radish-harvest-v1")
        s.inventory["seed-radish"] = (s.inventory["seed-radish"] ?? 0) + 1;
      if (def.id === "farm-first-seed-v1")
        s.inventory["seed-radish"] = (s.inventory["seed-radish"] ?? 0) + 1;
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
    const step =
      def?.topic === "orchard"
        ? def.steps.find((s) => s.id === action)
        : def?.steps[record?.step ?? -1];
    if (
      !def ||
      def.economyObjectives ||
      !record ||
      record.status !== "active" ||
      !step ||
      step.id !== action ||
      record.collected?.includes(action) ||
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
      if (def.topic === "orchard") {
        const r = s.records[id];
        r.collected ??= def.steps.slice(0, r.step).map((s) => s.id);
        if (r.collected.includes(action)) return false;
        r.collected.push(action);
        s.inventory.tangerine = (s.inventory.tangerine ?? 0) + 1;
      }
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
  private economyEvent(
    s: QuestSave,
    event: string,
    item?: string,
    crop?: string,
    plotId?: string,
  ) {
    for (const def of quests) {
      const r = s.records[def.id];
      const objective = def.economyObjectives?.[r?.step ?? -1];
      if (
        r?.status !== "active" ||
        !objective ||
        objective.event !== event ||
        (objective.item && objective.item !== item) ||
        (objective.crop && objective.crop !== crop)
      )
        continue;
      if (plotId && r.boundPlot && r.boundPlot !== plotId) continue;
      if (plotId && !r.boundPlot) r.boundPlot = plotId;
      r.step++;
    }
  }
  farmAction(
    plotId: string,
    action: FarmAction,
    cropId: CropId | undefined,
    txId: string,
    player: readonly [number, number],
    ground: (x: number, y: number) => boolean,
    now = Date.now(),
  ) {
    const def = plots.find((p) => p.id === plotId);
    if (
      !def ||
      !Number.isFinite(now) ||
      !nearGround(player, def.point, ground) ||
      !/^[a-zA-Z0-9:_-]{3,120}$/.test(txId)
    )
      return false;
    return this.commit((s) => {
      const tx = `farm:${txId}`;
      if (s.transactions.includes(tx)) return false;
      const p = s.economy.plots[plotId];
      let eventCrop = p.crop;
      if (action === "till") {
        if (p.stage !== "empty") return false;
        p.stage = "tilled";
      } else if (action === "plant") {
        if (
          !["empty", "tilled"].includes(p.stage) ||
          !cropId ||
          !(cropId in crops) ||
          !cropUnlocked(cropId, s.records)
        )
          return false;
        if (p.stage === "empty")
          this.economyEvent(s, "till", undefined, undefined, plotId);
        const crop = crops[cropId];
        if (!(s.inventory[crop.seed] > 0)) return false;
        s.inventory[crop.seed]--;
        p.stage = "planted";
        p.crop = cropId;
        p.plantedAt = now;
        p.growMs = crop.growMs;
        p.cycle++;
        eventCrop = cropId;
        // One bounded introductory crop per actual quest stage, never a repeatable speed boost.
        const intro = quests.find(
          (q) =>
            q.economyObjectives?.[s.records[q.id]?.step ?? -1]?.event ===
              "plant" &&
            q.economyObjectives[s.records[q.id].step].crop === cropId &&
            s.records[q.id].status === "active" &&
            (!s.records[q.id].boundPlot ||
              s.records[q.id].boundPlot === plotId),
        );
        if (intro) p.growMs = crop.introMs;
      } else if (action === "water") {
        if (p.stage !== "planted") return false;
        p.stage = "watered";
        p.wateredAt = now;
      } else if (action === "harvest") {
        if (!ready(p, now) || !p.crop) return false;
        const c = crops[p.crop];
        s.inventory[c.produce] = (s.inventory[c.produce] ?? 0) + c.yield;
        s.economy.harvests[p.crop] = (s.economy.harvests[p.crop] ?? 0) + 1;
        s.economy.plots[plotId] = {
          stage: "empty",
          cycle: p.cycle,
          lastHarvestedAt: now,
        };
      } else return false;
      this.economyEvent(s, action, undefined, eventCrop, plotId);
      s.transactions.push(tx);
      return true;
    });
  }
  trade(
    kind: "buy" | "sell",
    itemId: string,
    quantity: number,
    txId: string,
    context: {
      npcId: string;
      player: readonly [number, number];
      actor: readonly [number, number];
      ground: (x: number, y: number) => boolean;
    },
  ) {
    const item = items[itemId];
    if (
      !item ||
      !Number.isSafeInteger(quantity) ||
      quantity <= 0 ||
      quantity > ECONOMY.maxStack ||
      context.npcId !== SHOPKEEPER ||
      !nearGround(context.player, context.actor, context.ground, 112) ||
      !/^[a-zA-Z0-9:_-]{3,120}$/.test(txId)
    )
      return false;
    return this.commit((s) => {
      const tx = `trade:${txId}`;
      if (s.transactions.includes(tx)) return false;
      if (kind === "buy") {
        if (
          item.buy <= 0 ||
          (itemId.startsWith("seed-") &&
            !cropUnlocked(itemId.slice(5), s.records)) ||
          s.coins < item.buy * quantity ||
          (s.economy.stock[itemId] ?? 0) < quantity
        )
          return false;
        s.coins -= item.buy * quantity;
        s.economy.stock[itemId] -= quantity;
        s.inventory[itemId] = (s.inventory[itemId] ?? 0) + quantity;
      } else if (kind === "sell") {
        if (item.sell <= 0 || (s.inventory[itemId] ?? 0) < quantity)
          return false;
        s.inventory[itemId] -= quantity;
        s.coins += item.sell * quantity;
        s.economy.sales[itemId] = (s.economy.sales[itemId] ?? 0) + quantity;
      } else return false;
      this.economyEvent(s, kind, itemId);
      s.transactions.push(tx);
      return true;
    });
  }

  recoverStarter() {
    return this.commit((s) => {
      if (
        s.transactions.includes("recovery:starter:v2") ||
        Object.entries(s.inventory).some(
          ([id, n]) => id.startsWith("seed-") && n > 0,
        ) ||
        Object.values(s.economy.plots).some((p) => p.crop)
      )
        return false;
      s.inventory["seed-radish"] = 1;
      s.transactions.push("recovery:starter:v2");
      return true;
    });
  }
  /** Physical room events. Caller supplies actual in-room proximity/collision context. No remote HUD completion. */
  interiorEvent(
    event: string,
    item: string,
    txId: string,
    player: readonly [number, number],
    target: readonly [number, number],
    ground: (x: number, y: number) => boolean,
  ) {
    if (
      !nearGround(player, target, ground, 48) ||
      !/^[a-zA-Z0-9:_-]{3,120}$/.test(txId)
    )
      return false;
    return this.commit((s) => {
      const tx = "interior:" + txId;
      if (s.transactions.includes(tx)) return false;
      const before = JSON.stringify(s.records);
      this.economyEvent(s, event, item);
      if (JSON.stringify(s.records) === before) return false;
      s.transactions.push(tx);
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
