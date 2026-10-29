import { build } from "vite";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { checkAssetRights } from "../rights-gate.mjs";
const root = process.cwd();
const phase = JSON.parse(await fs.readFile("review-portal/phase.json", "utf8"));
if (!/^[a-z0-9-]+$/.test(phase.slug) || !/^[0-9a-f]{40}$/.test(phase.gameRef))
  throw Error("Invalid reviewed phase metadata");
const base = process.env.VITE_REVIEW_BASE ?? "/3D-pharse5-review/";
if (!/^\/(?:[A-Za-z0-9_-]+\/)*$/.test(base))
  throw Error(
    "VITE_REVIEW_BASE must be a static directory path with trailing slash",
  );
if (process.env.REVIEW_EXPOSURE && process.env.REVIEW_EXPOSURE !== "private")
  throw Error("PREVIEW_PUBLIC_EXPOSURE NOT APPROVED; no public output");
checkAssetRights("private-review");
const out = path.resolve(process.env.REVIEW_OUT ?? ".cache/review-portal");
if (!out.startsWith(root + "/.cache/"))
  throw Error("Output must stay within repository .cache/");
const gameCommit = execFileSync(
  "git",
  ["rev-parse", `${phase.gameRef}^{commit}`],
  {
    encoding: "utf8",
  },
).trim();
const portalCommit = execFileSync("git", ["rev-parse", "HEAD"], {
  encoding: "utf8",
}).trim();
const dirty = !!execFileSync("git", ["status", "--porcelain"], {
  encoding: "utf8",
}).trim();
const codePaths = [
  "src/game",
  "src/gate3",
  "src/npcs",
  "src/characters",
  "src/engine",
  "src/world",
  "src/platform",
  "src/rights",
  "assets-src/npcs",
  "public/assets",
];
if (
  execFileSync("git", ["diff", gameCommit, "--", ...codePaths], {
    encoding: "utf8",
    maxBuffer: 20 * 1024 * 1024,
  }).trim()
)
  throw Error(
    "Game/source asset differs from checked Phase3B-A snapshot; use an explicitly reviewed new phase adapter",
  );
await fs.mkdir(out, { recursive: true });
const play = path.join(out, "play");
await build({
  configFile: false,
  base: "./",
  publicDir: false,
  define: {
    "import.meta.env.VITE_RELEASE_PROFILE": JSON.stringify("private-review"),
  },
  plugins: [
    {
      name: "review-private-shell",
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
      name: "redact-internal-audit",
      async transform(code, id) {
        if (!id.replaceAll("\\", "/").endsWith("/src/rights/runtime.ts"))
          return;
        const records = JSON.parse(
          await fs.readFile("assets-src/rights/npc-inventory.json", "utf8"),
        );
        const safe = {
          assets: records.assets.map((a) => ({
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
    outDir: play,
    emptyOutDir: true,
    manifest: true,
    target: "es2022",
    chunkSizeWarningLimit: 1900,
    rolldownOptions: { input: { game: "index.html" } },
  },
});
await fs.writeFile(
  path.join(out, "build-input.json"),
  JSON.stringify(
    {
      ...phase,
      base,
      gameCommit,
      portalCommit,
      dirty,
      builtAt: new Date().toISOString(),
      exposure: "PRIVATE_ONLY_NOT_DEPLOYED",
    },
    null,
    2,
  ),
);
execFileSync("python3", ["tools/review-portal/assemble.py", out], {
  stdio: "inherit",
});
console.log(`PRIVATE candidate ${out}; NOT DEPLOYED; base ${base}`);
