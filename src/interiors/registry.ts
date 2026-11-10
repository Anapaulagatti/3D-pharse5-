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
export type RoomPoint = readonly [number, number];
export interface RoomLayout {
  width: number;
  height: number;
  spawn: RoomPoint;
  exit: RoomPoint;
  actor: RoomPoint;
  fragment: RoomPoint;
  sign: RoomPoint;
  courier: RoomPoint;
  service: RoomPoint;
  props: readonly (readonly [string, number, number])[];
  solids: readonly (readonly [number, number, number, number])[];
  counters: readonly (readonly [number, number, number, number])[];
}
/** Native 1:1 rooms; each footprint, circulation and furnishing belongs to its building. */
export const roomLayouts: Record<InteriorDefinition["id"], RoomLayout> = {
  "seed-shop": {
    width: 704,
    height: 512,
    spawn: [112, 454],
    exit: [112, 480],
    actor: [510, 216],
    fragment: [174, 330],
    sign: [330, 372],
    courier: [410, 416],
    service: [580, 370],
    props: [
      ["market-window", 136, 128],
      ["market-window", 570, 128],
      ["seed-rack", 262, 238],
      ["counter", 510, 284],
      ["counter-side", 620, 352],
      ["seed-crates", 200, 428],
      ["packing-table", 480, 352],
      ["lamp", 364, 248],
      ["notice-board", 330, 372],
    ],
    solids: [
      [208, 190, 104, 44],
      [416, 254, 188, 30],
      [586, 286, 66, 62],
      [152, 390, 100, 34],
      [424, 324, 112, 24],
    ],
    counters: [[416, 254, 188, 30]],
  },
  bookshop: {
    width: 640,
    height: 544,
    spawn: [320, 482],
    exit: [320, 510],
    actor: [500, 224],
    fragment: [144, 304],
    sign: [490, 416],
    courier: [420, 450],
    service: [174, 432],
    props: [
      ["library-window", 320, 136],
      ["bookshelf", 104, 242],
      ["bookshelf", 238, 242],
      ["book-desk", 500, 288],
      ["reading-table", 294, 388],
      ["stool", 294, 438],
      ["book-stack", 398, 236],
      ["lamp", 410, 290],
      ["rune-board", 490, 416],
      ["notice-board", 174, 432],
    ],
    solids: [
      [48, 196, 112, 42],
      [182, 196, 112, 42],
      [442, 262, 116, 24],
      [236, 358, 116, 26],
      [276, 426, 36, 10],
    ],
    counters: [[442, 262, 116, 24]],
  },
  workshop: {
    width: 704,
    height: 480,
    spawn: [580, 410],
    exit: [580, 448],
    actor: [180, 190],
    fragment: [112, 330],
    sign: [548, 294],
    courier: [460, 354],
    service: [200, 352],
    props: [
      ["workshop-vent", 560, 122],
      ["tool-rack", 292, 166],
      ["workbench", 212, 260],
      ["packing-table", 460, 320],
      ["tool-stand", 200, 352],
      ["stool", 348, 274],
      ["lamp", 376, 184],
      ["notice-board", 548, 294],
    ],
    solids: [
      [104, 232, 212, 24],
      [218, 140, 148, 22],
      [404, 292, 112, 24],
      [164, 326, 72, 18],
    ],
    counters: [[104, 232, 212, 24]],
  },
};
// Compatibility default for older callers; new rooms always supply their own layout.
export const ROOM = roomLayouts.bookshop;
export const roomSolids = ROOM.solids;
export function roomWalkable(x: number, y: number, layout: RoomLayout = ROOM) {
  return (
    x >= 54 &&
    x <= layout.width - 54 &&
    y >= 152 &&
    y <= layout.height - 30 &&
    !layout.solids.some(
      ([a, b, w, h]) =>
        x > a - 14 && x < a + w + 14 && y > b - 3 && y < b + h + 7,
    )
  );
}
/** Counter tops block feet, but not face-to-face conversation across the low service counter. */
export function roomInteractionGround(
  x: number,
  y: number,
  layout: RoomLayout,
) {
  return (
    roomWalkable(x, y, layout) ||
    layout.counters.some(
      ([a, b, w, h]) =>
        x >= a - 14 && x <= a + w + 14 && y >= b - 3 && y <= b + h + 7,
    )
  );
}
export const INTERIOR_SAVE = "korean-arena-interior-v1";
export interface InteriorSave {
  version: 1;
  layoutVersion?: 2;
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
      (q.layoutVersion !== 2 ||
        roomWalkable(
          q.position[0],
          q.position[1],
          roomLayouts[q.id as InteriorDefinition["id"]],
        ))
      ? {
          ...q,
          position: roomWalkable(
            q.position[0],
            q.position[1],
            roomLayouts[q.id as InteriorDefinition["id"]],
          )
            ? q.position
            : [...roomLayouts[q.id as InteriorDefinition["id"]].spawn],
        }
      : undefined;
  } catch {
    return undefined;
  }
}
