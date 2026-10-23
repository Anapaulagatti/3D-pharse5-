import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const errors = [],
  rows = [];
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
  for (const scene of ["recovery-pilots", "recovery-before"])
    for (const entry of ["north", "south", "namsan"]) {
      await p.goto(
        `http://127.0.0.1:4296/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit&pilotsOnly`,
      );
      await p.waitForFunction(
        () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      delete a.png;
      const options = await p
        .locator("#scene-picker option")
        .evaluateAll((v) => v.map((x) => x.value));
      rows.push({
        scene,
        entry,
        state: await p.evaluate(() => window.__GATE3__),
        audit: a,
        options,
      });
      if (options.join(",") !== "recovery-pilots,recovery-before,production")
        throw Error("Package selector exposes missing history scenes");
      console.log("ZIP", scene, entry, "ready");
    }
  await p.goto("http://127.0.0.1:4296/docs/gate3-recovery/VISUAL_REVIEW.html");
  await p.waitForLoadState("networkidle");
  const images = await p
    .locator("img")
    .evaluateAll((v) => v.every((i) => i.complete && i.naturalWidth > 0));
  if (!images) throw Error("Gallery image missing");
  await fs.writeFile(
    "docs/gate3-recovery/package-smoke.json",
    JSON.stringify(
      {
        method:
          "Extracted ZIP served locally; actual bundled Phaser runtime, six native scene loads, limited selector and gallery",
        rows,
        errors,
        galleryImages: images,
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join("\n"));
} finally {
  await b.close();
}
