/** Planning metadata only. No asset URLs, sprites or playable registrations. */
export interface FutureRosterSlot {
  id: string;
  names: { ko: string; vi: string; en: string };
  phase: "2B";
  status: "planned";
}
export const futureRoster: readonly FutureRosterSlot[] = [
  {
    id: "sori",
    names: { ko: "소리", vi: "Sori", en: "Sori" },
    phase: "2B",
    status: "planned",
  },
  {
    id: "jiwon",
    names: { ko: "지원", vi: "Jiwon", en: "Jiwon" },
    phase: "2B",
    status: "planned",
  },
  {
    id: "nari",
    names: { ko: "나리", vi: "Nari", en: "Nari" },
    phase: "2B",
    status: "planned",
  },
  {
    id: "taeyang",
    names: { ko: "태양", vi: "Taeyang", en: "Taeyang" },
    phase: "2B",
    status: "planned",
  },
  {
    id: "yuna",
    names: { ko: "유나", vi: "Yuna", en: "Yuna" },
    phase: "2B",
    status: "planned",
  },
  {
    id: "hyunwoo",
    names: { ko: "현우", vi: "Hyunwoo", en: "Hyunwoo" },
    phase: "2B",
    status: "planned",
  },
];
