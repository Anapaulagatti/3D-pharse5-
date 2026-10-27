import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2b-motion",
  rows = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  for (const id of ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"]) {
    const c = await b.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
    });
    await c.addInitScript(
      (id) =>
        localStorage.setItem(
          "korean-arena-player-preferences-v1",
          JSON.stringify({ version: 1, characterId: id }),
        ),
      id,
    );
    const p = await c.newPage(),
      errors = [];
    p.on("pageerror", (e) => errors.push(e.message));
    await p.goto(
      "http://127.0.0.1:4351/?native&renderer=canvas&pixelAudit&entry=transition",
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.locator("#stage canvas").click({ position: { x: 640, y: 450 } });
    const start = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
      id: window.__GATE3__.characterId,
    }));
    if (start.id !== id) throw Error("Package identity");
    const posePromise = p.evaluate(() =>
      window.__GATE3_PIXEL_POSE__("walk-right-0", 6000),
    );
    await p.keyboard.down("d");
    const pose = await posePromise;
    if (!pose.matched) throw Error("No native pose");
    await fs.writeFile(
      `${D}/${id}-extracted-package-native.png`,
      Buffer.from(pose.png.split(",")[1], "base64"),
    );
    delete pose.png;
    await p.waitForFunction((x) => window.__GATE3__.x > x + 44 * 3.2, start.x);
    await p.keyboard.up("d");
    await p.waitForFunction(() =>
      window.__GATE3__.frame.startsWith("idle-right-"),
    );
    const end = await p.evaluate(() => ({
      x: window.__GATE3__.x,
      y: window.__GATE3__.y,
      players: window.__GATE3__.playerSprites,
      id: window.__GATE3__.characterId,
    }));
    if (end.x <= start.x + 44 * 3 || end.players !== 1 || errors.length)
      throw Error("Package traversal/actor error");
    rows.push({
      id,
      start,
      end,
      pose,
      errors,
      method:
        "Actual independently extracted ZIP, real right input, normal speed, native POST_RENDER readback; no dev server or forced pose",
    });
    await c.close();
    console.log(id, "package positiveX, native pose, single player, stop");
  }
  await fs.writeFile(
    `${D}/package-motion-native.json`,
    JSON.stringify(rows, null, 2),
  );
} finally {
  await b.close();
}
