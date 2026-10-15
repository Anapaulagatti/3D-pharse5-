import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const out = "quality-reports/unified-v4/motion";
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
  missing = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
p.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
await p.goto("http://127.0.0.1:4201/3D-pharse5-/");
await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
const cdp = await ctx.newCDPSession(p),
  frames = [],
  segments = [];
let origin,
  phase = "idle",
  accept = true;
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
  everyNthFrame: 2,
});
async function wait(n) {
  const a = await p.evaluate(() => window.__PIXEL_METRICS__);
  const start = performance.now();
  await p.waitForFunction(
    ({ f, n }) => window.__PIXEL_METRICS__.frameCount >= f + n,
    { f: a.frameCount, n },
    { timeout: 25000 },
  );
  const z = await p.evaluate(() => window.__PIXEL_METRICS__);
  segments.push({
    phase,
    start: a,
    end: z,
    wallSeconds: (performance.now() - start) / 1000,
  });
}
await p.locator("canvas").focus();
await wait(150);
for (const action of ["wave", "celebrate", "pose"]) {
  phase = action;
  await p.locator("#" + action).click();
  await wait(60);
}
phase = "outfit-change";
await p.locator("#hair").selectOption("1");
await p.locator("#outfit").selectOption("1");
await wait(35);
await p.locator("canvas").focus();
for (const action of ["walk", "run"]) {
  if (action === "run") await p.keyboard.down("Shift");
  for (const key of ["ArrowDown", "ArrowRight", "ArrowUp", "ArrowLeft"]) {
    phase = action + "-" + key.replace("Arrow", "").toLowerCase();
    await p.keyboard.down(key);
    await wait(16);
    await p.keyboard.up(key);
  }
  if (action === "run") await p.keyboard.up("Shift");
}
phase = "return-idle";
await wait(80);
accept = false;
await cdp.send("Page.stopScreencast");
writeFileSync(
  out + "/capture.json",
  JSON.stringify(
    {
      status: "CAPTURED_PENDING_DECODED_INSPECTION",
      frames,
      segments,
      errors,
      missing,
      method:
        "Native keyboard/UI and CDP compositor frames, original timestamps, no teleports/pose injection/retiming. Cloud capture overhead is not physical-device performance.",
    },
    null,
    2,
  ),
);
await b.close();
if (errors.length || missing.length)
  throw Error(JSON.stringify({ errors, missing }));
console.log(
  JSON.stringify({ frames: frames.length, seconds: frames.at(-1).at }),
);
