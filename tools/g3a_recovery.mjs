import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const page = await browser.newPage({
  viewport: { width: 844, height: 390 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
});
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto("http://127.0.0.1:4271/gate3-review.html?scene=world&stress");
await page.waitForFunction(() => window.__GATE3__?.ready);
const initial = await page.evaluate(() => window.__GATE3__);
await page.locator("#scenic").click();
await page.locator("#start-tour").click();
const samples = [];
for (let i = 0; i < 20; i++) {
  await page.waitForTimeout(1000);
  samples.push(await page.evaluate(() => window.__GATE3__));
}
if (!(await page.locator("#return-juni").isVisible()))
  await page.locator("#tour-controls").click();
await page.locator("#return-juni").click();
await page.waitForTimeout(1500);
const final = await page.evaluate(() => window.__GATE3__);
if (
  final.chunks.evictions < 1 ||
  samples.some((s) => s.chunks.reservedBytes > s.chunks.budgetBytes)
)
  throw Error("Cache did not demonstrate bounded eviction");
// Explicit decode/mask network fault. Player must not move onto an unready chunk.
let rejected = false;
await page.route("**/assets/gate3/district/2-1.bin", async (route) => {
  if (!rejected) {
    rejected = true;
    await route.fulfill({
      status: 503,
      body: "deliberate G3-A fault injection",
    });
  } else await route.continue();
});
await page.goto("http://127.0.0.1:4271/gate3-review.html?scene=district");
await page.waitForFunction(() => window.__GATE3__?.chunks.errors > 0);
await page.keyboard.down("d");
await page.waitForTimeout(500);
await page.keyboard.up("d");
const gated = await page.evaluate(() => window.__GATE3__);
if (gated.x !== 1200)
  throw Error("Moved into a chunk with unavailable collision");
await page.waitForFunction(() => window.__GATE3__?.ready);
const recovered = await page.evaluate(() => window.__GATE3__);
// Renderer context restoration must retain the one-upload owned source textures.
const lost = await page.evaluate(() => {
  const canvas = document.querySelector("canvas");
  const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
  const ext = gl?.getExtension("WEBGL_lose_context");
  if (!ext) return false;
  ext.loseContext();
  setTimeout(() => ext.restoreContext(), 700);
  return true;
});
if (lost) {
  await page.waitForTimeout(2200);
  await page.waitForFunction(() => window.__GATE3__?.ready);
}
const restored = await page.evaluate(() => window.__GATE3__);
// Canvas fallback/native renderer check; main review uses AUTO/WebGL where supported.
await page.goto(
  "http://127.0.0.1:4271/gate3-review.html?scene=district&entry=station&native&renderer=canvas",
);
await page.waitForFunction(() => window.__GATE3__?.ready);
const fallback = await page.evaluate(() => window.__GATE3__);
if (fallback.renderer !== "Canvas") throw Error("Canvas fallback missing");
await fs.writeFile(
  "docs/gate3a-corrections/resilience-report.json",
  JSON.stringify(
    {
      scope: "Chromium emulation, NOT physical-device certification",
      stress: {
        budgetMiB: 24,
        initial,
        final,
        samples,
        juniPreserved: initial.x === final.x && initial.y === final.y,
      },
      networkFault: { rejected, gated, recovered },
      contextRestore: { available: lost, restored },
      fallback,
      errors,
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length) throw Error(errors.join("\n"));
console.log(
  "Bounded eviction, fault gating/recovery and Canvas fallback verified",
);
