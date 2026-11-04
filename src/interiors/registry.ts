/** Visible door approaches from canonical manifest target registry; facades never moved. */
export const interiors = [
  {
    id: "seed-shop",
    buildingId: "registration/cafe",
    name: "Góc hạt giống · 씨앗 가게",
    door: [717, 2605] as const,
    npc: "npc-minseo",
    kind: "market",
  },
  {
    id: "bookshop",
    buildingId: "registration/bookshop",
    name: "Hiệu sách · 서점",
    door: [1128, 2605] as const,
    npc: "npc-jiho",
    kind: "books",
  },
  {
    id: "workshop",
    buildingId: "registration/learning",
    name: "Xưởng cộng đồng · 공방",
    door: [1418, 2605] as const,
    npc: "npc-eunji",
    kind: "workshop",
  },
] as const;
export type InteriorDefinition = (typeof interiors)[number];
export const ROOM = {
  width: 640,
  height: 480,
  spawn: [320, 414] as const,
  exit: [320, 440] as const,
  actor: [414, 250] as const,
  fragment: [150, 308] as const,
  sign: [486, 304] as const,
  courier: [320, 284] as const,
};
export const roomSolids = [
  [40, 80, 88, 128],
  [490, 80, 100, 128],
  [260, 174, 120, 70],
  [80, 350, 72, 48],
  [488, 350, 72, 48],
] as const;
export function roomWalkable(x: number, y: number) {
  return (
    x >= 58 &&
    x <= 582 &&
    y >= 150 &&
    y <= 444 &&
    !roomSolids.some(
      ([a, b, w, h]) =>
        x > a - 20 && x < a + w + 20 && y > b - 4 && y < b + h + 8,
    )
  );
}
export const INTERIOR_SAVE = "korean-arena-interior-v1";
export interface InteriorSave {
  version: 1;
  id: string;
  world: [number, number];
  position: [number, number];
}
export function readInterior(): InteriorSave | undefined {
  try {
    const q = JSON.parse(localStorage.getItem(INTERIOR_SAVE) ?? "null");
    return q?.version === 1 &&
      interiors.some((r) => r.id === q.id) &&
      Array.isArray(q.world) &&
      q.world.length === 2 &&
      q.world.every(Number.isFinite) &&
      Math.hypot(
        q.world[0] - interiors.find((r) => r.id === q.id)!.door[0],
        q.world[1] - interiors.find((r) => r.id === q.id)!.door[1],
      ) < 55 &&
      Array.isArray(q.position) &&
      q.position.length === 2 &&
      q.position.every(Number.isFinite) &&
      roomWalkable(...(q.position as [number, number]))
      ? q
      : undefined;
  } catch {
    return undefined;
  }
}
