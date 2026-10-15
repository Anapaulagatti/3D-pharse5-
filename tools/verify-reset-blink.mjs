import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out = "quality-reports/pixel-reset-v2/blink";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const context = await browser.newContext({
  viewport: { width: 1440, height: 1100 },
  reducedMotion: "no-preference",
});
const page = await context.newPage();
const errors = [],
  missing = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
const observations = [];
for (const style of ["A", "B", "C"]) {
  await page.locator("#direction").selectOption(style);
  await page.waitForFunction(
    (s) => window.__PIXEL_METRICS__?.style === s,
    style,
  );
  // Observe naturally reached blink, then invoke the same Pause button used by
  // the user. No pose/animation state is assigned by this test.
  await page.waitForFunction(
    () => {
      const m = window.__PIXEL_METRICS__;
      if (m?.frame === "idle-down-1" && !m.paused) {
        document.querySelector("#pause").click();
        return true;
      }
      return false;
    },
    null,
    { timeout: 20000 },
  );
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.paused);
  const metrics = await page.evaluate(() => window.__PIXEL_METRICS__);
  if (metrics.frame !== "idle-down-1")
    throw Error("Blink was not held by UI pause");
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/${style}-natural-blink.png` });
  observations.push(metrics);
  await page.getByRole("button", { name: "Tiếp tục", exact: true }).click();
}
writeFileSync(
  `${out}/verification.json`,
  JSON.stringify(
    {
      status: "PASS_OBSERVED_RENDERED_BLINK_PENDING_IMAGE_REVIEW",
      observations,
      errors,
      missing,
      method:
        "Natural idle frame observed; normal Pause UI clicked to retain it for actual canvas screenshot. No injected pose. Phaser4 absolute frame duration120ms.",
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log("PASS natural idle blink observed and rendered in all3styles.");
