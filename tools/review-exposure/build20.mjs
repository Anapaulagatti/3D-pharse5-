/** Isolated PRIVATE 20-NPC staging adapter, not public permission or a new engine. */
import { build } from "vite";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { checkAssetRights } from "../rights-gate.mjs";
checkAssetRights("private-review"); // The canonical public/commercial gate stays intact.
const out = path.resolve(".cache/exposure20-private");
try {
  await fs.access(out);
  throw Error("Preserve existing candidate; use a fresh output");
} catch (e) {
  if (e.code !== "ENOENT") throw e;
}
const original = await fs.readFile("src/npcs/history.ts", "utf8");
// Delete the historical imports and construction only in the build transform.
// Use the existing 20 living catalog, registry, manager, FSM and animations.
const prefix = original.slice(
  0,
  original.indexOf("/** Pure eligibility extension:"),
);
if (!prefix.includes("export const runtimeNPCCatalog = historyArtCatalog;"))
  throw Error("Unexpected history module");
let restricted = `import { npcCatalog } from './catalog';
export const historyArtCatalog = npcCatalog;
export const runtimeNPCCatalog = npcCatalog;
export const historyCandidates = [];
export const productionHistoryCount = 0;
export const verifiedHistoricalClaimCount = 0;
export function historyArtReviewEnabled() { return false; }
export function selectNPCCatalog() { return npcCatalog; }
export function applyHistorySelection(eligible) { return new Set(eligible); }
export class HistoryArtReview {
 selected;
 constructor() {}
 setContext() {}
 dispose() {}
}
`;
await build({
  configFile: false,
  base: "./",
  publicDir: false,
  define: {
    "import.meta.env.VITE_RELEASE_PROFILE": JSON.stringify("private-review"),
  },
  plugins: [
    {
      name: "isolated-20npc-no-canonical-edits",
      async load(id) {
        if (
          id
            .replaceAll("\\", "/")
            .endsWith("/assets-src/npcs/daily-life/schedules.json")
        ) {
          const q = JSON.parse(await fs.readFile(id, "utf8"));
          q.schedules = q.schedules.filter(
            (p) => !p.npcId.startsWith("npc-history-"),
          );
          return JSON.stringify(q);
        }
      },
      transformIndexHtml: {
        order: "pre",
        handler(html) {
          return html.replace(
            "<head>",
            '<head><meta name="korean-arena-release-profile" content="private-review"><meta name="review-home" content="../"><meta name="robots" content="noindex,nofollow"><script type="module" src="/src/review/bridge.ts"></script>',
          );
        },
      },
      async transform(code, id) {
        const clean = id.replaceAll("\\", "/");
        if (clean.endsWith("/src/npcs/history.ts")) return restricted;
        if (clean.endsWith("/src/npcs/schedules.ts"))
          return code.replace(
            "source.schedules.map(",
            "source.schedules.filter(p => !p.npcId.startsWith('npc-history-')).map(",
          );
        if (clean.endsWith("/src/rights/runtime.ts")) {
          const source = JSON.parse(
            await fs.readFile("assets-src/rights/npc-inventory.json", "utf8"),
          );
          const safe = {
            assets: source.assets
              .filter((a) => !a.stableId.startsWith("npc-history-"))
              .map((a) => ({
                stableId: a.stableId,
                publicName: a.publicName,
                risk: a.risk,
                publication: a.publication,
              })),
          };
          return code
            .replace(
              'import source from "../../assets-src/rights/npc-inventory.json";',
              "",
            )
            .replace(
              'import { validateRightsInventory } from "./contract";',
              "",
            )
            .replace(
              /export const rightsInventory = validateRightsInventory\([\s\S]*?\);/,
              `export const rightsInventory = ${JSON.stringify(safe)};`,
            );
        }
      },
    },
  ],
  build: {
    outDir: path.join(out, "play"),
    emptyOutDir: true,
    target: "es2022",
    manifest: true,
    chunkSizeWarningLimit: 1900,
    rolldownOptions: { input: { game: "index.html" } },
  },
});
execFileSync("python3", ["tools/review-exposure/package.py", out], {
  stdio: "inherit",
});
console.log(
  "PRIVATE STAGING ONLY: 20 actual NPCs, 6 excluded. UNKNOWN terms block public release.",
);
