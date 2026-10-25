import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-jeju-bridges",
  old = JSON.parse(
    await fs.readFile("assets-src/gate3/station-clean-v1/scope.json", "utf8"),
  ).legacyObjectsRemoved.map((o) => o.image);
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 2048, height: 1380 },
  deviceScaleFactor: 1,
});
const requested = [],
  errors = [];
p.on("request", (r) => requested.push(r.url()));
p.on("pageerror", (e) => errors.push(e.message));
try {
  await p.goto(
    "http://127.0.0.1:4314/gate3-review.html?entry=station-all&native&wideNative&pixelAudit",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
  const state = await p.evaluate(() => window.__GATE3__);
  if (state.scene !== "jeju-bridges-world")
    throw Error("Default not two-bridge candidate");
  if ((await p.locator("#scene-picker option").count()) !== 1)
    throw Error("Historical scenes exposed in active review");
  const forbidden = requested.filter((u) => old.some((s) => u.endsWith(s)));
  if (forbidden.length) throw Error("Legacy station texture requested");
  const tests = [];
  let loadedGroup = "station";
  for (const [name, x, y, want] of [
    ["front-entry", 2598.5, 2610, true],
    ["bridge-a-wood", 3110, 3460, true],
    ["bridge-a-mid", 3300, 3555, true],
    ["bridge-a-island", 3530, 3640, true],
    ["bridge-a-front-rail", 3300, 3598, false],
    ["bridge-a-back-rail", 3300, 3520, false],
    ["bridge-b-mid", 3300, 4020, true],
    ["bridge-b-island", 3570, 4060, true],
    ["bridge-b-front-rail", 3300, 4055, false],
    ["bridge-b-back-rail", 3300, 3980, false],
    ["former-left-planter", 2400, 2670, true],
    ["former-right-planter", 2770, 2670, true],
    ["former-potted-tree", 2920, 2680, true],
    ["formerly-blocked-strip", 2954, 2680, true],
    ["platform-floor", 2970, 2680, true],
    ["side-passage", 2930, 2500, true],
    ["station-core", 2600, 2500, false],
    ["new-west-masonry-return", 2300, 2500, false],
    ["new-east-masonry-return", 2885, 2500, false],
  ]) {
    const group = name.startsWith("bridge-a")
      ? "a"
      : name.startsWith("bridge-b")
        ? "b"
        : "station";
    if (group !== loadedGroup) {
      const entry =
        group === "station" ? "station-all" : `bridge-${group}-full`;
      await p.goto(
        `http://127.0.0.1:4314/gate3-review.html?entry=${entry}&native&pixelAudit`,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      loadedGroup = group;
    }
    const actual = await p.evaluate(
      ([x, y]) => window.__GATE3_TEST__.walkable(x, y),
      [x, y],
    );
    tests.push({
      name,
      point: [x, y],
      expected: want,
      actual,
      status: actual === want ? "PASS" : "FAIL",
    });
    if (actual !== want) throw Error(name);
  }
  await fs.writeFile(
    `${D}/collision-runtime.json`,
    JSON.stringify(
      {
        method:
          "Read-only live Phaser collision queries plus separately recorded continuous real-control route; no mutation/teleport/collision override",
        defaultScene: state.scene,
        tests,
        oldStationTextureRequests: forbidden,
        allRequestedLocalURLs: requested,
        errors,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  console.log(
    `Default approved-station/two-bridge scene PASS;${tests.length} live collision points PASS;0 legacy station requests`,
  );
} finally {
  await b.close();
}
