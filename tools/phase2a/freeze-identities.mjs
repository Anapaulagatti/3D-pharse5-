import ts from "typescript";
import vm from "node:vm";
import fs from "node:fs";
import crypto from "node:crypto";
const root = "docs/phase2a/approved-definition-snapshots/",
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
const context = {
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
if (records.map((d) => d.id).join(",") !== "juni,haneul,bomi,minjun")
  throw Error("Wrong approval source");
fs.writeFileSync(
  "docs/phase2a/approved-identity-records.json",
  JSON.stringify(
    {
      sourceCommit: "51ac4b4f20f0af2f26d1566988580d92c0612356",
      characters: records,
      policy:
        "All identity/clip/native/movement fields stay equal; availability reason may record new human approval without altering art.",
    },
    null,
    2,
  ) + "\n",
);
const manifest = JSON.parse(
  fs.readFileSync("docs/phase2a/approved-four-characters.json", "utf8"),
);
manifest.definitionSnapshots = Object.fromEntries(
  [
    "src/characters/registry.ts",
    "src/characters/types.ts",
    "src/characters/RegistryMotion.ts",
    "src/engine/JuniMotion.ts",
  ].map((p) => [
    root + p,
    crypto
      .createHash("sha256")
      .update(fs.readFileSync(root + p))
      .digest("hex"),
  ]),
);
manifest.definitionSnapshots["docs/phase2a/approved-identity-records.json"] =
  crypto
    .createHash("sha256")
    .update(fs.readFileSync("docs/phase2a/approved-identity-records.json"))
    .digest("hex");
fs.writeFileSync(
  "docs/phase2a/approved-four-characters.json",
  JSON.stringify(manifest, null, 2) + "\n",
);
console.log(
  "Four approved identity/animation records recovered from the pre-functionality frozen source snapshot.",
);
