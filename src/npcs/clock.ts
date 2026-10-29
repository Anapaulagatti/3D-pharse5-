export const lifeClockKey = "korean-arena-npc-life-v1";
export const dayPhases = [
  "night",
  "morning",
  "midday",
  "afternoon",
  "evening",
] as const;
export type DayPhase = (typeof dayPhases)[number];
export const phaseBoundaries: readonly { minute: number; phase: DayPhase }[] = [
  { minute: 0, phase: "night" },
  { minute: 300, phase: "morning" },
  { minute: 660, phase: "midday" },
  { minute: 840, phase: "afternoon" },
  { minute: 1080, phase: "evening" },
  { minute: 1320, phase: "night" },
];
export function phaseAt(
  minute: number,
  boundaries = phaseBoundaries,
): DayPhase {
  const t = ((minute % 1440) + 1440) % 1440;
  return [...boundaries].reverse().find((b) => b.minute <= t)!.phase;
}
export function seededChoice(
  seed: number,
  day: number,
  key: string,
  count: number,
) {
  let n = (seed ^ day) >>> 0;
  for (const c of key) n = Math.imul(n ^ c.charCodeAt(0), 16777619) >>> 0;
  return n % Math.max(1, count);
}
export class NPCWorldClock {
  day = 0;
  minute = 540;
  seed = 20261029;
  rate = 1;
  readonly dayDurationMs: number;
  private checkpoint: Record<string, string> = {};
  constructor(
    private storage?: Pick<Storage, "getItem" | "setItem">,
    dayDurationMs = 1800000,
  ) {
    this.dayDurationMs =
      Number.isFinite(dayDurationMs) && dayDurationMs >= 30000
        ? dayDurationMs
        : 1800000;
    try {
      const q = JSON.parse(storage?.getItem(lifeClockKey) ?? "null");
      if (
        q?.version === 1 &&
        Number.isSafeInteger(q.day) &&
        q.day >= 0 &&
        q.day < 1000000 &&
        Number.isFinite(q.minute) &&
        q.minute >= 0 &&
        q.minute < 1440 &&
        Number.isInteger(q.seed) &&
        q.seed >= 0 &&
        q.seed <= 0xffffffff
      ) {
        this.day = q.day;
        this.minute = q.minute;
        this.seed = q.seed;
        if (q.scheduleCheckpoint && typeof q.scheduleCheckpoint === "object")
          this.checkpoint = Object.fromEntries(
            Object.entries(q.scheduleCheckpoint)
              .filter(
                ([k, v]) =>
                  /^npc-[a-z-]+$/.test(k) &&
                  typeof v === "string" &&
                  v.length < 150,
              )
              .slice(0, 26),
          ) as Record<string, string>;
      }
    } catch {
      /* Additive NPC-only storage; existing records remain untouched. */
    }
  }
  tick(delta: number, paused = false, hidden = false) {
    if (paused || hidden || !Number.isFinite(delta)) return;
    this.minute +=
      (Math.max(0, Math.min(delta, 200)) * 1440 * this.rate) /
      this.dayDurationMs;
    if (this.minute >= 1440) {
      this.day += Math.floor(this.minute / 1440);
      this.minute %= 1440;
    }
  }
  setReviewTime(minute: number, rate = this.rate) {
    if (Number.isFinite(minute))
      this.minute = Math.max(0, Math.min(1439.999, minute));
    if (Number.isFinite(rate)) this.rate = Math.max(0, Math.min(60, rate));
  }
  save(checkpoint = this.checkpoint) {
    this.checkpoint = Object.fromEntries(
      Object.entries(checkpoint).slice(0, 26),
    );
    try {
      this.storage?.setItem(
        lifeClockKey,
        JSON.stringify({
          version: 1,
          day: this.day,
          minute: this.minute,
          seed: this.seed,
          scheduleCheckpoint: this.checkpoint,
        }),
      );
    } catch {
      /* Never reset other stores. */
    }
  }
  snapshot() {
    return {
      version: 1,
      day: this.day,
      minute: this.minute,
      phase: phaseAt(this.minute),
      seed: this.seed,
      rate: this.rate,
      dayDurationMs: this.dayDurationMs,
      scheduleCheckpoint: { ...this.checkpoint },
      offlineCatchup: false,
    };
  }
}
