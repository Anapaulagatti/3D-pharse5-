import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out =
  process.env.RESET_REVIEW_DIR ?? "quality-reports/pixel-reset-v2/draft-render";
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
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
});
const page = await context.newPage();
const errors = [],
  missing = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
const states = {};
for (const s of ["A", "B", "C"]) {
  await page.locator("#direction").selectOption(s);
  await page.waitForFunction((s) => window.__PIXEL_METRICS__?.style === s, s);
  await page.locator("#zoom").selectOption("2");
  await page.waitForTimeout(150);
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/${s}-hero-idle.png` });
  states[s] = await page.evaluate(() => window.__PIXEL_METRICS__);
  await page.screenshot({ path: `${out}/${s}-page.png`, fullPage: true });
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForTimeout(180);
  await page.locator("canvas").screenshot({ path: `${out}/${s}-walk.png` });
  await page.keyboard.up("ArrowDown");
  await page.keyboard.press("Space");
  await page.waitForTimeout(160);
  await page.locator("canvas").screenshot({ path: `${out}/${s}-emote.png` });
  await page.locator("#zoom").selectOption("1");
  await page.waitForTimeout(120);
  await page.locator("canvas").screenshot({ path: `${out}/${s}-overview.png` });
}
const mobile = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  reducedMotion: "reduce",
});
const p = await mobile.newPage();
await p.goto("http://127.0.0.1:4201/3D-pharse5-/");
await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
for (const s of ["A", "B", "C"]) {
  await p.locator("#direction").selectOption(s);
  await p.waitForFunction((s) => window.__PIXEL_METRICS__?.style === s, s);
  await p.locator("canvas").screenshot({ path: `${out}/${s}-mobile.png` });
  await p.locator("#zoom").selectOption("1");
  await p.waitForTimeout(120);
  await p
    .locator("canvas")
    .screenshot({ path: `${out}/${s}-mobile-overview.png` });
  await p.locator("#zoom").selectOption("2");
}
writeFileSync(
  `${out}/render.json`,
  JSON.stringify(
    {
      status:
        errors.length || missing.length
          ? "FAIL"
          : "CAPTURED_PENDING_VISUAL_REVIEW",
      states,
      errors,
      missing,
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log(JSON.stringify({ out, errors, missing }));
