/** New scoped phase adapter: same Phaser game, same review portal, full26 catalog. */
import { build, createServer } from "vite";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { checkAssetRights } from "../rights-gate.mjs";
const sourcePaths = ["src", "tools", "tests", "public", "assets-src", "review-portal", "index.html", "package.json", "vite.config.ts"];
execFileSync("git", ["diff", "--exit-code", "HEAD", "--", ...sourcePaths]);
if (execFileSync("git", ["ls-files", "--others", "--exclude-standard", ...sourcePaths], {encoding:"utf8"}).trim()) throw Error("Uncheckpointed source assets");
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

const out = path.resolve(process.env.REVIEW_OUT ?? ".cache/roadmap-v2-review");
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
    phase: "Phase 3B-D · physical world gameplay",
    slug: "3b-d-in-world",
    base: "/3D-pharse5-review/",
    gameRef: ref,
    gameCommit: ref,
    portalCommit: ref,
    dirty: false,
    sourceCleanGate: "Tracked and untracked source/tool/test/art files checked; ongoing docs-only QA outputs excluded",
    builtAt: new Date().toISOString(),
    exposure: "PRIVATE_CANDIDATE_EXACT_PUBLIC_APPROVAL_PENDING",
  }),
);
// Explicit runtime closure previously supplied by assemble.py; no blanket directory copy.
const activeAssets = JSON.parse(execFileSync("python3", ["tools/phase3bd/runtime_assets.py"], {encoding:"utf8"}));
for (const name of activeAssets) {
  const dest = path.join(out,"play",name);
  await fs.mkdir(path.dirname(dest),{recursive:true});
  await fs.copyFile(path.join("public",name),dest);
}
execFileSync("python3", ["tools/phase3bd/world_guard.py","--artifact",path.join(out,"play")],{stdio:"inherit"});
// Keep existing portal framework. Only candidate metadata/copy/links change.
const previous=process.env.PREVIOUS_PORTAL;
if(!previous)throw Error('Explicit previous approved portal required');
for(const name of ['index.html','portal.css','portal.mjs','catalog.json','history.json','LICENSE','LICENSES.md','licenses','thumbs'])await fs.cp(path.join(previous,name),path.join(out,name),{recursive:true});
let html=await fs.readFile(path.join(out,'index.html'),'utf8');
html=html.replace(/<nav aria-label="Review">[\s\S]*?<\/nav>/,'<nav aria-label="Review"><a href="review/">V2 · Farm / Interiors / Quest</a><a href="#play">Chơi</a><a href="#npcs">26 NPC</a><a href="#life">Daily Life</a><a href="#qa">QA / quyền</a><a href="#feedback">Góp ý</a><a href="#history">Rollback</a></nav>');
html=html.replace(/Chỉ dùng trong staging[\s\S]*?thương mại\./,'Candidate cục bộ để nghiệm thu. Public build mới cần duyệt đúng manifest; không phải phát hành thương mại.');
html=html.replace(/Thêm lịch riêng,[\s\S]*?không giả là video build mới\./,'V2 thêm crop progression, icon HUD, ba phòng Phaser và chuỗi ghép bảng–giao sách. Các NPC và nhân vật đã duyệt giữ nguyên; footage mới trong gallery.');
html=html.replace(/20 NPC: LOW_CONCERN[\s\S]*?trước xuất bản\./,'26 NPC/12 nhân vật/24 cosmetics giữ nguyên byte từ bản public đã duyệt1a6e5a58. Art crop/prop mới do dự án tự vẽ native bằng mã, không có input bên thứ ba. Điều khoản OpenAI cũ dựa trên xác nhận chủ dự án; không tuyên bố clearance pháp lý. New public exposure và Korean/art review vẫn PENDING.');
html=html.replace(/Phase 3B-A: chờ chủ dự án duyệt[\s\S]*?NOT TESTED\./,'V2 local candidate · chờ duyệt tổng hợp. Live backend/multiplayer/ads chưa triển khai. Physical Android/iPhone/GPU: NOT TESTED.');
await fs.writeFile(path.join(out,'index.html'),html);
let js=await fs.readFile(path.join(out,'portal.mjs'),'utf8');js=js.replace('Điều khoản tạo art: UNKNOWN. Public exposure: NOT APPROVED.','Giữ nguyên art từ public baseline1a6e5a58; hồ sơ điều khoản cũ được giữ. Public exposure của build V2: PENDING.').replace('Hiện tại · Phase 3B-A','NPC giữ nguyên · V2').replace('Sprite pixel-identical. Chỉ hành vi thay đổi; không tái tạo artwork.','NPC sprite giữ nguyên. Crop và interior mới nằm trong gallery riêng.');await fs.writeFile(path.join(out,'portal.mjs'),js);
const catalog=JSON.parse(await fs.readFile(path.join(out,'catalog.json'),'utf8'));
for(const npc of catalog.npcs){npc.risk='PRIOR_REVIEW_RETAINED_NO_NEW_SPECIFIC_CONCERN';npc.publication='UNCHANGED_PRIOR_PUBLIC_PREVIEW_ASSET; NEW_BUILD_PENDING';}
await fs.writeFile(path.join(out,'catalog.json'),JSON.stringify(catalog,null,2));
const history=JSON.parse(await fs.readFile(path.join(out,'history.json'),'utf8'));for(const row of history.snapshots){row.phase+=' · Git archive (online)';row.path='https://github.com/Anapaulagatti/3D-pharse5-review/tree/1a6e5a58a8fb515730e553a30980d2ffb7274da6/'+row.path;}await fs.writeFile(path.join(out,'history.json'),JSON.stringify(history,null,2));
const old=JSON.parse(await fs.readFile(path.join(previous,'version.json'),'utf8'));await fs.writeFile(path.join(out,'version.json'),JSON.stringify({...old,phase:'Roadmap V2 local playable candidate',slug:'roadmap-v2-local',gameRef:ref,gameCommit:ref,portalCommit:ref,builtAt:new Date().toISOString(),archived:false,currentPath:'./',publicExposure:'PENDING_EXACT_OWNER_APPROVAL'},null,2));
await fs.writeFile(path.join(out,'phase.json'),JSON.stringify({phase:'Roadmap V2 local candidate',gameRef:ref,publicExposure:'PENDING_EXACT_OWNER_APPROVAL'},null,2));
await fs.writeFile(path.join(out,'qa.json'),JSON.stringify({status:'VALIDATION_IN_PROGRESS',summary:'Local candidate. Final QA packet must replace this before freeze. Hardware and human art/Korean review not PASS.'},null,2));
await fs.unlink(path.join(out,'build-input.json'));
console.log('Prepared isolated current candidate '+out+' source '+ref+'; no deployment');
