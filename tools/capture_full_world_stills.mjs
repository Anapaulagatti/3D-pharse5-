import { chromium } from "playwright";
import fs from "node:fs/promises";
import crypto from "node:crypto";
const base =
    process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/",
  out = "docs/full-world/quality";
await fs.mkdir(out, { recursive: true });
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [],
  shots = [];
function monitor(p) {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
}
async function stable(p) {
  const n = await p.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await p.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount >= n + 4,
    n,
  );
}
async function pose(p, x, y) {
  await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), [x, y]);
  await stable(p);
}
async function canvas(p, name) {
  const s = await p
    .locator("canvas")
    .evaluate((c) => ({ data: c.toDataURL(), size: [c.width, c.height] }));
  const bytes = Buffer.from(s.data.split(",")[1], "base64");
  await fs.writeFile(`${out}/${name}.png`, bytes);
  shots.push({
    name,
    native: s.size,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    state: await p.evaluate(() => window.__SEOUL__),
  });
}
try {
  const c = await b.newContext({
    viewport: { width: 1440, height: 1140 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const p = await c.newPage();
  monitor(p);
  await p.goto(base + "living-korea-review.html?qa&renderer=canvas");
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  for (const [name, x, y] of [
    ["royal-garden", 768, 496],
    ["academy", 544, 1280],
    ["museum-street", 1984, 2028],
  ]) {
    await pose(p, x, y);
    await canvas(p, `before-${name}-native`);
  }
  await p.goto(base + "full-world-review.html?qa&renderer=canvas");
  await p.waitForFunction(() => window.__FULL_WORLD__?.world[0] === 4352);
  for (const [name, x, y] of [
    ["royal-garden", 1792, 508],
    ["academy", 1568, 1292],
    ["museum-street", 3008, 2040],
    ["workshop", 2820, 1472],
    ["cultural-street", 2640, 2368],
    ["namsan-tower", 832, 2912],
    ["bora-bloom", 3712, 2768],
    ["coast-station", 2048, 2944],
    ["coast-ferry", 2848, 3136],
    ["jeju-garden", 2240, 4208],
  ]) {
    await pose(p, x, y);
    await canvas(p, `after-${name}-native`);
  }
  await c.close();
  // Exact full native outdoor render. HTML HUD hidden by documented overview mode, not painted out.
  const oc = await b.newContext({
    viewport: { width: 4352, height: 4800 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const op = await oc.newPage();
  monitor(op);
  await op.goto(base + "full-world-review.html?overview&renderer=canvas");
  await op.waitForFunction(() => window.__FULL_WORLD__?.world[0] === 4352);
  await stable(op);
  await canvas(op, "full-map-overview");
  await oc.close();
  for (const [name, width, height] of [
    ["mobile-landscape", 844, 390],
    ["mobile-small", 568, 320],
    ["mobile-wide", 932, 430],
  ]) {
    const mc = await b.newContext({
      viewport: { width, height },
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    const mp = await mc.newPage();
    monitor(mp);
    await mp.goto(base + "full-world-review.html?qa&renderer=canvas");
    await mp.waitForFunction(() => window.__FULL_WORLD__);
    await pose(mp, 2176, 1328);
    await mp.screenshot({ path: `${out}/${name}-interface.png` });
    await canvas(mp, `${name}-canvas-native`);
    if (name === "mobile-landscape") {
      await pose(mp, 3712, 2768);
      await mp.locator("#settings-open").tap();
      await mp.locator("#zoom").selectOption("0.5");
      await mp.locator("#settings-close").tap();
      await stable(mp);
      await mp.screenshot({
        path: `${out}/mobile-bloom-panorama-interface.png`,
      });
      await mp.setViewportSize({ width: 390, height: 844 });
      await mp.locator("#rotate-screen").waitFor({ state: "visible" });
      await mp.screenshot({ path: `${out}/portrait-rotate-interface.png` });
      await mp.setViewportSize({ width: 844, height: 390 });
    }
    await mc.close();
  }
  if (errors.length) throw Error(JSON.stringify(errors));
  const inputs = {};
  for (const path of [
    "assets-src/full-world/map/outdoor-bundle.json",
    "public/review/full-world/world/plaza.json",
    "assets-src/full-world/room-bundle.json",
  ])
    inputs[path] = crypto
      .createHash("sha256")
      .update(await fs.readFile(path))
      .digest("hex");
  await fs.writeFile(
    `${out}/stills.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser native Canvas PNGs and whole-browser mobile HUD, OS reduced-motion. QA placement for still camera only; no movement claim. Full map is native4352x4800actual engine render, not source composition. Matched heritage before/after uses+1024x and+12y to align old48px/new60pxfollow offsets; native scene pixels never resized/retouched. Physical phone not tested.",
        inputs,
        shots,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(JSON.stringify({ shots: shots.length, errors }));
} finally {
  await b.close();
}
