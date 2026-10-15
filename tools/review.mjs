import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
const out = process.env.REVIEW_DIR ?? ".cache/review/render";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const page = await browser.newPage({
  viewport: { width: 1440, height: 1100 },
  reducedMotion: "reduce",
});
const errors = [],
  missing = [],
  samples = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("response", (r) => {
  if (r.status() >= 400) missing.push(r.url());
});
async function sample(name) {
  const f = await page.evaluate(() => window.__PIXEL_METRICS__.frameCount);
  await page.waitForFunction(
    (n) => window.__PIXEL_METRICS__.frameCount > n + 3,
    f,
  );
  await page.locator("canvas").screenshot({ path: `${out}/${name}.png` });
  samples.push({
    file: name + ".png",
    metrics: await page.evaluate(() => window.__PIXEL_METRICS__),
  });
}
try {
  await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
  await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  await sample("town");
  // Frame the group at3x by walking, never injecting a position/camera pose.
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction(() => window.__PIXEL_METRICS__.y >= 605);
  await page.keyboard.up("ArrowDown");
  await page.waitForFunction(() =>
    window.__PIXEL_METRICS__.frame.startsWith("idle-"),
  );
  await page.locator("#zoom").selectOption("3");
  await page.waitForFunction(() => window.__PIXEL_METRICS__.cameraZoom === 3);
  await sample("characters");
  for (const hair of ["0", "1"])
    for (const outfit of ["0", "1"]) {
      await page.locator("#hair").selectOption(hair);
      await page.locator("#outfit").selectOption(outfit);
      await sample(`outfit-${hair}-${outfit}`);
    }
  await page.locator("#hair").selectOption("0");
  await page.locator("#outfit").selectOption("0");
  for (const [dr, key] of [
    ["down", "ArrowDown"],
    ["up", "ArrowUp"],
    ["left", "ArrowLeft"],
    ["right", "ArrowRight"],
  ]) {
    await page.locator("canvas").focus();
    await page.keyboard.down(key);
    await page.waitForFunction(
      (d) =>
        window.__PIXEL_METRICS__.direction === d &&
        window.__PIXEL_METRICS__.moving,
      dr,
    );
    await page.keyboard.up(key);
    await page.waitForFunction(
      (d) => window.__PIXEL_METRICS__.frame === `idle-${d}-0`,
      dr,
    );
    await sample("hero-" + dr);
  }
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowDown");
  await page.waitForFunction(
    () =>
      window.__PIXEL_METRICS__.direction === "down" &&
      window.__PIXEL_METRICS__.moving,
  );
  await page.keyboard.up("ArrowDown");
  await page.waitForFunction(
    () => window.__PIXEL_METRICS__.frame === "idle-down-0",
  );
  for (const mood of ["neutral", "happy", "focused", "surprised"]) {
    await page.locator("#expression").selectOption(mood);
    await page.waitForFunction(
      (e) => window.__PIXEL_METRICS__.expression === e,
      mood,
    );
    await sample("expression-" + mood);
  }
  await page.locator("#expression").selectOption("neutral");
  for (const id of ["sejong", "jang", "saimdang", "yi"]) {
    await page.locator(`[data-guest="${id}"]`).click();
    await page.waitForFunction((id) => {
      const g = window.__PIXEL_METRICS__.guests.find((g) => g.id === id);
      return g.frame.startsWith("wave-") && +g.frame.split("-").at(-1) >= 2;
    }, id);
    await page.locator("#pause").click();
    await page.waitForFunction(() => window.__PIXEL_METRICS__.paused);
    await sample("greeting-" + id);
    await page.locator("#close-dialog").click();
    await page.locator("#pause").click();
    await page.waitForFunction(
      (id) =>
        window.__PIXEL_METRICS__.guests
          .find((g) => g.id === id)
          .frame.startsWith("idle-"),
      id,
    );
  }
  const mobile = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  await mobile.goto("http://127.0.0.1:4201/3D-pharse5-/");
  await mobile.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
  await mobile.screenshot({ path: out + "/mobile.png", fullPage: true });
  await mobile.close();
  writeFileSync(
    out + "/samples.json",
    JSON.stringify(
      { status: "CAPTURED_FOR_VISUAL_INSPECTION", samples, errors, missing },
      null,
      2,
    ),
  );
  if (errors.length || missing.length)
    throw Error(JSON.stringify({ errors, missing }));
} finally {
  await browser.close();
}
