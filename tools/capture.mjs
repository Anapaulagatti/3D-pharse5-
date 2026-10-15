import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync, existsSync, renameSync } from "node:fs";
import { createHash, randomUUID } from "node:crypto";
const out = ".cache/review/motion";
if (existsSync(out))
  renameSync(out, `.cache/review/prior-capture-${randomUUID().slice(0, 8)}`);
mkdirSync(out, { recursive: true });
const b = await chromium.launch({
  headless: true,
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const ctx = await b.newContext({
  viewport: { width: 1440, height: 1100 },
  deviceScaleFactor: 1,
  reducedMotion: "no-preference",
});
const p = await ctx.newPage();
const errors = [],
  missing = [],
  frames = [],
  segments = [];
let phase = "idle",
  origin,
  accept = true,
  cdp;
p.on("pageerror", (e) => errors.push(e.message));
p.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
p.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
const metrics = () => p.evaluate(() => window.__PIXEL_METRICS__);
async function hold(ms) {
  const start = await metrics();
  await p.waitForTimeout(ms);
  segments.push({ phase, start, end: await metrics(), wallMilliseconds: ms });
}
async function drive(key, axis, amount, release = true) {
  await p.locator("canvas").focus();
  const start = await metrics();
  const target = start[axis] + amount;
  await p.keyboard.down(key);
  try {
    await p.waitForFunction(
      ({ axis, target, sign }) =>
        (window.__PIXEL_METRICS__[axis] - target) * sign >= 0,
      { axis, target, sign: Math.sign(amount) },
      { timeout: 10000 },
    );
  } finally {
    if (release) await p.keyboard.up(key);
  }
  segments.push({
    phase,
    start,
    end: await metrics(),
    method:
      "Native key held until observed physical distance; no injected position.",
  });
}
let status = "FAILED_CAPTURE";
try {
  await p.goto("http://127.0.0.1:4201/3D-pharse5-/");
  await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  cdp = await ctx.newCDPSession(p);
  cdp.on("Page.screencastFrame", (e) => {
    cdp
      .send("Page.screencastFrameAck", { sessionId: e.sessionId })
      .catch(() => {});
    if (!accept) return;
    if (origin === undefined) origin = e.metadata.timestamp;
    const data = Buffer.from(e.data, "base64"),
      n = frames.length;
    writeFileSync(`${out}/${String(n).padStart(4, "0")}.jpg`, data);
    frames.push({
      index: n,
      at: e.metadata.timestamp - origin,
      phase,
      sha256: createHash("sha256").update(data).digest("hex"),
    });
  });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 85,
    maxWidth: 1440,
    maxHeight: 1100,
    everyNthFrame: 1,
  });
  await hold(3500);
  await p.locator("#zoom").selectOption("3");
  for (const action of ["wave", "celebrate", "think", "pose"]) {
    phase = action;
    await p.locator("#" + action).click();
    await hold(action === "think" ? 1700 : 1400);
  }
  for (const mood of ["neutral", "happy", "focused", "surprised"]) {
    phase = "expression-" + mood;
    await p.locator("#expression").selectOption(mood);
    await hold(800);
  }
  await p.locator("#expression").selectOption("neutral");
  phase = "outfit-change";
  await p.locator("#hair").selectOption("1");
  await p.locator("#outfit").selectOption("1");
  await hold(1000);
  for (const action of ["walk", "run"]) {
    if (action === "run") await p.keyboard.down("Shift");
    const distance = action === "run" ? 44 : 28;
    for (const [dir, key, axis, sign] of [
      ["down", "ArrowDown", "y", 1],
      ["right", "ArrowRight", "x", 1],
      ["up", "ArrowUp", "y", -1],
      ["left", "ArrowLeft", "x", -1],
    ]) {
      phase = action + "-" + dir;
      await drive(key, axis, distance * sign);
      phase = action + "-stop-" + dir;
      await hold(350);
    }
    if (action === "run") await p.keyboard.up("Shift");
  }
  phase = "turning";
  await drive("ArrowRight", "x", 20, false);
  await p.keyboard.up("ArrowRight");
  await drive("ArrowUp", "y", -20);
  await hold(350);
  // Reframe by real walking before greeting guests; avoids pointing off-screen.
  phase = "walk-to-guests";
  let m = await metrics();
  if (Math.abs(m.x - 512) > 2)
    await drive(m.x > 512 ? "ArrowLeft" : "ArrowRight", "x", 512 - m.x);
  m = await metrics();
  if (Math.abs(m.y - 595) > 2)
    await drive(m.y > 595 ? "ArrowUp" : "ArrowDown", "y", 595 - m.y);
  await p.locator("#zoom").selectOption("2");
  await hold(300);
  for (const id of ["sejong", "jang", "saimdang", "yi"]) {
    phase = "npc-" + id;
    await p.locator(`[data-guest="${id}"]`).click();
    await p.waitForFunction(() => !document.querySelector("#dialog").hidden);
    await hold(200);
    await p.locator("#close-dialog").click();
    await p.evaluate(() => window.scrollTo(0, 0));
    await hold(1300);
  }
  phase = "return-idle";
  await hold(1800);
  if (errors.length || missing.length)
    throw Error(JSON.stringify({ errors, missing }));
  status = "CAPTURED_PENDING_DECODED_VISUAL_INSPECTION";
} finally {
  accept = false;
  if (cdp) await cdp.send("Page.stopScreencast").catch(() => {});
  writeFileSync(
    out + "/capture.json",
    JSON.stringify(
      {
        status,
        frames,
        segments,
        errors,
        missing,
        method:
          "Actual native keyboard/UI and CDP compositor frames at original timestamps, physical-distance paths, no teleport/pose injection/retiming; cloud capture overhead is not hardware FPS.",
      },
      null,
      2,
    ),
  );
  await b.close();
}
console.log(
  JSON.stringify({ status, frames: frames.length, seconds: frames.at(-1)?.at }),
);
