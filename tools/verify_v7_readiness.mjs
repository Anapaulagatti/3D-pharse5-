import { chromium } from "playwright";
import fs from "node:fs/promises";
const errors = [],
  external = [];
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1140 },
    reducedMotion: "reduce",
  });
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  page.on("request", (r) => {
    if (
      /^https?:/.test(r.url()) &&
      new URL(r.url()).origin !== "http://127.0.0.1:4201"
    )
      external.push(r.url());
  });
  const response = await page.goto(
    "http://127.0.0.1:4201/3D-pharse5-/v7-world-review.html",
  );
  await page.waitForFunction(
    () =>
      window.__SEOUL__?.ready && window.__V3_WORLD__?.candidate === "v7-world",
  );
  const before = await page.evaluate(() => ({
    world: window.__FULL_WORLD__,
    scene: window.__SEOUL__,
    metrics: window.__PIXEL_METRICS__,
    qa: !!window.__SEOUL_TEST__,
    canvas: [
      document.querySelector("canvas").width,
      document.querySelector("canvas").height,
    ],
  }));
  if (
    response.status() !== 200 ||
    before.qa ||
    before.scene.totalProps !== 475 ||
    before.metrics.animationFrames !== 144 ||
    before.world.world.join(",") !== "4352,5312" ||
    before.canvas.join(",") !== "1024,768"
  )
    throw Error("Normal-entry readiness mismatch " + JSON.stringify(before));
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForTimeout(1000);
  await page.keyboard.up("ArrowDown");
  const after = await page.evaluate(() => window.__SEOUL__);
  if (
    Math.hypot(after.x - before.scene.x, after.y - before.scene.y) <= 1 ||
    errors.length ||
    external.length
  )
    throw Error(
      "Normal entry movement/resource error " +
        JSON.stringify({ before, after, errors, external }),
    );
  const result = {
    status: "PASS",
    method:
      "Actual production normal V7 entry, no QA query/hook, HTTP200, Phaser canvas/world/475props/144frames and real keyboard movement; no errors/external requests. Not a public cloud preview link.",
    before,
    after,
    errors,
    external,
  };
  await fs.mkdir(".cache/v7-world", { recursive: true });
  await fs.writeFile(
    ".cache/v7-world/normal-readiness.json",
    JSON.stringify(result, null, 2) + "\n",
  );
  console.log(
    JSON.stringify({
      status: result.status,
      HTTP: response.status(),
      world: before.world.world,
      props: before.scene.totalProps,
      frames: before.metrics.animationFrames,
      qa: before.qa,
      canvas: before.canvas,
      moved: Math.hypot(after.x - before.scene.x, after.y - before.scene.y),
      errors,
      external,
    }),
  );
} finally {
  await browser.close();
}
