import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3a-corrections";
const routes = JSON.parse(await fs.readFile(D + "/route-points.json", "utf8"));
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const reports = [];
const errors = [];
for (const [id, entry] of [
  ["station-threshold", "station"],
  ["retail-to-station", "retail"],
  ["bakery-to-bridge", "bakery"],
]) {
  const context = await b.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: "/tmp/g3a-corrections-video",
      size: { width: 1280, height: 1000 },
    },
  });
  const p = await context.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  await p.goto(
    `http://127.0.0.1:4271/gate3-review.html?scene=registration&entry=${entry}`,
  );
  await p.waitForFunction(() => window.__GATE3__?.ready);
  await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
  const before = await p.evaluate(() => window.__GATE3__);
  for (const [x, y] of routes[id])
    for (const axis of ["x", "y"]) {
      const target = axis === "x" ? x : y,
        start = await p.evaluate(() => window.__GATE3__);
      if (Math.abs(start[axis] - target) < 1.6) continue;
      const key =
        axis === "x"
          ? target > start.x
            ? "d"
            : "a"
          : target > start.y
            ? "s"
            : "w";
      await p.keyboard.down(key);
      try {
        if (Math.abs(start[axis] - target) > 25) {
          await p.keyboard.down("Shift");
          await p.waitForFunction(
            ({ axis, target }) =>
              Math.abs(window.__GATE3__[axis] - target) < 20,
            { axis, target },
            {
              polling: "raf",
              timeout: 5000 + Math.abs(start[axis] - target) * 40,
            },
          );
          await p.keyboard.up("Shift");
        }
        await p.waitForFunction(
          ({ axis, target }) => Math.abs(window.__GATE3__[axis] - target) < 1.6,
          { axis, target },
          { polling: "raf", timeout: 10000 },
        );
      } finally {
        await p.keyboard.up(key);
        await p.keyboard.up("Shift");
      }
    }
  await p.waitForTimeout(300);
  const after = await p.evaluate(() => window.__GATE3__);
  await p.locator("canvas").screenshot({ path: D + "/" + id + "-end.png" });
  const video = p.video();
  await context.close();
  await video.saveAs("/tmp/g3a-" + id + ".webm");
  reports.push({
    id,
    entry,
    before,
    after,
    method:
      "Normal review entry, real WASD/Shift input at approved60/100px/s. No QA relocation, teleports or speed override. Recording is excluded from benchmark data.",
  });
  console.log(id, "done", after.x, after.y);
}
await fs.writeFile(
  D + "/traversal-report.json",
  JSON.stringify({ errors, reports }, null, 2),
);
await b.close();
if (errors.length) throw Error(errors.join("\n"));
