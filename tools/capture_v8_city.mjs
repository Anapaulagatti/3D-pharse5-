import { chromium } from "playwright";
import fs from "node:fs/promises";
const out =
  process.env.PIXEL_V8_CAPTURE_DIR ?? "docs/v8-city/quality/first-render";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4200/3D-pharse5-/";
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const errors = [],
  shots = [];
try {
  for (const [name, x, y] of [
    ["transition", 2112, 2400],
    ["namsan", 736, 3008],
    ["station", 2704, 2800],
    ["amusement", 3744, 3200],
    ["waterfront", 2528, 3736],
    ["urban-junction", 2112, 3008],
    ["jeju-arrival", 1888, 4464],
    ["jeju-village", 2048, 4800],
    ["jeju-loop", 2600, 4904],
  ]) {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 1140 },
      reducedMotion: "reduce",
      deviceScaleFactor: 1,
    });
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await page.goto(base + "v8-city-review.html?qa&renderer=canvas");
    await page.waitForFunction(
      () =>
        window.__SEOUL__?.ready && window.__V3_WORLD__?.candidate === "v8-city",
    );
    await page.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    await page.waitForTimeout(150);
    const data = await page.locator("canvas").evaluate((c) => c.toDataURL());
    await fs.writeFile(
      out + "/" + name + "-native.png",
      Buffer.from(data.split(",")[1], "base64"),
    );
    shots.push({
      name,
      x,
      y,
      camera: await page.evaluate(() => window.__FULL_WORLD__.camera),
    });
    await page.close();
  }
  const page = await browser.newPage({
    viewport: { width: 4352, height: 5312 },
    reducedMotion: "reduce",
    deviceScaleFactor: 1,
  });
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await page.goto(base + "v8-city-review.html?overview&renderer=canvas");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  await page.waitForTimeout(120);
  const data = await page
    .locator("canvas")
    .evaluate((c) => ({ url: c.toDataURL(), size: [c.width, c.height] }));
  if (data.size.join(",") !== "4352,5312") throw Error("Wrong native size");
  await fs.writeFile(
    out + "/full-native.png",
    Buffer.from(data.url.split(",")[1], "base64"),
  );
  await page.goto(
    base + "v8-city-review.html?overview&qa&ground-only&renderer=canvas",
  );
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  await page.waitForTimeout(120);
  const ground = await page.locator("canvas").evaluate((c) => c.toDataURL());
  await fs.writeFile(
    out + "/ground-only-native.png",
    Buffer.from(ground.split(",")[1], "base64"),
  );
  await page.close();
  const mobile = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const mp = await mobile.newPage();
  mp.on("pageerror", (e) => errors.push(e.message));
  mp.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await mp.goto(base + "v8-city-review.html?qa&renderer=canvas");
  await mp.waitForFunction(() => window.__SEOUL__?.ready);
  await mp.evaluate(() => window.__SEOUL_TEST__.place(2112, 3008));
  await mp.waitForTimeout(150);
  await mp.screenshot({ path: out + "/mobile-landscape-dpr3.png" });
  const mobileNative = await mp
    .locator("canvas")
    .evaluate((c) => c.toDataURL());
  await fs.writeFile(
    out + "/mobile-native.png",
    Buffer.from(mobileNative.split(",")[1], "base64"),
  );
  await mobile.close();
  await fs.writeFile(
    out + "/captures.json",
    JSON.stringify(
      {
        method:
          "Actual Phaser Canvas native PNGs; QA placements only for still framing, not traversal proof. Full camera0,0zoom1. No image filters.",
        shots,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(JSON.stringify({ shots: shots.length, full: data.size, errors }));
} finally {
  await browser.close();
}
