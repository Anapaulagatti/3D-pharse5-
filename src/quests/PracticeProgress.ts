import { isCorrectHangul, type LearningQuestion } from "./learning";
export interface PracticeRecord {
  itemId: string;
  correct: boolean;
  mode: "choice" | "typing";
  at: number;
  direction: "vi-ko" | "ko-vi";
}
/** Local practice history only. Never grants coins/mastery or writes a website account. */
export class PracticeProgress {
  private rows: PracticeRecord[] = [];
  constructor(private storage?: Pick<Storage, "getItem" | "setItem">) {
    try {
      const q = JSON.parse(
        storage?.getItem("korean-arena-practice-v4") ?? "null",
      );
      if (q?.version === 1 && Array.isArray(q.rows))
        this.rows = q.rows
          .filter(
            (r: PracticeRecord) =>
              typeof r.itemId === "string" &&
              typeof r.correct === "boolean" &&
              ["choice", "typing"].includes(r.mode) &&
              Number.isFinite(r.at) &&
              ["vi-ko", "ko-vi"].includes(r.direction),
          )
          .slice(-100);
    } catch {
      /* Preserve other game stores; optional practice history. */
    }
  }
  answer(q: LearningQuestion, response: number | string) {
    const valid =
      typeof response === "number"
        ? Number.isInteger(response) &&
          response >= 0 &&
          response < q.options.length
        : response.length <= 160;
    if (!valid)
      return {
        correct: false,
        explanation: "Chọn hoặc nhập một đáp án hợp lệ.",
      };
    const correct =
        typeof response === "number"
          ? response === q.correct
          : isCorrectHangul(q, response),
      row: PracticeRecord = {
        itemId: q.id,
        correct,
        mode: typeof response === "number" ? "choice" : "typing",
        at: Date.now(),
        direction: q.direction,
      };
    this.rows = [...this.rows, row].slice(-100);
    try {
      this.storage?.setItem(
        "korean-arena-practice-v4",
        JSON.stringify({ version: 1, rows: this.rows }),
      );
    } catch {
      /* Practice remains usable in memory; no economic mutation. */
    }
    return { correct, explanation: q.explanation };
  }
  snapshot() {
    return structuredClone(this.rows);
  }
}
