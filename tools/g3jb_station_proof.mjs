import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 2048, height: 1380 },
    deviceScaleFactor: 1,
  });
  await p.goto(
    "http://127.0.0.1:4314/gate3-review.html?entry=station-all&native&wideNative&pixelAudit",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    "docs/gate3-jeju-bridges/approved-hanbit-preserved-native.png",
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  await fs.writeFile(
    "docs/gate3-jeju-bridges/approved-hanbit-preserved-audit.json",
    JSON.stringify(a, null, 2),
  );
} finally {
  await b.close();
}
