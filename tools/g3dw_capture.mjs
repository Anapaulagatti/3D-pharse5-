import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-recovery-world",
  phase = process.env.PHASE,
  prior =
    phase === "after"
      ? JSON.parse(await fs.readFile(`${D}/native-captures.json`, "utf8"))
      : null,
  rows = prior?.rows.filter((r) => r.name.includes("-before-native")) ?? [],
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
    await fs.readFile(
      "public/assets/gate3/recovery-world/manifest.json",
      "utf8",
    ),
  );
  for (const scene of phase === "before"
    ? ["recovery-world-before"]
    : phase === "after"
      ? ["recovery-world"]
      : ["recovery-world-before", "recovery-world"]) {
    for (const entry of Object.keys(m.reviewEntries)) {
      if (
        scene === "recovery-world-before" &&
        ![
          "palace",
          "academy",
          "culture",
          "transition",
          "retail",
          "bookshop-occlusion",
          "station",
          "namsan",
          "amusement",
          "market",
          "jeju-culture",
        ].includes(entry)
      )
        continue;
      await p.goto(
        `http://127.0.0.1:4297/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit`,
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
      const name = `${entry}-${scene === "recovery-world" ? "after" : "before"}-native`;
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
  }
  await p.goto(
    "http://127.0.0.1:4297/gate3-review.html?scene=recovery-world&overview&pixelAudit",
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
    `${D}/world-overview-phaser.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        method:
          "Actual Phaser POST_RENDER. Native frames1280x900 backing, zoom1,DPR1, no screenshot resampling. Overview separately scaled, not pixel proof.",
        rows,
        overview: a,
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
