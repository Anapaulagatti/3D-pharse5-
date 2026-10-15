import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out = process.env.REVIEW_DIR ?? "docs/character-reboot";
const baseURL =
  process.env.REVIEW_BASE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const errors = [],
  missing = [],
  samples = [];
function observe(page) {
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) missing.push(`${r.status()} ${r.url()}`);
  });
}
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1100 },
    reducedMotion: "reduce",
  });
  observe(page);
  await page.goto(new URL("character-review.html", baseURL).href);
  await page.waitForFunction(() => window.__CHARACTER_REVIEW__?.ready);
  for (const view of ["front", "back", "left", "right"]) {
    await page.locator(`[data-view="${view}"]`).click();
    await page.waitForFunction(
      (view) => window.__CHARACTER_REVIEW__.view === view,
      view,
    );
    await page.waitForTimeout(120);
    await page
      .locator("canvas")
      .screenshot({ path: `${out}/phaser-${view}.png` });
    samples.push({
      name: `phaser-${view}`,
      metrics: await page.evaluate(() => window.__CHARACTER_REVIEW__),
    });
  }
  await page.locator('[data-view="front"]').click();
  await page.locator("#review-zoom").selectOption("1");
  await page.waitForFunction(() => window.__CHARACTER_REVIEW__.zoom === 1);
  await page.waitForTimeout(120);
  await page.locator("canvas").screenshot({ path: `${out}/phaser-native.png` });
  samples.push({
    name: "phaser-native",
    metrics: await page.evaluate(() => window.__CHARACTER_REVIEW__),
  });
  await page.locator("#review-zoom").selectOption("2");
  await page.waitForTimeout(120);
  await page.screenshot({ path: `${out}/review-page.png`, fullPage: true });
  const mobile = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  observe(mobile);
  await mobile.goto(
    new URL("character-review.html?renderer=canvas", baseURL).href,
  );
  await mobile.waitForFunction(() => window.__CHARACTER_REVIEW__?.ready);
  await mobile.screenshot({ path: `${out}/mobile.png`, fullPage: true });
  samples.push({
    name: "mobile-canvas",
    metrics: await mobile.evaluate(() => window.__CHARACTER_REVIEW__),
  });
  await page.getByRole("link", { name: "Mở game hiện tại →" }).click();
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  const original = await page.evaluate(() => window.__PIXEL_METRICS__);
  if (
    original.avatarVersion !== "chibi-motion-v2" ||
    original.guests.length !== 4
  )
    throw Error("Original working game was not preserved");
  const result = {
    status: "CAPTURED_REQUIRES_VISUAL_INSPECTION",
    method:
      "Native Phaser render of generated static direction drawings, existing Plaza preload/create reused. No injected sprites in screenshots, no character action animation claimed.",
    samples,
    preservedGame: {
      avatarVersion: original.avatarVersion,
      guests: original.guests.length,
      ready: original.ready,
    },
    errors,
    missing,
  };
  writeFileSync(
    `${out}/browser-verification.json`,
    JSON.stringify(result, null, 2) + "\n",
  );
  if (errors.length || missing.length)
    throw Error(JSON.stringify({ errors, missing }));
  console.log(
    JSON.stringify({ out, samples: samples.length, errors, missing }),
  );
} finally {
  await browser.close();
}
