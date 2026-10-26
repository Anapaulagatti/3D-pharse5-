/* global setInterval, clearInterval */
import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase1",
  rows = [],
  errors = [],
  samples = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const c = await b.newContext({
  viewport: { width: 1280, height: 900 },
  deviceScaleFactor: 1,
  hasTouch: true,
  recordVideo: {
    dir: "/tmp/phase1-videos",
    size: { width: 1280, height: 900 },
  },
});
const p = await c.newPage();
p.on("pageerror", (e) => errors.push(e.message));
async function capture(name, prefix) {
  const a = await p.evaluate(
    (prefix) =>
      prefix
        ? window.__GATE3_PIXEL_POSE__(prefix, 4000)
        : window.__GATE3_PIXEL_AUDIT__(),
    prefix,
  );
  if (prefix && !a.matched) throw Error("Native pose not observed: " + prefix);
  await fs.writeFile(
    `${D}/${name}-native-1x.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  return a;
}
try {
  await p.goto(
    "http://127.0.0.1:4320/3D-pharse5-/?pixelAudit&entry=palace-axis-local",
  );
  await p.locator("#character-selection").waitFor();
  await p.waitForTimeout(700);
  for (const id of ["haneul", "bomi", "minjun"]) {
    await p.locator(`[data-character="${id}"]`).click();
    if (!(await p.locator("#character-confirm").isDisabled()))
      throw Error("Incomplete art became playable");
    await p.waitForTimeout(450);
  }
  await p.locator('[data-character="juni"]').click();
  await p.locator('[data-action="walk"]').click();
  await p.waitForTimeout(700);
  await p.locator("#character-confirm").click();
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
  for (const running of [false, true])
    for (const [key, view] of [
      ["w", "back"],
      ["a", "left"],
      ["s", "front"],
      ["d", "right"],
    ]) {
      const before = await p.evaluate(() => window.__GATE3__);
      if (running) await p.keyboard.down("Shift");
      await p.keyboard.down(key);
      const seen = new Set();
      await p.evaluate(() => {
        window.__PHASE1_FRAME_TRACE__ = [];
        window.__PHASE1_TRACE_TIMER__ = setInterval(
          () => window.__PHASE1_FRAME_TRACE__.push(window.__GATE3__?.frame),
          20,
        );
      });
      let pose;
      const end = Date.now() + 1600;
      while (Date.now() < end) {
        const s = await p.evaluate(() => window.__GATE3__);
        samples.push({ x: s.x, y: s.y, frame: s.frame, ready: s.ready });
        seen.add(s.frame);
        if (!pose && s.frame.startsWith(`${running ? "run" : "walk"}-${view}-`))
          pose = await capture(
            `${running ? "run" : "walk"}-${view}`,
            `${running ? "run" : "walk"}-${view}-`,
          );
        await p.waitForTimeout(20);
      }
      const browserFrames = await p.evaluate(() => {
        clearInterval(window.__PHASE1_TRACE_TIMER__);
        return window.__PHASE1_FRAME_TRACE__;
      });
      for (const f of browserFrames) if (f) seen.add(f);
      await p.keyboard.up(key);
      await p.keyboard.up("Shift");
      await p.waitForTimeout(350);
      const after = await p.evaluate(() => window.__GATE3__);
      rows.push({
        action: running ? "run" : "walk",
        view,
        before: { x: before.x, y: before.y },
        after: { x: after.x, y: after.y },
        gaitFramesObserved: [...seen].filter((f) =>
          f.startsWith(`${running ? "run" : "walk"}-${view}-`),
        ),
        pose,
      });
      console.log(
        running ? "run" : "walk",
        view,
        rows.at(-1).gaitFramesObserved.length,
      );
    }
  for (const [key, prefix] of [
    ["Space", "wave-front-"],
    ["c", "celebrate-front-"],
  ]) {
    await p.keyboard.press(key);
    const pose = await capture(prefix.split("-")[0], prefix);
    rows.push({ emote: prefix, pose });
    await p.waitForFunction(() => window.__GATE3__.frame.startsWith("idle-"));
  }
  await p.keyboard.press("e");
  await p.locator("#dialog").waitFor();
  await p.locator("#close").click();
  const before = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
  }));
  await p.locator("#settings summary").click();
  await p.locator("#character-open").click();
  await p.waitForTimeout(400);
  await p.locator('[data-character="bomi"]').click();
  await p.waitForTimeout(400);
  await p.locator('[data-character="juni"]').click();
  await p.locator("#character-confirm").click();
  const after = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
  }));
  if (JSON.stringify(before) !== JSON.stringify(after))
    throw Error("Selection return changed player state");
  const final = await p.evaluate(() => window.__GATE3__);
  if (final.playerSprites !== 1) throw Error("Duplicate player sprite");
  await capture("juni-after-settings");
  await fs.writeFile(
    `${D}/input-gameplay.json`,
    JSON.stringify(
      {
        method:
          "Actual original WASD/Shift, Space,C,E plus real UI. No forced frames, positions, timers/speed/collision overrides. Only Juni complete; three new identities explicitly unavailable, not a different-avatar switching demonstration.",
        rows,
        samples,
        settingsRoundTrip: { before, after },
        errors,
        final,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  const video = p.video();
  await c.close();
  await video.saveAs(`${D}/selection-juni-gameplay.webm`);
} finally {
  await b.close();
}
