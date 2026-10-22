import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { ready, state } from "./gate2_browser_lib.mjs";
const dir = ".cache/gate2/acceptance/camera-video";
await fs.mkdir(dir, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--disable-background-timer-throttling",
  ],
});
const frames = [],
  writes = [],
  steps = [],
  errors = [];
try {
  const p = await browser.newPage({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 1,
    isMobile: true,
    hasTouch: true,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  await ready(p, "c");
  if (await p.evaluate(() => !!window.__GATE2_TEST__))
    throw Error("QA hook exposed");
  const cdp = await p.context().newCDPSession(p);
  cdp.on("Page.screencastFrame", (e) => {
    const name = String(frames.length).padStart(6, "0") + ".jpg";
    frames.push({ name, t: e.metadata.timestamp });
    writes.push(fs.writeFile(dir + "/" + name, Buffer.from(e.data, "base64")));
    void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
  });
  const touch = (type, pts) =>
    cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts });
  const mark = async (label) =>
    steps.push({ label, t: Date.now(), state: await state(p) });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 92,
    maxWidth: 844,
    maxHeight: 390,
    everyNthFrame: 2,
  });
  await p.waitForTimeout(900);
  await mark("Native follow");
  const b = await p.locator("#joystick").boundingBox(),
    j = { x: b.x + b.width / 2 + 30, y: b.y + b.height / 2, id: 1 };
  await touch("touchStart", [j]);
  await p.waitForTimeout(850);
  await touch("touchEnd", []);
  await p.waitForTimeout(300);
  await mark("Actual joystick walking / look-ahead");
  await p.tap("#scenic");
  await p.waitForTimeout(600);
  await mark("Scenic freezes player controls");
  await touch("touchStart", [{ x: 420, y: 170, id: 1 }]);
  for (let i = 1; i <= 12; i++) {
    await touch("touchMove", [{ x: 420 + i * 9, y: 170 + i * 3, id: 1 }]);
    await p.waitForTimeout(30);
  }
  await touch("touchEnd", []);
  await p.waitForTimeout(650);
  await mark("One-finger drag");
  await touch("touchStart", [
    { x: 280, y: 170, id: 1 },
    { x: 580, y: 170, id: 2 },
  ]);
  for (let i = 1; i <= 12; i++) {
    await touch("touchMove", [
      { x: 280 + i * 7, y: 170, id: 1 },
      { x: 580 - i * 7, y: 170, id: 2 },
    ]);
    await p.waitForTimeout(35);
  }
  await touch("touchEnd", []);
  await p.waitForTimeout(1000);
  await mark("Actual two-finger pinch, discrete nearest zoom");
  await p.tap("#overview-mode");
  await p.waitForTimeout(1900);
  await mark("Complete scene / Juni / destinations / previous viewport");
  await p.tap("#return-juni");
  await p.waitForTimeout(800);
  await mark("Return native1:1 without moving Juni");
  const r = await p.locator("#run").boundingBox();
  await touch("touchStart", [
    j,
    { x: r.x + r.width / 2, y: r.y + r.height / 2, id: 2 },
  ]);
  await p.waitForTimeout(700);
  await touch("touchEnd", []);
  await p.waitForTimeout(700);
  await mark("Actual joystick + run restored");
  await cdp.send("Page.stopScreencast");
  await Promise.all(writes);
  await browser.close();
  await fs.writeFile(
    dir + "/frames.txt",
    frames
      .map(
        (f, i) =>
          `file '${f.name}'\nduration ${Math.max(0.001, (frames[i + 1]?.t ?? f.t + 0.1) - f.t)}`,
      )
      .join("\n") + "\n",
  );
  execFileSync(
    "ffmpeg",
    [
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
      "20",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "docs/gate2/ACCEPTANCE_MOBILE_CAMERA.mp4",
    ],
    { timeout: 120000 },
  );
  await fs.writeFile(
    "docs/gate2/acceptance/camera-video-provenance.json",
    JSON.stringify(
      {
        source:
          "Normal-entry actual Phaser Canvas, mobile emulation, actual CDP touches/taps; no QA placement or static screenshot substitution. VFR preserves CDP timestamps; no speedup.",
        frames: frames.length,
        duration: frames.at(-1).t - frames[0].t,
        steps,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(
    "PASS",
    frames.length,
    "frames",
    frames.at(-1).t - frames[0].t,
    "seconds",
  );
} finally {
  await browser.close();
}
