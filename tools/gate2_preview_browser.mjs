import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [];
try {
  for (const id of ["a", "b", "c", "transition", "station"]) {
    const p = await b.newPage();
    await p.goto(
      `http://127.0.0.1:4268/${id === "c" ? "c-v2" : id}/preview.html`,
    );
    await p.waitForFunction(() => window.__scene?.ready);
    const routes = await p.evaluate(() => window.__scene.traverseAll());
    assert.equal(routes.ok, true);
    assert(routes.results.every((r) => r.ok));
    const snapshot = await p.evaluate(() => window.__scene.snapshot());
    await fs.mkdir(`docs/gate2/forge-preview/${id}`, { recursive: true });
    await fs.writeFile(
      `docs/gate2/forge-preview/${id}/scene-snapshot.json`,
      JSON.stringify({ routes, snapshot }, null, 2) + "\n",
    );
    await p.screenshot({
      path: `docs/gate2/forge-preview/${id}/technical-preview.png`,
    });
    rows.push({ scene: id, routes });
    console.log(id, JSON.stringify(routes));
    await p.close();
  }
  await fs.writeFile(
    "docs/gate2/preview-route-fallback.json",
    JSON.stringify(
      {
        method:
          "build_scene_preview.py --verify skipped missing bundled browser. Explicit system Chromium loaded the unmodified generated preview and ran __scene.traverseAll(); this is technical marker QA, not Phaser art evidence.",
        rows,
      },
      null,
      2,
    ) + "\n",
  );
} finally {
  await b.close();
}
