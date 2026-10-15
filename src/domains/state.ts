import { z } from "zod";
export const Style = z.enum(["A", "B", "C"]);
export type Direction = "down" | "left" | "right" | "up";
export const Guest = z.object({
  version: z.literal(1),
  style: Style,
  visits: z.number().int().nonnegative().max(100000),
  metMira: z.boolean(),
});
export type GuestState = z.infer<typeof Guest>;
export const defaultGuest: GuestState = {
  version: 1,
  style: "B",
  visits: 0,
  metMira: false,
};
export function decodeGuest(raw: string | null): GuestState {
  try {
    const result = Guest.safeParse(JSON.parse(raw ?? "null"));
    return result.success ? result.data : { ...defaultGuest };
  } catch {
    return { ...defaultGuest };
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
