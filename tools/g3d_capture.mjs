import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-recovery",
  rows = [],
  errors = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  for (const scene of ["recovery-before", "recovery-pilots"])
    for (const entry of ["north", "south", "namsan", "station"]) {
      await p.goto(
        `http://127.0.0.1:4295/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit`,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      await p.waitForTimeout(400);
      const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      const name = `${entry}-${scene === "recovery-before" ? "before" : "candidate"}-native`;
      await fs.writeFile(
        `${D}/${name}.png`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      rows.push({
        name,
        audit: a,
        state: await p.evaluate(() => window.__GATE3__),
      });
      console.log(name);
    }
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser POST_RENDER, matching cameras and Juni spawn,1280x900 backing, zoom1,DPR1, unscaled native screenshots",
        rows,
        errors,
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join("\n"));
} finally {
  await b.close();
}
