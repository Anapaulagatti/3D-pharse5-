import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state, walk, grid, capture } from "./gate2_browser_lib.mjs";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const dir = "docs/gate2/final-review",
  errors = [];
try {
  const p = await browser.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  await ready(p, "c");
  assert.equal(
    await p.evaluate(() => typeof window.__GATE2_TEST__),
    "undefined",
  );
  const g = await grid(p);
  const trace = [];
  for (const pt of [
    [540, 865],
    [560, 915],
    [628, 984],
    [650, 1050],
    [650, 1130],
    [635, 1185],
    [560, 1205],
    [500, 1205],
    [410, 1210],
    [410, 1190],
  ])
    trace.push({ target: pt, ...(await walk(p, g, pt)) });
  await p.keyboard.press("e");
  await p.waitForFunction(() => window.__GATE2__.visited.includes("culture"));
  await p.locator("#close").click();
  await p.waitForTimeout(150);
  await capture(p, dir + "/JEJU_ACCESS_GAMEPLAY_1X.png");
  const final = await state(p);
  await ready(p, "c", "&qa&native&overview");
  await p.evaluate(() => window.__GATE2_TEST__.place(410, 1190));
  await p.waitForTimeout(150);
  await capture(p, dir + "/JEJU_ACCESS_NATIVE_1X.png");
  assert.equal(errors.length, 0);
  await fs.writeFile(
    dir + "/access-qa.json",
    JSON.stringify(
      {
        normalEntryRealKeyboard: true,
        route: trace,
        final,
        errors,
        scope:
          "Localized exterior approach only; no interior gameplay; no scene rebuild. Native overview uses QA placement, traversal crop uses actual uninterrupted input.",
      },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS", trace.length, "actual input approach segments");
} finally {
  await browser.close();
}
