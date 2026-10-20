import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const Q = "docs/v8-city/quality",
  base = process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
for (const mode of ["v8-city-walkthrough"]) {
  const dir = `.cache/v8-city/${mode}-${Date.now()}`;
  await fs.mkdir(dir, { recursive: true });
  const b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
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
  await p.goto(base + "v8-city-review.html");
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
    quality: 80,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 2,
  });
  let failure = null;
  try {
    await p.waitForTimeout(500);
    const routes = JSON.parse(
      await fs.readFile("assets-src/v8-city/routes.json", "utf8"),
    );
    function path(id, reverse = false) {
      const r = routes.find((r) => r.id === id);
      if (!r) throw Error(id);
      const points =
        r.points.length > 20
          ? r.points.filter((_, i) => i % 4 === 0 || i === r.points.length - 1)
          : r.points;
      return reverse ? [...points].reverse() : points;
    }
    await travel("Preserved historical avenue", [
      [2176, 1984],
      [2176, 2240],
      ...path("cultural-gateway"),
    ]);
    await travel("Continuous civic boulevard", [
      [2112, 2864],
      ...path("station-plaza-link"),
      ...path("station-door"),
    ]);
    await interact();
    await emote("wave");
    await travel("Bookshop frontage", [
      [2704, 2864],
      [2112, 2864],
      [2112, 2800],
      [1728, 2800],
    ]);
    await interact();
    await travel("Main east-west avenue to Namsan entrance", [
      [2112, 2800],
      [2112, 3008],
      [1392, 3008],
      ...path("namsan-gate"),
    ]);
    await travel("Namsan full scenic loop", path("namsan-loop"));
    const park = path("namsan-loop", true),
      ti = park.findIndex((p) => p[0] < 440 && p[1] < 2940);
    await travel("Tower observation sequence", [
      ...park.slice(0, ti + 1),
      ...path("tower-approach"),
      [640, 2880],
    ]);
    await interact();
    await travel("Park gate return", [
      [736, 2896],
      [736, 2848],
      ...park.slice(0, ti + 1).reverse(),
      ...path("namsan-gate", true),
    ]);
    await travel("Library street block", [
      [1392, 3376],
      [1728, 3376],
    ]);
    await interact();
    await travel("Cafe street block", [
      [2112, 3376],
      [2704, 3376],
    ]);
    await interact();
    await travel("Station rear platform / rail safely separated", [
      [3200, 3376],
      [3200, 2864],
      ...path("platform-access"),
    ]);
    await travel("Enter independent amusement campus", [
      ...path("platform-access", true),
      [3200, 3520],
      ...path("amusement-urban-access"),
    ]);
    await travel("Complete amusement circulation loop", [
      [3744, 3376],
      [3344, 3376],
      [3344, 2944],
      ...path("amusement-loop"),
    ]);
    await travel("Ferris wheel court", [
      [3552, 2912],
      ...path("wheel-court-access"),
    ]);
    await interact();
    await travel("Carousel courtyard", [
      [3552, 2912],
      [4240, 2912],
      [4240, 3184],
      ...path("carousel-court-access"),
    ]);
    await interact();
    await travel("Entertainment gate to continuous seafront", [
      [4240, 3184],
      [4240, 3376],
      [3744, 3376],
      [3744, 3480],
      [3744, 3520],
      [3744, 3696],
      [2528, 3696],
    ]);
    await travel("Terminal waiting and ticket frontage", [
      [2528, 3648],
      ...path("terminal-front"),
    ]);
    await interact();
    await travel("Visible harbor boarding", [
      [2528, 3648],
      ...path("mainland-boarding"),
    ]);
    await interact(false);
    await p.locator("#travel-go").tap();
    await p.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
    visits.push({
      name: "Ferry arrived island",
      state: await p.evaluate(() => window.__SEOUL__),
    });
    await travel("Island arrival to scenic circuit", path("jeju-arrival"));
    await travel("Jeju complete exploration loop", path("jeju-scenic-loop"));
    await travel("Village courtyard front", [
      [2048, 4800],
      [1830, 4800],
    ]);
    await interact();
    await travel("Volcanic learning garden", [
      [2048, 4800],
      [2304, 4624],
      ...path("jeju-garden-access"),
    ]);
    await interact(false);
    await p.locator('button[data-discovery="true"]').tap();
    await p.locator("#talk").tap();
    await travel("Return along valid village-side route", [
      ...path("jeju-garden-access", true),
      [2048, 4800],
      [2048, 4640],
      ...path("jeju-arrival", true),
      ...path("island-boarding", true),
    ]);
    await emote("celebrate");
    await interact(false);
    await p.locator("#travel-go").tap();
    await p.waitForFunction(
      () => window.__FULL_WORLD__?.district === "busan-coast",
    );
    visits.push({
      name: "Reciprocal ferry returned mainland",
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
