import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const out = "docs/v10-production",
  base = process.env.V10_BASE_URL ?? "http://127.0.0.1:4220/3D-pharse5-/";
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const errors = [],
  rows = [],
  requests = new Set();
try {
  for (const [id, x, y, overview] of [
    ["FINAL_WORLD_NATIVE", 2176, 2960, true],
    ["MODERN_TOWN", 2352, 3000, false],
    ["NAMSAN", 736, 3040, false],
    ["STATION", 3776, 2832, false],
    ["ENTERTAINMENT", 960, 4080, false],
    ["WATERFRONT_FERRY", 3776, 4224, false],
    ["JEJU", 3104, 5456, false],
    ["NORTH", 2176, 1328, false],
  ]) {
    const p = await browser.newPage({
      viewport: { width: overview ? 4352 : 1440, height: 1140 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
      serviceWorkers: "block",
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("request", (r) => requests.add(new URL(r.url()).pathname));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    await p.goto(
      base +
        "v10-city-review.html?qa&renderer=canvas" +
        (overview ? "&overview" : ""),
    );
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
    await p.waitForFunction(
      (n) => window.__PIXEL_METRICS__.frameCount > n + 5,
      n,
    );
    const data = await p
      .locator("canvas")
      .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
    const buf = Buffer.from(data.png.split(",")[1], "base64");
    await fs.writeFile(`${out}/V10_${id}.png`, buf);
    rows.push({
      id,
      position: [x, y],
      camera: await p.evaluate(() => window.__FULL_WORLD__.camera),
      size: data.size,
      sha256: createHash("sha256").update(buf).digest("hex"),
    });
    await p.close();
  }
  await fs.writeFile(
    out + "/captures.json",
    JSON.stringify(
      {
        source:
          "Actual Phaser original V10 artwork canvases over HTTP; QA placement for camera composition, not navigation proof",
        base,
        rows,
        errors,
        requests: [...requests].sort(),
      },
      null,
      2,
    ) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(
    JSON.stringify({
      captures: rows.length,
      errors,
      legacyWorldRequested: [...requests].some(
        (r) => r.includes("/assets/world/") || r.includes("/v9-world/"),
      ),
    }),
  );
} finally {
  await browser.close();
}
