import { z } from "zod";
export const directions = ["front", "back", "left", "right"] as const;
export type Direction = (typeof directions)[number];
export const characterSchema = z
  .object({
    id: z.string().regex(/^[a-z][a-z0-9-]*$/),
    names: z.object({ ko: z.string().min(1), vi: z.string().min(1) }),
    description: z.string().min(1),
    preview: z.string(),
    native: z.object({
      width: z.number().int().positive(),
      height: z.number().int().positive(),
      anchor: z.tuple([z.number().nonnegative(), z.number().nonnegative()]),
    }),
    collision: z.object({
      policy: z.literal("shared-world-native-contact"),
      model: z.literal("swept-point-plus-native-mask"),
      footprint: z.enum([
        "approved-native-envelope",
        "pending-native-validation",
      ]),
    }),
    movement: z.object({
      walkSpeed: z.literal(60),
      runSpeed: z.literal(100),
      walkStride: z.number().positive(),
      runStride: z.number().positive(),
    }),
    cosmetics: z.object({
      palette: z.array(z.string()),
      outfit: z.string(),
      tags: z.array(z.string()),
    }),
    availability: z.object({
      status: z.enum(["playable", "incomplete"]),
      unlock: z.literal("free"),
      reason: z.string(),
    }),
    assets: z
      .object({ texture: z.string(), atlas: z.string(), key: z.string() })
      .nullable(),
    animations: z.record(
      z.string(),
      z.object({
        frames: z.array(z.string()).min(1),
        durationsMs: z.array(z.number().positive()),
        loop: z.boolean(),
      }),
    ),
  })
  .superRefine((c, ctx) => {
    if (
      c.native.anchor[0] > c.native.width ||
      c.native.anchor[1] > c.native.height
    )
      ctx.addIssue({ code: "custom", message: "Anchor outside native cell" });
    if (c.availability.status !== "playable") return;
    if (c.collision.footprint !== "approved-native-envelope")
      ctx.addIssue({
        code: "custom",
        message: "Playable character needs verified native contact envelope",
      });
    if (!c.assets)
      ctx.addIssue({
        code: "custom",
        message: "Playable character needs atlas",
      });
    for (const name of [
      ...directions.flatMap((d) =>
        ["idle", "walk", "run"].map((a) => `${a}-${d}`),
      ),
      "wave-front",
      "celebrate-front",
    ]) {
      const a = c.animations[name];
      if (!a || a.frames.length !== a.durationsMs.length)
        ctx.addIssue({
          code: "custom",
          message: `Missing/invalid animation ${name}`,
        });
      if (a && /^(walk|run)-/.test(name) && new Set(a.frames).size < 8)
        ctx.addIssue({
          code: "custom",
          message: `Eight unique gait frames required: ${name}`,
        });
    }
  });
export type CharacterDefinition = z.infer<typeof characterSchema>;
export interface AtlasData {
  frames: Record<
    string,
    { frame: { x: number; y: number; w: number; h: number } }
  >;
  meta?: { size?: { w: number; h: number } };
}
export function validateAtlas(def: CharacterDefinition, data: AtlasData) {
  if (!data || !data.frames) throw Error(`Missing atlas data: ${def.id}`);
  for (const clip of Object.values(def.animations))
    for (const name of clip.frames) {
      const f = data.frames[name]?.frame;
      if (
        !f ||
        f.w !== def.native.width ||
        f.h !== def.native.height ||
        ![f.x, f.y, f.w, f.h].every(Number.isInteger) ||
        f.x < 0 ||
        f.y < 0
      )
        throw Error(`Missing/invalid native frame ${def.id}/${name}`);
      const size = data.meta?.size;
      if (size && (f.x + f.w > size.w || f.y + f.h > size.h))
        throw Error(`Out-of-atlas frame ${name}`);
    }
}
