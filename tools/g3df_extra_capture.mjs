import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-alignment";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await p.goto(
    "http://127.0.0.1:4306/gate3-review.html?scene=aligned-road-proposal&entry=station-front&native&pixelAudit&worldOnly",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
  await p.waitForTimeout(300);
  const a = await p.evaluate(() =>
    window
      .__GATE3_PIXEL_AUDIT__()
      .then((a) => ({ ...a, state: window.__GATE3__ })),
  );
  await fs.writeFile(
    `${D}/station-road-proposal-native.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  await fs.writeFile(
    `${D}/station-road-proposal-audit.json`,
    JSON.stringify(a, null, 2),
  );
  console.log("Separate road proposal captured; main candidate unchanged");
} finally {
  await b.close();
}
