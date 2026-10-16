/* global MediaRecorder, cancelAnimationFrame, btoa */
import { chromium } from "playwright";
import fs from "node:fs/promises";
const base =
  process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/";
const out = "docs/world-refinement/quality";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1440, height: 1140 },
  reducedMotion: "no-preference",
});
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
await p.goto(base + "refinement-review.html?renderer=canvas");
await p.waitForFunction(() => window.__SEOUL__?.ready);
if (await p.evaluate(() => !!window.__SEOUL_TEST__))
  throw Error("Capture must not expose QA placement");
await p.locator("canvas").scrollIntoViewIfNeeded();
await p.locator("canvas").focus();
await p.evaluate(() => {
  const canvas = document.querySelector("canvas");
  const stream = canvas.captureStream(60);
  const mime = ["video/webm;codecs=vp9", "video/webm;codecs=vp8"].find((m) =>
    MediaRecorder.isTypeSupported(m),
  );
  if (!mime) throw Error("No supported recorder");
  const chunks = [];
  const rec = new MediaRecorder(stream, {
    mimeType: mime,
    videoBitsPerSecond: 6000000,
  });
  window.__CAPTURE__ = {
    rec,
    stream,
    chunks,
    mime,
    start: performance.now(),
    frames: window.__PIXEL_METRICS__.frameCount,
    rafTimes: [],
  };
  const c = window.__CAPTURE__;
  let last = performance.now();
  function tick(now) {
    c.rafTimes.push(now - last);
    last = now;
    c.raf = requestAnimationFrame(tick);
  }
  c.raf = requestAnimationFrame(tick);
  rec.ondataavailable = (e) => {
    if (e.data.size) chunks.push(e.data);
  };
  rec.start(1000);
});
let held = new Set();
const visits = [];
async function keys(next) {
  for (const k of held) if (!next.has(k)) await p.keyboard.up(k);
  for (const k of next) if (!held.has(k)) await p.keyboard.down(k);
  held = next;
}
async function travel(name, points, run = true) {
  const begin = Date.now();
  await p.locator("canvas").focus();
  for (const [x, y] of points) {
    const start = Date.now();
    for (;;) {
      const s = await p.evaluate(() => window.__SEOUL__);
      if (Math.abs(s.x - x) < 6 && Math.abs(s.y - y) < 6) break;
      if (Date.now() - start > 30000)
        throw Error("Capture stuck " + name + " at " + JSON.stringify(s));
      const next = new Set(run ? ["Shift"] : []);
      if (s.x < x - 4) next.add("ArrowRight");
      if (s.x > x + 4) next.add("ArrowLeft");
      if (s.y < y - 4) next.add("ArrowDown");
      if (s.y > y + 4) next.add("ArrowUp");
      await keys(next);
      await p.waitForTimeout(45);
    }
  }
  await keys(new Set());
  await p.waitForTimeout(200);
  visits.push({
    name,
    elapsedMs: Date.now() - begin,
    point: await p.evaluate(() => ({
      x: window.__SEOUL__.x,
      y: window.__SEOUL__.y,
      area: window.__SEOUL__.area,
    })),
  });
}
async function interact() {
  await keys(new Set());
  await p.keyboard.press("e");
  await p.waitForTimeout(700);
  if (await p.locator("#dialog").isVisible())
    await p.locator("#close-dialog").click();
  await p.locator("canvas").focus();
}
let failure;
try {
  await p.waitForTimeout(800);
  await interact();
  await travel(
    "Outer and inner gate to royal hall",
    [
      [1152, 500],
      [1152, 320],
    ],
    false,
  );
  await interact();
  await travel("Hanji court", [[1456, 404]]);
  await interact();
  await travel("Return by open gates", [
    [1152, 384],
    [1152, 500],
    [1152, 832],
  ]);
  await travel("Academy east garden shortcut", [
    [1152, 1328],
    [944, 1392],
    [768, 1392],
    [768, 1344],
    [544, 1344],
    [544, 1152],
  ]);
  await interact();
  await p.waitForFunction(() => window.__SEOUL__?.area === "room");
  await travel("Reading room desk", [[385, 392]], false);
  await p.keyboard.press("e");
  await p.waitForTimeout(700);
  await p.screenshot({ path: out + "/lesson-interface.png" });
  for (const answer of ["giyeok", "nieun", "mieum"]) {
    await p
      .locator("#dialog-copy")
      .getByRole("button", { name: answer, exact: true })
      .click();
    await p
      .locator("#dialog-copy")
      .getByRole("button", {
        name: answer === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  await p.locator("#close-dialog").click();
  await travel("Room exit", [[384, 490]], false);
  await interact();
  await p.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
  await travel("Workshop service entrance", [
    [544, 1344],
    [768, 1344],
    [768, 1392],
    [944, 1392],
    [1152, 1328],
    [1376, 1344],
    [1440, 1264],
    [1632, 1264],
    [1632, 1400],
    [1632, 1472],
  ]);
  await interact();
  await travel("Museum landscaped frontage", [
    [1632, 1536],
    [1584, 1632],
    [1640, 1792],
    [1856, 1840],
    [1984, 1808],
    [1984, 1744],
  ]);
  await interact();
  await travel("Cultural lane to modern books and tea", [
    [1984, 1808],
    [1856, 1840],
    [1640, 1792],
    [1408, 1760],
    [1120, 1664],
    [800, 1856],
    [512, 1872],
  ]);
  await interact();
  await p.locator("#celebrate").click();
  await p.waitForTimeout(1800);
  await p.locator("#night").click();
  await p.waitForTimeout(800);
} catch (e) {
  failure = String(e);
} finally {
  await keys(new Set());
  const result = await p.evaluate(async () => {
    const c = window.__CAPTURE__;
    cancelAnimationFrame(c.raf);
    const stop = new Promise((resolve) => (c.rec.onstop = resolve));
    c.rec.stop();
    await stop;
    c.stream.getTracks().forEach((t) => t.stop());
    const bytes = new Uint8Array(
      await new Blob(c.chunks, { type: c.mime }).arrayBuffer(),
    );
    let binary = "";
    for (let i = 0; i < bytes.length; i += 32768)
      binary += String.fromCharCode(...bytes.subarray(i, i + 32768));
    const sorted = c.rafTimes.slice(1).sort((a, b) => a - b);
    const elapsedMs = performance.now() - c.start;
    return {
      base64: btoa(binary),
      mime: c.mime,
      elapsedMs,
      actualPhaserFrames: window.__PIXEL_METRICS__.frameCount - c.frames,
      runtimeFPS:
        ((window.__PIXEL_METRICS__.frameCount - c.frames) * 1000) / elapsedMs,
      rafMs: {
        p50: sorted[Math.floor(sorted.length * 0.5)],
        p95: sorted[Math.floor(sorted.length * 0.95)],
        p99: sorted[Math.floor(sorted.length * 0.99)],
      },
      canvas: [
        document.querySelector("canvas").width,
        document.querySelector("canvas").height,
      ],
    };
  });
  await fs.writeFile(
    out + "/gameplay-original.webm",
    Buffer.from(result.base64, "base64"),
  );
  delete result.base64;
  await fs.writeFile(
    out + "/capture.json",
    JSON.stringify(
      {
        method:
          "Original browser canvas.captureStream(60) + MediaRecorder; continuous real keyboard/mouse input, no QA placement or injected frames; VP9/VP8 original retained. Canvas video does not include DOM dialogs, captured separately as screenshots. Shift100px/s only on documented running legs, walking60px/s unchanged. Runtime frames separate from encoded frames.",
        ...result,
        visits,
        errors,
        failure,
      },
      null,
      2,
    ),
  );
  await b.close();
  console.log({
    runtimeFPS: result.runtimeFPS,
    visits: visits.length,
    errors,
    failure,
  });
}
if (failure || errors.length) throw Error(failure ?? JSON.stringify(errors));
