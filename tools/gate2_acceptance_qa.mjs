import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import fsSync from "node:fs";
import assert from "node:assert/strict";
import { ready, state, walk, grid, capture } from "./gate2_browser_lib.mjs";
const D = "docs/gate2/acceptance";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--disable-background-timer-throttling",
  ],
});
const rows = process.argv[2]
    ? JSON.parse(fsSync.readFileSync(D + "/browser-qa-progress.json", "utf8"))
    : [],
  errors = [];
const record = (r) => {
  rows.push(r);
  fsSync.writeFileSync(
    D + "/browser-qa-progress.json",
    JSON.stringify(rows, null, 2) + "\n",
  );
};
const sessions = new WeakMap();
async function page(opts = {}) {
  const p = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    ...opts,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  return p;
}
const touch = async (p, type, pts) => {
  let c = sessions.get(p);
  if (!c) {
    c = await p.context().newCDPSession(p);
    sessions.set(p, c);
  }
  await c.send("Input.dispatchTouchEvent", { type, touchPoints: pts });
};
const screenshot = (p, name) => p.screenshot({ path: `${D}/${name}.png` });
function bounds(s, size) {
  const [x, y, w, h] = s.camera.worldView;
  assert(
    x >= -0.1 && y >= -0.1 && x + w <= size[0] + 3 && y + h <= size[1] + 3,
    JSON.stringify(s.camera),
  );
  const real = s.camera.renderedWorldView;
  assert(
    real[0] >= -0.1 &&
      real[1] >= -0.1 &&
      real[0] + real[2] <= size[0] + 3 &&
      real[1] + real[3] <= size[1] + 3,
    JSON.stringify(real),
  );
}
const stats = (a) => {
  const b = [...a].sort((x, y) => x - y);
  return {
    samples: b.length,
    p50: b[Math.floor(b.length * 0.5)],
    p95: b[Math.floor(b.length * 0.95)],
    max: b.at(-1),
  };
};
try {
  for (const [id, targets] of [
    [
      "original",
      [
        [510, 965],
        [510, 780],
      ],
    ],
    [
      "station",
      [
        [360, 520],
        [360, 430],
      ],
    ],
    [
      "seam",
      [
        [1520, 530],
        [1848, 430],
        [1288, 500],
      ],
    ],
    [
      "jeju-fit",
      [
        [210, 1000],
        [1150, 510],
        [1150, 955],
        [1240, 1290],
      ],
    ],
  ]) {
    if (
      rows.some(
        (r) => r.case === "Actual keyboard navigation" && r.scene === id,
      )
    )
      continue;
    const p = await page();
    await ready(p, id);
    const g = await grid(p);
    const routes = [];
    for (const target of targets)
      routes.push({ target, ...(await walk(p, g, target)) });
    record({
      case: "Actual keyboard navigation",
      scene: id,
      routes,
      state: await state(p),
    });
    if (id === "jeju-fit") {
      await ready(p, id, "&qa");
      for (const point of [
        [520, 960],
        [500, 1400],
        [1900, 1600],
      ])
        assert.equal(
          await p.evaluate(
            ([x, y]) => window.__GATE2_TEST__.walkable(x, y),
            point,
          ),
          false,
        );
      record({
        case: "Ferry sea and shoreline rejected",
        pass: true,
        points: [
          [520, 960],
          [500, 1400],
          [1900, 1600],
        ],
      });
    }
    await ready(p, id, "&qa&native&overview");
    const pt = {
      original: [510, 780],
      station: [360, 430],
      seam: [1520, 530],
      "jeju-fit": [1240, 1290],
    }[id];
    await p.evaluate(([x, y]) => window.__GATE2_TEST__.place(x, y), pt);
    await p.waitForTimeout(180);
    await capture(p, `${D}/${id.toUpperCase()}_NATIVE_1X.png`);
    await p.close();
  }
  for (const id of ["c", "b"]) {
    if (
      rows.some((r) => r.case.startsWith("Mobile real touch") && r.scene === id)
    )
      continue;
    const p = await page({
      viewport: { width: 844, height: 390 },
      isMobile: true,
      hasTouch: true,
    });
    await ready(p, id);
    await p.waitForTimeout(450);
    let s = await state(p);
    assert.equal(s.camera.mode, "follow");
    assert.equal(s.zoom, 1);
    assert.equal(s.camera.canvas[1], 390);
    await screenshot(p, `MOBILE_${id.toUpperCase()}_FOLLOW`);
    const start = { x: s.x, y: s.y },
      box = await p.locator("#joystick").boundingBox(),
      joy = { x: box.x + box.width / 2 + 32, y: box.y + box.height / 2, id: 1 };
    await touch(p, "touchStart", [joy]);
    await p.waitForTimeout(750);
    await touch(p, "touchEnd", []);
    s = await state(p);
    assert(s.x > start.x + 20);
    assert(s.camera.lookAhead[0] > 10);
    bounds(s, id === "c" ? [1024, 1536] : [1536, 1024]);
    const walking = s;
    const runBox = await p.locator("#run").boundingBox();
    const runTouch = {
      x: runBox.x + runBox.width / 2,
      y: runBox.y + runBox.height / 2,
      id: 2,
    };
    const beforeRun = s.x;
    await touch(p, "touchStart", [joy, runTouch]);
    await p.waitForTimeout(750);
    await touch(p, "touchEnd", []);
    s = await state(p);
    assert(s.x > beforeRun + 35);
    const running = s;
    await p.tap("#scenic");
    await p.waitForTimeout(180);
    const scenicStart = await state(p);
    assert.equal(scenicStart.camera.mode, "scenic");
    await touch(p, "touchStart", [{ x: 420, y: 180, id: 1 }]);
    await touch(p, "touchMove", [{ x: 620, y: 260, id: 1 }]);
    await touch(p, "touchEnd", []);
    await p.waitForTimeout(150);
    const dragged = await state(p);
    assert.equal(dragged.x, scenicStart.x);
    assert.notDeepEqual(dragged.camera.worldView, scenicStart.camera.worldView);
    await touch(p, "touchStart", [
      { x: 280, y: 170, id: 1 },
      { x: 580, y: 170, id: 2 },
    ]);
    await touch(p, "touchMove", [
      { x: 380, y: 170, id: 1 },
      { x: 480, y: 170, id: 2 },
    ]);
    await touch(p, "touchEnd", []);
    await p.waitForTimeout(180);
    s = await state(p);
    assert(s.zoom < 1);
    assert.equal(s.x, scenicStart.x);
    bounds(s, id === "c" ? [1024, 1536] : [1536, 1024]);
    await screenshot(p, `MOBILE_${id.toUpperCase()}_SCENIC`);
    const scenic = s;
    // Native DOM touch ownership: joystick disabled in Scenic, even when multi-touch occurs.
    await touch(p, "touchStart", [joy]);
    await p.waitForTimeout(300);
    await touch(p, "touchEnd", []);
    assert.equal((await state(p)).x, scenicStart.x);
    for (const [x, y] of [
      [-2000, -2000],
      [2400, 2400],
    ]) {
      await touch(p, "touchStart", [{ x: 420, y: 180, id: 1 }]);
      await touch(p, "touchMove", [{ x, y, id: 1 }]);
      await touch(p, "touchEnd", []);
      await p.waitForTimeout(60);
      bounds(await state(p), id === "c" ? [1024, 1536] : [1536, 1024]);
    }
    await p.tap("#overview-mode");
    await p.waitForTimeout(180);
    s = await state(p);
    assert.equal(s.camera.mode, "overview");
    {
      const expected = id === "c" ? [1024, 1536] : [1536, 1024];
      const v = s.camera.renderedWorldView;
      assert(
        Math.abs(v[0]) < 0.01 &&
          Math.abs(v[1]) < 0.01 &&
          Math.abs(v[2] - expected[0]) < 0.01 &&
          Math.abs(v[3] - expected[1]) < 0.01,
        JSON.stringify(v),
      );
    }
    assert((await p.locator("#map-labels span").count()) > 3);
    await screenshot(p, `MOBILE_${id.toUpperCase()}_OVERVIEW`);
    const overview = s;
    await p.tap("#return-juni");
    await p.waitForTimeout(450);
    s = await state(p);
    assert.equal(s.camera.mode, "follow");
    assert.equal(s.zoom, 1);
    assert.equal(s.x, scenicStart.x);
    await p.waitForTimeout(600);
    const after = await state(p);
    record({
      case: "Mobile real touch follow/run/drag/pinch/clamp/overview/return/no-control-conflict",
      scene: id,
      pass: true,
      walking,
      running,
      scenic,
      overview,
      returned: after,
      frameTimes: stats(after.frameTimes),
      oldViewport: [844, 281],
      newViewport: s.camera.canvas,
    });
    await p.close();
    const d = await page();
    await ready(d, id);
    await pSafeWait(d, 200);
    await screenshot(d, `DESKTOP_${id.toUpperCase()}_FOLLOW`);
    await d.close();
  }
  // Common aspect ratios and DPR2 are emulated; hardware performance is not asserted.
  for (const viewport of [
    { width: 740, height: 360 },
    { width: 932, height: 430 },
    { width: 960, height: 432 },
  ]) {
    const p = await page({
      viewport,
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: viewport.width === 932 ? 2 : 1,
    });
    await ready(p, "c");
    const s = await state(p);
    assert.equal(s.zoom, 1);
    bounds(s, [1024, 1536]);
    const boxes = await p
      .locator("#joystick,#run,#explore,#scenic")
      .evaluateAll((es) =>
        es.map((e) => {
          const r = e.getBoundingClientRect();
          return { x: r.x, y: r.y, w: r.width, h: r.height };
        }),
      );
    assert(
      boxes.every(
        (b) =>
          b.x >= 0 &&
          b.y >= 0 &&
          b.x + b.w <= viewport.width &&
          b.y + b.h <= viewport.height,
      ),
    );
    record({
      case: "Landscape HUD bounds",
      viewport,
      dpr: viewport.width === 932 ? 2 : 1,
      pass: true,
      boxes,
      camera: s.camera,
    });
    await p.close();
  }
  const p = await page({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await ready(p, "c");
  await p.waitForTimeout(1300);
  assert.equal((await state(p)).camera.mode, "follow");
  await p.locator("#settings summary").click();
  await p.locator("#showcases").check();
  await p.locator("#settings summary").click();
  await p.waitForFunction(() => window.__GATE2__.camera.mode === "showcase");
  const before = await state(p);
  await p.keyboard.down("d");
  await p.waitForTimeout(120);
  await p.keyboard.up("d");
  assert.equal((await state(p)).camera.mode, "follow");
  assert((await state(p)).x > before.x);
  await p.waitForTimeout(1600);
  assert.equal((await state(p)).camera.mode, "follow");
  record({
    case: "Showcase opt-in, real-input cancellation, no teleport and no repeat",
    pass: true,
  });
  await p.close();
  const reduced = await page({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  await ready(reduced, "b");
  await reduced.locator("#settings summary").click();
  assert(await reduced.locator("#showcases").isDisabled());
  record({ case: "Reduced motion suppresses showcases", pass: true });
  await reduced.close();
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    `${D}/browser-qa.json`,
    JSON.stringify(
      {
        rows,
        errors,
        limits: [
          "System Chromium Canvas/mobile emulation, not physical-device FPS",
          "Fixed reciprocal scenic zoom loses detail at reduced scales; native1:1 is art evidence",
          "Integration proof uses an independent Muneum/station native overlap, not a full-world seam system",
        ],
      },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS", rows.length, "acceptance cases");
} finally {
  await browser.close();
}
async function pSafeWait(p, t) {
  await p.waitForTimeout(t);
}
