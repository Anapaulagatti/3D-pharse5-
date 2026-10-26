import { futureRoster, type FutureRosterSlot } from "./futureRoster";
import { phase2bCharacters } from "./phase2bCharacters";
import { phase2aCharacters } from "./newCharacters";
import haneulClips from "../../assets-src/characters/phase1b/haneul/clips.json";
import bomiClips from "../../assets-src/characters/phase1b/bomi/clips.json";
import minjunClips from "../../assets-src/characters/phase1b/minjun/clips.json";
import juni from "../../assets-src/juni-animation/runtime.json";
import { characterSchema, directions, type CharacterDefinition } from "./types";
const clips: CharacterDefinition["animations"] = {};
for (const action of ["idle", "walk", "run", "start", "stop"])
  for (const d of directions) {
    const times =
      action === "walk" || action === "run"
        ? Array(8).fill(100)
        : juni.durations[action as keyof typeof juni.durations];
    clips[`${action}-${d}`] = {
      frames: times.map((_, i) => `${action}-${d}-${i}`),
      durationsMs: [...times],
      loop: ["idle", "walk", "run"].includes(action),
    };
  }
for (const action of ["wave", "celebrate", "social"] as const)
  clips[`${action}-front`] = {
    frames: juni.durations[action].map((_, i) => `${action}-front-${i}`),
    durationsMs: [...juni.durations[action]],
    loop: false,
  };
clips.turn = {
  frames: Array.from({ length: 8 }, (_, i) => `turn-${i}`),
  durationsMs: Array(8).fill(50),
  loop: false,
};
const shared = {
  native: { width: 96, height: 112, anchor: [48, 100] as [number, number] },
  collision: {
    policy: "shared-world-native-contact" as const,
    model: "swept-point-plus-native-mask" as const,
    footprint: "pending-native-validation" as const,
  },
  movement: {
    walkSpeed: 60 as const,
    runSpeed: 100 as const,
    walkStride: 44,
    runStride: 64,
  },
};
const authoredClips = {
  haneul: haneulClips,
  bomi: bomiClips,
  minjun: minjunClips,
};
const definitions: CharacterDefinition[] = [
  {
    ...shared,
    id: "juni",
    collision: { ...shared.collision, footprint: "approved-native-envelope" },
    names: { ko: "주니", vi: "Juni" },
    description:
      "Người bạn đồng hành tự tin, yêu những góc phố và câu chuyện Hàn Quốc.",
    preview: "assets/juni/juni.png",
    assets: {
      texture: "assets/juni/juni.png",
      atlas: "assets/juni/juni.json",
      key: "juni",
    },
    animations: clips,
    cosmetics: {
      palette: ["ivory", "lilac", "navy"],
      outfit: "Approved Juni outfit",
      tags: ["original", "protected"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason: "Original approved144-frame atlas",
    },
  },
  ...(
    [
      [
        "haneul",
        "하늘",
        "Haneul",
        "Nhà thám hiểm vui vẻ, luôn sẵn sàng ghé thăm một con phố mới.",
        ["blue", "sand"],
        "Blue casual explorer",
      ],
      [
        "bomi",
        "보미",
        "Bomi",
        "Dịu dàng và tinh tế, mang nét duyên hanbok vào hành trình hôm nay.",
        ["coral", "cream"],
        "Modern hanbok-inspired jacket",
      ],
      [
        "minjun",
        "민준",
        "Minjun",
        "Người học trò tò mò, thích ghi lại những điều nhỏ bé trong chuyến đi.",
        ["sage", "cream"],
        "Student explorer with notebook",
      ],
    ] as const
  ).map(([id, ko, vi, description, palette, outfit]) => ({
    ...shared,
    id,
    names: { ko, vi },
    description,
    preview: `assets/characters/${id}/preview-native.png`,
    collision: {
      ...shared.collision,
      footprint: "approved-native-envelope" as const,
    },
    assets: {
      texture: `assets/characters/${id}/atlas.png`,
      atlas: `assets/characters/${id}/atlas.json`,
      key: `character-${id}`,
    },
    animations: authoredClips[id],
    cosmetics: { palette: [...palette], outfit, tags: ["original-design"] },
    availability: {
      status: "playable" as const,
      unlock: "free" as const,
      reason:
        "Human-approved Phase1B native pack,112 frames including final Juni-referenced front/back corrections",
    },
  })),
];
definitions.push(...phase2aCharacters, ...phase2bCharacters);
export class CharacterRegistry {
  readonly all: readonly CharacterDefinition[];
  readonly planned: readonly FutureRosterSlot[];
  constructor(defs: readonly CharacterDefinition[] = definitions) {
    this.all = defs.map((d) => characterSchema.parse(d));
    if (
      new Set(futureRoster.map((slot) => slot.id)).size !== futureRoster.length
    )
      throw Error("Duplicate planned character ID");
    this.planned = futureRoster.filter(
      (slot) => !this.all.some((def) => def.id === slot.id),
    );
    if (
      new Set([...this.all, ...this.planned].map((d) => d.id)).size !==
      this.all.length + this.planned.length
    )
      throw Error("Duplicate character ID");
    if (
      !this.all.some(
        (d) => d.id === "juni" && d.availability.status === "playable",
      )
    )
      throw Error("Playable Juni fallback required");
  }
  get(id: string) {
    return this.all.find((c) => c.id === id);
  }
  resolve(id: string) {
    const def = this.get(id);
    return def?.availability.status === "playable" ? def : this.get("juni")!;
  }
}
export const characterRegistry = new CharacterRegistry();
