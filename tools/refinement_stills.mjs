import { chromium } from "playwright";
import fs from "node:fs/promises";
const out = "docs/world-refinement/quality";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1440, height: 1140 },
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
});
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
const shots = [];
for (const [entry, phase, places] of [
  [
    "production-review.html",
    "before",
    [
      ["palace", 2048, 500],
      ["academy", 672, 960],
      ["workshop", 3312, 860],
      ["museum", 3520, 1320],
    ],
  ],
  [
    "refinement-review.html",
    "after",
    [
      ["palace", 1152, 320],
      ["academy", 544, 1280],
      ["workshop", 1776, 1212],
      ["museum", 1952, 1736],
      ["modern", 512, 1872],
      ["opening", 1152, 832],
      ["royal-garden", 1024, 384],
      ["occlusion", 1440, 1504],
    ],
  ],
]) {
  await p.goto(base + entry + "?qa&renderer=canvas");
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  for (const [id, x, y] of places) {
    await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
    await p.waitForTimeout(220);
    await p
      .locator("canvas")
      .screenshot({ path: `${out}/${phase}-${id}-native.png` });
    shots.push({
      id,
      phase,
      point: [x, y],
      world: await p.evaluate(() => window.__SEOUL__),
      avatar: await p.evaluate(() => window.__PLAZA_REVIEW__),
    });
  }
  if (phase === "after") {
    await p.locator("#night").click();
    await p.waitForTimeout(220);
    await p.locator("canvas").screenshot({ path: out + "/evening-native.png" });
    await p.evaluate(() => window.__SEOUL_TEST__.place(544, 1152));
    await p.waitForTimeout(150);
    await p.locator("#interact").click();
    await p.waitForFunction(() => window.__SEOUL__?.area === "room");
    await p.locator("canvas").screenshot({ path: out + "/room-native.png" });
  }
}
await p.setViewportSize({ width: 1500, height: 1300 });
await p.goto(base + "refinement-review.html?overview&renderer=canvas");
await p.waitForFunction(() => window.__SEOUL__?.ready);
await p.waitForTimeout(250);
await p.locator("canvas").screenshot({ path: out + "/overview.png" });
await p.setViewportSize({ width: 390, height: 844 });
await p.goto(base + "refinement-review.html?renderer=canvas");
await p.waitForFunction(() => window.__SEOUL__?.ready);
await p.locator("canvas").screenshot({ path: out + "/mobile-native.png" });
await p.screenshot({ path: out + "/mobile-interface.png", fullPage: true });
await fs.writeFile(
  out + "/stills.json",
  JSON.stringify(
    {
      method:
        "Actual production Phaser Canvas screenshots, native1x camera unless overview explicitly0.5x; OS reduced-motion for deterministic comparison, DPR1. Source images are not substituted for engine output.",
      shots,
      errors,
    },
    null,
    2,
  ),
);
console.log({ shots: shots.length, errors });
await b.close();
if (errors.length) throw Error(JSON.stringify(errors));
