import { describe, it, expect } from "vitest";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { npcCatalog, modernVisitors } from "../../../src/npcs/catalog";
import {
  historyArtCatalog,
  historyCandidates,
  selectNPCCatalog,
  historyArtReviewEnabled,
  applyHistorySelection,
  productionHistoryCount,
  verifiedHistoricalClaimCount,
} from "../../../src/npcs/history";
import baseline from "../../../docs/phase3a-final-six/BASELINE_MANIFEST.json";
import { validateNPCAtlas } from "../../../src/npcs/types";
import evidence from "../../../docs/phase3a-final-six/SOURCE_EVIDENCE.json";
describe("six historical art candidates without fabricated source verification", () => {
  it("retains the exact20 live definitions and100 existing nodes", () => {
    expect(npcCatalog.npcs).toHaveLength(20);
    for (const def of npcCatalog.npcs)
      expect(historyArtCatalog.get(def.id)).toEqual(def);
    for (const [id, node] of npcCatalog.nodes)
      expect(historyArtCatalog.nodes.get(id)).toEqual(node);
  });
  it("has exactly six distinct requested IDs and26 validated candidate definitions", () => {
    expect(historyArtCatalog.npcs).toHaveLength(26);
    expect(new Set(historyArtCatalog.npcs.map((n) => n.id)).size).toBe(26);
    expect(historyCandidates.map((h) => h.id)).toEqual(
      ["seondeok", "sejong", "jang", "saimdang", "yi", "yu"].map(
        (id) => "npc-history-" + id,
      ),
    );
    expect(historyCandidates.map((h) => h.chronologyOrder)).toEqual([
      0, 1, 2, 3, 4, 5,
    ]);
  });
  it("never equates a failed request or an owner anchor with verified history", () => {
    expect(evidence.verifiedClaims).toBe(0);
    expect(evidence.claims.every((c) => c.status === "UNVERIFIED")).toBe(true);
    expect(evidence.claims.every((c) => c.supportingExcerpt === null)).toBe(
      true,
    );
    expect(productionHistoryCount).toBe(6);
    expect(verifiedHistoricalClaimCount).toBe(0);
    for (const query of [
      "",
      "qa",
      "historyArtReview=1",
      "qa&historyArtReview=0",
    ])
      expect(selectNPCCatalog(new URLSearchParams(query))).toBe(
        historyArtCatalog,
      );
    expect(
      historyArtReviewEnabled(new URLSearchParams("qa&historyArtReview=1")),
    ).toBe(true);
    expect(selectNPCCatalog(new URLSearchParams("qa&historyArtReview=1"))).toBe(
      historyArtCatalog,
    );
  });
  it("substitutes only the selected host slot and any visitor sharing that slot", () => {
    const eligible = new Set(npcCatalog.npcs.map((n) => n.id));
    for (const h of historyCandidates) {
      const after = applyHistorySelection(eligible, h.id, modernVisitors);
      expect(after.has(h.id)).toBe(true);
      expect(after.has(h.hostResidentId)).toBe(false);
      expect([...after].filter((id) => id.startsWith("npc-history-"))).toEqual([
        h.id,
      ]);
      for (const v of modernVisitors.filter(
        (v) => v.hostResidentId === h.hostResidentId,
      ))
        expect(after.has(v.id)).toBe(false);
      expect(eligible.has(h.hostResidentId)).toBe(true);
      const def = historyArtCatalog.get(h.id)!;
      const host = npcCatalog.get(h.hostResidentId)!;
      expect(def.route).toEqual(host.route);
      expect(def.spawn).toEqual(host.spawn);
      expect(def.reviewSpawn).toEqual(host.reviewSpawn);
      expect(def.walkSpeed).toBe(host.walkSpeed);
    }
    expect(applyHistorySelection(eligible, "invalid", modernVisitors)).toEqual(
      eligible,
    );
  });
  it("keeps all twenty source illustrations, rigs, clips and atlases byte-identical", () => {
    const paths = Object.entries(baseline.files).filter(
      ([path]) =>
        path.startsWith("assets-src/npcs/") ||
        path.startsWith("public/assets/npcs/"),
    );
    expect(paths.length).toBeGreaterThan(3000);
    for (const [path, hash] of paths)
      expect(
        createHash("sha256").update(readFileSync(path)).digest("hex"),
        path,
      ).toBe(hash);
  });
  it("provides six reachable neutral review graphs with explicit reconstruction and inert lesson hooks", () => {
    for (const h of historyCandidates) {
      expect(h.reconstructionNotice.vi).toContain("chưa được kiểm chứng");
      expect(h.vocabulary).toHaveLength(4);
      const def = historyArtCatalog.get(h.id)!;
      const nodes = [...historyArtCatalog.nodes.values()].filter(
        (n) => n.npcId === h.id,
      );
      expect(nodes).toHaveLength(6);
      expect(
        nodes.find((n) => n.id === h.id + "-notice")?.content.vi,
      ).toContain("nhân vật hư cấu");
      expect(def.future.questProviderId).toBeNull();
      for (const node of nodes) {
        expect(node.futureQuestHook).toBeNull();
        expect(node.content.ko).toMatch(/[가-힣]/);
      }
    }
  });
  it("ships624 registered native cells in six independent PNG atlases without old-art fallback", () => {
    const hashes = new Set<string>();
    const oldHashes = new Set(
      npcCatalog.npcs.map((n) =>
        createHash("sha256")
          .update(readFileSync("public/" + n.assets.texture))
          .digest("hex"),
      ),
    );
    for (const h of historyCandidates) {
      const def = historyArtCatalog.get(h.id)!;
      const bytes = readFileSync("public/" + def.assets.texture);
      expect(bytes.subarray(1, 4).toString()).toBe("PNG");
      const width = bytes.readUInt32BE(16),
        height = bytes.readUInt32BE(20);
      expect([width, height]).toEqual([768, 1456]);
      const atlas = JSON.parse(
        readFileSync("public/" + def.assets.atlas, "utf8"),
      );
      expect(Object.keys(atlas.frames)).toHaveLength(104);
      validateNPCAtlas(def, atlas, width, height);
      const hash = createHash("sha256").update(bytes).digest("hex");
      expect(oldHashes.has(hash)).toBe(false);
      hashes.add(hash);
    }
    expect(hashes.size).toBe(6);
  });
});
