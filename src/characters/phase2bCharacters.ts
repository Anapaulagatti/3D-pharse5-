import soriClips from "../../assets-src/characters/phase2b/sori/clips.json";
import jiwonClips from "../../assets-src/characters/phase2b/jiwon/clips.json";
import nariClips from "../../assets-src/characters/phase2b/nari/clips.json";
import taeyangClips from "../../assets-src/characters/phase2b/taeyang/clips.json";
import type { CharacterDefinition } from "./types";
/** Complete native review candidates. Future slots are removed by existing registry promotion. */
export const phase2bCharacters: CharacterDefinition[] = [
  {
    id: "sori",
    names: {
      ko: "소리",
      vi: "Sori",
    },
    description:
      "Cô bạn yêu âm nhạc, mang nhịp điệu vui tươi đến những con phố mới.",
    preview: "assets/characters/sori/preview-native.png",
    native: {
      width: 96,
      height: 112,
      anchor: [48, 100],
    },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: {
      walkSpeed: 60,
      runSpeed: 100,
      walkStride: 44,
      runStride: 64,
    },
    cosmetics: {
      palette: ["lavender", "cream", "plum"],
      outfit:
        "Lavender raglan bomber, tailored shorts, long socks and musical brooch",
      tags: ["original-design", "phase2b-review", "default-only"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Complete independent native pack, internal native art/phase gate inspected; actual Phaser wave evidence required; final human artistic acceptance pending",
    },
    assets: {
      key: "character-sori",
      texture: "assets/characters/sori/atlas.png",
      atlas: "assets/characters/sori/atlas.json",
    },
    animations: { ...soriClips, "social-front": soriClips["wave-front"] },
  },
  {
    id: "jiwon",
    names: {
      ko: "지원",
      vi: "Jiwon",
    },
    description:
      "Người bạn mê sách trầm tĩnh, luôn tò mò về những câu chuyện quanh mình.",
    preview: "assets/characters/jiwon/preview-native.png",
    native: {
      width: 96,
      height: 112,
      anchor: [48, 100],
    },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: {
      walkSpeed: 60,
      runSpeed: 100,
      walkStride: 44,
      runStride: 64,
    },
    cosmetics: {
      palette: ["navy", "beige", "warm-white"],
      outfit: "Cable-knit academic vest, rolled white shirt and book brooch",
      tags: ["original-design", "phase2b-review", "default-only"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Complete independent native pack, internal native art/phase gate inspected; actual Phaser wave evidence required; final human artistic acceptance pending",
    },
    assets: {
      key: "character-jiwon",
      texture: "assets/characters/jiwon/atlas.png",
      atlas: "assets/characters/jiwon/atlas.json",
    },
    animations: { ...jiwonClips, "social-front": jiwonClips["wave-front"] },
  },
  {
    id: "nari",
    names: {
      ko: "나리",
      vi: "Nari",
    },
    description:
      "Cô bạn yêu cây cỏ, thích khám phá khu vườn và những con đường tự nhiên.",
    preview: "assets/characters/nari/preview-native.png",
    native: {
      width: 96,
      height: 112,
      anchor: [48, 100],
    },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: {
      walkSpeed: 60,
      runSpeed: 100,
      walkStride: 44,
      runStride: 64,
    },
    cosmetics: {
      palette: ["sage", "yellow", "cream"],
      outfit:
        "Gardener field vest, yellow shirt, practical trousers and botanical pin",
      tags: ["original-design", "phase2b-review", "default-only"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Complete independent native pack, internal native art/phase gate inspected; actual Phaser wave evidence required; final human artistic acceptance pending",
    },
    assets: {
      key: "character-nari",
      texture: "assets/characters/nari/atlas.png",
      atlas: "assets/characters/nari/atlas.json",
    },
    animations: { ...nariClips, "social-front": nariClips["wave-front"] },
  },
  {
    id: "taeyang",
    names: {
      ko: "태양",
      vi: "Taeyang",
    },
    description: "Nhà thám hiểm thể thao đầy năng lượng và tự tin.",
    preview: "assets/characters/taeyang/preview-native.png",
    native: {
      width: 96,
      height: 112,
      anchor: [48, 100],
    },
    collision: {
      policy: "shared-world-native-contact",
      model: "swept-point-plus-native-mask",
      footprint: "approved-native-envelope",
    },
    movement: {
      walkSpeed: 60,
      runSpeed: 100,
      walkStride: 44,
      runStride: 64,
    },
    cosmetics: {
      palette: ["amber", "dark-blue", "cream"],
      outfit:
        "Athletic amber windbreaker, navy trekking trousers and adventure shoes",
      tags: ["original-design", "phase2b-review", "default-only"],
    },
    availability: {
      status: "playable",
      unlock: "free",
      reason:
        "Complete independent native pack, internal native art/phase gate inspected; actual Phaser wave evidence required; final human artistic acceptance pending",
    },
    assets: {
      key: "character-taeyang",
      texture: "assets/characters/taeyang/atlas.png",
      atlas: "assets/characters/taeyang/atlas.json",
    },
    animations: { ...taeyangClips, "social-front": taeyangClips["wave-front"] },
  },
];
