import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [],
  errors = [];
try {
  for (const renderer of ["auto", "canvas"]) {
    const p = await b.newPage({
      viewport: { width: 1281, height: 1001 },
      deviceScaleFactor: 1,
    });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
    });
    await p.goto(
      `http://127.0.0.1:4282/gate3-review.html?scene=district&entry=alley&renderer=${renderer}&pixelAudit`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    const first = await p.evaluate(() => window.__GATE3__.x);
    await p.keyboard.down("a");
    await p.waitForTimeout(450);
    const moving = await p.evaluate(() => window.__GATE3__.x);
    await p.keyboard.up("a");
    if (moving >= first) throw Error("WASD did not move Juni");
    const audit = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    delete audit.png;
    const rect = await p.locator("canvas").boundingBox();
    if (![rect.x, rect.y].every(Number.isInteger))
      throw Error("Fractional canvas CSS origin");
    if (renderer === "canvas" && audit.camera.roundPixels !== false)
      throw Error("Canvas destination expansion guard missing");
    await p.locator("#scenic").click();
    await p.mouse.move(420, 195);
    await p.mouse.wheel(0, 100);
    await p.waitForTimeout(200);
    const scenic = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    delete scenic.png;
    if (scenic.camera.zoom !== 0.5) throw Error("Scenic zoom policy changed");
    rows.push({
      renderer,
      startX: first,
      movingX: moving,
      rect,
      camera: audit.camera,
      scenicCamera: scenic.camera,
      status: "PASS",
    });
    await p.close();
  }
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    "docs/gate3a-pixel-audit/package-smoke.json",
    JSON.stringify(
      { status: "PASS", rows, errors, physicalDeviceResult: "NOT TESTED" },
      null,
      2,
    ),
  );
  console.log(
    "PASS packaged WebGL/Canvas, real WASD, odd CSS origin, scenic0.5, no page/missing-resource errors",
  );
} finally {
  await b.close();
}
