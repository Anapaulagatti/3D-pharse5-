import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state, grid, walk } from "./gate2_browser_lib.mjs";
const D = "docs/gate25-reconstruction";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const p = await b.newPage({
  viewport: { width: 844, height: 390 },
  isMobile: true,
  hasTouch: true,
});
try {
  await ready(p, "district-reconstruction");
  const g = await grid(p),
    routes = [];
  for (const target of [
    [1552, 780],
    [1998, 780],
    [2196, 796],
  ])
    routes.push(await walk(p, g, target));
  const above = await state(p);
  assert(above.behind.includes("bollard-09"));
  assert.equal(above.occluders.find((o) => o.id === "bollard-09").depth, 818);
  await p.screenshot({ path: D + "/FOREGROUND_ABOVE.png" });
  await p.keyboard.down("s");
  await p.waitForTimeout(750);
  await p.keyboard.up("s");
  const blocked = await state(p);
  assert(blocked.y < 810 && blocked.y >= above.y);
  await p.keyboard.down("w");
  await p.waitForTimeout(160);
  await p.keyboard.up("w");
  routes.push(await walk(p, g, [2236, 844]));
  routes.push(await walk(p, g, [2196, 844]));
  const below = await state(p);
  assert(below.y > 818);
  assert(!below.behind.includes("bollard-09"));
  await p.screenshot({ path: D + "/FOREGROUND_BELOW.png" });
  await fs.writeFile(
    D + "/foreground-qa.json",
    JSON.stringify(
      {
        normalEntry: true,
        noQaPlacement: true,
        actualKeyboardInput: true,
        routes,
        above,
        blocked,
        below,
        footCollisionPass: true,
        sortThresholdPass: true,
        note: "Rendered screenshots provided for human inspection; state assertions alone do not approve visual occlusion.",
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "PASS real-input foreground above/below / foot collision / opaque depth",
  );
} finally {
  await b.close();
}
