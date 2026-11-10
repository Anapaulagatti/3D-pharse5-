/** Retained original translation practice; not a Hangul assessment. */
import type { LearningQuestion } from "./learning";
const question = (
  id: string,
  prompt: string,
  options: string[],
  correct: number,
  explanation: string,
): LearningQuestion => ({
  id: "translation:" + id,
  difficulty: "beginner",
  grade: "basic",
  prompt,
  options,
  correct,
  explanation,
  direction: "ko-vi",
  answerLanguage: "vi",
  review: "PENDING_HUMAN_REVIEW",
  acceptedAnswers: [options[correct]],
  choiceIds: options.map((_, i) => "translation:" + id + ":" + i),
  distractorRationale: options.map((_, i) =>
    i === correct
      ? explanation
      : "Different meaning from the requested Korean expression",
  ),
  provenance:
    "Original project examples retained from V2; no exam bank or textbook input",
});
export const translationQuestions: Record<string, LearningQuestion[]> = {
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
