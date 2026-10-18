import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const Q = "docs/full-world/quality",
  base = process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
for (const mode of ["mobile-gameplay", "multi-district-traversal"]) {
  const dir = `.cache/full-world/${mode}-${Date.now()}`;
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
  await p.goto(base + "full-world-review.html");
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
    if (mode === "mobile-gameplay") {
      await interact();
      await travel(
        "Walk diagonally across ceremonial court",
        [
          [2272, 1008],
          [2176, 1104],
        ],
        false,
      );
      await emote("wave");
      await travel("Run toward cultural street", [[2176, 1512]]);
      await interact();
      await emote("celebrate");
      await travel("Return toward monument", [[2176, 1216]], false);
      await p.waitForTimeout(1200);
    } else {
      await travel("Heritage south avenue", [
        [2176, 1328],
        [2176, 2016],
        [2176, 2368],
      ]);
      await travel("Woodland approach", [
        [1600, 2368],
        [1440, 2464],
        [1280, 2416],
        [1024, 2416],
        [832, 2560],
        [608, 2624],
        [608, 2928],
        [704, 2992],
        [832, 2992],
        [832, 2912],
      ]);
      await interact();
      await emote("wave");
      await travel("Namsan to flower town", [
        [832, 2992],
        [704, 2992],
        [608, 2928],
        [608, 2624],
        [832, 2560],
        [1024, 2416],
        [1280, 2416],
        [1440, 2464],
        [1600, 2368],
        [2176, 2368],
        [2944, 2368],
        [2992, 2512],
        [2976, 2784],
        [3136, 2800],
        [3328, 2816],
        [3456, 2848],
        [3712, 2848],
      ]);
      await interact();
      await emote("celebrate");
      await travel("Flower town to Blue Letter promenade", [
        [3712, 3120],
        [3712, 3296],
        [3328, 3296],
        [3072, 3136],
        [2912, 3136],
        [2848, 3136],
      ]);
      await interact(false);
      await p.locator("#travel-go").tap();
      await p.waitForFunction(() => window.__FULL_WORLD__.district === "jeju");
      await travel("Windstone island loop", [
        [1952, 4480],
        [2080, 4256],
        [2240, 4128],
        [2528, 4160],
        [2688, 4352],
        [2656, 4544],
        [2368, 4608],
        [2080, 4576],
        [1760, 4544],
      ]);
      await interact(false);
      await p.locator("#travel-go").tap();
      await p.waitForFunction(
        () => window.__FULL_WORLD__.district === "busan-coast",
      );
      await travel("Promenade bridge and station crossing", [
        [2656, 3136],
        [2464, 3160],
        [2384, 3160],
        [2304, 3160],
        [2176, 3160],
        [1792, 3136],
        [1792, 3024],
        [2048, 3024],
        [2048, 2944],
        [2048, 2784],
      ]);
      await interact();
      await emote("wave");
    }
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
