import { chromium } from "playwright";
import fs from "node:fs/promises";
const out =
  process.env.PIXEL_V7_CAPTURE_DIR ?? "docs/v7-world/quality/first-render";
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
    ["transition", 2176, 2240],
    ["namsan", 800, 3192],
    ["station", 2240, 2888],
    ["amusement", 3712, 3264],
    ["waterfront", 2240, 3752],
    ["bridge", 2816, 3712],
    ["jeju-arrival", 2704, 4352],
    ["jeju-village", 2048, 4800],
    ["jeju-loop", 2504, 4600],
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
    await page.goto(base + "v7-world-review.html?qa&renderer=canvas");
    await page.waitForFunction(
      () =>
        window.__SEOUL__?.ready &&
        window.__V3_WORLD__?.candidate === "v7-world",
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
  await page.goto(base + "v7-world-review.html?overview&renderer=canvas");
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
