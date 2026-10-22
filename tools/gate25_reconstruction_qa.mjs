import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
const D = "docs/gate25-reconstruction",
  rows = [],
  errors = [];
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--disable-background-timer-throttling",
  ],
});
const mobile = () =>
  browser.newPage({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 1,
    isMobile: true,
    hasTouch: true,
  });
const watch = (p) => {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
};
async function record(p, name) {
  const dir = ".cache/gate25-reconstruction/" + name;
  await fs.mkdir(dir, { recursive: true });
  const c = await p.context().newCDPSession(p),
    frames = [],
    writes = [];
  c.on("Page.screencastFrame", (e) => {
    const n = String(frames.length).padStart(6, "0") + ".jpg";
    frames.push({ name: n, t: e.metadata.timestamp });
    writes.push(fs.writeFile(dir + "/" + n, Buffer.from(e.data, "base64")));
    void c.send("Page.screencastFrameAck", { sessionId: e.sessionId });
  });
  await c.send("Page.startScreencast", {
    format: "jpeg",
    quality: 88,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 4,
  });
  return async () => {
    await c.send("Page.stopScreencast");
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
      "-threads",
      "2",
      "-preset",
      "fast",
      "-crf",
      "22",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      D + "/" + name + ".mp4",
    ]);
    return {
      source:
        "actual Phaser/CDP normal-entry real input, no QA placement or speed change",
      frames: frames.length,
      seconds: frames.at(-1).t - frames[0].t,
    };
  };
}
async function control(p, id) {
  if (
    await p.evaluate(
      () =>
        window.__GATE2__.camera.mode === "tour" &&
        window.__GATE2__.camera.tour.controlsCollapsed,
    )
  )
    await p.tap("#tour-controls");
  await p.tap(id);
}
try {
  for (const id of ["district-polish", "district-reconstruction"]) {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    watch(p);
    await ready(p, id, "&native&overview");
    await p.waitForTimeout(300);
    await capture(
      p,
      D +
        "/" +
        (id === "district-polish" ? "BEFORE" : "AFTER") +
        "_NATIVE_1X.png",
    );
    await p.close();
  }
  const p = await mobile();
  watch(p);
  await ready(p, "district-reconstruction");
  assert.equal(
    await p.evaluate(() => typeof window.__GATE2_TEST__),
    "undefined",
  );
  const g = await grid(p),
    finish = await record(p, "DISTRICT_CROSSINGS"),
    routes = [];
  for (const t of [
    [1552, 780],
    [1998, 780],
    [2548, 790],
    [2824, 697],
  ]) {
    routes.push(await walk(p, g, t));
    await p.screenshot({ path: D + `/PLAYER_${t[0]}.png` });
  }
  const video = await finish();
  for (const t of [
    [1998, 780],
    [1552, 780],
    [1200, 780],
  ])
    routes.push(await walk(p, g, t));
  const s = await state(p);
  assert.equal(s.chunks.resident.length, 3);
  assert.equal(s.chunks.events.filter((e) => e.event === "request").length, 1);
  rows.push({
    case: "reconstructed joins normal movement both directions / independently owned foreground / native chunks",
    pass: true,
    routes,
    state: s,
    video,
  });
  await p.close();
  console.log("PASS district crossings");
  const t = await mobile();
  watch(t);
  await ready(t, "c");
  const origin = await state(t);
  await t.tap("#scenic");
  const stopVideo = await record(t, "JEJU_TOUR");
  await t.tap("#start-tour");
  const stops = [];
  for (let i = 0; i < 4; i++) {
    await t.waitForFunction(
      (i) => {
        const c = window.__GATE2__?.camera;
        return (
          c?.mode === "tour" && c.tour.index === i && c.tour.elapsed > 2050
        );
      },
      i,
      { timeout: 12000 },
    );
    const s = await state(t);
    assert.equal(s.zoom, 0.5);
    assert.equal(s.x, origin.x);
    assert.equal(s.y, origin.y);
    stops.push(s.camera);
    await t.screenshot({ path: D + `/TOUR_${i + 1}.png` });
    if (i === 0) {
      await t.waitForFunction(
        () => window.__GATE2__.camera.tour.controlsCollapsed,
        { timeout: 4000 },
      );
      await t.screenshot({ path: D + "/TOUR_COLLAPSED.png" });
      await t.tap("#tour-controls");
      await t.waitForFunction(
        () => !window.__GATE2__.camera.tour.controlsCollapsed,
      );
      await t.screenshot({ path: D + "/TOUR_EXPANDED.png" });
    }
    if (i === 1) {
      await control(t, "#tour-pause");
      await t.waitForTimeout(100);
      const center = (await state(t)).camera.center;
      await t.waitForTimeout(350);
      assert.deepEqual((await state(t)).camera.center, center);
      await control(t, "#tour-pause");
    }
  }
  assert(
    stops[0].worldView[1] - stops[1].worldView[1] >= 240,
    "coast /oreum must be compositionally distinct",
  );
  await t.waitForFunction(() => window.__GATE2__.camera.tour.complete, {
    timeout: 10000,
  });
  await control(t, "#return-juni");
  await t.waitForFunction(() => window.__GATE2__.camera.mode === "follow");
  assert.equal((await state(t)).x, origin.x);
  rows.push({
    case: "preserved four-stop50% tour / coast-oreum separation / inactive collapse / accessible restore / pause / native return / Juni retained",
    pass: true,
    stops,
    video: await stopVideo(),
  });
  await t.tap("#scenic");
  await t.tap("#start-tour");
  await t.waitForTimeout(400);
  await control(t, "#tour-next");
  await t.waitForFunction(() => window.__GATE2__.camera.tour.index === 1);
  await t.keyboard.down("d");
  await t.waitForTimeout(450);
  await t.keyboard.up("d");
  assert.equal((await state(t)).camera.mode, "follow");
  rows.push({ case: "Skip and movement cancellation preserved", pass: true });
  await t.close();
  console.log("PASS tour");
  const reduced = await mobile();
  await reduced.emulateMedia({ reducedMotion: "reduce" });
  await ready(reduced, "c");
  await reduced.tap("#scenic");
  await reduced.tap("#start-tour");
  await reduced.waitForFunction(() => window.__GATE2__.camera.mode === "tour");
  await reduced.waitForTimeout(100);
  const a = await state(reduced);
  await reduced.waitForTimeout(2700);
  assert.deepEqual((await state(reduced)).camera.center, a.camera.center);
  assert.equal((await state(reduced)).camera.tour.controlsCollapsed, false);
  await reduced.tap("#tour-next");
  await reduced.waitForFunction(() => window.__GATE2__.camera.tour.index === 1);
  await reduced.tap("#return-juni");
  await reduced.waitForFunction(() => window.__GATE2__.camera.zoom === 1);
  rows.push({
    case: "reduced motion static stops / no auto-hide / manual selection / instant native return",
    pass: true,
  });
  await reduced.close();
  for (const [width, height, dpr] of [
    [740, 360, 1],
    [932, 430, 2],
    [960, 432, 1],
  ]) {
    const q = await browser.newPage({
      viewport: { width, height },
      deviceScaleFactor: dpr,
      isMobile: true,
      hasTouch: true,
    });
    watch(q);
    await ready(q, "c");
    await q.tap("#scenic");
    await q.tap("#start-tour");
    await q.waitForTimeout(400);
    const s = await state(q),
      boxes = await q
        .locator(
          "#tour-caption,#tour-pause,#tour-next,#return-juni,#tour-controls",
        )
        .evaluateAll((es) =>
          es.map((e) => {
            const r = e.getBoundingClientRect();
            return [r.left, r.top, r.right, r.bottom];
          }),
        );
    assert(
      boxes.every(
        (b) => b[0] >= 0 && b[1] >= 0 && b[2] <= width && b[3] <= height,
      ),
    );
    assert(
      boxes.every((b) => b[0] >= s.camera.viewport[0] + s.camera.viewport[2]),
    );
    await q.screenshot({ path: D + `/UX_${width}x${height}.png` });
    rows.push({
      case:
        "landscape gutter controls outside artwork " +
        width +
        "x" +
        height +
        " DPR" +
        dpr,
      pass: true,
      boxes,
    });
    await q.close();
  }
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    D + "/browser-qa.json",
    JSON.stringify(
      {
        rows,
        errors,
        physicalAndroid: "NOT TESTED",
        physicalIPhone: "NOT TESTED",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS",
    rows.length,
    "polish cases / native evidence / real videos",
  );
} catch (e) {
  await fs.writeFile(
    D + "/qa-failure.json",
    JSON.stringify({ rows, errors, error: String(e) }, null, 2),
  );
  throw e;
} finally {
  await browser.close();
}
