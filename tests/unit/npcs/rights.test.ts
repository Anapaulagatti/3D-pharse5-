import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import source from "../../../assets-src/rights/npc-inventory.json";
import {
  validateRightsInventory,
  assertReleaseAllowed,
} from "../../../src/rights/contract";
import { runtimeNPCCatalog } from "../../../src/npcs/history";
const ids = runtimeNPCCatalog.npcs.map((n) => n.id);
describe("development approval is not commercial clearance", () => {
  it("covers every runtime ID/name and exact real source hashes", () => {
    const q = validateRightsInventory(source, ids);
    expect(q.assets).toHaveLength(26);
    for (const r of q.assets) {
      expect(r.publicName).toEqual(runtimeNPCCatalog.get(r.stableId)!.names);
      for (const e of r.sourceEvidence)
        expect(
          createHash("sha256").update(readFileSync(e.path)).digest("hex"),
        ).toBe(e.sha256);
      expect(r.artModified).toBe(false);
      expect(r.beforeAtlasSHA256).toBe(r.afterAtlasSHA256);
    }
  });
  it("permits private review and blocks all uncleared required public assets", () => {
    const q = validateRightsInventory(source, ids);
    expect(() => assertReleaseAllowed(q, "private-review")).not.toThrow();
    expect(() => assertReleaseAllowed(q, "public")).toThrow(
      "public build BLOCKED",
    );
    expect(
      q.assets.every((a) => a.publication === "BLOCKED_PENDING_REVIEW"),
    ).toBe(true);
  });
  it("rejects missing coverage and a fictional-name/boolean-only license claim", () => {
    const q = structuredClone(source);
    q.assets.pop();
    expect(() => validateRightsInventory(q, ids)).toThrow();
    const fake = structuredClone(source);
    fake.assets[0].approvedForCommercialRelease = true;
    expect(() => validateRightsInventory(fake, ids)).toThrow(
      "actual terms/review evidence",
    );
  });
  it("also blocks an included uncleared factual reference without required actors", () => {
    const q = validateRightsInventory(
      {
        ...source,
        assets: [],
        excludedReferences: [
          {
            id: "test-card",
            includedInGame: true,
            risk: "NEEDS_REVIEW",
            publication: "BLOCKED_PENDING_REVIEW",
            reason: "unverified",
          },
        ],
      },
      [],
    );
    expect(() => assertReleaseAllowed(q, "public")).toThrow("test-card");
  });
});
