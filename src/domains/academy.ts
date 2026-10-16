/** Letter NAMES: intentionally not a romanized pronunciation lesson. */
export const letterLesson = [
  {
    glyph: "ㄱ",
    name: "giyeok",
    vi: "Tên chữ: giyeok (기역). Âm thực tế phụ thuộc vị trí trong âm tiết.",
  },
  {
    glyph: "ㄴ",
    name: "nieun",
    vi: "Tên chữ: nieun (니은). Đây là một phụ âm cơ bản của Hangul.",
  },
  {
    glyph: "ㅁ",
    name: "mieum",
    vi: "Tên chữ: mieum (미음). Hãy tìm hình vuông khép kín.",
  },
] as const;
export type AcademyProgress = { version: 1; mastered: string[] };
export const progressKey = "korean-arena-academy-v1";
export function parseAcademyProgress(raw: string | null): AcademyProgress {
  try {
    const p: unknown = JSON.parse(raw ?? "null");
    if (
      typeof p !== "object" ||
      !p ||
      !("version" in p) ||
      p.version !== 1 ||
      !("mastered" in p) ||
      !Array.isArray(p.mastered)
    )
      throw Error("Invalid save");
    const mastered = p.mastered;
    return {
      version: 1,
      mastered: letterLesson
        .filter((l) => mastered.includes(l.glyph))
        .map((l) => l.glyph),
    };
  } catch {
    return { version: 1, mastered: [] };
  }
}
