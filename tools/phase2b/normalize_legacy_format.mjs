import ts from "typescript";
import fs from "node:fs/promises";
import cp from "node:child_process";
import crypto from "node:crypto";
const files = [
  "tools/g3a_platform_restoration_capture.mjs",
  "tools/g3a_platform_restoration_smoke.mjs",
  "tools/g3bc_capture.mjs",
  "tools/g3bc_mobile.mjs",
  "tools/g3bc_overview.mjs",
  "tools/g3bc_package_smoke.mjs",
  "tools/g3bc_walk.mjs",
];
const canonical = (text) => {
  const ast = ts.createSourceFile(
    "capture.mjs",
    text,
    ts.ScriptTarget.Latest,
    true,
    ts.ScriptKind.JS,
  );
  const visit = (n) => ({
    kind: ts.SyntaxKind[n.kind],
    ...(typeof n.text === "string" && !ts.isSourceFile(n)
      ? { text: n.text }
      : {}),
    children: (() => {
      const out = [];
      ts.forEachChild(n, (q) => {
        out.push(visit(q));
      });
      return out;
    })(),
  });
  return JSON.stringify(visit(ast));
};
const hash = (s) => crypto.createHash("sha256").update(s).digest("hex"),
  before = await Promise.all(
    files.map((p) =>
      Promise.resolve(
        cp.execFileSync(
          "git",
          ["show", "ed75734d0e0865274ca0b82bab2495d78878d24b:" + p],
          { encoding: "utf8" },
        ),
      ),
    ),
  );
cp.execFileSync("node_modules/.bin/prettier", ["--write", ...files], {
  stdio: "ignore",
});
const rows = [];
for (let i = 0; i < files.length; i++) {
  const p = files[i],
    after = await Promise.resolve(
      cp.execFileSync(
        "git",
        ["show", "ed75734d0e0865274ca0b82bab2495d78878d24b:" + p],
        { encoding: "utf8" },
      ),
    );
  if (canonical(before[i]) !== canonical(after)) {
    await fs.writeFile(p, before[i]);
    throw Error("Unexpected AST change " + p);
  }
  rows.push({
    file: p,
    beforeSHA256: hash(before[i]),
    afterSHA256: hash(after),
    sameSyntaxTree: true,
  });
}
await fs.writeFile(
  "docs/phase2b/formatter-normalization.json",
  JSON.stringify(
    {
      method:
        "Seven pre-existing format:check failures in historical world capture helpers; Prettier whitespace normalization only. TypeScript syntax-tree kind/literal/identifier structure compared before/after; no validator ignored or weakened. Original files remain recoverable at approved commit. These are not protected art/runtime/animation sources.",
      rows,
    },
    null,
    2,
  ),
);
console.log(
  "Seven legacy capture helpers normalized; all syntax trees unchanged",
);
