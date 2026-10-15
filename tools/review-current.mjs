import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out = process.env.REVIEW_DIR ?? ".cache/review";
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
try {
  await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  await page.locator("canvas").screenshot({ path: out + "/town.png" });
  await page.locator("#zoom").selectOption("3");
  await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 3);
  await page.locator("canvas").screenshot({ path: out + "/characters.png" });
  await page.locator("canvas").focus();
  await page.keyboard.press("e");
  await page.waitForFunction(() => !document.querySelector("#dialog").hidden);
  const dialogue = await page.locator("#dialog-copy").textContent();
  if (!dialogue.includes("세종대왕") || !dialogue.includes("글자"))
    throw Error("Sejong interaction missing");
  await page.screenshot({ path: out + "/dialogue.png", fullPage: true });
  const metrics = await page.evaluate(() => window.__PIXEL_METRICS__);
  writeFileSync(
    out + "/inspection.json",
    JSON.stringify(
      {
        status: "CAPTURED_FOR_VISUAL_INSPECTION",
        dialogue,
        metrics,
        errors,
        missing,
      },
      null,
      2,
    ),
  );
  if (errors.length || missing.length)
    throw Error(JSON.stringify({ errors, missing }));
} finally {
  await browser.close();
}
