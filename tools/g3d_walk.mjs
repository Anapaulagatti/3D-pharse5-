import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-recovery",
  rows = [],
  errors = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const cases = [
  {
    id: "north",
    points: [
      [2280, 1110],
      [2560, 1110],
      [2560, 1050],
      [2560, 1110],
      [2280, 1110],
    ],
  },
  {
    id: "south",
    points: [
      [1128, 2690],
      [717, 2690],
      [717, 2605],
      [717, 2690],
      [1418, 2690],
      [1418, 2605],
    ],
  },
  {
    id: "namsan",
    points: [
      [1200, 3260],
      [1460, 3260],
      [950, 3260],
      [1200, 3260],
      [1200, 3245],
    ],
  },
];
try {
  for (const c of cases) {
    const ctx = await b.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
      recordVideo: {
        dir: "/tmp/g3d-video",
        size: { width: 1280, height: 1000 },
      },
    });
    const p = await ctx.newPage();
    p.on("pageerror", (e) => errors.push(e.message));
    await p.goto(
      `http://127.0.0.1:4295/gate3-review.html?scene=recovery-pilots&entry=${c.id}&pixelAudit`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    let held = null;
    const samples = [],
      legs = [];
    async function up() {
      if (held) await p.keyboard.up(held);
      held = null;
    }
    async function axis(axis, target) {
      let prior = null,
        last = Date.now(),
        end = last + 25000;
      while (Date.now() < end) {
        const s = await p.evaluate(() => window.__GATE3__);
        if (Math.abs(target - s[axis]) < 3) {
          await up();
          return;
        }
        const key =
          axis === "x" ? (target > s.x ? "d" : "a") : target > s.y ? "s" : "w";
        if (key !== held) {
          await up();
          await p.keyboard.down(key);
          held = key;
        }
        if (prior === null || Math.abs(s[axis] - prior) > 0.3) {
          last = Date.now();
          prior = s[axis];
        }
        samples.push({ x: s.x, y: s.y, camera: s.camera, chunks: s.chunks });
        if (Date.now() - last > 2200)
          throw Error(`Blocked at${s.x},${s.y}, target${axis}${target}`);
        await p.waitForTimeout(30);
      }
      throw Error("Movement timeout");
    }
    await p.keyboard.down("Shift");
    for (const [x, y] of c.points.slice(1)) {
      let fail = null;
      const start = await p.evaluate(() => ({
        x: window.__GATE3__.x,
        y: window.__GATE3__.y,
      }));
      try {
        await axis("x", x);
        await axis("y", y);
      } catch (e) {
        fail = e.message;
      }
      await up();
      const end = await p.evaluate(() => ({
        x: window.__GATE3__.x,
        y: window.__GATE3__.y,
      }));
      legs.push({
        start,
        target: [x, y],
        end,
        status: fail ? "FAIL" : "PASS_REAL_MOVEMENT",
        failure: fail,
      });
      console.log(c.id, JSON.stringify(legs.at(-1)));
      if (fail) break;
    }
    await p.keyboard.up("Shift");
    await up();
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    await fs.writeFile(
      `${D}/${c.id}-moving-native.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    const final = await p.evaluate(() => window.__GATE3__);
    const video = p.video();
    await ctx.close();
    await video.saveAs(`${D}/${c.id}-traversal.webm`);
    rows.push({
      pilot: c.id,
      legs,
      samples,
      final,
      audit: a,
      status: legs.every((l) => !l.failure)
        ? "PASS_SELECTED_FOOTPOINT_MOVEMENT"
        : "FAIL",
      limits:
        "Not whole-region navigation or49px-body clearance acceptance; inherited P1s remain.",
    });
  }
  await fs.writeFile(
    `${D}/movement-report.json`,
    JSON.stringify(
      {
        method:
          "Actual original keyboard Shift+WASD, no teleport/collision override; one initial review spawn per pilot; Follow camera active",
        rows,
        errors,
        physicalDeviceEvidence: false,
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
