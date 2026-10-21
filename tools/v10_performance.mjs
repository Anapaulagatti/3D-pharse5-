import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const results = [];
try {
  for (const [renderer, mobile] of [
    ["canvas", false],
    ["webgl", false],
    ["canvas", true],
  ]) {
    const context = await browser.newContext({
      viewport: mobile
        ? { width: 844, height: 390 }
        : { width: 1440, height: 1140 },
      deviceScaleFactor: 1,
      isMobile: mobile,
      hasTouch: mobile,
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const errors = [],
      requests = new Set();
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("response", (r) => {
      if (r.status() >= 400) errors.push(r.url());
    });
    page.on("request", (r) => requests.add(new URL(r.url()).pathname));
    const begin = Date.now();
    await page.goto(
      `http://127.0.0.1:4220/3D-pharse5-/v10-city-review.html?qa&renderer=${renderer}`,
    );
    await page.waitForFunction(() => window.__SEOUL__?.ready);
    const readyMs = Date.now() - begin;
    const samples = [];
    for (const [name, x, y] of [
      ["town", 2352, 2960],
      ["station", 3776, 2832],
      ["namsan", 736, 3040],
      ["campus", 960, 4080],
      ["waterfront", 3776, 4224],
      ["jeju", 3104, 5392],
    ]) {
      await page.evaluate(
        ([x, y]) => window.__SEOUL_TEST__.place(x, y),
        [x, y],
      );
      await page.waitForTimeout(500);
      const timing = await page.evaluate(
        () =>
          new Promise((resolve) => {
            const d = [],
              begin = performance.now();
            let last = begin;
            function tick(t) {
              d.push(t - last);
              last = t;
              if (t - begin < 2500) requestAnimationFrame(tick);
              else {
                d.sort((a, b) => a - b);
                resolve({
                  frames: d.length,
                  medianMs: d[Math.floor(d.length * 0.5)],
                  p95Ms: d[Math.floor(d.length * 0.95)],
                  averageFps: (d.length * 1000) / (t - begin),
                  metrics: window.__PIXEL_METRICS__,
                });
              }
            }
            requestAnimationFrame(tick);
          }),
      );
      samples.push({ name, ...timing });
    }
    let touch = null;
    if (mobile) {
      await page.evaluate(() => window.__SEOUL_TEST__.place(2352, 2960));
      await page.waitForTimeout(400);
      const dir = ".cache/v10-production/mobile-frames";
      await fs.mkdir(dir, { recursive: true });
      const frames = [],
        writes = [],
        cdp = await context.newCDPSession(page);
      cdp.on("Page.screencastFrame", (e) => {
        const name = String(frames.length).padStart(6, "0") + ".jpg";
        frames.push({ name, t: e.metadata.timestamp });
        writes.push(
          fs.writeFile(dir + "/" + name, Buffer.from(e.data, "base64")),
        );
        void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
      });
      await cdp.send("Page.startScreencast", {
        format: "jpeg",
        quality: 85,
        maxWidth: 844,
        maxHeight: 390,
        everyNthFrame: 2,
      });
      const b = await page.locator("#joystick").boundingBox(),
        x = b.x + b.width / 2,
        y = b.y + b.height / 2,
        start = await page.evaluate(() => window.__SEOUL__.x);
      const touchPositions = [];
      for (const sign of [1, -1]) {
        await cdp.send("Input.dispatchTouchEvent", {
          type: "touchStart",
          touchPoints: [{ x, y, id: 1 }],
        });
        await cdp.send("Input.dispatchTouchEvent", {
          type: "touchMove",
          touchPoints: [{ x: x + sign * b.width * 0.3, y, id: 1 }],
        });
        await page.waitForTimeout(2500);
        touchPositions.push(await page.evaluate(() => window.__SEOUL__.x));
        await cdp.send("Input.dispatchTouchEvent", {
          type: "touchEnd",
          touchPoints: [],
        });
        await page.waitForTimeout(1000);
      }
      touch = {
        positions: touchPositions,
        maxExcursion: Math.max(
          ...touchPositions.map((x) => Math.abs(x - start)),
        ),
        start,
        after: await page.evaluate(() => window.__SEOUL__.x),
        source:
          "Emulated landscape mobile, one QA camera start then real CDP joystick touches",
      };
      await page
        .locator("canvas")
        .screenshot({ path: "docs/v10-production/V10_MOBILE_NATIVE.png" });
      await cdp.send("Page.stopScreencast");
      await Promise.all(writes);
      await fs.writeFile(
        dir + "/frames.txt",
        frames
          .map(
            (f, i) =>
              `file '${f.name}'\nduration ${Math.max(0.001, (frames[i + 1]?.t ?? f.t + 0.1) - f.t)}`,
          )
          .join("\n") + "\n",
      );
      execFileSync("ffmpeg", [
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        dir + "/frames.txt",
        "-fps_mode",
        "vfr",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "docs/v10-production/V10_MOBILE_LANDSCAPE.mp4",
      ]);
      if (touch.maxExcursion < 30)
        throw Error("Joystick did not move through the new town");
      touch.recordedSeconds = frames.at(-1).t - frames[0].t;
    }
    results.push({
      renderer,
      mobile,
      readyMs,
      samples,
      touch,
      errors,
      requests: [...requests],
    });
    await context.close();
  }
  await fs.writeFile(
    "docs/v10-production/performance.json",
    JSON.stringify(
      {
        environment:
          "Headless Linux Chromium; WebGL uses software SwiftShader; mobile is emulation, not phone hardware. Per-camera RAF measurements, 2.5s after 0.5s warmup. Other QA processes may share host.",
        results,
      },
      null,
      2,
    ) + "\n",
  );
  if (results.some((r) => r.errors.length)) throw Error("Runtime errors");
} finally {
  await browser.close();
}
