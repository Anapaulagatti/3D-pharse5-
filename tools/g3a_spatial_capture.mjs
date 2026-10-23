import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const dir = "docs/g3a-spatial-review",
  b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
const p = await b.newPage({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
});
const errors = [],
  results = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.status() + " " + r.url());
});
try {
  for (const [name, scene, entry, renderer] of [
    ["bakery-waterfront", "registration", "bakery", "auto"],
    ["bakery-quay", "registration-refined", "bakery", "auto"],
    ["maru-original", "registration", "convenience", "auto"],
    ["maru-revised", "registration-refined", "convenience", "auto"],
    ["namsan-access", "registration-refined", "namsan", "auto"],
    ["station", "registration-refined", "station", "auto"],
    ["retail", "registration-refined", "retail", "auto"],
    ["render-after-native", "district", "station", "canvas"],
    ["render-webgl-control", "district", "station", "auto"],
  ]) {
    await p.goto(
      `http://127.0.0.1:4284/gate3-review.html?scene=${scene}&entry=${entry}&renderer=${renderer}&native&pixelAudit`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
    await p.waitForTimeout(200);
    const image = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    await fs.writeFile(
      `${dir}/${name}-1x.png`,
      Buffer.from(image.png.split(",")[1], "base64"),
    );
    delete image.png;
    results.push({
      name,
      scene,
      entry,
      state: await p.evaluate(() => window.__GATE3__),
      renderAudit: image,
    });
  }
  if (errors.length) throw Error(errors.join("\n"));
  await fs.copyFile(
    "docs/gate3a-pixel-audit/before-canvas-native.png",
    `${dir}/render-before-native-1x.png`,
  );
  await fs.writeFile(
    `${dir}/native-captures.json`,
    JSON.stringify({ results, errors }, null, 2),
  );
  console.log(
    "PASS 9 native POST_RENDER Phaser captures; no page/resource errors",
  );
} finally {
  await b.close();
}
