import { z } from "zod";
export type Direction = "down" | "left" | "right" | "up";
const Choice = z.union([z.literal(0), z.literal(1)]);
const AvatarPreferences = z.object({
  hair: Choice,
  outfit: Choice,
  accessory: z.boolean(),
});
export type AvatarPreferences = z.infer<typeof AvatarPreferences>;
export const defaultAvatarPreferences: AvatarPreferences = {
  hair: 0,
  outfit: 0,
  accessory: true,
};
export function decodeAvatarPreferences(raw: string | null): AvatarPreferences {
  try {
    const r = AvatarPreferences.safeParse(JSON.parse(raw ?? "null"));
    return r.success ? r.data : { ...defaultAvatarPreferences };
  } catch {
    return { ...defaultAvatarPreferences };
  }
}
export function inputVector(x: number, y: number): { x: number; y: number } {
  const length = Math.hypot(x, y);
  return length ? { x: x / length, y: y / length } : { x: 0, y: 0 };
}
export function facing(x: number, y: number, previous: Direction): Direction {
  if (!x && !y) return previous;
  return Math.abs(x) > Math.abs(y)
    ? x < 0
      ? "left"
      : "right"
    : y < 0
      ? "up"
      : "down";
}
export const ContentLabel = z.object({
  id: z.string().regex(/^[a-z-]+$/),
  ko: z
    .string()
    .min(1)
    .refine((v) => v === v.normalize("NFC"), "NFC required"),
  vi: z.string().min(1),
  provenance: z.literal("ORIGINAL"),
  review: z.enum(["PENDING_HUMAN_REVIEW", "REVIEWED"]),
});
