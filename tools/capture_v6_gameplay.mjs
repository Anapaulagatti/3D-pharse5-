import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const Q = "docs/v6-restructure/quality",
  base = process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
for (const mode of ["v6-restructure-walkthrough"]) {
  const dir = `.cache/v6-restructure/${mode}-${Date.now()}`;
  await fs.mkdir(dir, { recursive: true });
  const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const c = await b.newContext({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 1,
    reducedMotion: "no-preference",
  });
  const p = await c.newPage(),
    errors = [],
    frames = [],
    visits = [],
    writes = new Set();
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await p.goto(base + "v6-world-review.html");
  await p.waitForFunction(() => window.__FULL_WORLD__?.world[0] === 4352);
  if (await p.evaluate(() => !!window.__SEOUL_TEST__))
    throw Error("QA hook forbidden in footage");
  const d = await c.newCDPSession(p);
  let active = true,
    held = false;
  d.on("Page.screencastFrame", (f) => {
    void d
      .send("Page.screencastFrameAck", { sessionId: f.sessionId })
      .catch(() => {});
    if (!active) return;
    const data = Buffer.from(f.data, "base64"),
      file = `${dir}/${String(frames.length).padStart(6, "0")}.jpg`;
    frames.push({
      file,
      timestamp: f.metadata.timestamp,
      sha256: createHash("sha256").update(data).digest("hex"),
      bytes: data.length,
    });
    const job = fs.writeFile(file, data);
    writes.add(job);
    void job.finally(() => writes.delete(job));
  });
  const box = await p.locator("#joystick").boundingBox(),
    run = await p.locator("#run").boundingBox(),
    center = { x: box.x + box.width / 2, y: box.y + box.height / 2 },
    radius = box.width * 0.34;
  async function stick(x, y, sprint = true) {
    if (!held) {
      await d.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [
          { ...center, id: 1 },
          ...(sprint
            ? [{ x: run.x + run.width / 2, y: run.y + run.height / 2, id: 2 }]
            : []),
        ],
      });
      held = true;
    }
    await d.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [
        { x: center.x + x * radius, y: center.y + y * radius, id: 1 },
        ...(sprint
          ? [{ x: run.x + run.width / 2, y: run.y + run.height / 2, id: 2 }]
          : []),
      ],
    });
  }
  async function release() {
    if (held)
      await d.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
    held = false;
  }
  async function travel(name, points, sprint = true) {
    const start = Date.now();
    for (const [x, y] of points) {
      const began = Date.now();
      for (;;) {
        const s = await p.evaluate(() => window.__SEOUL__);
        const dx = x - s.x,
          dy = y - s.y,
          dist = Math.hypot(dx, dy);
        if (dist < 5) break;
        if (Date.now() - began > 45000)
          throw Error("Stuck " + name + " " + JSON.stringify(s));
        await stick(dx / dist, dy / dist, sprint);
        await p.waitForTimeout(40);
      }
    }
    await release();
    await p.waitForTimeout(200);
    visits.push({
      name,
      elapsedMs: Date.now() - start,
      state: await p.evaluate(() => ({
        world: window.__FULL_WORLD__,
        x: window.__SEOUL__.x,
        y: window.__SEOUL__.y,
      })),
    });
    console.log(mode, name);
  }
  async function interact(close = true) {
    await release();
    await p.locator("#interact").tap();
    await p.waitForTimeout(450);
    if (close && (await p.locator("#dialog").isVisible()))
      await p.locator("#talk").tap();
  }
  async function emote(id) {
    await release();
    await p.locator("#emote").tap();
    await p.locator("#" + id).tap();
    await p.waitForTimeout(1500);
  }
  await p.evaluate(
    () =>
      (window.__FULL_CAPTURE__ = {
        start: performance.now(),
        frame: window.__PIXEL_METRICS__.frameCount,
      }),
  );
  await d.send("Page.startScreencast", {
    format: "jpeg",
    quality: 85,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 1,
  });
  let failure = null;
  try {
    await p.waitForTimeout(500);
    await travel("Historical palace avenue to civic junction", [
      [2176, 2016],
      [2176, 2608],
    ]);
    await travel("Western boulevard and real Namsan entrance", [
      [1472, 2608],
      [1472, 3536],
      [1120, 3536],
    ]);
    await travel("Winding hillside trail to tower", [
      [960, 3456],
      [704, 3376],
      [544, 3296],
      [512, 3120],
      [704, 3120],
      [704, 3072],
    ]);
    await interact();
    await emote("wave");
    await travel("Actual lookout terrace central stair", [
      [704, 3120],
      [512, 3120],
      [544, 3296],
      [704, 3376],
      [960, 3456],
      [1120, 3536],
      [1120, 3296],
    ]);
    await travel("Station side approach and front forecourt", [
      [1120, 3536],
      [1472, 3536],
      [1472, 2608],
      [1856, 2608],
      [1856, 3024],
      [2240, 3024],
      [2240, 2976],
    ]);
    await interact();
    await travel("Relocated timber crossing and real platform stair", [
      [2240, 3024],
      [2240, 3312],
    ]);
    await travel("Shop frontage below railway", [
      [2016, 3312],
      [2016, 3520],
      [1776, 3520],
    ]);
    await interact();
    await travel("Eastern boulevard and amusement campus arch", [
      [2016, 3520],
      [2016, 3536],
      [3024, 3536],
      [3024, 3584],
      [3552, 3584],
      [3552, 3424],
      [3520, 3152],
    ]);
    await travel("Separate Ferris wheel and carousel courts", [
      [3328, 3152],
      [3328, 3104],
      [3328, 3152],
      [3968, 3152],
      [3968, 3072],
    ]);
    await interact();
    await travel("Discovery hall entrance", [
      [3968, 3152],
      [3792, 3152],
      [3792, 3584],
      [4016, 3584],
    ]);
    await interact();
    await travel("Continuous promenade to public ferry jetty", [
      [3792, 3584],
      [3024, 3584],
      [3024, 3744],
      [2496, 3744],
      [2496, 3912],
    ]);
    await interact(false);
    await p.locator("#travel-go").tap();
    await p.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
    visits.push({
      name: "Public ferry arrival in Jeju",
      state: await p.evaluate(() => window.__SEOUL__),
    });
    await travel("Oreum natural approach", [
      [2496, 4376],
      [2528, 4560],
      [2528, 4464],
      [2240, 4464],
    ]);
    await interact();
    await travel("Cliff lookout real side approach", [
      [2528, 4464],
      [2544, 4352],
      [2736, 4352],
    ]);
    await interact();
    await travel("Basalt discovery route", [
      [2544, 4352],
      [2528, 4464],
      [2528, 4560],
      [2528, 4640],
      [2240, 4640],
      [2240, 4800],
      [2144, 4800],
      [2144, 4840],
    ]);
    await interact(false);
    await p.locator('button[data-discovery="true"]').tap();
    await p.locator("#talk").tap();
    await travel("Original Jeju cultural courtyard through its real gate", [
      [2144, 4800],
      [1830, 4800],
      [1830, 4704],
    ]);
    await interact();
    await travel("Traditional southern gateway and original island boat", [
      [1830, 4800],
      [1830, 4896],
      [1760, 4896],
      [1760, 5008],
    ]);
    await emote("wave");
    await travel("Back to village garden", [
      [1760, 4896],
      [1830, 4896],
      [1830, 4800],
    ]);
    await travel("Nature centre and garden", [
      [1830, 4800],
      [2240, 4800],
      [2240, 4640],
      [2528, 4640],
      [2736, 4640],
      [2736, 4896],
      [2464, 4896],
    ]);
    await interact();
    await emote("celebrate");
    await travel("Return to northern island ferry landing", [
      [2736, 4896],
      [2736, 4640],
      [2528, 4640],
      [2528, 4560],
      [2496, 4376],
      [2496, 4208],
    ]);
    await interact(false);
    await p.locator("#travel-go").tap();
    await p.waitForFunction(
      () => window.__FULL_WORLD__?.district === "busan-coast",
    );
    visits.push({
      name: "Public reciprocal ferry returned to coast",
      state: await p.evaluate(() => window.__SEOUL__),
    });
  } catch (e) {
    failure = String(e);
    console.log(failure);
  } finally {
    await release();
    const runtime = await p.evaluate(() => ({
      elapsedMs: performance.now() - window.__FULL_CAPTURE__.start,
      actualFrames:
        window.__PIXEL_METRICS__.frameCount - window.__FULL_CAPTURE__.frame,
      renderer: window.__PIXEL_METRICS__.renderer,
    }));
    await d.send("Page.stopScreencast");
    active = false;
    await Promise.all([...writes]);
    const ordered = [...frames].sort((a, b) => a.timestamp - b.timestamp),
      span = ordered.at(-1).timestamp - ordered[0].timestamp;
    await fs.writeFile(
      `${Q}/${mode}-capture.json`,
      JSON.stringify(
        {
          method:
            "Actual normal public Phaser entry; CDP touchscreen analog joystick + independent held sprint and public action buttons. No QA hook, placement, injected animation or scene skips. Raw capture timestamps retained; footage normal speed. Not a standalone performance benchmark.",
          noQAPlacement: true,
          rawFramesDirectory: dir,
          frames,
          visits,
          errors,
          failure,
          runtime,
          sourceWholeBrowserAverageFPS: (frames.length - 1) / span,
        },
        null,
        2,
      ) + "\n",
    );
    await b.close();
    console.log({
      mode,
      frames: frames.length,
      seconds: span,
      errors,
      failure,
    });
  }
  if (failure || errors.length) throw Error(failure ?? JSON.stringify(errors));
}
