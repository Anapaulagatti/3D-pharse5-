import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import {
  validateRightsInventory,
  assertReleaseAllowed,
} from "../src/rights/contract.ts";
const root = new URL("../", import.meta.url);
export function checkAssetRights(profile = "private-review") {
  const read = (p) => JSON.parse(readFileSync(new URL(p, root), "utf8"));
  const ids = [
    "phase3a/registry.json",
    "phase3a-npc-expansion/modern-definitions.json",
    "phase3a-final-six/definitions.json",
  ].flatMap((p) => read("assets-src/npcs/" + p).npcs.map((n) => n.id));
  const q = validateRightsInventory(
    read("assets-src/rights/npc-inventory.json"),
    ids,
  );
  assertReleaseAllowed(q, profile);
  return {
    profile,
    assets: q.assets.length,
    publicApproved: q.assets.filter((a) => a.approvedForCommercialRelease)
      .length,
  };
}
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  try {
    console.log(
      checkAssetRights(
        process.argv.includes("--public") ? "public" : "private-review",
      ),
    );
  } catch (e) {
    console.error(e.message);
    process.exitCode = 1;
  }
}
