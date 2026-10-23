import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
});
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
await p.goto(
  "http://127.0.0.1:4271/gate3-review.html?scene=district&entry=station&native",
);
await p.waitForFunction(() => window.__GATE3__?.ready);
await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
await p
  .locator("canvas")
  .screenshot({ path: "docs/gate3a-corrections/BEFORE_CONTEXT_NATIVE.png" });
const supported = await p.evaluate(() => {
  const c = document.querySelector("canvas"),
    gl = c.getContext("webgl2") || c.getContext("webgl"),
    e = gl?.getExtension("WEBGL_lose_context");
  if (!e) return false;
  e.loseContext();
  setTimeout(() => e.restoreContext(), 600);
  return true;
});
await p.waitForTimeout(2000);
await p
  .locator("canvas")
  .screenshot({ path: "docs/gate3a-corrections/RESTORED_CONTEXT_NATIVE.png" });
await fs.writeFile(
  "docs/gate3a-corrections/context-restore-state.json",
  JSON.stringify(
    { supported, errors, state: await p.evaluate(() => window.__GATE3__) },
    null,
    2,
  ),
);
await b.close();
if (errors.length) throw Error(errors.join("\n"));
