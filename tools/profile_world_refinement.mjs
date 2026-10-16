/* global cancelAnimationFrame, PerformanceObserver */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import os from "node:os";
const phase = process.env.PROFILE_PHASE ?? "before";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const entry = process.env.PROFILE_ENTRY ?? "production-review.html";
const out = "docs/world-refinement/quality";
await fs.mkdir(out, { recursive: true });
const results = [];
for (const [name, mobile, renderer] of [
  ["desktop-WebGL", false, ""],
  ["desktop-Canvas", false, "canvas"],
  ["mobile-Canvas", true, "canvas"],
]) {
  const browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args:
      renderer === "canvas"
        ? ["--no-sandbox"]
        : [
            "--no-sandbox",
            "--use-gl=angle",
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
          ],
  });
  const c = await browser.newContext({
    viewport: mobile
      ? { width: 390, height: 844 }
      : { width: 1440, height: 1140 },
    deviceScaleFactor: 1,
    isMobile: mobile,
    hasTouch: mobile,
    reducedMotion: "no-preference",
  });
  const p = await c.newPage();
  const errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  await p.goto(
    base +
      entry +
      "?qa" +
      (renderer ? "&renderer=" + renderer : "") +
      (process.env.PROFILE_QUERY ?? ""),
  );
  await p.waitForFunction(() => window.__SEOUL__?.ready);
  if (process.env.PROFILE_START)
    await p.evaluate(
      ([x, y]) => window.__SEOUL_TEST__.place(x, y),
      JSON.parse(process.env.PROFILE_START),
    );
  await p.locator("canvas").scrollIntoViewIfNeeded();
  await p.waitForTimeout(1200);
  const cdp = await c.newCDPSession(p);
  await cdp.send("Profiler.enable");
  await cdp.send("Profiler.setSamplingInterval", { interval: 1000 });
  await cdp.send("Profiler.start");
  await p.evaluate(() => {
    window.__FRAME_PROBE__ = {
      times: [],
      samples: [],
      longTasks: [],
      start: performance.now(),
      frame: window.__PIXEL_METRICS__.frameCount,
    };
    const probe = window.__FRAME_PROBE__;
    let last = performance.now();
    probe.observer = new PerformanceObserver((l) =>
      probe.longTasks.push(
        ...l
          .getEntries()
          .map((e) => ({ start: e.startTime, duration: e.duration })),
      ),
    );
    probe.observer.observe({ entryTypes: ["longtask"] });
    function tick(now) {
      if (!window.__FRAME_PROBE__) return;
      probe.times.push(now - last);
      probe.samples.push({
        t: now,
        x: window.__SEOUL__.x,
        y: window.__SEOUL__.y,
        frame: window.__PIXEL_METRICS__.frameCount,
        fps: window.__PIXEL_METRICS__.fps,
      });
      last = now;
      probe.raf = requestAnimationFrame(tick);
    }
    probe.raf = requestAnimationFrame(tick);
  });
  await p.locator("canvas").focus();
  for (let i = 0; i < 3; i++) {
    await p.keyboard.down("ArrowRight");
    await p.waitForTimeout(1300);
    await p.keyboard.up("ArrowRight");
    await p.keyboard.down("ArrowLeft");
    await p.waitForTimeout(1300);
    await p.keyboard.up("ArrowLeft");
  }
  const data = await p.evaluate(() => {
    const p = window.__FRAME_PROBE__;
    p.observer.disconnect();
    cancelAnimationFrame(p.raf);
    const sorted = p.times.slice(1).sort((a, b) => a - b);
    const ms = performance.now() - p.start;
    const out = {
      elapsedMs: ms,
      actualPhaserFrames: window.__PIXEL_METRICS__.frameCount - p.frame,
      measuredPhaserFPS:
        ((window.__PIXEL_METRICS__.frameCount - p.frame) * 1000) / ms,
      rafFrameMs: {
        p50: sorted[Math.floor(sorted.length * 0.5)],
        p95: sorted[Math.floor(sorted.length * 0.95)],
        p99: sorted[Math.floor(sorted.length * 0.99)],
      },
      rafOver33ms: sorted.filter((v) => v > 33.34).length,
      rafOver50ms: sorted.filter((v) => v > 50).length,
      longTasks: p.longTasks,
      samples: p.samples,
      renderer: window.__PIXEL_METRICS__.renderer,
      world: window.__SEOUL__.world,
    };
    delete window.__FRAME_PROBE__;
    return out;
  });
  const cpu = (await cdp.send("Profiler.stop")).profile;
  await fs.writeFile(`${out}/${phase}-${name}.cpuprofile`, JSON.stringify(cpu));
  results.push({ name, ...data, errors });
  await c.close();
  await browser.close();
  console.log(name, data.measuredPhaserFPS, data.rafFrameMs);
}
await fs.writeFile(
  `${out}/performance-${phase}.json`,
  JSON.stringify(
    {
      phase,
      entry,
      hardware: {
        cpu: os.cpus()[0].model,
        logicalCPUs: os.cpus().length,
        platform: os.platform(),
        node: process.version,
      },
      method:
        "System Chromium / software ANGLE Swiftshader explicitly forced for WebGL; Canvas uses default Chromium compositor (no forced software ANGLE). Browser launched separately per case; measured actual Phaser frame count and rAF intervals over real keyboard movement, 1x native camera; CPU sampling enabled consistently. No video encoding in this benchmark; emulated mobile, not physical hardware.",
      results,
    },
    null,
    2,
  ) + "\n",
);
