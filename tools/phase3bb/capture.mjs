import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const stage = process.argv[2] ?? "before",
  D = `docs/phase3bb-hotfix/${stage}`;
await fs.mkdir(D, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  viewport: { width: 960, height: 640 },
  deviceScaleFactor: 1,
  recordVideo: {
    dir: `/tmp/phase3bb-${stage}`,
    size: { width: 960, height: 640 },
  },
});
await context.addInitScript(() =>
  localStorage.setItem(
    "korean-arena-player-preferences-v1",
    JSON.stringify({ version: 1, characterId: "juni" }),
  ),
);
const page = await context.newPage(),
  errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto(
  "http://127.0.0.1:4320/3D-pharse5-/?qa&renderer=canvas&entry=transition",
);
await page.waitForFunction(
  () =>
    window.__GATE3__?.ready &&
    window.__NPC_WORLD__ &&
    window.__GATE3__.chunks.inflight === 0,
  {},
  { timeout: 90000 },
);
await page.waitForTimeout(1000);
await page.evaluate(() => {
  window.__motionTrace = [];
  let n = 0;
  const sample = () => {
    const s = window.__GATE3__;
    if (s)
      window.__motionTrace.push({
        t: performance.now(),
        x: s.x,
        y: s.y,
        frame: s.frame,
        camera: s.camera,
        paused: s.paused,
      });
    if (++n < 900) requestAnimationFrame(sample);
  };
  requestAnimationFrame(sample);
});
await page.screenshot({ path: `${D}/stationary-native.png` });
for (const keys of [
  ["d"],
  ["d", "w"],
  ["w"],
  ["a", "w"],
  ["a"],
  ["s"],
  ["Shift", "d"],
  ["Shift", "d", "s"],
]) {
  for (const key of keys) await page.keyboard.down(key);
  await page.waitForTimeout(350);
  await page.screenshot({ path: `${D}/motion-${keys.join("-")}.png` });
  for (const key of keys) await page.keyboard.up(key);
  await page.waitForTimeout(160);
}
await page.keyboard.press("Space");
await page.waitForTimeout(1000);
await fs.writeFile(
  `${D}/motion-trace.json`,
  JSON.stringify(
    { samples: await page.evaluate(() => window.__motionTrace), errors },
    null,
    2,
  ),
);
await page.screenshot({ path: `${D}/final-native.png` });
const video = page.video();
await context.close();
await video.saveAs(`${D}/gameplay.webm`);
await browser.close();
if (errors.length) throw Error(errors.join("\n"));
console.log(stage, "actual Phaser movement and native evidence captured");
