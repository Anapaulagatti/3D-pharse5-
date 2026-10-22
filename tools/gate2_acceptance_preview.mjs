import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const rows = [];
try {
  for (const id of process.argv.slice(2).length
    ? process.argv.slice(2)
    : ["original", "station", "seam", "jeju-fit"]) {
    const p = await b.newPage();
    await p.goto(`http://127.0.0.1:4274/${id}/preview/preview.html`);
    await p.waitForFunction(() => window.__scene?.ready);
    const routes = await p.evaluate(() => window.__scene.traverseAll());
    assert.equal(routes.ok, true);
    assert(routes.results.every((r) => r.ok));
    const snapshot = await p.evaluate(() => window.__scene.snapshot());
    await fs.writeFile(
      `docs/gate2/acceptance/contracts/${id}/scene-snapshot.json`,
      JSON.stringify({ routes, snapshot }, null, 2) + "\n",
    );
    rows.push({ scene: id, routes });
    await p.close();
    console.log(id, "all routes PASS");
  }
  await fs.writeFile(
    "docs/gate2/acceptance/contracts/preview-routes.json",
    JSON.stringify(
      {
        method:
          "Unmodified Forge preview loaded via system Chromium; technical marker route checks, not Phaser artwork evidence",
        rows,
      },
      null,
      2,
    ) + "\n",
  );
} finally {
  await b.close();
}
