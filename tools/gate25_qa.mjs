import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
const resume = process.argv.includes("--resume");
const districtOnly = process.argv.includes("--district-only");
const D = "docs/gate25",
  errors = [],
  rows = [];
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
async function record(p, name) {
  const dir = ".cache/gate25/" + name;
  await fs.mkdir(dir, { recursive: true });
  const cdp = await p.context().newCDPSession(p),
    frames = [],
    writes = [];
  cdp.on("Page.screencastFrame", (e) => {
    const n = String(frames.length).padStart(6, "0") + ".jpg";
    frames.push({ name: n, t: e.metadata.timestamp });
    writes.push(fs.writeFile(dir + "/" + n, Buffer.from(e.data, "base64")));
    void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
  });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 88,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 4,
  });
  return async () => {
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
      source: "actual CDP screencast / normal entry / no QA placement",
      frames: frames.length,
      duration: frames.at(-1).t - frames[0].t,
    };
  };
}
const watch = (p) => {
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
};
try {
  if (districtOnly)
    rows.push(
      ...JSON.parse(
        await fs.readFile(D + "/browser-qa.json", "utf8"),
      ).rows.filter((r) => !r.case.startsWith("three independent")),
    );
  if (!districtOnly) {
    const p = await mobile();
    watch(p);
    await ready(p, "c");
    assert.equal(
      await p.evaluate(() => typeof window.__GATE2_TEST__),
      "undefined",
    );
    if (resume)
      rows.push(
        ...JSON.parse(await fs.readFile(D + "/qa-failure.json", "utf8")).rows,
      );
    if (!resume) {
      const origin = await state(p),
        stops = [];
      await p.screenshot({ path: D + "/FOLLOW.png" });
      await p.tap("#scenic");
      await p.screenshot({ path: D + "/SCENIC.png" });
      await p.tap("#overview-mode");
      await p.screenshot({ path: D + "/OVERVIEW.png" });
      await p.tap("#scenic");
      const finish = await record(p, "JEJU_TOUR");
      await p.tap("#start-tour");
      for (let i = 0; i < 4; i++) {
        await p.waitForFunction(
          (i) => {
            const c = window.__GATE2__?.camera;
            return (
              c?.mode === "tour" && c.tour.index === i && c.tour.elapsed > 2050
            );
          },
          i,
          { timeout: 15000 },
        );
        const s = await state(p);
        assert(
          Math.abs(s.x - origin.x) < 0.01 && Math.abs(s.y - origin.y) < 0.01,
        );
        assert.equal(s.camera.zoom, 0.5);
        stops.push(s.camera);
        await p.screenshot({ path: D + `/TOUR_${i + 1}.png` });
        if (i === 1) {
          await p.tap("#tour-pause");
          const before = await state(p);
          await p.waitForTimeout(400);
          assert.deepEqual(
            (await state(p)).camera.center,
            before.camera.center,
          );
          const cdp = await p.context().newCDPSession(p);
          await cdp.send("Input.dispatchTouchEvent", {
            type: "touchStart",
            touchPoints: [{ x: 430, y: 160, id: 1 }],
          });
          await cdp.send("Input.dispatchTouchEvent", {
            type: "touchMove",
            touchPoints: [{ x: 430, y: 100, id: 1 }],
          });
          await cdp.send("Input.dispatchTouchEvent", {
            type: "touchEnd",
            touchPoints: [],
          });
          await p.waitForTimeout(100);
          assert.notDeepEqual(
            (await state(p)).camera.center,
            before.camera.center,
          );
          await p.tap("#tour-pause");
        }
      }
      await p.waitForFunction(() => window.__GATE2__.camera.tour.complete, {
        timeout: 10000,
      });
      const complete = await state(p);
      assert.deepEqual(
        complete.camera.tour.history.map((x) => x.id),
        ["coast", "oreum", "orchard", "house"],
      );
      await p.tap("#return-juni");
      await p.waitForTimeout(450);
      assert.equal((await state(p)).camera.mode, "follow");
      assert(Math.abs((await state(p)).x - origin.x) < 0.01);
      const video = await finish();
      rows.push({
        case: "complete Jeju tour / native player retained / all4 stops50% / pause-drag-resume / return",
        pass: true,
        stops,
        video,
      });
    }
    await p.tap("#scenic");
    await p.tap("#start-tour");
    await p.waitForTimeout(500);
    await p.tap("#tour-next");
    await p.waitForFunction(() => window.__GATE2__.camera.tour.index === 1);
    await p.keyboard.down("d");
    await p.waitForTimeout(500);
    await p.keyboard.up("d");
    assert.equal((await state(p)).camera.mode, "follow");
    rows.push({
      case: "Skip and movement-intent safely cancel automatic camera",
      pass: true,
    });
    await ready(p, "b");
    await p.tap("#scenic");
    await p.tap("#start-tour");
    await p.waitForTimeout(2600);
    await p.screenshot({ path: D + "/MUNEUM_TOUR.png" });
    assert.equal((await state(p)).camera.mode, "tour");
    rows.push({
      case: "shared tour architecture / one additional Muneum demo",
      pass: true,
    });
    await p.close();
    const reduce = await mobile();
    watch(reduce);
    await reduce.emulateMedia({ reducedMotion: "reduce" });
    await ready(reduce, "c");
    await reduce.tap("#scenic");
    await reduce.tap("#start-tour");
    await reduce.waitForFunction(() => window.__GATE2__.camera.mode === "tour");
    await reduce.waitForTimeout(80);
    const r = await state(reduce);
    await reduce.waitForTimeout(600);
    assert.deepEqual((await state(reduce)).camera.center, r.camera.center);
    assert.equal(r.camera.tour.paused, true);
    await reduce.tap("#tour-next");
    await reduce.waitForFunction(
      () => window.__GATE2__.camera.tour.index === 1,
    );
    await reduce.tap("#return-juni");
    await reduce.waitForFunction(() => window.__GATE2__.camera.zoom === 1);
    rows.push({
      case: "reduced motion static selection / explicit next / instant native return",
      pass: true,
    });
    await reduce.close();
  }
  const district = await mobile();
  watch(district);
  await ready(district, "district");
  const before = await state(district);
  assert.equal(before.chunks.resident.length, 2);
  const fin = await record(district, "DISTRICT_WALK");
  const g = await grid(district),
    routes = [];
  for (const target of [
    [1540, 790],
    [1998, 790],
    [2520, 790],
    [2824, 697],
  ]) {
    routes.push(await walk(district, g, target));
    await district.screenshot({ path: D + `/DISTRICT_${target[0]}.png` });
  }
  const ds = await state(district);
  assert.equal(ds.chunks.resident.length, 3);
  assert.equal(ds.chunks.events.filter((e) => e.event === "request").length, 1);
  assert.equal(ds.chunks.pending.length, 0);
  await district.waitForTimeout(5100);
  const perf = await state(district);
  const footage = await fin();
  rows.push({
    case: "three independent native chunks / all joins / actual normal movement / one adjacent load / bounded retained cache",
    pass: true,
    routes,
    state: ds,
    performance: perf,
    video: footage,
  });
  await district.close();
  if (!districtOnly) {
    const fit = await mobile();
    watch(fit);
    await ready(fit, "jeju25");
    const fg = await grid(fit),
      fr = [];
    const scene = await fit.evaluate(
      async () => await (await fetch("assets/gate2/jeju25/scene.json")).json(),
    );
    const endBridge = await record(fit, "JEJU_BRIDGE");
    let bridgeVideo;
    for (const t of scene.targets.filter((t) =>
      /bridge|pier|exact-landing/.test(t.id),
    )) {
      fr.push(await walk(fit, fg, [t.x, t.y]));
      if (t.id === "bridge") bridgeVideo = await endBridge();
    }
    rows.push({
      case: "approved Jeju bridge/landing registration actual normal traversal",
      pass: true,
      video: bridgeVideo,
      routes: fr,
      state: await state(fit),
    });
    await fit.close();
  }
  for (const id of ["c", "district", "jeju25"]) {
    const n = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    watch(n);
    await ready(n, id, "&native&overview");
    await n.waitForTimeout(500);
    await capture(n, D + "/" + id.toUpperCase() + "_NATIVE_1X.png");
    await n.close();
  }
  assert.equal(errors.length, 0, JSON.stringify(errors));
  await fs.writeFile(
    D + "/browser-qa.json",
    JSON.stringify(
      {
        rows: [...new Map(rows.map((r) => [r.case, r])).values()],
        errors,
        physicalDevices: "NOT TESTED",
        emulator:
          "Linux Chromium Canvas /844x390 touch emulation /not device hardware",
      },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS", rows.length, "Gate2.5 cases / screenshots / real videos");
} catch (e) {
  await fs.writeFile(
    D + "/qa-failure.json",
    JSON.stringify({ rows, errors, error: String(e) }, null, 2),
  );
  throw e;
} finally {
  await browser.close();
}
