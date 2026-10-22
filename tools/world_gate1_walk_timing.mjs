import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
const reports = [],
  errors = [];
const routes = {
  before: [
    {
      id: "cafe-to-namsan",
      points: [
        [700, 2690],
        [2048, 2690],
        [2048, 3260],
        [1460, 3260],
      ],
    },
    {
      id: "market-to-ferry",
      points: [
        [1440, 3740],
        [1440, 3790],
        [2900, 3790],
        [2900, 3480],
      ],
    },
  ],
  after: [
    {
      id: "cafe-to-namsan",
      points: [
        [700, 2690],
        [940, 2790],
        [950, 3280],
        [1460, 3260],
      ],
    },
    {
      id: "market-to-ferry",
      points: [
        [1440, 3740],
        [2048, 3480],
        [2900, 3480],
      ],
    },
  ],
};
async function run(version, port) {
  const browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-background-timer-throttling",
      "--disable-renderer-backgrounding",
    ],
  });
  try {
    const p = await browser.newPage({
      viewport: { width: 1024, height: 888 },
      deviceScaleFactor: 1,
    });
    p.on("pageerror", (e) => errors.push(e.message));
    await p.goto(`http://127.0.0.1:${port}/3D-pharse5-/world-gate1.html?qa`);
    await p.waitForFunction(() => window.__WORLD_PLAN__?.ready);
    for (const route of routes[version]) {
      await p.evaluate(
        ([x, y]) => window.__WORLD_PLAN_TEST__.place(x, y),
        route.points[0],
      );
      await p.waitForTimeout(80);
      let keys = new Set(),
        distance = 0,
        last = await p.evaluate(() => ({
          x: window.__WORLD_PLAN__.x,
          y: window.__WORLD_PLAN__.y,
          t: performance.now(),
        })),
        start = last.t;
      const trace = [last];
      for (const [tx, ty] of route.points.slice(1)) {
        const deadline =
          Date.now() +
          (Math.hypot(tx - last.x, ty - last.y) / 60) * 2000 +
          5000;
        while (true) {
          const pos = await p.evaluate(() => ({
            x: window.__WORLD_PLAN__.x,
            y: window.__WORLD_PLAN__.y,
            t: performance.now(),
          }));
          distance += Math.hypot(pos.x - last.x, pos.y - last.y);
          trace.push(pos);
          last = pos;
          const dx = tx - pos.x,
            dy = ty - pos.y;
          if (Math.abs(dx) < 3 && Math.abs(dy) < 3) break;
          if (Date.now() > deadline)
            throw Error(
              `Stuck ${version}/${route.id}: ${JSON.stringify(pos)} toward ${tx},${ty}`,
            );
          const wanted = new Set();
          if (Math.abs(dx) >= 3)
            wanted.add(dx > 0 ? "ArrowRight" : "ArrowLeft");
          if (Math.abs(dy) >= 3) wanted.add(dy > 0 ? "ArrowDown" : "ArrowUp");
          for (const k of keys) if (!wanted.has(k)) await p.keyboard.up(k);
          for (const k of wanted) if (!keys.has(k)) await p.keyboard.down(k);
          keys = wanted;
          await p.waitForTimeout(45);
        }
      }
      for (const k of keys) await p.keyboard.up(k);
      const wallSeconds = (last.t - start) / 1000,
        ideal = route.points
          .slice(1)
          .reduce(
            (sum, pt, i) =>
              sum +
              Math.hypot(
                pt[0] - route.points[i][0],
                pt[1] - route.points[i][1],
              ),
            0,
          );
      assert(
        Math.hypot(
          last.x - route.points.at(-1)[0],
          last.y - route.points.at(-1)[1],
        ) < 5,
      );
      const report = {
        version,
        id: route.id,
        configuredWalkSpeed: 60,
        runKeyUsed: false,
        qaPlacement: "Start only; all subsequent travel real keyboard",
        idealPolylinePx: Math.round(ideal),
        actualDistancePx: Math.round(distance),
        wallSeconds: Math.round(wallSeconds * 100) / 100,
        observedPxPerSecond: Math.round((distance / wallSeconds) * 100) / 100,
        points: route.points,
        trace,
      };
      reports.push(report);
      console.log(
        JSON.stringify({
          ...report,
          trace: `${trace.length} actual sampled positions`,
        }),
      );
    }
  } finally {
    await browser.close();
  }
}
const outcomes = await Promise.allSettled([
  run("before", 4242),
  run("after", 4240),
]);
for (const r of outcomes)
  if (r.status === "rejected") errors.push(String(r.reason));
await fs.writeFile(
  "docs/world-gate1/walking-input-timing.json",
  JSON.stringify(
    {
      baselineCommit: "21554fac5f3037d51ea3db3e1d79247ce772668e",
      reports,
      errors,
      limits: [
        "These are recommended itinerary comparisons, not claims that collision-grid minima changed.",
        "Polyline lengths are ideal analog-path distances; eight-direction keyboard traces can be longer.",
        "Browser wall time includes rendering and input overhead; configured speeds remain 60/100.",
        "No teleport except one initial QA placement per itinerary.",
      ],
    },
    null,
    2,
  ) + "\n",
);
assert.equal(errors.length, 0, JSON.stringify(errors));
