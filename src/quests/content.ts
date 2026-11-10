export { LocalLearningProgress } from "./learning";
export type { LearningQuestion, LearningProgressAdapter } from "./learning";

export interface QuestDefinition {
  id: string;
  title: string;
  prerequisite?: string;
  requires?: readonly string[];
  storyline?: "letters" | "farm" | "merchant" | "culture" | "jeju";
  optional?: boolean;
  deliveryItem?: string;
  consumeOnReturn?: { item: string; count: number };
  ko: string;
  giver: string;
  recipient?: string;
  topic: string;
  steps: readonly {
    id: string;
    label: string;
    point: readonly [number, number];
  }[];
  economyObjectives?: readonly {
    event:
      | "till"
      | "plant"
      | "water"
      | "harvest"
      | "buy"
      | "sell"
      | "enter"
      | "fragment"
      | "repair"
      | "courier"
      | "visit"
      | "service";
    crop?: string;
    item?: string;
  }[];
  reward: { coins: number; xp: number; items: Record<string, number> };
}
export const quests: readonly QuestDefinition[] = [
  {
    id: "jeju-orchard-v1",
    title: "Quýt Jeju",
    ko: "제주 귤 모으기",
    giver: "npc-harin",
    topic: "orchard",
    steps: [
      {
        id: "fruit-a",
        label: "Gom quýt ở giỏ phía tây · 귤을 모아요",
        point: [3900, 4070],
      },
      {
        id: "fruit-b",
        label: "Gom quýt ở lối giữa · 귤을 모아요",
        point: [3930, 4080],
      },
      {
        id: "fruit-c",
        label: "Gom quýt ở lối đông · 귤을 모아요",
        point: [3960, 4080],
      },
    ],
    reward: { coins: 25, xp: 15, items: { tangerine: 1 } },
  },
  {
    id: "modern-delivery-v1",
    title: "Một gói sách",
    ko: "책 배달",
    giver: "npc-minseo",
    recipient: "npc-jiho",
    topic: "delivery",
    steps: [],
    reward: { coins: 20, xp: 15, items: {} },
  },
  {
    id: "farm-first-seed-v1",
    title: "Hạt giống đầu tiên",
    ko: "첫 씨앗",
    giver: "npc-cheolsu",
    topic: "farm",
    steps: [
      { id: "plant", label: "Gieo hạt vào một luống thật", point: [470, 669] },
      {
        id: "water",
        label: "Dùng bình tưới cho cây vừa gieo",
        point: [470, 669],
      },
      {
        id: "harvest",
        label: "Thu hoạch cây chín rồi trở lại Cheolsu",
        point: [470, 669],
      },
    ],
    economyObjectives: [
      { event: "plant", crop: "radish" },
      { event: "water", crop: "radish" },
      { event: "harvest", crop: "radish" },
    ],
    reward: { coins: 20, xp: 20, items: { "seed-radish": 2, sprout: 1 } },
  },
  {
    id: "farm-radish-harvest-v1",
    title: "Một hàng củ cải",
    ko: "무 기르기",
    giver: "npc-nayeon",
    topic: "farm",
    steps: [
      {
        id: "till",
        label: "Gặp Nayeon; xới hàng thực hành ở một luống",
        point: [470, 481],
      },
      {
        id: "plant",
        label: "Gieo hạt củ cải vào hàng đã xới",
        point: [470, 481],
      },
      { id: "water", label: "Tưới hàng củ cải", point: [470, 481] },
      {
        id: "harvest",
        label: "Thu hoạch củ cải chín; lứa hướng dẫn6giây",
        point: [470, 481],
      },
    ],
    economyObjectives: [
      { event: "till" },
      { event: "plant", crop: "radish" },
      { event: "water", crop: "radish" },
      { event: "harvest", crop: "radish" },
    ],
    reward: { coins: 18, xp: 20, items: {} },
  },
  {
    id: "shop-garden-market-v1",
    title: "Từ vườn đến quầy hàng",
    ko: "농장에서 가게까지",
    giver: "npc-minseo",
    topic: "shop",
    steps: [
      {
        id: "buy",
        label: "Mua hạt hành lá từ Minseo (6xu; nhiệm vụ cũ luôn miễn phí)",
        point: [650, 2620],
      },
      {
        id: "plant",
        label: "Gieo hạt hành lá ở một hàng đã xới",
        point: [470, 481],
      },
      { id: "water", label: "Tưới hàng hành lá", point: [470, 481] },
      {
        id: "harvest",
        label: "Thu hoạch hành lá chín; lứa hướng dẫn10giây",
        point: [470, 481],
      },
      {
        id: "sell",
        label: "Bán hành lá cho Minseo rồi trả lời tiếng Hàn",
        point: [650, 2620],
      },
    ],
    economyObjectives: [
      { event: "buy", item: "seed-scallion" },
      { event: "plant", crop: "scallion" },
      { event: "water", crop: "scallion" },
      { event: "harvest", crop: "scallion" },
      { event: "sell", item: "scallion" },
    ],
    reward: { coins: 22, xp: 20, items: {} },
  },
  {
    id: "town-first-delivery-v2",
    title: "Những nét chữ thất lạc",
    ko: "잃어버린 글자",
    giver: "npc-eunji",
    recipient: "npc-jiho",
    topic: "delivery",
    prerequisite: "farm-first-seed-v1",
    steps: [
      {
        id: "visit-seeds",
        label: "Ghé cửa hàng hạt tại cafe",
        point: [717, 2605],
      },
      {
        id: "fragment-workshop",
        label: "Nhặt mảnh nét trong xưởng cộng đồng",
        point: [1418, 2605],
      },
      {
        id: "fragment-bookshop",
        label: "Tìm mảnh nét bên kệ sách",
        point: [1128, 2605],
      },
      {
        id: "fragment-market",
        label: "Tìm mảnh nét trên bàn cửa hàng hạt",
        point: [717, 2605],
      },
      {
        id: "repair",
        label: "Ghép bảng chữ 책 tại xưởng",
        point: [1418, 2605],
      },
      {
        id: "courier-start",
        label: "Nhận tuyến giao sách tại xưởng",
        point: [1418, 2605],
      },
      {
        id: "courier-stop",
        label: "Xác nhận địa chỉ tại cửa hàng hạt",
        point: [717, 2605],
      },
      {
        id: "deliver",
        label: "Giao đến quầy hiệu sách rồi gặp Jiho",
        point: [1128, 2605],
      },
    ],
    economyObjectives: [
      { event: "enter", item: "seed-shop" },
      { event: "fragment", item: "workshop" },
      { event: "fragment", item: "bookshop" },
      { event: "fragment", item: "seed-shop" },
      { event: "repair", item: "workshop" },
      { event: "courier", item: "workshop" },
      { event: "courier", item: "seed-shop" },
      { event: "courier", item: "bookshop" },
    ],
    reward: { coins: 36, xp: 20, items: {} },
  },
  {
    id: "farm-variety-v2",
    optional: true,
    title: "Một vụ cà rốt mới",
    ko: "당근 기르기",
    giver: "npc-nayeon",
    topic: "farm",
    prerequisite: "farm-first-seed-v1",
    steps: [
      { id: "buy", label: "Mua hạt cà rốt đã mở khóa", point: [717, 2605] },
      { id: "plant", label: "Gieo cà rốt", point: [470, 669] },
      { id: "water", label: "Tưới cà rốt", point: [470, 669] },
      { id: "harvest", label: "Thu hoạch cà rốt", point: [470, 669] },
      { id: "sell", label: "Bán một cà rốt", point: [717, 2605] },
    ],
    economyObjectives: [
      { event: "buy", item: "seed-carrot" },
      { event: "plant", crop: "carrot" },
      { event: "water", crop: "carrot" },
      { event: "harvest", crop: "carrot" },
      { event: "sell", item: "carrot" },
    ],
    reward: { coins: 24, xp: 15, items: { "seed-cabbage": 1 } },
  },
  {
    id: "culture-postcard-v4",
    title: "Dấu chữ trên sân xưa",
    ko: "마당의 글자",
    giver: "npc-seoyeon",
    recipient: "npc-jiho",
    topic: "delivery",
    storyline: "culture",
    requires: ["farm-first-seed-v1"],
    deliveryItem: "archive-note",
    steps: [
      {
        id: "palace-observation",
        label: "Dừng đọc biển sân cung điện; rồi tìm sân học hanok",
        point: [2048, 990],
      },
      {
        id: "academy-observation",
        label: "Quan sát ký hiệu tại sân học hanok; mang ghi chú tới Jiho",
        point: [800, 1500],
      },
    ],
    economyObjectives: [
      { event: "visit", item: "culture:palace" },
      { event: "visit", item: "culture:academy" },
    ],
    reward: { coins: 16, xp: 10, items: {} },
  },
  {
    id: "workshop-imprint-v4",
    title: "Dấu đóng cho người giao thư",
    ko: "배달 도장",
    giver: "npc-eunji",
    topic: "delivery",
    storyline: "letters",
    requires: ["culture-postcard-v4"],
    steps: [
      {
        id: "tool-inspection",
        label: "Tại xưởng, kiểm tra dụng cụ trên bàn",
        point: [1418, 2605],
      },
      {
        id: "packing",
        label: "Đóng dấu gói hàng tại bàn giao của xưởng; báo Eunji",
        point: [1418, 2605],
      },
    ],
    economyObjectives: [
      { event: "service", item: "workshop:tools" },
      { event: "service", item: "workshop:packing" },
    ],
    reward: { coins: 14, xp: 10, items: { "packing-seal": 1 } },
  },
  {
    id: "jeju-supply-v4",
    title: "Một chuyến tiếp tế qua cầu",
    ko: "제주에 전해요",
    giver: "npc-minseo",
    recipient: "npc-harin",
    topic: "delivery",
    storyline: "jeju",
    requires: ["shop-garden-market-v1", "workshop-imprint-v4"],
    deliveryItem: "supply-parcel",
    steps: [
      {
        id: "market-packing",
        label: "Kiểm tra gói tiếp tế tại quầy hạt giống",
        point: [717, 2605],
      },
      {
        id: "island-junction",
        label: "Qua cầu tới nút giao lát đá trên đảo Jeju",
        point: [3690, 4090],
      },
      {
        id: "house-approach",
        label: "Theo đường cong phía đông hanok tới thềm cửa; gặp Harin",
        point: [3590, 4390],
      },
    ],
    economyObjectives: [
      { event: "service", item: "seed-shop:packing" },
      { event: "visit", item: "jeju:junction" },
      { event: "visit", item: "jeju:threshold" },
    ],
    reward: { coins: 28, xp: 15, items: {} },
  },
  {
    id: "island-ledger-v4",
    title: "Một giỏ quýt, hai miền phố",
    ko: "귤과 마을",
    giver: "npc-harin",
    recipient: "npc-minseo",
    topic: "delivery",
    storyline: "merchant",
    requires: ["jeju-orchard-v1", "culture-postcard-v4"],
    deliveryItem: "orchard-order",
    consumeOnReturn: { item: "tangerine", count: 1 },
    steps: [
      {
        id: "orchard-house",
        label: "Ghi đơn quýt ở thềm hanok bằng lối cong đã khám phá",
        point: [3590, 4390],
      },
      {
        id: "shop-return",
        label: "Mang đơn cùng một quýt tới quầy Minseo trên đất liền",
        point: [717, 2605],
      },
    ],
    economyObjectives: [
      { event: "visit", item: "jeju:threshold" },
      { event: "service", item: "seed-shop:packing" },
    ],
    reward: { coins: 24, xp: 15, items: {} },
  },
  {
    id: "town-reunion-v4",
    title: "Tấm bảng nối những người bạn",
    ko: "다시 만난 이야기",
    giver: "npc-jiho",
    topic: "delivery",
    storyline: "letters",
    requires: ["town-first-delivery-v2", "island-ledger-v4"],
    steps: [
      {
        id: "workshop-signature",
        label: "Xin dấu xác nhận ở bàn giao xưởng Eunji",
        point: [1418, 2605],
      },
      {
        id: "market-signature",
        label: "Ghé quầy hạt giống để nối đơn hàng với câu chuyện",
        point: [717, 2605],
      },
      {
        id: "bookshop-notice",
        label: "Gắn bảng liên lạc tại hiệu sách rồi báo Jiho",
        point: [1128, 2605],
      },
    ],
    economyObjectives: [
      { event: "service", item: "workshop:packing" },
      { event: "service", item: "seed-shop:packing" },
      { event: "service", item: "bookshop:notice" },
    ],
    reward: { coins: 30, xp: 20, items: { "town-bookmark": 1 } },
  },
];
export const itemNames: Record<string, string> = {
  "archive-note": "Ghi chú sân xưa",
  "packing-seal": "Dấu đóng gói",
  "supply-parcel": "Gói tiếp tế Jeju",
  "orchard-order": "Đơn hàng quýt",
  "town-bookmark": "Dấu sách thị trấn",
  tangerine: "Quýt",
  parcel: "Gói sách",
  seed: "Hạt giống",
  sprout: "Mầm cây thực hành",
};

/** One prerequisite authority shared by model/UI. Old prerequisite remains backward compatible. */
export function questRequirements(q: QuestDefinition) {
  return [
    ...new Set([
      ...(q.prerequisite ? [q.prerequisite] : []),
      ...(q.requires ?? []),
    ]),
  ];
}
export function questAvailable(
  q: QuestDefinition,
  records: Record<string, { status: string }>,
) {
  return questRequirements(q).every(
    (id) => records[id]?.status === "completed",
  );
}
export function questStoryline(q: QuestDefinition) {
  return (
    q.storyline ??
    (q.topic === "farm"
      ? "farm"
      : q.topic === "orchard"
        ? "jeju"
        : q.id === "town-first-delivery-v2"
          ? "letters"
          : "merchant")
  );
}
export const discoveryPoints = [
  { id: "culture:palace", point: [2048, 990] },
  { id: "culture:academy", point: [800, 1500] },
  { id: "jeju:junction", point: [3690, 4090] },
  { id: "jeju:threshold", point: [3590, 4390] },
] as const;
