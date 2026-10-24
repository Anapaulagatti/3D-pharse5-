import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-residual",
  rows = [],
  errors = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const ctx = await b.newContext({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
  recordVideo: {
    dir: "/tmp/g3de-gate-video",
    size: { width: 1280, height: 1000 },
  },
});
const p = await ctx.newPage();
p.on("pageerror", (e) => errors.push(e.message));
try {
  for (const [scene, entry, key, axis, target, expected] of [
    [
      "residual-world",
      "archive-corridor",
      "w",
      "y",
      923,
      "CURRENT_WALL_BLOCKS",
    ],
    [
      "residual-gate-proposal",
      "archive-corridor",
      "w",
      "y",
      923,
      "PROPOSAL_GATE_REACHES_THRESHOLD",
    ],
    [
      "residual-world",
      "rail-coast",
      "a",
      "x",
      2930,
      "CURRENT_PLATFORM_STRIP_BLOCKS",
    ],
  ]) {
    await p.goto(
      `http://127.0.0.1:4308/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit&worldOnly`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    const start = await p.evaluate(() => window.__GATE3__);
    let last = start[axis],
      lastMove = Date.now();
    const samples = [];
    await p.keyboard.down(key);
    const deadline = Date.now() + 20000;
    while (Date.now() < deadline) {
      const s = await p.evaluate(() => window.__GATE3__);
      samples.push({ t: Date.now(), x: s.x, y: s.y, frame: s.frame });
      if (Math.abs(s[axis] - last) > 0.1) {
        last = s[axis];
        lastMove = Date.now();
      }
      if (s[axis] <= target + 1 || Date.now() - lastMove > 1600) break;
      await p.waitForTimeout(50);
    }
    await p.keyboard.up(key);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    const name = expected.toLowerCase();
    await fs.writeFile(
      `${D}/${name}-native.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    await fs.writeFile(`${D}/${name}-audit.json`, JSON.stringify(a, null, 2));
    const end = a.state;
    const ok = expected.startsWith("PROPOSAL")
      ? end.y <= 924
      : expected.includes("WALL")
        ? end.y >= 1064 && end.y <= 1067
        : Math.round(end.x) >= 2958 && Math.round(end.x) <= 2961;
    rows.push({
      scene,
      entry,
      expected,
      start: { x: start.x, y: start.y },
      end: { x: end.x, y: end.y },
      result: ok ? "PASS_EXPECTED_BEHAVIOR" : "FAIL",
      samples,
    });
    console.log(expected, rows.at(-1).result, end.x, end.y);
  }
  const video = p.video();
  await ctx.close();
  await video.saveAs(`${D}/gate-comparison.webm`);
  await fs.writeFile(
    `${D}/gate-movement.json`,
    JSON.stringify(
      {
        method:
          "Three explicitly separate review scenes, real held keyboard input, actual collision.88px gate is proposal-only; no live masterplan/collision amendment. Scene reload is declared, not a continuous world route.",
        rows,
        errors,
        artAcceptance: "PENDING HUMAN",
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  if (errors.length || rows.some((r) => r.result === "FAIL"))
    throw Error("Gate/strip actual movement failed");
} finally {
  await b.close();
}
