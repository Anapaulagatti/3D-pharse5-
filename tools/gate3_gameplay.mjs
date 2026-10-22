import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const dir = "docs/gate3a";
const routes = JSON.parse(
  await fs.readFile(dir + "/route-points.json", "utf8"),
);
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  headless: true,
  args: ["--no-sandbox"],
});
const errors = [];
const reports = [];
async function walk(page, points) {
  for (const [x, y] of points) {
    for (const axis of ["x", "y"]) {
      const target = axis === "x" ? x : y;
      const start = await page.evaluate(() => window.__GATE3__);
      if (Math.abs(start[axis] - target) < 1.5) continue;
      const key =
        axis === "x"
          ? target > start.x
            ? "d"
            : "a"
          : target > start.y
            ? "s"
            : "w";
      await page.keyboard.down("Shift");
      await page.keyboard.down(key);
      try {
        await page.waitForFunction(
          ({ axis, target }) => Math.abs(window.__GATE3__[axis] - target) < 1.7,
          { axis, target },
          {
            polling: "raf",
            timeout: 5000 + Math.abs(start[axis] - target) * 35,
          },
        );
      } finally {
        await page.keyboard.up(key);
        await page.keyboard.up("Shift");
      }
    }
  }
}
for (const [name, search, points] of [
  ["district-traversal", "scene=district", routes["district-crossings"]],
  [
    "north-registration-traversal",
    "scene=world&entry=north",
    routes["north-to-spine"],
  ],
]) {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: "/tmp/gate3-video",
      size: { width: 1280, height: 1000 },
    },
  });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("http://127.0.0.1:4261/gate3-review.html?" + search);
  await page.waitForFunction(() => window.__GATE3__?.ready);
  await page.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  const before = await page.evaluate(() => window.__GATE3__);
  await walk(page, points);
  await page.waitForTimeout(400);
  const after = await page.evaluate(() => window.__GATE3__);
  await page.locator("canvas").screenshot({ path: `${dir}/${name}-end.png` });
  const video = page.video();
  await context.close();
  await video.saveAs(`/tmp/${name}.webm`);
  reports.push({
    id: name,
    method:
      "Real keyboard WASD + Shift at original100px/s; normal entry bookmarks; no teleport, speed overrides or coordinate mutation",
    before,
    after,
  });
  console.log(name, after.x, after.y, after.chunks);
}
// Repeated real Scenic Tour / overview / return: camera only, Juni remains in place.
const context = await browser.newContext({
  viewport: { width: 844, height: 390 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
  recordVideo: { dir: "/tmp/gate3-video", size: { width: 844, height: 390 } },
});
const page = await context.newPage();
page.on("pageerror", (e) => errors.push(e.message));
await page.goto("http://127.0.0.1:4261/gate3-review.html?scene=world");
await page.waitForFunction(() => window.__GATE3__?.ready);
const initial = await page.evaluate(() => window.__GATE3__);
const samples = [];
await page.locator("#scenic").click();
await page.locator("#start-tour").click();
for (let i = 0; i < 22; i++) {
  await page.waitForTimeout(1000);
  samples.push(await page.evaluate(() => window.__GATE3__));
}
if (!(await page.locator("#return-juni").isVisible()))
  await page.locator("#tour-controls").click();
await page.locator("#return-juni").click();
await page.waitForTimeout(1500);
await page.locator("#scenic").click();
await page.locator("#overview-mode").click();
await page.waitForTimeout(600);
await page.locator("canvas").screenshot({ path: dir + "/mobile-overview.png" });
if (!(await page.locator("#return-juni").isVisible()))
  await page.locator("#tour-controls").click();
await page.locator("#return-juni").click();
await page.waitForTimeout(1200);
// Repeat to prove revisiting loads/evicts rather than accumulating all world textures.
await page.locator("#scenic").click();
await page.locator("#start-tour").click();
for (let i = 0; i < 20; i++) {
  await page.waitForTimeout(1000);
  samples.push(await page.evaluate(() => window.__GATE3__));
}
await page.locator("canvas").screenshot({ path: dir + "/mobile-tour.png" });
if (!(await page.locator("#return-juni").isVisible()))
  await page.locator("#tour-controls").click();
await page.locator("#return-juni").click();
await page.waitForTimeout(1200);
const final = await page.evaluate(() => window.__GATE3__);
const video = page.video();
await context.close();
await video.saveAs("/tmp/camera-tour.webm");
reports.push({
  id: "mobile-emulated-camera-churn",
  physicalDevice: "NOT TESTED",
  initial,
  final,
  samples,
  juniPreserved: Math.hypot(initial.x - final.x, initial.y - final.y) === 0,
  bounded: samples.every((s) => s.chunks.reservedBytes <= s.chunks.budgetBytes),
});
await fs.writeFile(
  dir + "/gameplay-report.json",
  JSON.stringify({ errors, reports }, null, 2),
);
await browser.close();
if (errors.length) throw Error(errors.join("\n"));
