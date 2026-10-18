/* global MediaRecorder, cancelAnimationFrame, btoa */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
const base =
    process.env.PIXEL_CAPTURE_URL ?? "http://127.0.0.1:4201/3D-pharse5-/",
  out = "docs/living-korea/quality",
  dir = `.cache/living-korea/tour-${Date.now()}`;
await fs.mkdir(dir, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  viewport: { width: 844, height: 390 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
  reducedMotion: "no-preference",
});
const p = await context.newPage(),
  errors = [],
  visits = [],
  frames = [],
  writes = new Set();
p.on("pageerror", (e) => errors.push(e.message));
p.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
await p.goto(base + "living-korea-review.html?renderer=canvas");
await p.waitForFunction(() => window.__KOREA__?.district === "heritage");
if (await p.evaluate(() => !!window.__SEOUL_TEST__))
  throw Error("No QA placement allowed during gameplay capture");
await p.evaluate(() => {
  const stream = document.querySelector("canvas").captureStream(60),
    mime = ["video/webm;codecs=vp9", "video/webm;codecs=vp8"].find((m) =>
      MediaRecorder.isTypeSupported(m),
    );
  if (!mime) throw Error("Recorder unavailable");
  const chunks = [],
    rec = new MediaRecorder(stream, {
      mimeType: mime,
      videoBitsPerSecond: 2200000,
    });
  const q = {
    stream,
    rec,
    mime,
    chunks,
    start: performance.now(),
    frame: window.__PIXEL_METRICS__.frameCount,
    times: [],
  };
  window.__K_CAPTURE__ = q;
  let last = performance.now();
  const tick = (now) => {
    q.times.push(now - last);
    last = now;
    q.raf = requestAnimationFrame(tick);
  };
  q.raf = requestAnimationFrame(tick);
  rec.ondataavailable = (e) => {
    if (e.data.size) chunks.push(e.data);
  };
  rec.start(1000);
});
const cdp = await context.newCDPSession(p);
let active = true;
cdp.on("Page.screencastFrame", (f) => {
  void cdp
    .send("Page.screencastFrameAck", { sessionId: f.sessionId })
    .catch(() => {});
  if (!active) return;
  const data = Buffer.from(f.data, "base64"),
    id = String(frames.length).padStart(6, "0"),
    file = `${dir}/${id}.jpg`;
  frames.push({
    file,
    timestamp: f.metadata.timestamp,
    sha256: createHash("sha256").update(data).digest("hex"),
    bytes: data.length,
    width: 844,
    height: 390,
  });
  const job = fs.writeFile(file, data);
  writes.add(job);
  void job.finally(() => writes.delete(job));
});
await cdp.send("Page.startScreencast", {
  format: "jpeg",
  quality: 85,
  maxWidth: 844,
  maxHeight: 390,
  everyNthFrame: 1,
});
const selectors = {
  up: '[aria-label="Đi lên"]',
  down: '[aria-label="Đi xuống"]',
  left: '[aria-label="Sang trái"]',
  right: '[aria-label="Sang phải"]',
  run: "#run",
};
let held = new Set();
async function touch(next) {
  if ([...next].sort().join() === [...held].sort().join()) return;
  if (held.size)
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
  if (next.size) {
    const points = [];
    for (const key of next) {
      const b = await p.locator(selectors[key]).boundingBox();
      points.push({
        x: b.x + b.width / 2,
        y: b.y + b.height / 2,
        id: points.length + 1,
      });
    }
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: points,
    });
  }
  held = next;
}
async function travel(name, points, run = true) {
  const start = Date.now();
  for (const [x, y] of points) {
    const begin = Date.now();
    for (;;) {
      const s = await p.evaluate(() => window.__SEOUL__);
      if (Math.abs(s.x - x) < 6 && Math.abs(s.y - y) < 6) break;
      if (Date.now() - begin > 30000)
        throw Error("Stuck on " + name + " " + JSON.stringify(s));
      const next = new Set(run ? ["run"] : []);
      if (s.x < x - 4) next.add("right");
      if (s.x > x + 4) next.add("left");
      if (s.y < y - 4) next.add("down");
      if (s.y > y + 4) next.add("up");
      await touch(next);
      await p.waitForTimeout(45);
    }
  }
  await touch(new Set());
  await p.waitForTimeout(200);
  visits.push({
    name,
    run,
    elapsedMs: Date.now() - start,
    state: await p.evaluate(() => ({
      district: window.__KOREA__.district,
      x: window.__SEOUL__.x,
      y: window.__SEOUL__.y,
    })),
  });
  console.log("visit", name);
}
async function interact(close = true) {
  await touch(new Set());
  await p.locator("#interact").tap();
  await p.waitForTimeout(550);
  if (close && (await p.locator("#dialog").isVisible()))
    await p.locator("#close-dialog").tap();
}
let failure;
try {
  await p.waitForTimeout(600);
  await interact();
  await travel(
    "Open palace gateways to royal hall",
    [
      [1152, 500],
      [1152, 352],
    ],
    false,
  );
  await interact();
  await p.locator("#wave").tap();
  await p.waitForTimeout(1200);
  await travel("Hanji court", [[1456, 404]]);
  await interact();
  await travel("Return through real palace gates", [
    [1152, 384],
    [1152, 500],
    [1152, 832],
  ]);
  await travel("Academy east shortcut", [
    [1152, 1328],
    [944, 1392],
    [768, 1392],
    [768, 1344],
    [544, 1344],
    [544, 1152],
  ]);
  await interact();
  await p.waitForFunction(() => window.__KOREA__?.district === "room");
  await travel("Retained Hangul desk", [[385, 392]], false);
  await interact(false);
  await p.screenshot({ path: out + "/walkthrough-lesson-interface.png" });
  for (const answer of ["giyeok", "nieun", "mieum"]) {
    await p.getByRole("button", { name: answer, exact: true }).tap();
    await p.waitForTimeout(300);
    await p
      .getByRole("button", {
        name: answer === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .tap();
  }
  await p.locator("#close-dialog").tap();
  await travel("Reading room return", [[384, 490]], false);
  await interact();
  await p.waitForFunction(() => window.__KOREA__?.district === "heritage");
  await travel("Workshop service and front gates", [
    [544, 1344],
    [768, 1344],
    [768, 1392],
    [944, 1392],
    [1152, 1328],
    [1376, 1344],
    [1440, 1264],
    [1632, 1264],
    [1632, 1472],
  ]);
  await interact();
  await travel("Repaired institutional cross-lane and museum frontage", [
    [1632, 1536],
    [1632, 1616],
    [2144, 1616],
    [1632, 1616],
    [1584, 1760],
    [1640, 2016],
    [1856, 2064],
    [1984, 2032],
  ]);
  await interact();
  await travel("Cultural street and modern travel garden", [
    [1856, 2064],
    [1456, 2080],
    [1152, 2080],
  ]);
  await interact(false);
  await p.locator("#travel-go").tap();
  await p.waitForFunction(() => window.__KOREA__?.district === "namsan");
  await travel(
    "Namsan wooded hill ascent",
    [
      [704, 1024],
      [512, 960],
      [384, 816],
    ],
    false,
  );
  await interact();
  await travel(
    "Observation tower arrival",
    [
      [416, 688],
      [576, 688],
      [704, 752],
      [832, 752],
      [832, 672],
    ],
    false,
  );
  await interact();
  await p.locator("#celebrate").tap();
  await p.waitForTimeout(1500);
  await travel(
    "Accessible scenic terrace and telescope",
    [
      [832, 752],
      [832, 784],
      [992, 864],
      [1056, 880],
      [1120, 928],
      [1120, 784],
    ],
    false,
  );
  await interact();
  await travel("Return along the compact park loop", [
    [1120, 928],
    [928, 1056],
    [704, 1024],
    [704, 1088],
  ]);
  await interact(false);
  await p.locator("#travel-go").tap();
  await p.waitForFunction(() => window.__KOREA__?.district === "heritage");
  await p.waitForTimeout(500);
  await p.locator("#wave").tap();
  await p.waitForTimeout(1200);
} catch (e) {
  failure = String(e);
  console.log(failure);
} finally {
  await touch(new Set());
  const runtime = await p.evaluate(() => {
    const q = window.__K_CAPTURE__;
    cancelAnimationFrame(q.raf);
    const elapsedMs = performance.now() - q.start,
      t = q.times.slice(1).sort((a, b) => a - b);
    return {
      elapsedMs,
      actualGameFrames: window.__PIXEL_METRICS__.frameCount - q.frame,
      measuredGameFPS:
        ((window.__PIXEL_METRICS__.frameCount - q.frame) * 1000) / elapsedMs,
      rafFrameMs: {
        p50: t[Math.floor(t.length * 0.5)],
        p95: t[Math.floor(t.length * 0.95)],
        p99: t[Math.floor(t.length * 0.99)],
      },
      scope:
        "During simultaneous native canvas recording and real browser screencast, ending BEFORE recorder stop/serialization. Independent benchmark excludes capture work.",
    };
  });
  await cdp.send("Page.stopScreencast");
  active = false;
  await Promise.all([...writes]);
  const native = await p.evaluate(async () => {
    const q = window.__K_CAPTURE__,
      stop = new Promise((resolve) => (q.rec.onstop = resolve));
    q.rec.stop();
    await stop;
    q.stream.getTracks().forEach((t) => t.stop());
    const a = new Uint8Array(
      await new Blob(q.chunks, { type: q.mime }).arrayBuffer(),
    );
    let binary = "";
    for (let i = 0; i < a.length; i += 32768)
      binary += String.fromCharCode(...a.subarray(i, i + 32768));
    return { data: btoa(binary), mime: q.mime };
  });
  await fs.writeFile(
    out + "/native-gameplay-original.webm",
    Buffer.from(native.data, "base64"),
  );
  const first = frames[0]?.timestamp,
    last = frames.at(-1)?.timestamp;
  await fs.writeFile(
    out + "/capture.json",
    JSON.stringify(
      {
        method:
          "Actual full-browser CDP JPEG85 screencast844x390 plus original canvas.captureStream(60)/VP9 MediaRecorder2.2Mbps. Real multi-pointer D-pad+run/tap UI throughout normal public entry. NO QA hook/placement/injected frames. Only public room/travel transitions change areas. UI JPEG source frames retained in ignored cache; hashes/timestamps permanent. Runtime FPS is separate from encoded capture FPS.",
        rawFramesDirectory: dir,
        frames,
        sourceWholeBrowserFrames: frames.length,
        sourceWholeBrowserFirstLastSeconds: last - first,
        sourceWholeBrowserAverageFPS: (frames.length - 1) / (last - first),
        runtime,
        visits,
        errors,
        failure: failure ?? null,
        noQAPlacement: true,
        nativeMime: native.mime,
      },
      null,
      2,
    ) + "\n",
  );
  await browser.close();
  console.log({
    visits: visits.length,
    sourceFrames: frames.length,
    sourceFPS: (frames.length - 1) / (last - first),
    runtimeFPS: runtime.measuredGameFPS,
    failure,
    errors,
  });
}
if (failure || errors.length) throw Error(failure ?? JSON.stringify(errors));
