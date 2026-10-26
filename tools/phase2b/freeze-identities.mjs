import ts from "typescript";
import vm from "node:vm";
import fs from "node:fs";
import crypto from "node:crypto";
const root = "docs/phase2b/approved-source-snapshots/",
  file = root + "src/characters/registry.ts";
const raw = fs.readFileSync(file, "utf8"),
  ast = ts.createSourceFile(file, raw, ts.ScriptTarget.Latest, true);
const stripped = ast.statements
  .filter((node) => !ts.isImportDeclaration(node))
  .map((node) => raw.slice(node.pos, node.end))
  .join("\n");
const code = ts.transpileModule(stripped, {
  compilerOptions: {
    module: ts.ModuleKind.CommonJS,
    target: ts.ScriptTarget.ES2022,
  },
}).outputText;
const peerRaw=fs.readFileSync(root+'src/characters/newCharacters.ts','utf8');
const peerAst=ts.createSourceFile('newCharacters.ts',peerRaw,ts.ScriptTarget.Latest,true);
const peerCode=ts.transpileModule(peerAst.statements.filter(n=>!ts.isImportDeclaration(n)).map(n=>peerRaw.slice(n.pos,n.end)).join('\n'),{compilerOptions:{module:ts.ModuleKind.CommonJS}}).outputText;
const peer={exports:{},araClips:JSON.parse(fs.readFileSync('assets-src/characters/phase2a/ara/clips.json','utf8')),doyunClips:JSON.parse(fs.readFileSync('assets-src/characters/phase2a/doyun/clips.json','utf8'))};vm.runInNewContext(peerCode,peer);
const context = {futureRoster:[],phase2aCharacters:peer.exports.phase2aCharacters,
  exports: {},
  characterSchema: { parse: (v) => v },
  directions: ["front", "back", "left", "right"],
  ...Object.fromEntries(
    ["haneul", "bomi", "minjun"].map((id) => [
      id + "Clips",
      JSON.parse(
        fs.readFileSync(
          `assets-src/characters/phase1b/${id}/clips.json`,
          "utf8",
        ),
      ),
    ]),
  ),
  juni: JSON.parse(
    fs.readFileSync("assets-src/juni-animation/runtime.json", "utf8"),
  ),
};
vm.runInNewContext(code, context, { timeout: 1000 });
const records = context.exports.characterRegistry.all;
if (records.map((d) => d.id).join(",") !== "juni,haneul,bomi,minjun,ara,doyun")
  throw Error("Wrong approval source");
fs.writeFileSync(
  "docs/phase2b/approved-identity-records.json",
  JSON.stringify(
    {
      sourceCommit: "ed75734d0e0865274ca0b82bab2495d78878d24b",
      characters: records,
      policy:
        "All identity/clip/native/movement fields stay equal; availability reason may record new human approval without altering art.",
    },
    null,
    2,
  ) + "\n",
);
