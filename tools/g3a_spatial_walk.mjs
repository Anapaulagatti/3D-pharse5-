import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1000, height: 700 },
  deviceScaleFactor: 1,
});
const results = [];
try {
  for (const [entry, pts] of [
    [
      "quay",
      [
        [1490, 4790],
        [984, 4790],
        [984, 4770],
      ],
    ],
    [
      "namsan",
      [
        [700, 3380],
        [326, 3380],
        [326, 3343],
      ],
    ],
    ["station", [[2598.5, 2610]]],
  ]) {
    await p.goto(
      `http://127.0.0.1:4284/gate3-review.html?scene=registration-refined&entry=${entry}`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    const start = await p.evaluate(() => ({
        x: window.__GATE3__.x,
        y: window.__GATE3__.y,
      })),
      samples = [];
    for (const goal of pts) {
      const deadline = Date.now() + 25000;
      let previous = [];
      while (true) {
        const s = await p.evaluate(() => ({
          x: window.__GATE3__.x,
          y: window.__GATE3__.y,
          view: window.__GATE3__.camera.worldView,
        }));
        const dx = goal[0] - s.x,
          dy = goal[1] - s.y;
        if (Math.hypot(dx, dy) < 1.8) {
          samples.push({ goal, actual: s });
          break;
        }
        if (Date.now() > deadline)
          throw Error(
            "Traversal timeout " + JSON.stringify({ entry, goal, s }),
          );
        const keys = [];
        if (Math.abs(dx) > 1.3) keys.push(dx > 0 ? "d" : "a");
        if (Math.abs(dy) > 1.3) keys.push(dy > 0 ? "s" : "w");
        if (Math.hypot(dx, dy) > 18) keys.push("Shift");
        for (const key of previous)
          if (!keys.includes(key)) await p.keyboard.up(key);
        for (const key of keys)
          if (!previous.includes(key)) await p.keyboard.down(key);
        previous = keys;
        await p.waitForTimeout(60);
      }
      for (const key of previous) await p.keyboard.up(key);
    }
    results.push({
      entry,
      start,
      samples,
      status: "PASS",
      method:
        "Real WASD/Shift input; no teleport, logical position updates or QA movement overrides",
    });
  }
  await fs.writeFile(
    "docs/g3a-spatial-review/traversal.json",
    JSON.stringify(results, null, 2),
  );
  console.log(
    "PASS real keyboard traversal: quay1500px, Maru/Namsan approach, protected station threshold",
  );
} finally {
  await b.close();
}
