/* global cancelAnimationFrame */
import { chromium } from "playwright";
import fs from "node:fs/promises";
const phase = process.env.PROFILE_PHASE ?? "before";
const old = phase === "before";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const page = await browser.newPage({
  viewport: { width: 1440, height: 1140 },
  reducedMotion: "no-preference",
});
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
await page.goto(
  (process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/") +
    (old ? "production-review.html" : "refinement-review.html") +
    "?qa&renderer=canvas",
);
await page.waitForFunction(() => window.__SEOUL__?.ready);
const trips = old
  ? [
      {
        name: "Gate → Academy front",
        start: [2048, 832],
        via: [
          [2048, 1424],
          [1856, 1424],
          [1600, 1408],
          [1312, 1280],
          [960, 1248],
          [672, 1200],
        ],
      },
      {
        name: "Academy front → Workshop",
        start: [672, 1200],
        via: [
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
        ],
      },
      {
        name: "Workshop → Museum",
        start: [3168, 1184],
        via: [
          [3184, 1280],
          [3520, 1456],
          [3552, 1392],
        ],
      },
    ]
  : [
      {
        name: "Gate → Academy front",
        start: [1152, 832],
        via: [
          [1152, 1328],
          [1008, 1472],
          [864, 1536],
          [544, 1520],
        ],
      },
      {
        name: "Academy front → Workshop",
        start: [544, 1520],
        via: [
          [864, 1536],
          [1008, 1472],
          [1152, 1328],
          [1376, 1344],
          [1376, 1504],
          [1632, 1536],
        ],
      },
      {
        name: "Workshop → Museum",
        start: [1632, 1536],
        via: [
          [1584, 1632],
          [1640, 1792],
          [1856, 1840],
          [1984, 1808],
        ],
      },
    ];
const results = [];
let held = new Set();
async function keys(next) {
  for (const k of held) if (!next.has(k)) await page.keyboard.up(k);
  for (const k of next) if (!held.has(k)) await page.keyboard.down(k);
  held = next;
}
try {
  for (const trip of trips) {
    await page.evaluate(
      ([x, y]) => window.__SEOUL_TEST__.place(x, y),
      trip.start,
    );
    await page.waitForTimeout(200);
    await page.locator("canvas").focus();
    await page.evaluate(() => {
      window.__TRAVEL__ = {
        start: performance.now(),
        last: [window.__SEOUL__.x, window.__SEOUL__.y],
        distance: 0,
        samples: [],
        frame: window.__PIXEL_METRICS__.frameCount,
      };
      const m = window.__TRAVEL__;
      function tick() {
        const p = window.__SEOUL__;
        m.distance += Math.hypot(p.x - m.last[0], p.y - m.last[1]);
        m.last = [p.x, p.y];
        m.samples.push({
          t: performance.now(),
          x: p.x,
          y: p.y,
          speed: window.__PIXEL_METRICS__.speed,
        });
        m.raf = requestAnimationFrame(tick);
      }
      m.raf = requestAnimationFrame(tick);
    });
    for (const [x, y] of trip.via) {
      const start = Date.now();
      for (;;) {
        const pos = await page.evaluate(() => window.__SEOUL__);
        if (Math.abs(pos.x - x) < 7 && Math.abs(pos.y - y) < 7) break;
        if (Date.now() - start > 45000)
          throw Error(`Stuck ${trip.name} ${x},${y} at ${JSON.stringify(pos)}`);
        const next = new Set();
        if (pos.x < x - 5) next.add("ArrowRight");
        if (pos.x > x + 5) next.add("ArrowLeft");
        if (pos.y < y - 5) next.add("ArrowDown");
        if (pos.y > y + 5) next.add("ArrowUp");
        await keys(next);
        await page.waitForTimeout(50);
      }
    }
    await keys(new Set());
    await page.waitForTimeout(140);
    const m = await page.evaluate(() => {
      const t = window.__TRAVEL__;
      cancelAnimationFrame(t.raf);
      const d = {
        elapsedSeconds: (performance.now() - t.start) / 1000,
        actualDistancePx: t.distance,
        phaserFrames: window.__PIXEL_METRICS__.frameCount - t.frame,
        speeds: [...new Set(t.samples.map((s) => s.speed))],
        samples: t.samples,
      };
      delete window.__TRAVEL__;
      return d;
    });
    results.push({ ...trip, ...m });
    console.log(trip.name, m.elapsedSeconds, m.actualDistancePx);
  }
} finally {
  await keys(new Set());
  await browser.close();
  await fs.writeFile(
    `docs/world-refinement/quality/travel-${phase}.json`,
    JSON.stringify(
      {
        phase,
        method:
          "Actual normal-speed keyboard movement; no Shift/Run, no speed changes. Opt-in QA placement ONLY resets each independent trip start, never during a timed route. Identical functional destinations, documented changed streets. Distances sum actual resolved position changes; includes acceleration/turning.",
        results,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
}
