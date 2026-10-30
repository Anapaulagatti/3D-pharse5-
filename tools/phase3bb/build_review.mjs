/** New scoped phase adapter: same Phaser game, same review portal, full26 catalog. */
import { build } from "vite";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { checkAssetRights } from "../rights-gate.mjs";
checkAssetRights("private-review");
const out = path.resolve(process.env.REVIEW_OUT ?? ".cache/phase3bb-review");
if (!out.startsWith(path.resolve(".cache") + path.sep)) throw Error("Private candidate must remain in .cache");
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
    phase: "Phase 3B-B · movement / head cosmetics / fictional26",
    slug: "3b-b",
    base: "/3D-pharse5-review/",
    gameRef: ref,
    gameCommit: ref,
    portalCommit: ref,
    dirty: true,
    builtAt: new Date().toISOString(),
    exposure: "PRIVATE_CANDIDATE_EXACT_PUBLIC_APPROVAL_PENDING",
  }),
);
execFileSync("python3", ["tools/phase3bb/assemble.py", out], {
  stdio: "inherit",
});
