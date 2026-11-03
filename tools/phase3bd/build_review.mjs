/** New scoped phase adapter: same Phaser game, same review portal, full26 catalog. */
import { build, createServer } from "vite";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { checkAssetRights } from "../rights-gate.mjs";
checkAssetRights("private-review");
// Presentation-only public export: leave canonical provenance untouched, but do
// not deliver obsolete historical identity/date proposals in the public bundle.
const ssr = await createServer({
  configFile: false,
  server: { middlewareMode: true },
  appType: "custom",
});
let publicDefinitions, publicDialogues;
try {
  const identity = await ssr.ssrLoadModule("/src/npcs/identity.ts");
  const definitions = JSON.parse(
    await fs.readFile(
      "assets-src/npcs/phase3a-final-six/definitions.json",
      "utf8",
    ),
  );
  const dialogues = JSON.parse(
    await fs.readFile(
      "assets-src/npcs/phase3a-final-six/dialogues.json",
      "utf8",
    ),
  );
  const byId = new Map(
    identity.historicalIdentities.map((row) => [row.npcId, row]),
  );
  publicDefinitions = {
    ...definitions,
    npcs: definitions.npcs.map((row) =>
      identity.presentNPCIdentity(row, byId.get(row.id)),
    ),
  };
  publicDialogues = {
    ...dialogues,
    nodes: dialogues.nodes.map((row) =>
      identity.presentArchiveDialogue(row, byId.get(row.npcId)),
    ),
  };
} finally {
  await ssr.close();
}
const metadata = JSON.parse(
  await fs.readFile("assets-src/npcs/phase3a-final-six/metadata.json", "utf8"),
);
const publicMetadata = metadata.map(
  ({ id, hostResidentId, era, chronologyOrder }) => ({
    id,
    hostResidentId,
    era,
    chronologyOrder,
  }),
);

const out = path.resolve(process.env.REVIEW_OUT ?? ".cache/phase3bd-review");
if (!out.startsWith(path.resolve(".cache") + path.sep))
  throw Error("Private candidate must remain in .cache");
try {
  await fs.access(out);
  throw Error("Preserve previous review candidate; use a fresh version");
} catch (e) {
  if (e.code !== "ENOENT") throw e;
}
const ref = execFileSync("git", ["rev-parse", "HEAD"], {
  encoding: "utf8",
}).trim();
await build({
  configFile: false,
  base: "./",
  publicDir: false,
  define: {
    "import.meta.env.VITE_RELEASE_PROFILE": JSON.stringify("private-review"),
  },
  plugins: [
    {
      name: "fictional-presentation-no-private-history-proposals",
      load(id) {
        const clean = id.replaceAll("\\", "/");
        if (
          clean.endsWith("/assets-src/npcs/phase3a-final-six/definitions.json")
        )
          return JSON.stringify(publicDefinitions);
        if (clean.endsWith("/assets-src/npcs/phase3a-final-six/dialogues.json"))
          return JSON.stringify(publicDialogues);
        if (clean.endsWith("/assets-src/npcs/phase3a-final-six/metadata.json"))
          return JSON.stringify(publicMetadata);
      },
    },
    {
      name: "same-review-bridge",
      transformIndexHtml: {
        order: "pre",
        handler(html) {
          return html.replace(
            "<head>",
            '<head><meta name="korean-arena-release-profile" content="private-review"><meta name="review-home" content="../"><meta name="robots" content="noindex,nofollow"><script type="module" src="/src/review/bridge.ts"></script>',
          );
        },
      },
    },
    {
      name: "retain-public-summary-only",
      async transform(code, id) {
        if (!id.replaceAll("\\", "/").endsWith("/src/rights/runtime.ts"))
          return;
        const inv = JSON.parse(
          await fs.readFile("assets-src/rights/npc-inventory.json", "utf8"),
        );
        const safe = {
          assets: inv.assets.map((a) => ({
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
          .replace('import { validateRightsInventory } from "./contract";', "")
          .replace(
            /export const rightsInventory = validateRightsInventory\([\s\S]*?\);/,
            `export const rightsInventory = ${JSON.stringify(safe)};`,
          );
      },
    },
  ],
  build: {
    outDir: path.join(out, "play"),
    emptyOutDir: true,
    manifest: false,
    target: "es2022",
    chunkSizeWarningLimit: 1900,
    rolldownOptions: { input: { game: "index.html" } },
  },
});
await fs.writeFile(
  path.join(out, "build-input.json"),
  JSON.stringify({
    phase: "Phase 3B-D · farming / shops / source cleanup",
    slug: "3b-d",
    base: "/3D-pharse5-review/",
    gameRef: ref,
    gameCommit: ref,
    portalCommit: ref,
    dirty:
      execFileSync("git", ["status", "--porcelain", "--untracked-files=no"], {
        encoding: "utf8",
      }).trim().length > 0,
    builtAt: new Date().toISOString(),
    exposure: "PRIVATE_CANDIDATE_EXACT_PUBLIC_APPROVAL_PENDING",
  }),
);
execFileSync("python3", ["tools/phase3bd/assemble.py", out], {
  stdio: "inherit",
});
