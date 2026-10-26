/* global setInterval, clearInterval */
import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase1b",
  base = "http://127.0.0.1:4320/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const errors = [],
  rows = [],
  shots = [],
  switches = [];
const ctx = await browser.newContext({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
  recordVideo: {
    dir: "/tmp/phase1b-video",
    size: { width: 1280, height: 1000 },
  },
});
const p = await ctx.newPage();
p.on("pageerror", (e) => errors.push(e.message));
async function ready() {
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
}
async function shot(name, prefix) {
  const q = await p.evaluate(
    (prefix) =>
      prefix
        ? window.__GATE3_PIXEL_POSE__(prefix, 4000)
        : window.__GATE3_PIXEL_AUDIT__(),
    prefix,
  );
  if (prefix && !q.matched)
    throw Error(
      "Unobserved " +
        prefix +
        " state=" +
        JSON.stringify(await p.evaluate(() => window.__GATE3__)),
    );
  await fs.writeFile(
    `${D}/${name}-native-1x.png`,
    Buffer.from(q.png.split(",")[1], "base64"),
  );
  delete q.png;
  shots.push({ name, ...q });
  return q;
}
async function switchTo(id, first = false) {
  if (!first) {
    if (!(await p.locator("#character-open").isVisible()))
      await p.locator("#settings summary").click();
    await p.locator("#character-open").click();
  }
  await p.locator(`[data-character="${id}"]`).click();
  await p.locator('[data-action="walk"]').click();
  await p.waitForTimeout(500);
  await p.screenshot({
    path: `${D}/selection-${id}-desktop.jpg`,
    type: "jpeg",
    quality: 82,
  });
  const before = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
  }));
  await p.locator("#character-confirm").click();
  await p.locator("#character-selection").waitFor({ state: "hidden" });
  await ready();
  await p.waitForFunction((id) => window.__GATE3__.characterId === id, id);
  const after = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
    characterId: window.__GATE3__.characterId,
    playerSprites: window.__GATE3__.playerSprites,
  }));
  if (
    after.characterId !== id ||
    after.playerSprites !== 1 ||
    before.x !== after.x ||
    before.y !== after.y ||
    JSON.stringify(before.visited) !== JSON.stringify(after.visited)
  )
    throw Error("Switch state loss");
  switches.push({ id, before, after });
  if (await p.locator("#settings[open]").count())
    await p.locator("#settings summary").click();
}
try {
  await p.goto(base + "?renderer=canvas&pixelAudit&entry=transition");
  await p.locator("#character-selection").waitFor();
  for (const id of ["juni", "haneul", "bomi", "minjun"]) {
    if (id !== "juni") {
      await p.goto(base + "?renderer=canvas&pixelAudit&entry=transition");
      await ready();
    }
    await switchTo(id, id === "juni");
    await p
      .locator("canvas")
      .first()
      .click({ position: { x: 640, y: 450 } });
    await p.waitForTimeout(150);
    await shot(`${id}-idle`);
    for (const running of [false, true])
      for (const [key, view] of [
        ["w", "back"],
        ["a", "left"],
        ["s", "front"],
        ["d", "right"],
      ]) {
        const prefix = `${running ? "run" : "walk"}-${view}-`;
        const before = await p.evaluate(() => window.__GATE3__);
        await p.evaluate(() => {
          window.__P1B_TRACE__ = [];
          window.__P1B_TIMER__ = setInterval(
            () =>
              window.__P1B_TRACE__.push({
                x: window.__GATE3__.x,
                y: window.__GATE3__.y,
                frame: window.__GATE3__.frame,
              }),
            16,
          );
        });
        if (running) await p.keyboard.down("Shift");
        await p.keyboard.down(key);
        await shot(`${id}-${running ? "run" : "walk"}-${view}`, prefix);
        await p.waitForTimeout(running ? 1400 : 1700);
        await p.keyboard.up(key);
        await p.keyboard.up("Shift");
        const trace = await p.evaluate(() => {
          clearInterval(window.__P1B_TIMER__);
          return window.__P1B_TRACE__;
        });
        await p.waitForTimeout(300);
        const after = await p.evaluate(() => window.__GATE3__);
        const seen = [
          ...new Set(
            trace.map((s) => s.frame).filter((f) => f.startsWith(prefix)),
          ),
        ];
        rows.push({
          id,
          action: running ? "run" : "walk",
          view,
          before: [before.x, before.y],
          after: [after.x, after.y],
          observedFrames: seen,
          trace,
        });
        console.log(id, prefix, seen.length);
      }
    for (const [key, action] of [
      ["Space", "wave"],
      ["c", "celebrate"],
    ]) {
      await p.keyboard.press(key);
      await shot(`${id}-${action}`, `${action}-front-`);
      await p.waitForFunction(() => window.__GATE3__.frame.startsWith("idle-"));
    }
  }
  // Same station view with each character; switching is real and position-stable.
  await p.goto(base + "?renderer=canvas&pixelAudit&entry=station-all");
  await ready();
  await p.keyboard.press("e");
  await p.locator("#dialog").waitFor();
  await p.locator("#close").click();
  for (const id of ["juni", "haneul", "bomi", "minjun"]) {
    await switchTo(id);
    await shot(`${id}-station-frontage`);
    for (const k of ["a", "d"]) {
      await p.keyboard.down(k);
      await p.waitForTimeout(750);
      await p.keyboard.up(k);
      await p.waitForTimeout(250);
    }
  }
  const preReload = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
  }));
  await p.reload();
  await ready();
  if ((await p.evaluate(() => window.__GATE3__.characterId)) !== "minjun")
    throw Error("Persistence lost");
  const postReload = await p.evaluate(() => ({
    x: window.__GATE3__.x,
    y: window.__GATE3__.y,
    visited: window.__GATE3__.visited,
  }));
  if (JSON.stringify(preReload) !== JSON.stringify(postReload))
    throw Error("Reload position/visited loss");
  switches.push({ reload: true, before: preReload, after: postReload });
  const video = p.video();
  await ctx.close();
  await video.saveAs(`${D}/four-character-gameplay.webm`);
  // Real mobile-browser UI + native joystick across all four. No physical-device claim.
  const mobile = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
  });
  const m = await mobile.newPage();
  await m.goto(base);
  await m.locator("#character-selection").waitFor();
  const touch = await mobile.newCDPSession(m);
  const mobileRows = [];
  for (const id of ["juni", "haneul", "bomi", "minjun"]) {
    if (id !== "juni") {
      if (!(await m.locator("#character-open").isVisible()))
        await m.locator("#settings summary").tap();
      await m.locator("#character-open").tap();
    }
    await m.locator(`[data-character="${id}"]`).tap();
    await m.locator('[data-action="walk"]').tap();
    await m.waitForTimeout(250);
    await m.screenshot({
      path: `${D}/selection-${id}-mobile-landscape.jpg`,
      type: "jpeg",
      quality: 78,
    });
    await m.locator("#character-confirm").tap();
    await m.locator("#character-selection").waitFor({ state: "hidden" });
    await m.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    if (await m.locator("#settings[open]").count())
      await m.locator("#settings summary").tap();
    const before = await m.evaluate(() => window.__GATE3__);
    const box = await m.locator("#joystick").boundingBox();
    const x = box.x + box.width / 2,
      y = box.y + box.height / 2;
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x, y, id: 1 }],
    });
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: x + box.width * 0.3, y, id: 1 }],
    });
    await m.waitForFunction((x) => window.__GATE3__.x > x + 8, before.x);
    await touch.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    const after = await m.evaluate(() => window.__GATE3__);
    if (
      after.characterId !== id ||
      after.camera.pointers !== 0 ||
      after.playerSprites !== 1
    )
      throw Error("Mobile ownership/input failure");
    mobileRows.push({
      id,
      before: [before.x, before.y],
      after: [after.x, after.y],
      pointers: after.camera.pointers,
      status: "PASS_BROWSER_EMULATION",
    });
  }
  await mobile.close();
  await fs.writeFile(
    `${D}/gameplay-evidence.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser post-render native PNGs and original controls. Each avatar direction showcase starts at the existing transition review entry via normal page navigation; station switching and the progress recording demonstrate genuine in-place swaps. No mid-route teleports, forced frames, game-time/speed or collision overrides. Browser video is separate from native pixel proof.",
        rows,
        shots,
        switches,
        mobileRows,
        errors,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join(";"));
} finally {
  await browser.close();
}
