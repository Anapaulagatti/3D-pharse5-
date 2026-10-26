import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({
  viewport: { width: 1280, height: 1000 },
  deviceScaleFactor: 1,
});
try {
  await p.goto(
    "http://127.0.0.1:4293/gate3-review.html?scene=production&entry=transition&overview&pixelAudit",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    "docs/gate3-world/world-overview-phaser.png",
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  await fs.writeFile(
    "docs/gate3-world/overview-capture.json",
    JSON.stringify(
      {
        method:
          "Actual Phaser overview proxy rendering; overview is scaled, NOT native pixel-quality evidence",
        audit: a,
        state: await p.evaluate(() => window.__GATE3__),
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
