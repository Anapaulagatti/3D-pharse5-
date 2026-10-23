import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/g3a-forecourt-restoration";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const errors = [],
  rows = [],
  walk = [];
async function load(page, scene, renderer = "auto", native = true) {
  await page.goto(
    `http://127.0.0.1:4286/gate3-review.html?scene=${scene}&entry=station&pixelAudit${native ? "&native" : ""}&renderer=${renderer}`,
  );
  await page.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
}
async function capture(page, name, scene, renderer) {
  const a = await page.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    `${D}/${name}.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  rows.push({
    name,
    scene,
    renderer,
    audit: a,
    state: await page.evaluate(() => window.__GATE3__),
  });
}
async function move(page, key, target, axis, less = false) {
  await page.keyboard.down(key);
  const end = Date.now() + 12000;
  while (true) {
    const s = await page.evaluate(() => window.__GATE3__);
    walk.push({ t: Date.now(), key, x: s.x, y: s.y });
    if (less ? s[axis] <= target : s[axis] >= target) break;
    if (Date.now() > end)
      throw Error(`Movement blocked: ${key} ${JSON.stringify(s)}`);
    await page.waitForTimeout(40);
  }
  await page.keyboard.up(key);
}
try {
  const p = await browser.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.status() + " " + r.url());
  });
  for (const [scene, phase] of [
    ["registration-refined", "before"],
    ["registration-forecourt", "after"],
  ])
    for (const renderer of ["auto", "canvas"]) {
      await load(p, scene, renderer);
      await capture(
        p,
        `${phase}-${renderer}-frontage-juni-native`,
        scene,
        renderer,
      );
      await move(p, "s", 2855, "y");
      await p.waitForTimeout(150);
      await capture(p, `${phase}-${renderer}-native`, scene, renderer);
    }
  await load(p, "registration-forecourt");
  const clearance = await p.evaluate(() => {
    const f = window.__GATE3_TEST__.walkable;
    const r = [];
    for (let y = 2610; y <= 2734; y++)
      for (let x = 2554; x < 2643; x++) r.push(f(x, y));
    return { sampled: r.length, allWalkable: r.every(Boolean) };
  });
  await fs.writeFile(
    `${D}/clearance-runtime.json`,
    JSON.stringify(clearance, null, 2),
  );
  // Actual keyboard approach, return and lateral forecourt movement; no state writes/teleport.
  await move(p, "w", 2610, "y", true);
  await capture(
    p,
    "after-entrance-juni-native",
    "registration-forecourt",
    "auto",
  );
  await move(p, "s", 2732, "y");
  await move(p, "a", 2560, "x", true);
  await move(p, "d", 2640, "x");
  await move(p, "a", 2599, "x", true);
  await p.close();
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: "/tmp/g3-forecourt-video",
      size: { width: 1280, height: 900 },
    },
  });
  const v = await ctx.newPage();
  await load(v, "registration-forecourt", "auto", false);
  await v.waitForTimeout(500);
  await move(v, "w", 2610, "y", true);
  await capture(
    v,
    "after-moving-camera-native",
    "registration-forecourt",
    "auto",
  );
  await v.waitForTimeout(600);
  await move(v, "s", 2732, "y");
  await move(v, "a", 2560, "x", true);
  await move(v, "d", 2640, "x");
  await move(v, "a", 2599, "x", true);
  await v.waitForTimeout(500);
  const video = v.video();
  await ctx.close();
  await video.saveAs(`${D}/forecourt-walk.webm`);
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    `${D}/captures.json`,
    JSON.stringify(
      {
        rows,
        errors,
        walk,
        method:
          "Phaser POST_RENDER native canvas PNG; original controls only. Video uses live follow camera, native screenshots use fixed native framing. No teleport/state writes.",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS native captures and actual keyboard traversal; clearance",
    clearance,
  );
} finally {
  await browser.close();
}
