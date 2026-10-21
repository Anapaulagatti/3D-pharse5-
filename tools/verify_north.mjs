import { chromium } from "playwright";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
const sha = "f92e0944500e6638d2b2d3cffd2cbc2d9196abf8508e533b0070adb8932c25a5";
const old =
  process.cwd() + `/.cache/portable-http/${sha}/Korean-Arena-V8-World-Review`;
const server = spawn(
  "python3",
  [old + "/start.py", "--port", "4218", "--no-browser"],
  { stdio: "ignore" },
);
let browser;
const errors = [],
  rows = [];
const out = "docs/v9-world/quality/north-preservation";
await fs.mkdir(out, { recursive: true });
try {
  for (let i = 0; i < 80; i++) {
    try {
      if (
        (await fetch("http://127.0.0.1:4218/3D-pharse5-/v8-city-review.html"))
          .ok
      )
        break;
    } catch {
      // The archive HTTP process may still be starting.
    }
    if (i === 79)
      throw Error(
        "Archived V8 launcher unavailable; restore exact ZIP from recovery tag",
      );
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
  });
  for (const [name, base, entry] of [
    ["before-v8", "http://127.0.0.1:4218/3D-pharse5-/", "v8-city-review.html"],
    [
      "after-cleanup",
      "http://127.0.0.1:4201/3D-pharse5-/",
      "v9-world-review.html",
    ],
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
    await p.goto(base + entry + "?qa&renderer=canvas");
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    await p.evaluate(() => window.__SEOUL_TEST__.place(2176, 1328));
    const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
    await p.waitForFunction(
      (n) => window.__PIXEL_METRICS__.frameCount > n + 5,
      n,
    );
    const data = await p
      .locator("canvas")
      .evaluate((c) => ({ png: c.toDataURL(), size: [c.width, c.height] }));
    const bytes = Buffer.from(data.png.split(",")[1], "base64");
    await fs.writeFile(`${out}/${name}.png`, bytes);
    rows.push({
      name,
      pixelPNGHash: createHash("sha256").update(bytes).digest("hex"),
      size: data.size,
      camera: await p.evaluate(() => window.__FULL_WORLD__.camera),
    });
    await p.close();
  }
  const equal = rows[0].pixelPNGHash === rows[1].pixelPNGHash;
  await fs.writeFile(
    out + "/actual-render-comparison.json",
    JSON.stringify(
      {
        status: equal && !errors.length ? "PASS" : "FAIL",
        method:
          "Actual archived V8 ZIP HTTP vs current full V9 production, same native1024x768 camera2176,1328 zoom1/Canvas/viewport1440x1140/DPR1/reduced-motion. No filters.",
        rows,
        errors,
      },
      null,
      2,
    ),
  );
  if (!equal || errors.length)
    throw Error(JSON.stringify({ equal, errors, rows }));
  console.log("Actual north Phaser frame byte-identical after cleanup");
} finally {
  if (browser) await browser.close();
  server.kill("SIGINT");
}
