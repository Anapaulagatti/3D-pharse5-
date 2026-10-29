import { z } from "zod";
import source from "../../assets-src/npcs/daily-life/schedules.json";
import { dayPhases, phaseAt, seededChoice, type NPCWorldClock } from "./clock";
import type { NPCDefinition } from "./types";
export const activityTypes = [
  "WORK",
  "SHORT_BREAK",
  "WALK_AROUND",
  "SOCIAL_PAUSE",
  "REST",
  "COMMUTE_OR_REPOSITION",
] as const;
export type DailyActivity = (typeof activityTypes)[number];
export const scheduleSchema = z.object({
  npcId: z.string(),
  scheduleId: z.string(),
  context: z.enum(["present-day", "archive-story"]),
  zone: z.string(),
  entries: z
    .array(
      z.object({
        id: z.string(),
        phase: z.enum(dayPhases),
        activity: z.enum(activityTypes),
        anchorIndices: z.array(z.number().int().min(0)).min(1),
        durationGameMinutes: z.number().positive(),
        priority: z.literal(40),
        interruption: z.literal("player-first"),
        dialogueKey: z.string().nullable(),
      }),
    )
    .min(1),
});
export const dailySchedules = source.schedules.map((p) =>
  scheduleSchema.parse(p),
);
export interface ActivityIntent {
  id: string;
  activity: DailyActivity;
  anchorIndex: number;
  context: "present-day" | "archive-story";
  label: { vi: string; ko: string };
}
export const activityLabels: Record<DailyActivity, { vi: string; ko: string }> =
  {
    WORK: { vi: "Đang làm việc", ko: "일하는 중" },
    SHORT_BREAK: { vi: "Đang nghỉ ngắn", ko: "잠시 쉬는 중" },
    WALK_AROUND: { vi: "Đang đi một vòng", ko: "둘러보는 중" },
    SOCIAL_PAUSE: { vi: "Đang đón khách", ko: "손님을 맞이하는 중" },
    REST: { vi: "Đang nghỉ", ko: "쉬는 중" },
    COMMUTE_OR_REPOSITION: {
      vi: "Đang đi đến điểm hẹn",
      ko: "약속 장소로 가는 중",
    },
  };
export function resolveActivity(
  def: NPCDefinition,
  clock: ReturnType<NPCWorldClock["snapshot"]>,
  archiveElapsedMs = 0,
): ActivityIntent | undefined {
  const p = dailySchedules.find((p) => p.npcId === def.id);
  if (!p) return;
  if (p.zone !== def.homeZone) throw Error("Schedule zone mismatch " + def.id);
  const minute =
    p.context === "archive-story"
      ? (archiveElapsedMs / 1250) % 1440
      : clock.minute;
  const entry =
    p.context === "archive-story"
      ? p.entries[Math.floor(archiveElapsedMs / 8000) % p.entries.length]
      : (p.entries.find((e) => e.phase === phaseAt(minute)) ?? p.entries[0]);
  const i =
    (Math.floor(minute / entry.durationGameMinutes) +
      seededChoice(
        clock.seed,
        p.context === "archive-story" ? 0 : clock.day,
        entry.id,
        entry.anchorIndices.length,
      )) %
    entry.anchorIndices.length;
  const anchorIndex = entry.anchorIndices[i];
  if (!def.route[anchorIndex]) throw Error("Invalid schedule anchor " + def.id);
  return {
    id: entry.id,
    activity: entry.activity,
    anchorIndex,
    context: p.context,
    label: activityLabels[entry.activity],
  };
}
export function validateSchedules(definitions: readonly NPCDefinition[]) {
  const ids = new Set<string>();
  for (const p of dailySchedules) {
    const d = definitions.find((d) => d.id === p.npcId);
    if (!d || d.homeZone !== p.zone || ids.has(p.npcId))
      throw Error("Invalid schedule registration " + p.npcId);
    ids.add(p.npcId);
    if (
      new Set(p.entries.map((e) => e.id)).size !== p.entries.length ||
      new Set(p.entries.map((e) => e.phase)).size !== 5 ||
      (p.context === "archive-story") !== p.npcId.startsWith("npc-history-")
    )
      throw Error("Invalid phase/context " + p.npcId);
    for (const e of p.entries)
      for (const i of e.anchorIndices)
        if (!d.route[i]) throw Error("Invalid anchor " + p.npcId);
  }
  return ids.size;
}
