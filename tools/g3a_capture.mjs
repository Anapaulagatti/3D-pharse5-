import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const dir = "docs/gate3a-corrections";
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
for (const entry of ["station", "retail", "bakery", "convenience"]) {
  await p.goto(
    "http://127.0.0.1:4271/gate3-review.html?scene=registration&entry=" +
      entry +
      "&native",
  );
  await p.waitForFunction(() => window.__GATE3__?.ready);
  await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  await p.waitForTimeout(300);
  await p.locator("canvas").screenshot({ path: `${dir}/${entry}-native.png` });
  await fs.writeFile(
    `${dir}/${entry}-state.json`,
    JSON.stringify(await p.evaluate(() => window.__GATE3__), null, 2),
  );
}
for (const entry of ["north", "jeju"]) {
  await p.goto(
    "http://127.0.0.1:4271/gate3-review.html?scene=world&entry=" +
      entry +
      "&native",
  );
  await p.waitForFunction(() => window.__GATE3__?.ready);
  await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  await p
    .locator("canvas")
    .screenshot({ path: dir + "/preserved-" + entry + "-native.png" });
}
// Same native district framing used by the first approved source comparison.
await p.goto(
  "http://127.0.0.1:4271/gate3-review.html?scene=district&entry=station&native",
);
await p.waitForFunction(() => window.__GATE3__?.ready);
await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
await p
  .locator("canvas")
  .screenshot({ path: dir + "/preserved-district-native.png" });
await fs.writeFile(
  dir + "/preserved-district-state.json",
  JSON.stringify(await p.evaluate(() => window.__GATE3__), null, 2),
);
await p.goto("http://127.0.0.1:4271/gate3-review.html?scene=registration");
await p.waitForFunction(() => window.__GATE3__?.ready);
await p.locator("#scenic").click();
await p.locator("#overview-mode").click();
await p.waitForTimeout(800);
await p
  .locator("canvas")
  .screenshot({ path: dir + "/registration-overview.png" });
await fs.writeFile(
  dir + "/capture-errors.json",
  JSON.stringify(errors, null, 2),
);
await b.close();
if (errors.length) throw Error(errors.join("\n"));
