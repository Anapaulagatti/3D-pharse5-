import { describe, it, expect } from "vitest";
import { historicalIdentities } from "../../../src/npcs/identity";
import { runtimeNPCCatalog } from "../../../src/npcs/history";
import source from "../../../assets-src/npcs/phase3a-final-six/definitions.json";
import { npcSchema } from "../../../src/npcs/types";

const expected = [
  ["seondeok", "한연화", "Han Yeonhwa"],
  ["sejong", "백준서", "Baek Junseo"],
  ["jang", "남경우", "Nam Gyeongu"],
  ["saimdang", "윤화연", "Yun Hwayeon"],
  ["yi", "강무영", "Kang Muyeong"],
  ["yu", "서다은", "Seo Daeun"],
];
const oldNames = [
  "선덕여왕",
  "세종대왕",
  "장영실",
  "신사임당",
  "이순신",
  "유관순",
  "Seondeok",
  "Sejong",
  "Jang Yeong-sil",
  "Shin Saimdang",
  "Yi Sun-sin",
  "Yu Gwan-sun",
];

describe("owner-directed fictional archive presentation", () => {
  it("applies exactly the six proposed names while every non-presentation actor property is preserved", () => {
    for (const [suffix, ko, vi] of expected) {
      const id = "npc-history-" + suffix;
      const npc = runtimeNPCCatalog.get(id)!;
      const original = npcSchema.parse(source.npcs.find((n) => n.id === id));
      expect(npc.names).toEqual({ ko, vi });
      expect(npc.occupation).toContain("nhân vật hư cấu");
      const nonPresentation = (definition: typeof original) =>
        Object.fromEntries(
          Object.entries(definition).filter(
            ([key]) => !["names", "occupation"].includes(key),
          ),
        );
      expect(nonPresentation(npc)).toEqual(nonPresentation(original));
    }
  });
  it("contains no old personal identities or biographical achievements in any public actor or dialogue text", () => {
    for (const row of historicalIdentities) {
      const npc = runtimeNPCCatalog.get(row.npcId)!;
      const nodes = [...runtimeNPCCatalog.nodes.values()].filter(
        (n) => n.npcId === row.npcId,
      );
      expect(nodes).toHaveLength(6);
      const publicText = JSON.stringify([
        npc.names,
        npc.occupation,
        ...nodes.map((n) => [n.content, n.hint, n.choices.map((c) => c.label)]),
      ]);
      for (const old of oldNames) expect(publicText).not.toContain(old);
      expect(publicText).not.toMatch(
        /Hunminjeongeum|1446|1919|632|1598|훈민정음|명량/,
      );
      expect(
        nodes.find((n) => n.id.endsWith("-welcome"))!.content.vi,
      ).toContain(row.publicName.vi);
      expect(nodes.find((n) => n.id.endsWith("-notice"))!.content.ko).toContain(
        "실제 역사 인물이 아닙니다",
      );
      for (const node of nodes) expect(node.futureQuestHook).toBeNull();
    }
  });
  it("keeps references out of public mapping and does not infer commercial clearance from six aliases", () => {
    expect(historicalIdentities).toHaveLength(6);
    for (const row of historicalIdentities) {
      expect(row).not.toHaveProperty("historicalReference");
      expect(row.commercialReleaseStatus).toBe("review-required");
      expect(row.likenessStatus).toBe("not-legally-certified");
      expect(row.verifiedHistoricalContent).toBe("pending-excluded");
      expect(row.artworkAction).toBe("preserve-byte-identical");
    }
  });
});
