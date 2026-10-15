import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
const b = await chromium.launch({
  headless: true,
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const p = await b.newPage({
  viewport: { width: 1440, height: 1100 },
  reducedMotion: "no-preference",
});
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
await p.goto("http://127.0.0.1:4201/3D-pharse5-/");
await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
await p.waitForFunction(() => window.__PIXEL_METRICS__.frame === "idle-down-1");
await p.locator("#pause").click();
await p
  .locator("canvas")
  .screenshot({ path: "quality-reports/unified-v4/render/natural-blink.png" });
const blink = await p.evaluate(() => window.__PIXEL_METRICS__);
await p.locator("#pause").click();
async function axis(axis, target) {
  const current = await p.evaluate((a) => window.__PIXEL_METRICS__[a], axis);
  if (Math.abs(current - target) < 3) return;
  const sign = target > current ? 1 : -1;
  const key =
    axis === "x"
      ? sign > 0
        ? "ArrowRight"
        : "ArrowLeft"
      : sign > 0
        ? "ArrowDown"
        : "ArrowUp";
  await p.locator("canvas").focus();
  await p.keyboard.down(key);
  try {
    await p.waitForFunction(
      ({ axis, target, sign }) =>
        (window.__PIXEL_METRICS__[axis] - target) * sign >= 0,
      { axis, target, sign },
      { timeout: 20000 },
    );
  } finally {
    await p.keyboard.up(key);
  }
}
await axis("x", 440);
await axis("y", 448);
await axis("x", 340);
await p.waitForFunction(() => !window.__PIXEL_METRICS__.moving);
await p.locator("canvas").screenshot({
  path: "quality-reports/unified-v4/render/house-detail-gameplay.png",
});
writeFileSync(
  "quality-reports/unified-v4/render/details.json",
  JSON.stringify(
    {
      method:
        "House: actual native keyboard navigation. Natural blink retained with Pause UI. Tree detail: separately cropped from the actual2x gameplay canvas without resampling, explicitly labelled. No injected player/camera poses.",
      blink,
      house: await p.evaluate(() => window.__PIXEL_METRICS__),
      errors,
    },
    null,
    2,
  ),
);
await b.close();
if (errors.length) throw Error(errors.join("\n"));
console.log(
  "Native house detail and natural blink captured; tree detail is actual2x canvas crop.",
);
