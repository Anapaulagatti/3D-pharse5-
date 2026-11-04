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
  carrot: {
    name: "Cà rốt · 당근",
    seed: "seed-carrot",
    produce: "carrot",
    growMs: 120_000,
    introMs: 12000,
    yield: 3,
    frame: 2,
  },
  cabbage: {
    name: "Bắp cải · 양배추",
    seed: "seed-cabbage",
    produce: "cabbage",
    growMs: 150_000,
    introMs: 15000,
    yield: 2,
    frame: 3,
  },
  rice: {
    name: "Lúa · 벼",
    seed: "seed-rice",
    produce: "rice",
    growMs: 240_000,
    introMs: 18000,
    yield: 4,
    frame: 4,
  },
  chili: {
    name: "Ớt · 고추",
    seed: "seed-chili",
    produce: "chili",
    growMs: 180_000,
    introMs: 15000,
    yield: 3,
    frame: 5,
  },
  "sweet-potato": {
    name: "Khoai lang · 고구마",
    seed: "seed-sweet-potato",
    produce: "sweet-potato",
    growMs: 210_000,
    introMs: 18000,
    yield: 3,
    frame: 6,
  },
  soybean: {
    name: "Đậu nành · 콩",
    seed: "seed-soybean",
    produce: "soybean",
    growMs: 180_000,
    introMs: 15000,
    yield: 4,
    frame: 7,
  },
  pumpkin: {
    name: "Bí ngô · 호박",
    seed: "seed-pumpkin",
    produce: "pumpkin",
    growMs: 300_000,
    introMs: 20000,
    yield: 2,
    frame: 8,
  },
  cucumber: {
    name: "Dưa leo · 오이",
    seed: "seed-cucumber",
    produce: "cucumber",
    growMs: 180_000,
    introMs: 15000,
    yield: 3,
    frame: 9,
  },
  tomato: {
    name: "Cà chua · 토마토",
    seed: "seed-tomato",
    produce: "tomato",
    growMs: 210_000,
    introMs: 18000,
    yield: 3,
    frame: 10,
  },
  strawberry: {
    name: "Dâu tây · 딸기",
    seed: "seed-strawberry",
    produce: "strawberry",
    growMs: 300_000,
    introMs: 20000,
    yield: 3,
    frame: 11,
  },
} as const;
for (const [id, crop] of Object.entries(crops))
  if (!(id in items)) {
    const [name, ko] = crop.name.split(" · ");
    items[id] = {
      name,
      ko,
      stack: 99,
      buy: 0,
      sell: Math.ceil((6 + crop.frame) / crop.yield) + 1,
      stock: 0,
    };
    items[crop.seed] = {
      name: `Hạt ${name.toLowerCase()}`,
      ko: `${ko} 씨앗`,
      stack: 99,
      buy: 6 + crop.frame,
      sell: 0,
      stock: 50,
    };
  }
export function cropUnlocked(
  id: string,
  records: Record<string, { status: string }>,
) {
  if (id === "radish" || id === "scallion") return true;
  if (id === "carrot" || id === "cabbage")
    return records["farm-first-seed-v1"]?.status === "completed";
  return records["shop-garden-market-v1"]?.status === "completed";
}
export function cropUnlockHint(id: string) {
  return id === "carrot" || id === "cabbage"
    ? "Hoàn thành Hạt giống đầu tiên"
    : "Hoàn thành Từ vườn đến quầy hàng";
}

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
  farmCellSchema?: 1;
  interactionSchema?: 2;
  revision: number;
  plots: Record<string, PlotState>;
  stock: Record<string, number>;
  harvests: Record<string, number>;
  sales: Record<string, number>;
}
/** Six approved beds; six independent cells each. Legacy bed IDs remain bottom-centre cells. */
export const beds = farm.plots.map((p) => ({
  id: p.id,
  rect: p.cropDisplayRect as [number, number, number, number],
  worldRect: p.worldRect,
}));
function cell(
  p: (typeof farm.plots)[number],
  row: number,
  col: number,
  legacy = false,
) {
  const [x, y] = p.cropDisplayRect;
  const root: [number, number] = [x + 22 + col * 48, y + row * 44 + 40];
  return {
    id: legacy ? p.id : `${p.id}-C${row * 3 + col + 1}`,
    bedId: p.id,
    cell: [row, col] as const,
    label: `Luống ${Number(p.id.slice(-2))} · ô ${row * 3 + col + 1}`,
    point: [root[0] + 6, row === 0 ? y - 24 : p.interactionAnchor[1]] as [
      number,
      number,
    ],
    root,
    row: [x + col * 48, y + row * 44, 44, 44] as const,
    sourceRect: [x + col * 48, y + row * 44, 44, 44],
    bed: [x, y, 140, 88] as [number, number, number, number],
  };
}
export const plots = [
  ...farm.plots.map((p) => cell(p, 1, 1, true)),
  ...farm.plots.flatMap((p) => [
    cell(p, 0, 0),
    cell(p, 0, 1),
    cell(p, 0, 2),
    cell(p, 1, 0),
    cell(p, 1, 2),
  ]),
];
export function freshEconomy(): EconomyState {
  return {
    interactionSchema: 2,
    farmCellSchema: 1,
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
