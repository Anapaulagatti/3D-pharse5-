import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const result = [];
try {
  for (const [name, url] of [
    ["before-approved20", "http://127.0.0.1:4498/"],
    ["after-hotfix", "http://127.0.0.1:4320/3D-pharse5-/"],
  ]) {
    const c = await b.newContext({
      viewport: { width: 960, height: 640 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    });
    await c.addInitScript(() =>
      localStorage.setItem(
        "korean-arena-player-preferences-v1",
        JSON.stringify({ version: 1, characterId: "juni" }),
      ),
    );
    const p = await c.newPage();
    await p.goto(url + "?qa&renderer=canvas&entry=transition");
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 60000 },
    );
    await p.waitForTimeout(500);
    const start = await p.evaluate(() => window.__GATE3__);
    await p.screenshot({
      path: `docs/phase3bb-hotfix/${name}-reduced-stationary.png`,
    });
    await p.keyboard.down("d");
    await p.waitForFunction((x) => window.__GATE3__.x > x + 0.01, start.x);
    const moving = await p.evaluate(() => window.__GATE3__);
    await p.screenshot({
      path: `docs/phase3bb-hotfix/${name}-reduced-moving.png`,
    });
    await p.keyboard.up("d");
    result.push({
      name,
      start: { x: start.x, y: start.y, camera: start.camera },
      moving: {
        x: moving.x,
        y: moving.y,
        frame: moving.frame,
        camera: moving.camera,
      },
    });
    await c.close();
  }
  if (result[0].moving.camera.lookAhead[0] !== 60)
    throw Error("Could not reproduce previous reduced-motion lead");
  if (result[1].moving.camera.lookAhead.some((v) => v !== 0))
    throw Error("Input-driven camera pop remains");
  await fs.writeFile(
    "docs/phase3bb-hotfix/CAMERA_REGRESSION.json",
    JSON.stringify(
      {
        status: "PASS ACTUAL PHASER BEFORE/AFTER",
        result,
        scope:
          "Reduced-motion input lead regression, not hardware frame pacing certification",
      },
      null,
      2,
    ),
  );
  console.log("PASS actual before60px/after0px camera lead");
} finally {
  await b.close();
}
