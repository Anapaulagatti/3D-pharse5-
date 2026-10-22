import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const dir = "docs/gate3a";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  headless: true,
  args: ["--no-sandbox"],
});
const page = await browser.newPage({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
});
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
for (const [name, params] of [
  ["north-native", "scene=world&entry=north&native"],
  ["jeju-native", "scene=world&entry=jeju&native"],
  ["station-native", "scene=district&entry=station&native"],
  ["world-overview", "scene=world"],
]) {
  await page.goto("http://127.0.0.1:4261/gate3-review.html?" + params);
  await page.waitForFunction(() => window.__GATE3__?.ready, { timeout: 30000 });
  if (name === "world-overview") {
    await page.locator("#scenic").click();
    await page.locator("#overview-mode").click();
    await page.waitForTimeout(1000);
  }
  await page.waitForFunction(() => window.__GATE3__?.chunks.inflight === 0);
  await page.waitForTimeout(350);
  await page.locator("canvas").screenshot({ path: `${dir}/${name}.png` });
  await fs.writeFile(
    `${dir}/${name}-state.json`,
    JSON.stringify(await page.evaluate(() => window.__GATE3__), null, 2),
  );
  console.log(
    name,
    await page.evaluate(() => ({
      ready: window.__GATE3__.ready,
      chunks: window.__GATE3__.chunks,
      view: window.__GATE3__.camera.worldView,
    })),
  );
}
await fs.writeFile(
  dir + "/browser-errors.json",
  JSON.stringify(errors, null, 2),
);
await browser.close();
if (errors.length) throw Error(errors.join("\n"));
