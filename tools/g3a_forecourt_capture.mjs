import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/g3a-forecourt-audit",
  b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
const rows = [],
  errors = [];
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  for (const [scene, renderer, targetY] of [
    ["district", "auto", 1050],
    ["district", "canvas", 1050],
    ["registration-refined", "auto", 2855],
  ]) {
    await p.goto(
      `http://127.0.0.1:4284/gate3-review.html?scene=${scene}&entry=station&native&pixelAudit&renderer=${renderer}`,
    );
    await p.waitForFunction(() => window.__GATE3__?.ready);
    await p.waitForFunction(() => window.__GATE3__.chunks.inflight === 0);
    // Move Juni out of the audited paving through ordinary controls; do not teleport or alter camera/art.
    await p.keyboard.down("s");
    const deadline = Date.now() + 8000;
    while ((await p.evaluate(() => window.__GATE3__.y)) < targetY) {
      if (Date.now() > deadline)
        throw Error("Cannot clear audit crop with normal input");
      await p.waitForTimeout(35);
    }
    await p.keyboard.up("s");
    await p.waitForTimeout(150);
    for (const phase of ["before", "after"]) {
      const result = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      const path = `${scene}-${renderer}-${phase}-native.png`;
      await fs.writeFile(
        `${D}/${path}`,
        Buffer.from(result.png.split(",")[1], "base64"),
      );
      delete result.png;
      rows.push({
        scene,
        renderer,
        phase,
        path,
        state: await p.evaluate(() => window.__GATE3__),
        audit: result,
      });
      await p.waitForTimeout(200);
    }
  }
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    `${D}/captures.json`,
    JSON.stringify(
      {
        rows,
        errors,
        note: "Before/after focused audit of unchanged renderer/art. No source repair applied or visual improvement claimed. PNGs captured directly at POST_RENDER, native1280x900. Juni moved with S key only.",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS six native Phaser frames, WebGL/Canvas, Juni outside audited zones",
  );
} finally {
  await b.close();
}
