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
  ko: string;
  giver: string;
  recipient?: string;
  topic: string;
  steps: readonly {
    id: string;
    label: string;
    point: readonly [number, number];
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
      {
        id: "prepare",
        label: "Chuẩn bị khay thực hành bên luống 4 · 흙을 준비해요",
        point: [470, 669],
      },
      {
        id: "plant",
        label: "Gieo hạt vào khay · 씨앗을 심어요",
        point: [470, 669],
      },
      {
        id: "water",
        label: "Tưới khay thực hành · 물을 줘요",
        point: [470, 669],
      },
    ],
    reward: { coins: 20, xp: 20, items: { seed: 2, sprout: 1 } },
  },
];
export const itemNames: Record<string, string> = {
  tangerine: "Quýt",
  parcel: "Gói sách",
  seed: "Hạt giống",
  sprout: "Mầm cây thực hành",
};
