import { chromium } from "@playwright/test";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const manifest = JSON.parse(
  readFileSync("downloads/unified-v4/package-manifest.json", "utf8"),
);
const out = "quality-reports/unified-v4/package";
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
const reports = [];
for (const [name, viewport, dpr] of [
  ["desktop", { width: 1280, height: 1000 }, 1],
  ["mobile", { width: 390, height: 844 }, 2],
]) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: dpr,
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  const errors = [];
  const failures = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) failures.push(r.url());
  });
  const url = "http://127.0.0.1:4202/3D-pharse5-/";
  const response = await context.request.get(url);
  const sha = createHash("sha256")
    .update(await response.body())
    .digest("hex");
  if (sha !== manifest.files.find((f) => f.path === "index.html").sha256)
    throw Error("Extracted artifact hash mismatch");
  await page.goto(url);
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  await page.screenshot({ path: `${out}/package-${name}.png`, fullPage: true });
  await page
    .locator("canvas")
    .screenshot({ path: `${out}/package-${name}-canvas.png` });
  const before = await page.evaluate(() => window.__PIXEL_METRICS__);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForTimeout(300);
  const moved = await page.evaluate(() => window.__PIXEL_METRICS__);
  await page.keyboard.up("ArrowDown");
  if (moved.y <= before.y) throw Error("Package input did not move");
  const crisp = await page.locator("canvas").evaluate((e) => ({
    nativeWidth: e.width,
    cssWidth: e.getBoundingClientRect().width,
    nativeHeight: e.height,
    cssHeight: e.getBoundingClientRect().height,
    imageRendering: getComputedStyle(e).imageRendering,
  }));
  if (
    crisp.nativeWidth !== crisp.cssWidth ||
    crisp.nativeHeight !== crisp.cssHeight
  )
    throw Error("Fractional canvas scaling");
  if (
    await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)
  )
    throw Error("Horizontal page overflow");
  if (errors.length || failures.length)
    throw Error(JSON.stringify({ errors, failures }));
  reports.push({ name, dpr, sha, before, moved, crisp, errors, failures });
  await context.close();
}
writeFileSync(
  `${out}/exact-package-verification.json`,
  JSON.stringify(
    {
      status: "PASS",
      reports,
      limitation:
        "Actual extracted HTTP/browser checks; local desktop Python GUI launch not claimed tested on Windows.",
    },
    null,
    2,
  ),
);
await browser.close();
console.log(
  "PASS extracted exact ZIP: desktop/mobile, 1:1 native pixels at DPR2, real movement, no errors.",
);
