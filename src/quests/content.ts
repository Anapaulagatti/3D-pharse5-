/** Original beginner content. Human Korean educational review is PENDING. */
export interface LearningQuestion {
  id: string;
  difficulty: "beginner";
  prompt: string;
  options: readonly string[];
  correct: number;
  explanation: string;
}
export interface LearningProgressAdapter {
  readonly mode: "local-demo" | "authorized-integration";
  questions(topic: string): readonly LearningQuestion[];
}
const question = (
  id: string,
  prompt: string,
  options: string[],
  correct: number,
  explanation: string,
): LearningQuestion => ({
  id,
  difficulty: "beginner",
  prompt,
  options,
  correct,
  explanation,
});
export class LocalLearningProgress implements LearningProgressAdapter {
  readonly mode = "local-demo" as const;
  questions(topic: string) {
    return questions[topic] ?? [];
  }
}
const questions: Record<string, LearningQuestion[]> = {
  shop: [
    question(
      "shop-1",
      "씨앗을 사요. · Người nói làm gì?",
      ["Bán rau", "Mua hạt giống", "Đọc sách"],
      1,
      "사요 = mua. 씨앗을 사요: Tôi mua hạt giống.",
    ),
    question(
      "shop-2",
      "‘팔아요’는 무슨 뜻이에요?",
      ["Bán", "Mua", "Gieo"],
      0,
      "팔아요 = bán. 파를 팔아요: Tôi bán hành lá.",
    ),
    question(
      "shop-3",
      "‘얼마예요?’는 무슨 뜻이에요?",
      ["Đi đâu?", "Mấy giờ?", "Bao nhiêu tiền?"],
      2,
      "얼마예요? dùng để hỏi giá: Bao nhiêu tiền ạ?",
    ),
  ],
  orchard: [
    question(
      "fruit-1",
      "귤이 세 개 있어요. · Có bao nhiêu quả quýt?",
      ["Hai", "Ba", "Bốn"],
      1,
      "세 개 nghĩa là ba cái/quả; 귤 là quýt.",
    ),
    question(
      "fruit-2",
      "‘귤’은 무슨 뜻이에요? · 귤 nghĩa là gì?",
      ["Quýt", "Táo", "Hạt giống"],
      0,
      "귤 là quýt. 귤을 모아요: Tôi gom quýt.",
    ),
    question(
      "fruit-3",
      "‘과일’은 무슨 뜻이에요? · 과일 nghĩa là gì?",
      ["Bưu kiện", "Đồng ruộng", "Trái cây"],
      2,
      "과일 là trái cây. 귤은 과일이에요: Quýt là trái cây.",
    ),
  ],
  delivery: [
    question(
      "parcel-1",
      "책을 배달해요. · Người nói đang giao gì?",
      ["Nước", "Sách", "Hoa"],
      1,
      "책 là sách; 배달해요 nghĩa là giao hàng.",
    ),
    question(
      "parcel-2",
      "‘서점’은 무슨 뜻이에요? · 서점 nghĩa là gì?",
      ["Hiệu sách", "Nhà ga", "Vườn cây"],
      0,
      "서점 là hiệu sách. 서점에 가요: Tôi đến hiệu sách.",
    ),
    question(
      "parcel-3",
      "‘주세요’는 무슨 뜻이에요? · 주세요 nghĩa là gì?",
      ["Chạy nhanh", "Đọc xong", "Xin hãy cho tôi"],
      2,
      "주세요 là cách đề nghị lịch sự: 책을 주세요 — Xin cho tôi quyển sách.",
    ),
  ],
  farm: [
    question(
      "farm-1",
      "씨앗을 심어요. · Người nói làm gì?",
      ["Tưới nước", "Gieo hạt", "Giao sách"],
      1,
      "씨앗 là hạt giống; 심어요 nghĩa là trồng/gieo.",
    ),
    question(
      "farm-2",
      "물을 줘요. · Hành động nào phù hợp?",
      ["Tưới nước", "Thu hoạch", "Đọc sách"],
      0,
      "물을 줘요 nghĩa là cho nước, trong vườn là tưới nước.",
    ),
    question(
      "farm-3",
      "‘농장’은 무슨 뜻이에요? · 농장 nghĩa là gì?",
      ["Bến tàu", "Cửa hàng", "Nông trại"],
      2,
      "농장 là nông trại. 농장에 가요: Tôi đến nông trại.",
    ),
  ],
};
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
