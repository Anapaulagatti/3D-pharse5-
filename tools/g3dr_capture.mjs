import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-reconciliation",
  rows = process.env.AFTER_ONLY
    ? JSON.parse(
        await fs.readFile(`${D}/native-captures.json`, "utf8"),
      ).rows.filter((r) => r.name.includes("-before-native"))
    : [],
  errors = [];
const entries = [
  "palace-compound",
  "palace-court",
  "palace-west",
  "palace-east",
  "station-precinct",
  "station-rear",
  "station-left",
  "station-right",
  "station-forecourt",
  "station-amusement",
  "modern",
  "jeju-bridge",
  "jeju-offshore",
  "jeju-south",
];
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
  for (const scene of [
    "reconciled-before",
    "reconciled-world",
    "reconciled-palace-proposal",
  ]) {
    if (process.env.AFTER_ONLY && scene === "reconciled-before") continue;
    for (const entry of scene.endsWith("proposal")
      ? ["palace-compound", "palace-court"]
      : entries) {
      const wide = ["palace-compound", "station-precinct"].includes(entry);
      await p.setViewportSize(
        wide ? { width: 2048, height: 1380 } : { width: 1280, height: 1000 },
      );
      await p.goto(
        `http://127.0.0.1:4304/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit${wide ? "&wideNative" : ""}`,
      );
      await p.waitForFunction(
        () =>
          window.__GATE3__?.chunks.resident > 0 &&
          window.__GATE3__.chunks.inflight === 0,
        {},
        { timeout: 45000 },
      );
      await p.waitForTimeout(250);
      const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
      const phase = scene.endsWith("proposal")
          ? "proposal"
          : scene.endsWith("before")
            ? "before"
            : "after",
        name = `${entry}-${phase}-native`;
      await fs.writeFile(
        `${D}/${name}.png`,
        Buffer.from(a.png.split(",")[1], "base64"),
      );
      delete a.png;
      rows.push({
        name,
        scene,
        entry,
        wide,
        audit: a,
        state: await p.evaluate(() => window.__GATE3__),
      });
      console.log(name);
    }
  }
  await p.setViewportSize({ width: 1280, height: 1000 });
  for (const scene of ["reconciled-before", "reconciled-world"]) {
    await p.goto(
      `http://127.0.0.1:4304/gate3-review.html?scene=${scene}&pixelAudit`,
    );
    await p.waitForFunction(
      () =>
        window.__GATE3__?.chunks.resident > 0 &&
        window.__GATE3__.chunks.inflight === 0,
    );
    await p.locator("#scenic").click();
    await p.locator("#overview-mode").click();
    await p.waitForFunction(() => window.__GATE3__.camera.mode === "overview");
    await p.waitForTimeout(300);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    const phase = scene.endsWith("before") ? "before" : "after";
    await fs.writeFile(
      `${D}/world-${phase}-overview-phaser.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    await fs.writeFile(
      `${D}/overview-${phase}-audit.json`,
      JSON.stringify(a, null, 2),
    );
  }
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        method:
          "Genuine Phaser POST_RENDER;1:1 native backing and nearest sampling.2048x1280 diagnostic viewport for full palace/station;1280x900 detail frames. Overview is separately scaled, not pixel proof.",
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
