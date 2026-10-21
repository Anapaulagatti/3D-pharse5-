import { chromium } from "playwright";
import fs from "node:fs/promises";
const phase = process.argv[2] ?? "final",
  out = `docs/v9-world/${phase === "graybox" ? "quality/graybox" : "quality/final"}`;
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [],
  errors = [];
try {
  for (const [id, x, y] of [
    ["CITY_STREETS", 2176, 2936],
    ["NAMSAN", 3520, 3064],
    ["STATION", 1504, 3912],
    ["ENTERTAINMENT", 3552, 4056],
    ["WATERFRONT", 2528, 4688],
    ["JEJU", 1376, 5624],
  ]) {
    const p = await browser.newPage({
      viewport: { width: 1440, height: 1140 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(
      "http://127.0.0.1:4201/3D-pharse5-/v9-world-review.html?qa&renderer=canvas",
    );
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
    await p.waitForFunction(
      (n) => window.__PIXEL_METRICS__.frameCount >= n + 5,
      n,
    );
    const png = await p.locator("canvas").evaluate((c) => c.toDataURL());
    await fs.writeFile(
      `${out}/V9_${id}.png`,
      Buffer.from(png.split(",")[1], "base64"),
    );
    rows.push({
      id,
      position: [x, y],
      camera: await p.evaluate(() => window.__FULL_WORLD__.camera),
      native: [1024, 768],
    });
    await p.close();
  }
  const p = await browser.newPage({
    viewport: { width: 4352, height: 1400 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  p.on("pageerror", (e) => errors.push(e.message));
  await p.goto(
    "http://127.0.0.1:4201/3D-pharse5-/v9-world-review.html?qa&overview&renderer=canvas",
  );
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount >= n + 5,
    n,
  );
  const data = await p
    .locator("canvas")
    .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
  await fs.writeFile(
    `${out}/V9_FULL_WORLD_OVERVIEW.png`,
    Buffer.from(data.png.split(",")[1], "base64"),
  );
  rows.push({ id: "OVERVIEW", size: data.size });
  await p.close();
  await fs.writeFile(
    `${out}/captures.json`,
    JSON.stringify(
      {
        phase,
        source:
          "Actual Phaser production HTTP canvas, native resolution, no post-process",
        rows,
        errors,
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(phase, rows.length, "actual engine captures");
} finally {
  await browser.close();
}
