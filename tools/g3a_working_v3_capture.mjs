import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/g3a-controlled-finalization",
  errors = [],
  rows = [],
  walk = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
async function load(p, scene, entry, native = true) {
  await p.goto(
    `http://127.0.0.1:4289/gate3-review.html?scene=${scene}&entry=${entry}&pixelAudit${native ? "&native" : ""}`,
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
}
async function shot(p, name) {
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    `${D}/${name}.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  rows.push({
    name,
    audit: a,
    state: await p.evaluate(() => window.__GATE3__),
  });
}
async function move(p, key, target, axis, less = false) {
  await p.keyboard.down(key);
  const end = Date.now() + 14000;
  while (true) {
    const s = await p.evaluate(() => window.__GATE3__);
    walk.push({ key, x: s.x, y: s.y, t: Date.now() });
    if (less ? s[axis] <= target : s[axis] >= target) break;
    if (Date.now() > end) throw Error(`Blocked ${key} ${JSON.stringify(s)}`);
    await p.waitForTimeout(35);
  }
  await p.keyboard.up(key);
}
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  for (const [scene, phase] of [
    ["registration-review", "before"],
    ["registration-working-v3", "after"],
  ]) {
    await load(p, scene, "station");
    await shot(p, `${phase}-station-juni-native`);
    await move(p, "s", 2855, "y");
    await shot(p, `${phase}-station-native`);
  }
  for (const entry of ["convenience", "retail", "namsan", "waterfront"]) {
    await load(p, "registration-working-v3", entry);
    await shot(p, `${entry}-native`);
  }
  await load(p, "registration-working-v3", "convenience");
  await move(p, "w", 3343, "y", true);
  await p.keyboard.press("e");
  const door = await p.locator("#dialog").isVisible();
  await fs.writeFile(
    `${D}/maru-interaction.json`,
    JSON.stringify(
      {
        at: await p.evaluate(() => ({
          x: window.__GATE3__.x,
          y: window.__GATE3__.y,
        })),
        dialogVisible: door,
        title: await p.locator("#title").textContent(),
      },
      null,
      2,
    ),
  );
  if (!door) throw Error("Maru explore failed");
  await p.close();
  const ctx = await b.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: "/tmp/g3-working-v3-video",
      size: { width: 1280, height: 900 },
    },
  });
  const v = await ctx.newPage();
  await load(v, "registration-working-v3", "platform", false);
  await shot(v, "platform-juni-native");
  await move(v, "w", 2350, "y", true);
  await shot(v, "platform-north-juni-native");
  await move(v, "s", 2550, "y");
  await move(v, "a", 2960, "x", true);
  await move(v, "w", 2530, "y", true);
  await shot(v, "platform-opening-juni-native");
  await move(v, "s", 2555, "y");
  await move(v, "d", 2980, "x");
  await move(v, "s", 2690, "y");
  const video = v.video();
  await ctx.close();
  await video.saveAs(`${D}/platform-traversal.webm`);
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        rows,
        walk,
        errors,
        method:
          "Actual Phaser POST_RENDER; native1280x900 canvas, no image scaling; actual keyboard controls only, no QA teleport",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS native frames, Maru door interaction and platform traversal",
  );
} finally {
  await b.close();
}
