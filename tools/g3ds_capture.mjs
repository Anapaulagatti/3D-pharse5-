import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/gate3-final";
const prior =
  process.env.PHASE === "after" || process.env.UPDATE_ENTRIES
    ? JSON.parse(await fs.readFile(`${D}/native-captures.json`, "utf8")).rows
    : [];
const updating = process.env.UPDATE_ENTRIES?.split(",");
const rows = updating
  ? prior.filter((r) => r.phase === "before" || !updating.includes(r.entry))
  : process.env.PHASE === "after"
    ? prior.filter((r) => r.phase === "before")
    : [];
const errors = [];
const entries = [
  "farm",
  "western-house",
  "western-courtyard",
  "house-court",
  "station-precinct",
  "station-upper",
  "station-front",
  "station-right",
  "bridge-mainland",
  "bridge-island",
  "bridge-full",
  "coast-middle",
  "palace-entrance",
  "retail-block",
];
const scenes =
  process.env.PHASE === "before"
    ? ["final-before"]
    : process.env.PHASE === "after"
      ? ["final-world", "final-station-candidate", "final-station-ground"]
      : ["final-before", "final-world", "final-station-candidate"];
const cases = scenes.flatMap((scene) =>
  entries
    .filter(
      (entry) =>
        !scene.startsWith("final-station-") || entry.startsWith("station-"),
    )
    .map((entry) => ({
      scene,
      entry,
      phase:
        scene === "final-before"
          ? "before"
          : scene === "final-world"
            ? "after"
            : scene === "final-station-candidate"
              ? "station-candidate"
              : "station-ground",
    })),
);
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
  for (const { scene, entry, phase } of cases) {
    if (
      process.env.UPDATE_ENTRIES &&
      (phase === "before" ||
        !process.env.UPDATE_ENTRIES.split(",").includes(entry))
    )
      continue;
    const wide = ["house-court", "station-precinct", "retail-block"].includes(
      entry,
    );
    await p.setViewportSize(
      wide ? { width: 2048, height: 1380 } : { width: 1280, height: 1000 },
    );
    await p.goto(
      `http://127.0.0.1:4310/gate3-review.html?scene=${scene}&entry=${entry}&native&pixelAudit${wide ? "&wideNative" : ""}`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    await p.waitForTimeout(200);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    const name = `${entry}-${phase}-native`;
    await fs.writeFile(
      `${D}/${name}.png`,
      Buffer.from(a.png.split(",")[1], "base64"),
    );
    delete a.png;
    const state = a.state;
    delete a.state;
    rows.push({ name, scene, entry, phase, wide, audit: a, state });
    console.log(name);
  }
  await p.setViewportSize({ width: 1280, height: 1000 });
  for (const scene of scenes) {
    await p.goto(
      `http://127.0.0.1:4310/gate3-review.html?scene=${scene}&pixelAudit`,
    );
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    await p.locator("#scenic").click();
    await p.locator("#overview-mode").click();
    await p.waitForFunction(() => window.__GATE3__.camera.mode === "overview");
    await p.waitForTimeout(200);
    const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
    const phase =
      scene === "final-before"
        ? "before"
        : scene === "final-world"
          ? "after"
          : scene === "final-station-candidate"
            ? "station-candidate"
            : "station-ground";
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
          "Actual native Phaser POST_RENDER, DPR1, zoom1, integer camera, nearest sampling.2048x1280 full diagnostic frames or1280x900 detail; identical-camera BEFORE/AFTER. Proposals explicitly isolated. Overview is scaled context only.",
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
