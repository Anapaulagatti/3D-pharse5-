import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const tour = JSON.parse(
  await fs.readFile("assets-src/v9-world/plan/walkthrough.json", "utf8"),
);
const base = process.env.PIXEL_VIDEO_DIR ?? `.cache/v9-video-${Date.now()}`;
await fs.mkdir(base + "/frames", { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
let context,
  cdp,
  page,
  capturing = false,
  active = false;
const frames = [],
  visits = [],
  errors = [],
  writes = [],
  trace = [];
let pendingError;
try {
  context = await browser.newContext({
    viewport: { width: 1280, height: 960 },
    deviceScaleFactor: 1,
    hasTouch: true,
    reducedMotion: "no-preference",
  });
  page = await context.newPage();
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (e) => {
    if (e.type() === "error") errors.push(e.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await page.goto(
    "http://127.0.0.1:4201/3D-pharse5-/v9-world-review.html?renderer=canvas",
  );
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  if (await page.evaluate(() => !!window.__SEOUL_TEST__))
    throw Error("Normal entry must not expose placement hook");
  cdp = await context.newCDPSession(page);
  let number = 0;
  cdp.on("Page.screencastFrame", (event) => {
    const index = number++,
      file = `frames/${String(index).padStart(6, "0")}.jpg`,
      bytes = Buffer.from(event.data, "base64");
    frames.push({
      index,
      file,
      timestamp: event.metadata.timestamp,
      sha256: createHash("sha256").update(bytes).digest("hex"),
    });
    const writing = fs.writeFile(base + "/" + file, bytes).catch((e) => {
      pendingError = e;
    });
    writes.push(writing);
    void cdp
      .send("Page.screencastFrameAck", { sessionId: event.sessionId })
      .catch((e) => {
        pendingError = e;
      });
  });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 84,
    maxWidth: 1280,
    maxHeight: 960,
    everyNthFrame: 2,
  });
  capturing = true;
  const stick = await page.locator("#joystick").boundingBox(),
    run = await page.locator("#run").boundingBox();
  if (!stick || !run) throw Error("Public controls unavailable");
  const cx = stick.x + stick.width / 2,
    cy = stick.y + stick.height / 2,
    radius = stick.width * 0.34,
    runner = { x: run.x + run.width / 2, y: run.y + run.height / 2, id: 2 };
  const start = async () => {
    if (!active) {
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x: cx, y: cy, id: 1 }, runner],
      });
      active = true;
    }
  };
  const stop = async () => {
    if (active) {
      await cdp.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
      active = false;
    }
  };
  async function drive(points) {
    await start();
    let previous = await page.evaluate(() => [
        window.__SEOUL__.x,
        window.__SEOUL__.y,
      ]),
      lastProgress = Date.now();
    for (const [tx, ty] of points) {
      for (;;) {
        if (pendingError) throw pendingError;
        const p = await page.evaluate(() => ({
          x: window.__SEOUL__.x,
          y: window.__SEOUL__.y,
          action: window.__PLAZA_REVIEW__.action,
          frame: window.__PLAZA_REVIEW__.frame,
          paused: window.__PIXEL_METRICS__.paused,
        }));
        const dx = tx - p.x,
          dy = ty - p.y,
          d = Math.hypot(dx, dy);
        trace.push({
          time: Date.now(),
          x: p.x,
          y: p.y,
          action: p.action,
          frame: p.frame,
        });
        if (d < 5) break;
        if (Math.hypot(p.x - previous[0], p.y - previous[1]) > 4) {
          previous = [p.x, p.y];
          lastProgress = Date.now();
        }
        if (Date.now() - lastProgress > 8000)
          throw Error(
            `Input stuck at${p.x},${p.y} toward${tx},${ty}; paused=${p.paused}`,
          );
        const strength = Math.min(1, Math.max(0.2, d / 28)),
          distance = radius * (0.14 + 0.86 * strength);
        await cdp.send("Input.dispatchTouchEvent", {
          type: "touchMove",
          touchPoints: [
            { x: cx + (dx / d) * distance, y: cy + (dy / d) * distance, id: 1 },
            runner,
          ],
        });
        await page.waitForTimeout(Math.min(110, Math.max(35, d * 4)));
      }
    }
    await stop();
  }
  async function action(kind) {
    if (!kind) return;
    if (kind === "wave" || kind === "celebrate") {
      await page.locator("#emote").click();
      await page.locator("#" + kind).click();
      await page.waitForFunction(
        (kind) => window.__PLAZA_REVIEW__?.action === kind,
        kind,
      );
      await page.waitForFunction(
        () => window.__PLAZA_REVIEW__?.action === "idle",
      );
      return;
    }
    await page.locator("#interact").click();
    await page.locator("#dialog").waitFor({ state: "visible" });
    await page.waitForTimeout(1100);
    if (kind === "ferry") {
      const before = await page.evaluate(() => window.__SEOUL__.y);
      await page.locator("#travel-go").click();
      await page.waitForFunction(
        (before) =>
          before < 5000 ? window.__SEOUL__.y > 5000 : window.__SEOUL__.y < 5000,
        before,
      );
      await page.waitForTimeout(700);
    } else {
      if (kind === "discovery") {
        await page.locator('[data-discovery="true"]').click();
        await page.waitForTimeout(1300);
      }
      await page.locator("#close-dialog").click();
    }
  }
  await page.waitForTimeout(1500);
  for (const segment of tour.visits) {
    console.log("Visit", segment.id, flushTime());
    await drive(segment.points);
    await action(segment.action);
    const state = await page.evaluate(() => ({
      x: window.__SEOUL__.x,
      y: window.__SEOUL__.y,
      district: window.__FULL_WORLD__.district,
      discovery: window.__WORLD_REVIEW__.discoveryFound,
    }));
    visits.push({
      id: segment.id,
      requested: segment.requested,
      actual: state,
      time: Date.now(),
    });
    await fs.writeFile(
      base + "/progress.json",
      JSON.stringify(
        { status: "RECORDING", visits, frames: frames.length },
        null,
        2,
      ),
    );
    if (errors.length) throw Error(JSON.stringify(errors));
  }
  await action("wave");
  await page.waitForTimeout(2000);
  await cdp.send("Page.stopScreencast");
  capturing = false;
  await new Promise((resolve) => setTimeout(resolve, 150));
  await Promise.all(writes);
  if (pendingError) throw pendingError;
  const sorted = [...frames].sort(
    (a, b) => a.timestamp - b.timestamp || a.index - b.index,
  );
  if (sorted.length < 100) throw Error("Too few real captured frames");
  const first = sorted[0].timestamp;
  await fs.writeFile(
    base + "/capture.json",
    JSON.stringify(
      {
        status: "PASS",
        normalEntry: true,
        placementHookPresent: false,
        input:
          "Public two-pointer joystick + Run button, visible dialog/emote/ferry controls only. Read-only position telemetry.",
        viewport: [1280, 960],
        deviceScaleFactor: 1,
        renderer: "Canvas",
        method:
          "Actual CDP browser screencast JPEG84, everyNthFrame2. All delivered frames retained with original timestamps; no cuts, loops, speed changes, gameplay hooks or external video.",
        sourceBundleSha256: tour.sourceBundleSha256,
        visits,
        errors,
        frames: sorted,
        elapsedSeconds: sorted.at(-1).timestamp - first,
      },
      null,
      2,
    ),
  );
  await fs.writeFile(base + "/movement-trace.json", JSON.stringify(trace));
  const concat = ["ffconcat version 1.0"];
  for (let i = 0; i < sorted.length; i++) {
    concat.push(`file '${sorted[i].file}'`);
    if (i + 1 < sorted.length)
      concat.push(
        "duration " +
          (sorted[i + 1].timestamp - sorted[i].timestamp).toFixed(6),
      );
  }
  await fs.writeFile(base + "/frames.ffconcat", concat.join("\n") + "\n");
  console.log(
    "CAPTURE_PASS",
    base,
    sorted.length,
    "frames",
    sorted.at(-1).timestamp - first,
    "seconds",
  );
} catch (e) {
  await fs.writeFile(
    base + "/failure.json",
    JSON.stringify(
      {
        status: "FAIL",
        error: String(e),
        visits,
        frames: frames.length,
        errors,
      },
      null,
      2,
    ),
  );
  throw e;
} finally {
  if (capturing && cdp) await cdp.send("Page.stopScreencast").catch(() => {});
  await Promise.all(writes);
  await browser.close();
}
function flushTime() {
  return new Date().toISOString();
}
