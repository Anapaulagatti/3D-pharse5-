import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state } from "./gate2_browser_lib.mjs";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
try {
  const p = await b.newPage({
    viewport: { width: 844, height: 390 },
    isMobile: true,
    hasTouch: true,
  });
  await ready(p, "c", "&qa");
  await p.evaluate(() => window.__GATE2_TEST__.place(675, 105));
  await p.waitForTimeout(1800);
  assert.equal(await p.evaluate(() => document.body.dataset.edgeFocus), "true");
  assert(await p.locator("#scenic").isVisible());
  await p.screenshot({ path: "docs/gate2/acceptance/MOBILE_NORTH_EDGE.png" });
  const atEdge = await state(p);
  await p.tap("#scenic");
  await p.waitForTimeout(180);
  assert.equal(
    await p.evaluate(() => document.body.dataset.edgeFocus),
    "false",
  );
  await p.tap("#return-juni");
  await p.waitForTimeout(450);
  assert.equal((await state(p)).camera.mode, "follow");
  await fs.writeFile(
    "docs/gate2/acceptance/edge-hud.json",
    JSON.stringify(
      {
        pass: true,
        atEdge,
        meaning:
          "QA placement only for northern-edge framing; HUD collapses to bottom Scenic button so it cannot cover Juni; normal movement/Run/Explore unchanged.",
      },
      null,
      2,
    ) + "\n",
  );
  console.log("PASS northern-edge HUD and return");
} finally {
  await b.close();
}
