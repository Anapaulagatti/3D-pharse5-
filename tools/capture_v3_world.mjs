import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const Q = "docs/v3-final/quality",
  base = process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
for (const mode of ["mobile-gameplay", "multi-district-traversal"]) {
  const dir = `.cache/v3-final/${mode}-${Date.now()}`;
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
  await p.goto(base + "v3-world-review.html");
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
      await travel("Woodland to modern Namsan tower", [
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
      await travel("Actual viewing terrace stairs", [
        [832, 2992],
        [704, 2992],
        [704, 3264],
        [928, 3296],
        [1120, 3168],
        [1120, 3104],
        [1120, 3024],
      ]);
      await interact();
      await emote("wave");
      await travel("Useful woodland to sea cafe shortcut", [
        [1120, 3168],
        [1280, 3232],
        [1408, 3232],
        [1568, 3232],
      ]);
      await interact();
      await travel("Real platform stair and safe rail crossing", [
        [1792, 3232],
        [1792, 3040],
        [2048, 3040],
        [2048, 2944],
        [2048, 2784],
      ]);
      await travel("Contemporary urban hub", [
        [2560, 2784],
        [2560, 2752],
      ]);
      await interact();
      await travel("Urban gateway to Bora Bloom", [
        [2560, 2784],
        [2976, 2784],
        [3136, 2800],
        [3328, 2816],
        [3456, 2848],
        [3712, 2848],
      ]);
      await interact();
      await emote("celebrate");
      await travel("Creative hall and park social loop", [
        [3920, 2864],
        [3920, 3096],
        [4144, 3096],
        [4144, 3136],
      ]);
      await interact();
      await travel("Open amusement entrance", [
        [4144, 3096],
        [3712, 3096],
        [3712, 3120],
        [3712, 3296],
      ]);
      await interact();
      await travel("Park to coastal ferry", [
        [3328, 3296],
        [3072, 3136],
        [2912, 3136],
        [2848, 3136],
      ]);
      await interact(false);
      await p.locator("#travel-go").tap();
      await p.waitForFunction(() => window.__FULL_WORLD__.district === "jeju");
      await travel("Jeju open cultural courtyard", [
        [1952, 4480],
        [1830, 4480],
        [1830, 4384],
      ]);
      await interact();
      await travel("Windstone oreum and orchard loop", [
        [1830, 4480],
        [1952, 4480],
        [2080, 4480],
        [2080, 4256],
        [2240, 4144],
      ]);
      await interact();
      await travel("Actual cliff lookout approach", [
        [2528, 4160],
        [2528, 4032],
        [2736, 4032],
      ]);
      await interact();
      await travel("Modern basalt nature centre", [
        [2528, 4032],
        [2528, 4160],
        [2528, 4320],
        [2752, 4432],
        [2720, 4576],
        [2464, 4640],
        [2464, 4544],
      ]);
      await interact();
      await travel("Original basalt discovery", [[2144, 4608]]);
      await interact(false);
      await p.locator('button[data-discovery="false"]').first().tap();
      await p.waitForTimeout(650);
      await p.locator('button[data-discovery="true"]').tap();
      await p.waitForTimeout(900);
      if (!(await p.evaluate(() => window.__V3_WORLD__.discoveryFound)))
        throw Error("Discovery completion missing");
      await p.locator("#talk").tap();
      await emote("celebrate");
      await travel("Explicit reciprocal ferry return", [
        [2080, 4608],
        [1760, 4544],
      ]);
      await interact(false);
      await p.locator("#travel-go").tap();
      await p.waitForFunction(
        () => window.__FULL_WORLD__.district === "busan-coast",
      );
      await travel("Real inlet bridge and coastal deck stair", [
        [2656, 3136],
        [2464, 3160],
        [2304, 3160],
        [2304, 3224],
        [2112, 3224],
        [2112, 3208],
        [2112, 3104],
      ]);
      await interact();
      await travel("Coastal promenade to station", [
        [2112, 3208],
        [2304, 3224],
        [2304, 3040],
        [2048, 3040],
        [2048, 2944],
        [2048, 2816],
        [1792, 2816],
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
