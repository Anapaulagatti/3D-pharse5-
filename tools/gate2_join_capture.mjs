import { chromium } from "@playwright/test";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
  });
  await ready(p, "seam");
  const g = await grid(p),
    routes = [];
  for (const t of [
    [1520, 530],
    [1848, 430],
    [1288, 500],
  ])
    routes.push(await walk(p, g, t));
  const s = await state(p);
  await fs.writeFile(
    "docs/gate2/acceptance/small-join-qa.json",
    JSON.stringify({ routes, state: s }, null, 2) + "\n",
  );
  await ready(p, "seam", "&qa&native&overview");
  await p.evaluate(() => window.__GATE2_TEST__.place(1520, 530));
  await p.waitForTimeout(180);
  await capture(p, "docs/gate2/acceptance/SEAM_NATIVE_1X.png");
  console.log("PASS actual independent-asset join navigation");
} finally {
  await b.close();
}
