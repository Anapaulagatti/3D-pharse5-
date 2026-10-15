import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out = "quality-reports/unified-v4/render";
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
const page = await browser.newPage({
  viewport: { width: 1440, height: 1100 },
  reducedMotion: "reduce",
});
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
await page.locator("canvas").screenshot({ path: out + "/gameplay-2x.png" });
await page.screenshot({ path: out + "/desktop.png", fullPage: true });
await page.locator("#zoom").selectOption("1");
await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 1);
await page.locator("canvas").screenshot({ path: out + "/overview-1x.png" });
await page.locator("#zoom").selectOption("3");
await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 3);
await page.locator("canvas").screenshot({ path: out + "/idle-closeup.png" });
for (const hair of ["0", "1"])
  for (const outfit of ["0", "1"]) {
    await page.locator("#hair").selectOption(hair);
    await page.locator("#outfit").selectOption(outfit);
    await page.waitForFunction(
      ({ h, o }) =>
        window.__PIXEL_METRICS__.hair === Number(h) &&
        window.__PIXEL_METRICS__.outfit === Number(o),
      { h: hair, o: outfit },
    );
    await page
      .locator("canvas")
      .screenshot({ path: `${out}/outfit-h${hair}-o${outfit}.png` });
  }
await page.locator("#hair").selectOption("0");
await page.locator("#outfit").selectOption("0");
await page.locator("#zoom").selectOption("2");
for (const action of ["wave", "celebrate", "pose"]) {
  await page.locator("#" + action).click();
  await page.waitForFunction(
    (a) =>
      window.__PIXEL_METRICS__.frame.startsWith(a + "-") &&
      Number(window.__PIXEL_METRICS__.frame.split("-").at(-1)) >= 2,
    action,
  );
  await page.locator("#pause").click();
  await page.locator("canvas").screenshot({ path: `${out}/${action}.png` });
  await page.locator("#pause").click();
  await page.waitForTimeout(950);
}
writeFileSync(
  out + "/desktop.json",
  JSON.stringify(
    {
      errors,
      missing,
      metrics: await page.evaluate(() => window.__PIXEL_METRICS__),
    },
    null,
    2,
  ),
);
const mobile = await browser.newPage({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  reducedMotion: "reduce",
});
await mobile.goto("http://127.0.0.1:4201/3D-pharse5-/");
await mobile.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
await mobile.screenshot({ path: out + "/mobile.png", fullPage: true });
await mobile.locator("canvas").screenshot({ path: out + "/mobile-canvas.png" });
await browser.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log("Actual Phaser overview/idle/emotes/4outfits/mobile captured.");
