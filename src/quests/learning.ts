/** Original local language drafts, not certified curriculum or formal mastery. */
import bank from "./hangul-bank.json";
export type LearningGrade = "alphabet" | "basic" | "intermediate";
export interface LearningQuestion {
  id: string;
  topic?: string;
  difficulty: "beginner" | "intermediate";
  grade: LearningGrade;
  prompt: string;
  options: readonly string[];
  correct: number;
  explanation: string;
  direction: "vi-ko" | "ko-vi";
  answerLanguage: "ko" | "vi";
  acceptedAnswers: readonly string[];
  choiceIds: readonly string[];
  distractorRationale: readonly string[];
  review: "PENDING_HUMAN_REVIEW";
  provenance: string;
}
export interface LearningProgressAdapter {
  readonly mode: "local-demo" | "authorized-integration";
  questions(topic: string): readonly LearningQuestion[];
}
export const hangulQuestions = bank as LearningQuestion[];
export class LocalLearningProgress implements LearningProgressAdapter {
  readonly mode = "local-demo" as const;
  questions(topic: string) {
    return hangulQuestions.filter((q) => q.topic === topic);
  }
}
/** NFC/NFD equivalence, optional whitespace and terminal punctuation only. No romanization shortcuts. */
export function normalizeHangulAnswer(value: string) {
  return value
    .normalize("NFC")
    .trim()
    .replace(/[\u200B-\u200D\uFEFF]/g, "")
    .replace(/\s+/g, "")
    .replace(/[.!?。！？]+$/u, "");
}
export function isCorrectHangul(q: LearningQuestion, value: string) {
  const n = normalizeHangulAnswer(value);
  return (
    q.answerLanguage === "ko" &&
    /\p{Script=Hangul}/u.test(n) &&
    !/[A-Za-z0-9]/.test(n) &&
    q.acceptedAnswers.some((a) => normalizeHangulAnswer(a) === n)
  );
}
