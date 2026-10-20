import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const Q = "docs/v7-world/quality",
  base = process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
for (const mode of ["v7-world-walkthrough"]) {
  const dir = `.cache/v7-world/${mode}-${Date.now()}`;
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
  await p.goto(base + "v7-world-review.html");
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
    const routes = JSON.parse(
      await fs.readFile("assets-src/v7-world/routes.json", "utf8"),
    );
    function path(id, reverse = false) {
      const r = routes.find((r) => r.id === id);
      if (!r) throw Error(id);
      const points = r.points.filter(
        (_, i) => i % 4 === 0 || i === r.points.length - 1,
      );
      return reverse ? [...points].reverse() : points;
    }
    await travel("Historical avenue and warm era threshold", [
      [2176, 1984],
      ...path("historic-threshold"),
    ]);
    await travel(
      "Station west garden and balanced forecourt",
      path("west-station-arrival"),
    );
    await travel("Station entrance", [
      [2240, 2928],
      [2240, 2888],
    ]);
    await interact();
    await emote("wave");
    await travel("Real railway crossing and platform stair", [
      [2240, 2928],
      ...path("rail-and-platform-stair"),
    ]);
    await travel("West boulevard to Namsan main entrance", [
      [1456, 3376],
      [1456, 3712],
      ...path("namsan-arrival"),
    ]);
    await travel("Namsan complete winding loop", path("namsan-tower-loop"));
    const loop = path("namsan-tower-loop", true),
      towerIndex = loop.findIndex((p) => p[0] < 848 && p[1] < 3112);
    await travel("Namsan eastern loop to tower", loop.slice(0, towerIndex + 1));
    await travel("Tower observation court", [
      [704, 3096],
      [704, 3072],
    ]);
    await interact();
    await travel("Namsan eastern loop and actual terrace stairs", [
      [704, 3096],
      ...loop.slice(0, towerIndex + 1).reverse(),
      ...path("lookout-stairs"),
    ]);
    await travel("Park exit and modern civic frontage", [
      [1024, 3472],
      [1120, 3472],
      ...path("namsan-arrival", true),
      [2240, 3712],
      [2744, 3712],
    ]);
    await travel(
      "Actual traversable coastal channel bridge",
      path("coastal-channel-bridge"),
    );
    await travel("Amusement gateway", [
      [3152, 3712],
      ...path("amusement-entry"),
    ]);
    await travel("West amusement loop and Ferris court", [
      [3352, 3456],
      [3352, 3200],
      [3472, 3128],
      ...path("wheel-arrival"),
    ]);
    await interact();
    await travel("Carousel separate decorative court", [
      [3464, 3128],
      [3920, 3128],
      ...path("carousel-arrival"),
    ]);
    await interact();
    await travel("Discovery hall, planted courts and main gate", [
      [4000, 3128],
      [4168, 3200],
      [4168, 3488],
      ...path("hall-arrival"),
    ]);
    await interact();
    await travel("Amusement gateway exit", [
      [3968, 3536],
      [3712, 3456],
      [3712, 3712],
      [3152, 3712],
      [2896, 3712],
      ...path("coastal-channel-bridge", true),
      [2240, 3712],
    ]);
    await travel(
      "Ferry terminal waiting court and visible boarding stairs",
      path("mainland-boarding"),
    );
    await interact(false);
    await p.locator("#travel-go").tap();
    await p.waitForFunction(() => window.__FULL_WORLD__?.district === "jeju");
    visits.push({
      name: "Public ferry arrival",
      state: await p.evaluate(() => window.__SEOUL__),
    });
    await travel(
      "Jeju dock to oreum",
      path("jeju-arrival").filter((p) => p[1] <= 4520),
    );
    await travel("Scenic volcanic hill loop", path("jeju-oreum-loop"));
    await interact();
    await travel("Village arrival around courtyard", [
      [2312, 4528],
      ...path("jeju-village-route"),
    ]);
    await interact();
    await travel("Island southern scenic loop", path("jeju-scenic-circuit"));
    await travel("Learning garden", path("jeju-garden-link"));
    await travel("Basalt discovery", path("jeju-learning-arrival"));
    await interact(false);
    await p.locator('button[data-discovery="true"]').tap();
    await p.locator("#talk").tap();
    await travel("Nature centre", [
      [2160, 4800],
      ...path("jeju-garden-link", true),
      [2640, 4704],
      ...path("jeju-nature-centre"),
    ]);
    await interact();
    await emote("celebrate");
    await travel("Return island landing", [
      ...path("jeju-nature-centre", true),
      [2504, 4600],
      ...path("jeju-arrival", true),
      [2704, 4240],
    ]);
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
