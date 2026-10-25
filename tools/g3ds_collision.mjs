import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-final",
  plots = JSON.parse(await fs.readFile(`${D}/FARM_PLOTS.json`, "utf8")).plots;
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
});
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
async function load(scene, entry) {
  await p.goto(
    `http://127.0.0.1:4310/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit&worldOnly`,
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
}
try {
  await load("final-world", "farm");
  const farm = [];
  for (const q of plots) {
    const a = await p.evaluate(
      (q) => ({
        id: q.id,
        interactionWalkable: window.__GATE3_TEST__.walkable(
          ...q.interactionAnchor,
        ),
        soilWalkable: window.__GATE3_TEST__.walkable(...q.cropDisplayAnchor),
      }),
      q,
    );
    if (!a.interactionWalkable || a.soilWalkable)
      throw Error("Farm collision " + JSON.stringify(a));
    farm.push(a);
  }
  await load("final-world", "western-courtyard");
  const garden = await p.evaluate(() => ({
    publicLaneOpen: window.__GATE3_TEST__.walkable(580, 1663),
    newSupportBlocked: !window.__GATE3_TEST__.walkable(622, 1663),
  }));
  if (!garden.publicLaneOpen || !garden.newSupportBlocked)
    throw Error("Garden corner collision");
  await load("final-station-candidate", "rail-coast");
  const start = await p.evaluate(() => window.__GATE3__);
  await p.keyboard.down("a");
  const samples = [];
  let last = start.x,
    lastMove = Date.now();
  const deadline = Date.now() + 12000;
  while (Date.now() < deadline) {
    const s = await p.evaluate(() => window.__GATE3__);
    samples.push({ t: Date.now(), x: s.x, y: s.y, frame: s.frame });
    if (Math.abs(last - s.x) > 0.1) {
      last = s.x;
      lastMove = Date.now();
    }
    if (Date.now() - lastMove > 1800) break;
    await p.waitForTimeout(45);
  }
  await p.keyboard.up("a");
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    `${D}/station-platform-strip-blocked-native.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  const end = a.state;
  if (Math.round(end.x) !== 2958 || samples.some((s) => Math.round(s.x) < 2958))
    throw Error("Strip unexpected movement");
  await fs.writeFile(
    `${D}/collision-runtime.json`,
    JSON.stringify(
      {
        method:
          "Actual live Phaser .walkable readback plus real held A input until blocked; no collision override or position mutation",
        farm,
        garden,
        stationPlatform: {
          start: { x: start.x, y: start.y },
          end: { x: end.x, y: end.y },
          samples,
          expectedBlocked: true,
          actualPlatformTransfer: "FAIL / still blocked by unchanged8px strip",
          native: a,
        },
        errors,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  console.log(
    "Runtime collision PASS:6 plot anchors,6 blocked soils,garden lane/support; station platform transfer remains FAIL",
  );
} finally {
  await b.close();
}
