import doyunClips from "../../assets-src/characters/phase2a/doyun/clips.json";
import araClips from "../../assets-src/characters/phase2a/ara/clips.json";
import type { CharacterDefinition } from "./types";
export const phase2aCharacters: CharacterDefinition[] = [
  {
    id: "ara",
    names: { ko: "아라", vi: "Ara" },
    description:
      "Cô bạn miền biển tò mò, mang sắc ngọc lam đến từng chuyến đi.",
    preview: "assets/characters/ara/preview-native.png",
    native: { width: 96, height: 112, anchor: [48, 100] },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: { walkSpeed: 60, runSpeed: 100, walkStride: 44, runStride: 64 },
    cosmetics: {
      palette: ["turquoise", "cream", "chestnut"],
      outfit: "Coastal traveler jacket and culottes",
      tags: ["original-design", "phase2a-review"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Independent host-image identity,112 own-layer native frames; native art/locomotion gate inspected, final human Phase2A review pending",
    },
    assets: {
      key: "character-ara",
      texture: "assets/characters/ara/atlas.png",
      atlas: "assets/characters/ara/atlas.json",
    },
    animations: araClips,
  },
  {
    id: "doyun",
    names: { ko: "도윤", vi: "Doyun" },
    description:
      "Chàng trai thành phố vui vẻ, thích khám phá từng ngõ phố mới.",
    preview: "assets/characters/doyun/preview-native.png",
    native: { width: 96, height: 112, anchor: [48, 100] },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: { walkSpeed: 60, runSpeed: 100, walkStride: 44, runStride: 64 },
    cosmetics: {
      palette: ["muted-orange", "cocoa", "cream"],
      outfit: "Korean city overshirt and cuffed trousers",
      tags: ["original-design", "phase2a-review"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Independent host-image identity,112 own-layer native frames; native art/locomotion gate inspected, final human Phase2A review pending",
    },
    assets: {
      key: "character-doyun",
      texture: "assets/characters/doyun/atlas.png",
      atlas: "assets/characters/doyun/atlas.json",
    },
    animations: doyunClips,
  },
];
