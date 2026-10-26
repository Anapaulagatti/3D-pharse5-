import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const p = await b.newPage({ viewport: { width: 1280, height: 1000 } });
const errors = [];
p.on("pageerror", (e) => errors.push(e.message));
p.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
try {
  await p.goto("http://127.0.0.1:4294/");
  await p
    .getByText("PLAY continuous full-world prototype", { exact: true })
    .click();
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  const before = await p.evaluate(() => window.__GATE3__);
  await p.keyboard.down("s");
  await p.waitForTimeout(500);
  await p.keyboard.up("s");
  const after = await p.evaluate(() => window.__GATE3__);
  if (after.y <= before.y) throw Error("Extracted package movement failed");
  await p.goto("http://127.0.0.1:4294/docs/gate3-world/VISUAL_REVIEW.html");
  await p.evaluate(
    async () =>
      await Promise.all(
        Array.from(document.images).map(async (i) => {
          const image = new Image();
          image.src = i.src;
          await image.decode();
        }),
      ),
  );
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    "docs/gate3-world/package-smoke.json",
    JSON.stringify(
      {
        status: "PASS",
        extractedZIP: true,
        actualMovement: { from: [before.x, before.y], to: [after.x, after.y] },
        galleryAllLocalPreviewsLoaded: true,
        errors,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  console.log("PASS extracted ZIP movement, gallery and assets");
} finally {
  await b.close();
}
