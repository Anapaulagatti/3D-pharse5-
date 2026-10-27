import { z } from "zod";
import { directions, type AtlasData } from "../characters/types";
export const pointSchema = z.tuple([z.number().finite(), z.number().finite()]);
const clipSchema = z
  .object({
    frames: z.array(z.string()).min(1),
    durationsMs: z.array(z.number().positive()),
    loop: z.boolean(),
  })
  .superRefine((v, c) => {
    if (v.frames.length !== v.durationsMs.length)
      c.addIssue({ code: "custom", message: "NPC duration/frame mismatch" });
  });
export const npcSchema = z
  .object({
    id: z.string().regex(/^npc-[a-z][a-z0-9-]*$/),
    names: z.object({ vi: z.string().min(1), ko: z.string().regex(/[가-힣]/) }),
    occupation: z.string().min(1),
    homeZone: z.enum([
      "palace",
      "modern",
      "station",
      "jeju",
      "farm",
      "nature-leisure",
      "coast",
    ]),
    spawn: pointSchema,
    interactionPosition: pointSchema,
    reviewSpawn: pointSchema,
    direction: z.enum(directions),
    footprint: z.tuple([
      z.number().int().min(1).max(20),
      z.number().int().min(1).max(8),
    ]),
    route: z.array(pointSchema).min(2).max(12),
    idleBehavior: z.string().min(1),
    walkSpeed: z.number().min(18).max(45),
    interactionRadius: z.number().min(64).max(110),
    assets: z.object({
      texture: z.string(),
      atlas: z.string(),
      key: z.string().regex(/^npc-/),
    }),
    animations: z.record(z.string(), clipSchema),
    dialogueId: z.string(),
    future: z.object({
      questProviderId: z.string().nullable(),
      shopProviderId: z.string().nullable(),
      learningTopicTags: z.array(z.string()),
    }),
  })
  .superRefine((v, c) => {
    for (const d of directions)
      for (const a of ["idle", "walk", "greet", "activity"]) {
        const clip = v.animations[`${a}-${d}`];
        if (!clip || (a === "walk" && new Set(clip.frames).size !== 8))
          c.addIssue({
            code: "custom",
            message: `Missing native NPC clip ${a}-${d}`,
          });
      }
    if (new Set(v.route.map((p) => p.join(","))).size !== v.route.length)
      c.addIssue({ code: "custom", message: "Duplicate route waypoint" });
    if (v.assets.key !== v.id)
      c.addIssue({ code: "custom", message: "NPC texture ownership mismatch" });
  });
export type NPCDefinition = z.infer<typeof npcSchema>;
export type Point = [number, number];
export type NPCDirection = (typeof directions)[number];
export const npcStates = [
  "IDLE",
  "LOOK_AROUND",
  "PATROL",
  "MOVE_TO_WAYPOINT",
  "WAIT",
  "GREET",
  "TALK",
  "RETURN_TO_ACTIVITY",
] as const;
export type NPCState = (typeof npcStates)[number];
export const dialogueSchema = z.object({
  id: z.string(),
  npcId: z.string(),
  content: z.object({ ko: z.string().regex(/[가-힣]/), vi: z.string().min(1) }),
  hint: z.object({ ko: z.string(), vi: z.string() }),
  choices: z
    .array(
      z.object({
        id: z.string(),
        label: z.object({ ko: z.string(), vi: z.string() }),
        next: z.string(),
      }),
    )
    .max(4),
  next: z.string().nullable(),
  conditions: z.array(z.literal("always")),
  futureQuestHook: z.string().nullable(),
  lessonTopicTags: z.array(z.string()),
});
export type DialogueNode = z.infer<typeof dialogueSchema>;
/** Future authenticated integrations only; client appearance/NPC state is never ownership or lesson proof. */
export interface AuthenticatedLearningContext {
  subjectId: string;
  curriculumIds: readonly string[];
  verifiedCompletedLessonIds: readonly string[];
  verifiedAt: string;
}
export interface NPCLearningContextProvider {
  readVerifiedContext(): Promise<AuthenticatedLearningContext | null>;
}
export interface NPCQuestProvider {
  readonly id: string;
}
export interface NPCShopProvider {
  readonly id: string;
}
export function validateNPCAtlas(
  def: NPCDefinition,
  atlas: AtlasData,
  width: number,
  height: number,
) {
  for (const clip of Object.values(def.animations))
    for (const name of clip.frames) {
      const f = atlas.frames?.[name]?.frame;
      if (
        !f ||
        f.w !== 96 ||
        f.h !== 112 ||
        ![f.x, f.y].every(Number.isInteger) ||
        f.x < 0 ||
        f.y < 0 ||
        f.x + 96 > width ||
        f.y + 112 > height
      )
        throw Error(`Missing/out-of-bounds NPC cell ${def.id}/${name}`);
    }
}
