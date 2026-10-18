/* global cancelAnimationFrame, PerformanceObserver */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import os from "node:os";
import { createHash } from "node:crypto";
const base =
    process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/",
  out = "docs/v3-final/quality";
const results = [];
for (const [name, entry, pose, mobile, gl, dpr] of [
  ["before-Canvas", "full-world-review.html", [2176, 1328], false, false, 1],
  [
    "before-software-WebGL",
    "full-world-review.html",
    [2176, 1328],
    false,
    true,
    1,
  ],
  [
    "after-heritage-Canvas",
    "v3-world-review.html",
    [2176, 1328],
    false,
    false,
    1,
  ],
  ["after-namsan-Canvas", "v3-world-review.html", [832, 2912], false, false, 1],
  ["after-bora-Canvas", "v3-world-review.html", [3712, 2896], false, false, 1],
  [
    "after-coast-mobile-DPR1",
    "v3-world-review.html",
    [2048, 2944],
    true,
    false,
    1,
  ],
  [
    "after-jeju-mobile-DPR3",
    "v3-world-review.html",
    [2240, 4208],
    true,
    false,
    3,
  ],
  [
    "after-software-WebGL",
    "v3-world-review.html",
    [2176, 1328],
    false,
    true,
    1,
  ],
]) {
  const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: gl
      ? [
          "--no-sandbox",
          "--use-gl=angle",
          "--use-angle=swiftshader",
          "--enable-unsafe-swiftshader",
        ]
      : ["--no-sandbox"],
  });
  try {
    const c = await b.newContext({
      viewport: mobile
        ? { width: 844, height: 390 }
        : { width: 1440, height: 1140 },
      isMobile: mobile,
      hasTouch: mobile,
      deviceScaleFactor: dpr,
      reducedMotion: "no-preference",
    });
    const p = await c.newPage(),
      errors = [];
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("console", (m) => {
      if (m.type() === "error") errors.push(m.text());
    });
    await p.goto(base + entry + "?qa&renderer=" + (gl ? "webgl" : "canvas"));
    await p.waitForFunction(() => window.__SEOUL__?.ready);
    await p.evaluate(([x, y]) => window.__SEOUL_TEST__.place(x, y), pose);
    await p.waitForTimeout(1200);
    const d = await c.newCDPSession(p);
    await d.send("Profiler.enable");
    await d.send("Profiler.setSamplingInterval", { interval: 1000 });
    await d.send("Profiler.start");
    await p.evaluate(() => {
      const q = {
        start: performance.now(),
        frame: window.__PIXEL_METRICS__.frameCount,
        times: [],
        samples: [],
        longTasks: [],
      };
      window.__KOREA_PROBE__ = q;
      let last = performance.now();
      q.observer = new PerformanceObserver((l) =>
        q.longTasks.push(
          ...l
            .getEntries()
            .map((e) => ({ start: e.startTime, duration: e.duration })),
        ),
      );
      q.observer.observe({ entryTypes: ["longtask"] });
      const tick = (now) => {
        q.times.push(now - last);
        last = now;
        q.samples.push({
          t: now,
          x: window.__SEOUL__.x,
          y: window.__SEOUL__.y,
          frame: window.__PIXEL_METRICS__.frameCount,
          animation: window.__PLAZA_REVIEW__?.frame,
        });
        q.raf = requestAnimationFrame(tick);
      };
      q.raf = requestAnimationFrame(tick);
    });
    await p.locator("canvas").focus();
    for (let i = 0; i < 3; i++)
      for (const key of ["ArrowRight", "ArrowLeft"]) {
        await p.keyboard.down(key);
        await p.waitForTimeout(1300);
        await p.keyboard.up(key);
      }
    const data = await p.evaluate(() => {
      const q = window.__KOREA_PROBE__;
      q.observer.disconnect();
      cancelAnimationFrame(q.raf);
      const elapsedMs = performance.now() - q.start,
        t = q.times.slice(1).sort((a, b) => a - b);
      return {
        elapsedMs,
        actualPhaserFrames: window.__PIXEL_METRICS__.frameCount - q.frame,
        measuredPhaserFPS:
          ((window.__PIXEL_METRICS__.frameCount - q.frame) * 1000) / elapsedMs,
        rafFrameMs: {
          p50: t[Math.floor(t.length * 0.5)],
          p95: t[Math.floor(t.length * 0.95)],
          p99: t[Math.floor(t.length * 0.99)],
        },
        longTasks: q.longTasks,
        samples: q.samples,
        renderer: window.__PIXEL_METRICS__.renderer,
        world: window.__SEOUL__.world,
        visibleProps: window.__SEOUL__.activeProps,
        totalProps: window.__SEOUL__.totalProps,
        canvas: [
          document.querySelector("canvas").width,
          document.querySelector("canvas").height,
        ],
        cue: window.__FULL_WORLD__,
        fallback: document.body.dataset.fallback,
        dpr: window.devicePixelRatio,
      };
    });
    const cpu = (await d.send("Profiler.stop")).profile;
    await fs.writeFile(`${out}/${name}.cpuprofile`, JSON.stringify(cpu));
    results.push({ name, ...data, errors });
    if (errors.length) throw Error(JSON.stringify(errors));
    console.log(name, data.measuredPhaserFPS, data.rafFrameMs);
  } finally {
    await b.close();
  }
}
const inputs = {};
for (const f of [
  "assets-src/v3-final/map/outdoor-bundle.json",
  "public/review/v3-final/world/plaza.json",
])
  inputs[f] = createHash("sha256")
    .update(await fs.readFile(f))
    .digest("hex");
await fs.writeFile(
  `${out}/performance.json`,
  JSON.stringify(
    {
      hardware: {
        cpu: os.cpus()[0].model,
        logicalCPUs: os.cpus().length,
        platform: os.platform(),
        node: process.version,
      },
      method:
        "Actual Phaser frame deltas and rAF intervals during7.8s of real movement;1ms CPU profiling identical per case. No video/encoder runs concurrently. Separate fresh browser per target. Candidate uses actual default software-GPU detection, no renderer override; baseline Canvas explicitly selected. Canvas default compositor; explicit software ANGLE Swiftshader only for WebGL cases. Mobile844x390DPR1/3 is emulated; same actual keyboard movement across baseline/candidate, not physical device. Same desktop native1024x768 baseline vs candidate; no universal FPS improvement claim.",
      inputs,
      results,
    },
    null,
    2,
  ) + "\n",
);
