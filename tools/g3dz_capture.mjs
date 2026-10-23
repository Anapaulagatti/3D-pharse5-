import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-zoned-world",
  phase = process.env.PHASE,
  prior =
    phase === "after" || process.env.APPEND
      ? JSON.parse(await fs.readFile(`${D}/native-captures.json`, "utf8"))
      : null,
  rows = process.env.APPEND
    ? prior.rows
    : (prior?.rows.filter((r) => r.name.includes("-before-native")) ?? []),
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
  const m = JSON.parse(
    await fs.readFile("public/assets/gate3/zoned-world/manifest.json", "utf8"),
  );
  for (const scene of phase === "before"
    ? ["zoned-before"]
    : phase === "after"
      ? ["zoned-world"]
      : ["zoned-world", "zoned-before"]) {
    for (const entry of Object.keys(m.reviewEntries).sort(
      (a, b) =>
        (["jeju-bridge", "station-amusement", "urban-density"].includes(a)
          ? -1
          : 0) -
        (["jeju-bridge", "station-amusement", "urban-density"].includes(b)
          ? -1
          : 0),
    )) {
      if (
        process.env.CAPTURE_ENTRIES &&
        !process.env.CAPTURE_ENTRIES.split(",").includes(entry)
      )
        continue;
      await p.goto(
        `http://127.0.0.1:4302/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit`,
      );
      await p.waitForFunction(
        () =>
          window.__GATE3__ &&
          window.__GATE3__.chunks.resident > 0 &&
          window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      await p.waitForTimeout(250);
      const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      const name = `${entry}-${scene === "zoned-world" ? "after" : "before"}-native`;
      await fs.writeFile(
        `${D}/${name}.png`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      const previous = rows.findIndex((r) => r.name === name);
      if (previous >= 0) rows.splice(previous, 1);
      rows.push({
        name,
        audit: a,
        state: await p.evaluate(() => window.__GATE3__),
      });
      console.log(name);
    }
  }
  for (const scene of ["zoned-before", "zoned-world"]) {
    await p.goto(
      `http://127.0.0.1:4302/gate3-review.html?scene=${scene}&pixelAudit`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    );
    await p.locator("#scenic").click();
    await p.locator("#overview-mode").click();
    await p.waitForFunction(() => window.__GATE3__?.camera.mode === "overview");
    await p.waitForTimeout(500);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    await fs.writeFile(
      `${D}/world-${scene === "zoned-world" ? "after" : "before"}-overview-phaser.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    await fs.writeFile(
      `${D}/${scene}-overview-audit.json`,
      JSON.stringify(a, null, 2),
    );
  }
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser POST_RENDER. Native frames1280x900 backing, zoom1,DPR1, no screenshot resampling. Overview separately scaled, not pixel proof.",
        rows,
        overview:
          "zoned-world-overview-audit.json / zoned-before-overview-audit.json",
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
