export { LocalLearningProgress } from "./learning";
export type { LearningQuestion, LearningProgressAdapter } from "./learning";

export interface QuestDefinition {
  id: string;
  title: string;
  prerequisite?: string;
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
      | "courier";
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
];
export const itemNames: Record<string, string> = {
  tangerine: "Quýt",
  parcel: "Gói sách",
  seed: "Hạt giống",
  sprout: "Mầm cây thực hành",
};
