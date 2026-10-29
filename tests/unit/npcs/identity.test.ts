import { describe, expect, it } from "vitest";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import {
  historicalIdentities,
  identityPresentationSchema,
  presentNPCIdentity,
  presentArchiveDialogue,
} from "../../../src/npcs/identity";
import {
  historyArtCatalog,
  productionHistoryCount,
  selectNPCCatalog,
  verifiedHistoricalClaimCount,
} from "../../../src/npcs/history";
import { npcCatalog } from "../../../src/npcs/catalog";
import approved from "../../../docs/phase3a-finalization/APPROVED_BASELINE.json";

describe("approved26NPC identity and rights separation", () => {
  it("keeps all26source packs,world,players and cosmetic assets byte-identical to human-approved review", () => {
    const files = Object.entries(approved.files).filter(
      ([p]) =>
        p.startsWith("assets-src/npcs/") ||
        p.startsWith("assets-src/characters/") ||
        p.startsWith("assets-src/cosmetics/") ||
        p.startsWith("public/assets/"),
    );
    expect(files.length).toBeGreaterThan(5000);
    for (const [path, hash] of files)
      expect(
        createHash("sha256").update(readFileSync(path)).digest("hex"),
        path,
      ).toBe(hash);
  });
  it("registers26unique approved actors independently of URL flags without claiming verified history", () => {
    for (const query of [
      "",
      "qa",
      "qa&historyArtReview=0",
      "historyArtReview=1",
    ]) {
      const registry = selectNPCCatalog(new URLSearchParams(query));
      expect(registry).toBe(historyArtCatalog);
      expect(registry.npcs).toHaveLength(26);
      expect(new Set(registry.npcs.map((n) => n.id)).size).toBe(26);
    }
    expect(productionHistoryCount).toBe(6);
    expect(verifiedHistoricalClaimCount).toBe(0);
    expect(npcCatalog.npcs).toHaveLength(20); // Original living collection remains intact.
  });
  it("uses six owner-selected fictional names without claiming legal clearance", () => {
    expect(historicalIdentities).toHaveLength(6);
    for (const identity of historicalIdentities) {
      expect(identity.identityKind).toBe("original-fictional");
      expect(identity.publicName).toEqual(identity.fictionalAlias);
      expect(identity.identityDecision).toBe(
        "owner-directed-fictional-identity",
      );
      expect(identity).not.toHaveProperty("historicalReference");
      expect(identity.fallbackEvidence?.depictionStatus).toBe(
        "reviewed-no-specific-copy-identified-not-legal-clearance",
      );
      expect(identity.artworkAction).toBe("preserve-byte-identical");
      expect(identity.commercialReleaseStatus).toBe("review-required");
      expect(identity.generatedAssetTermsStatus).toBe(
        "not-independently-confirmed",
      );
      expect(identity.factCardIds).toEqual([]);
    }
  });
  it("does not permit a fictional rename without separate identity and depiction review", () => {
    const fiction = {
      ...historicalIdentities[0],
      identityKind: "original-fictional",
      publicName: { ko: "테스트 안내인", vi: "Người dẫn chuyện thử" },
      fictionalAlias: { ko: "테스트 안내인", vi: "Người dẫn chuyện thử" },
      identityDecision: "fictional-fallback-approved",
      fallbackEvidence: null,
    };
    expect(identityPresentationSchema.safeParse(fiction).success).toBe(false);
    expect(
      identityPresentationSchema.safeParse({
        ...fiction,
        fallbackEvidence: {
          identityDecisionReference: "unit-fixture-only",
          depictionDecisionReference: "unit-fixture-only",
          depictionStatus: "not-reviewed",
        },
      }).success,
    ).toBe(false);
    expect(
      identityPresentationSchema.safeParse({
        ...fiction,
        publicName: { ko: "다른 이름", vi: "Tên khác với bí danh" },
      }).success,
    ).toBe(false);
  });
  it("can migrate a reviewed fictional presentation without changing IDs,assets,clips,routes or saved keys", () => {
    const base = historyArtCatalog.get(historicalIdentities[0].npcId)!;
    const fiction = identityPresentationSchema.parse({
      ...historicalIdentities[0],
      identityKind: "original-fictional",
      publicName: { ko: "테스트 안내인", vi: "Người dẫn chuyện thử" },
      fictionalAlias: { ko: "테스트 안내인", vi: "Người dẫn chuyện thử" },
      identityDecision: "fictional-fallback-approved",
      fallbackEvidence: {
        identityDecisionReference: "unit-fixture-only-not-shipped",
        depictionDecisionReference: "unit-fixture-only-not-shipped",
        depictionStatus: "independent-reviewed",
      },
    });
    const after = presentNPCIdentity(base, fiction);
    expect(after.id).toBe(base.id);
    expect(after.assets).toBe(base.assets);
    expect(after.animations).toBe(base.animations);
    expect(after.route).toBe(base.route);
    expect(after.reviewSpawn).toBe(base.reviewSpawn);
    expect(after.dialogueId).toBe(base.dialogueId);
    expect(after.future).toBe(base.future);
    expect(after.names).toEqual(fiction.publicName);
    expect(fiction.commercialReleaseStatus).toBe("review-required"); // A new name does not grant clearance.
    const notice = historyArtCatalog.nodes.get(base.id + "-notice")!;
    const migrated = presentArchiveDialogue(notice, fiction);
    expect(migrated.id).toBe(notice.id);
    expect(migrated.next).toBe(notice.next);
    expect(migrated.content.ko).toContain("가상 인물");
    expect(migrated.content.vi).toContain("nhân vật hư cấu");
    expect(() =>
      presentArchiveDialogue(
        { ...notice, id: base.id + "-biography" },
        fiction,
      ),
    ).toThrow("independently rewritten");
  });
  it("keeps all original20definitions/dialogues untouched and six reconstruction graphs truthful", () => {
    for (const n of npcCatalog.npcs)
      expect(historyArtCatalog.get(n.id)).toEqual(n);
    for (const [id, node] of npcCatalog.nodes)
      expect(historyArtCatalog.nodes.get(id)).toEqual(node);
    for (const identity of historicalIdentities) {
      const nodes = [...historyArtCatalog.nodes.values()].filter(
        (n) => n.npcId === identity.npcId,
      );
      expect(nodes).toHaveLength(6);
      expect(nodes.find((n) => n.id.endsWith("-notice"))!.content.vi).toContain(
        "kiểm chứng",
      );
      expect(
        nodes.some((n) =>
          /미술 시안|bản thử mỹ thuật/i.test(n.content.ko + " " + n.content.vi),
        ),
      ).toBe(false);
      for (const n of nodes) expect(n.futureQuestHook).toBeNull();
    }
  });
});
