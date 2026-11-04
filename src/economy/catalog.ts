import farm from "../../public/assets/gate3/final-world/farm-plots.json";
export const EDUCATIONAL_REVIEW_STATUS = "PENDING_HUMAN_REVIEW";
export const ECONOMY = {
  slots: 12,
  maxStack: 99,
  maxCoins: 1_000_000,
  offlineCapMs: 86_400_000,
  maxReceipts: 4096,
} as const;
export const SHOPKEEPER = "npc-minseo";
export const items: Record<
  string,
  {
    name: string;
    ko: string;
    stack: number;
    buy: number;
    sell: number;
    stock: number;
  }
> = {
  "seed-radish": {
    name: "Hạt củ cải",
    ko: "무 씨앗",
    stack: 99,
    buy: 4,
    sell: 0,
    stock: 50,
  },
  "seed-scallion": {
    name: "Hạt hành lá",
    ko: "파 씨앗",
    stack: 99,
    buy: 6,
    sell: 0,
    stock: 50,
  },
  radish: { name: "Củ cải", ko: "무", stack: 99, buy: 0, sell: 3, stock: 0 },
  scallion: { name: "Hành lá", ko: "파", stack: 99, buy: 0, sell: 3, stock: 0 },
  "jeju-postcard": {
    name: "Bưu thiếp Jeju · đồ lưu niệm",
    ko: "제주 엽서",
    stack: 1,
    buy: 12,
    sell: 0,
    stock: 5,
  },
};
export const crops = {
  radish: {
    name: "Củ cải · 무",
    seed: "seed-radish",
    produce: "radish",
    growMs: 45_000,
    introMs: 6000,
    yield: 2,
    frame: 0,
  },
  scallion: {
    name: "Hành lá · 파",
    seed: "seed-scallion",
    produce: "scallion",
    growMs: 90_000,
    introMs: 10000,
    yield: 3,
    frame: 1,
  },
} as const;
export type CropId = keyof typeof crops;
export type FarmAction = "till" | "plant" | "water" | "harvest";
export interface PlotState {
  lastHarvestedAt?: number;
  stage: "empty" | "tilled" | "planted" | "watered";
  cycle: number;
  crop?: CropId;
  plantedAt?: number;
  wateredAt?: number;
  growMs?: number;
}
export interface EconomyState {
  interactionSchema?: 2;
  revision: number;
  plots: Record<string, PlotState>;
  stock: Record<string, number>;
  harvests: Record<string, number>;
  sales: Record<string, number>;
}
export const plots = farm.plots.map((p) => ({
  id: p.id,
  point: p.interactionAnchor as [number, number],
  row: [
    p.cropDisplayRect[0] + 12,
    p.cropDisplayRect[1] + p.cropDisplayRect[3] - 16,
    116,
    12,
  ] as const,
  sourceRect: p.worldRect,
}));
export function freshEconomy(): EconomyState {
  return {
    interactionSchema: 2,
    revision: 0,
    plots: Object.fromEntries(
      plots.map((p) => [p.id, { stage: "empty", cycle: 0 }]),
    ),
    stock: Object.fromEntries(
      Object.entries(items)
        .filter(([, v]) => v.stock > 0)
        .map(([id, v]) => [id, v.stock]),
    ),
    harvests: {},
    sales: {},
  };
}
export function ready(p: PlotState, now: number) {
  return (
    p.stage === "watered" &&
    p.wateredAt !== undefined &&
    p.growMs !== undefined &&
    Math.max(0, Math.min(ECONOMY.offlineCapMs, now - p.wateredAt)) >= p.growMs
  );
}
export function validInventory(inv: Record<string, number>) {
  return (
    Object.values(inv).every((n) => Number.isSafeInteger(n) && n >= 0) &&
    Object.entries(inv).filter(([, n]) => n > 0).length <= ECONOMY.slots &&
    Object.entries(inv).every(
      ([id, n]) => n <= (items[id]?.stack ?? ECONOMY.maxStack),
    )
  );
}
export function nearGround(
  player: readonly [number, number],
  target: readonly [number, number],
  ground: (x: number, y: number) => boolean,
  radius = 34,
) {
  if (Math.hypot(player[0] - target[0], player[1] - target[1]) > radius)
    return false;
  for (let i = 0; i <= 20; i++)
    if (
      !ground(
        player[0] + ((target[0] - player[0]) * i) / 20,
        player[1] + ((target[1] - player[1]) * i) / 20,
      )
    )
      return false;
  return true;
}
