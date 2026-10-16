import { chromium } from "playwright";
import fs from "node:fs/promises";
const out = "docs/seoul-production/quality";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const c = await b.newContext({
  viewport: { width: 1024, height: 900 },
  deviceScaleFactor: 1,
  recordVideo: {
    dir: ".cache/production/video",
    size: { width: 1024, height: 900 },
  },
});
const p = await c.newPage();
const video = p.video();
const errors = [],
  route = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
await p.goto(
  (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/") +
    "production-review.html?renderer=canvas",
);
await p.waitForFunction(() => window.__SEOUL__?.ready);
if (await p.evaluate(() => !!window.__SEOUL_TEST__))
  throw Error("Walkthrough must not expose placement hook");
await p.addStyleTag({
  content:
    "header,.intro,aside,.directions,footer{display:none!important}main{padding:0!important;width:1024px!important;max-width:none!important}.play-layout{display:block!important;width:1024px!important}.stage-wrap{width:1024px!important}#stage{width:1024px!important;height:768px!important}.touch-pad{display:none!important}.game-bar{flex-wrap:wrap!important}body{margin:0!important}",
});
await p.waitForTimeout(500);
let held = new Set();
async function keys(next) {
  for (const k of held) if (!next.has(k)) await p.keyboard.up(k);
  for (const k of next) if (!held.has(k)) await p.keyboard.down(k);
  held = next;
}
async function go(x, y, label) {
  await p.locator("canvas").focus();
  const start = Date.now();
  for (;;) {
    const pos = await p.evaluate(() => window.__SEOUL__);
    if (Math.abs(pos.x - x) < 4 && Math.abs(pos.y - y) < 4) break;
    if (Date.now() - start > 35000)
      throw Error(`route stuck ${label} ${JSON.stringify(pos)}`);
    const next = new Set(["Shift"]);
    if (pos.x < x - 3) next.add("ArrowRight");
    if (pos.x > x + 3) next.add("ArrowLeft");
    if (pos.y < y - 3) next.add("ArrowDown");
    if (pos.y > y + 3) next.add("ArrowUp");
    await keys(next);
    await p.waitForTimeout(60);
  }
  await keys(new Set());
  await p.waitForTimeout(180);
  route.push({
    label,
    target: [x, y],
    actual: await p.evaluate(() => window.__SEOUL__),
    time: Date.now(),
  });
  console.log(label);
}
async function explore() {
  await p.locator("#interact").click();
  await p.waitForTimeout(950);
}
async function close() {
  await p.locator("#close-dialog").click();
}
try {
  await go(2048, 1328, "Ceremonial axis");
  await go(2048, 832, "Gateway");
  await explore();
  await close();
  await go(2048, 496, "First outer court / inner palace closed");
  await go(2048, 832, "Return through gate");
  await explore();
  await close();
  for (const [x, y] of [
    [2048, 1424],
    [1856, 1424],
    [1600, 1408],
    [1312, 1280],
    [960, 1248],
    [672, 1200],
    [672, 960],
  ])
    await go(x, y, "Organic academy approach");
  await p.locator("#wave").click();
  await p.waitForTimeout(1500);
  await go(672, 832, "Reading hall doorway");
  await explore();
  await p.waitForFunction(() => window.__SEOUL__?.area === "room");
  await go(384, 397, "Existing reading lesson");
  await explore();
  await p
    .locator("#dialog-copy")
    .getByRole("button", { name: "giyeok", exact: true })
    .click();
  await p.waitForTimeout(1100);
  await close();
  await go(384, 490, "Reciprocal room exit");
  await explore();
  await p.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
  for (const [x, y] of [
    [672, 1200],
    [960, 1248],
    [1312, 1280],
    [1600, 1408],
    [1856, 1424],
    [2048, 1424],
    [2432, 1424],
    [2688, 1312],
    [2880, 1216],
    [3184, 1280],
    [3168, 1184],
  ])
    await go(x, y, "Connected history street");
  await explore();
  await close();
  await go(3168, 980, "Science courtyard");
  await p.locator("#wave").click();
  await p.waitForTimeout(1400);
  for (const [x, y] of [
    [3168, 1184],
    [3184, 1280],
    [3520, 1456],
    [3552, 1392],
  ])
    await go(x, y, "Museum terrace");
  await explore();
  await close();
  await p.locator("#celebrate").click();
  await p.waitForTimeout(1800);
} finally {
  await keys(new Set());
  await fs.writeFile(
    `${out}/walkthrough-input-log.json`,
    JSON.stringify(
      {
        method:
          "Continuous real keyboard/touch-button Phaser capture. No teleport/place hook, no screenshots during recording. CSS hides surrounding page only; native world1x.",
        errors,
        route,
      },
      null,
      2,
    ) + "\n",
  );
  await c.close();
  await video.saveAs(".cache/production/walkthrough.webm");
  await b.close();
}
if (errors.length) throw Error(JSON.stringify(errors));
console.log("Actual input walkthrough complete");
