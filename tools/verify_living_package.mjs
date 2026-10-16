import { chromium } from "@playwright/test";
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";
const out = "docs/living-seoul",
  source = "http://127.0.0.1:4201/3D-pharse5-/",
  portable = "http://127.0.0.1:4208/3D-pharse5-/";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const errors = [],
  comparison = [],
  performance = [];
try {
  for (const mobile of [false, true]) {
    const renders = [];
    for (const base of [source, portable]) {
      const context = await browser.newContext({
        viewport: mobile
          ? { width: 390, height: 844 }
          : { width: 1440, height: 1200 },
        deviceScaleFactor: mobile ? 2 : 1,
        isMobile: mobile,
        hasTouch: mobile,
        reducedMotion: "reduce",
      });
      const page = await context.newPage();
      page.on("pageerror", (e) => errors.push(e.message));
      page.on("response", (r) => {
        if (r.status() >= 400) errors.push(r.url());
      });
      if (mobile)
        await page.addInitScript(() => {
          const original = HTMLCanvasElement.prototype.getContext;
          HTMLCanvasElement.prototype.getContext = function (type, ...args) {
            if (type.includes("webgl")) return null;
            return original.call(this, type, ...args);
          };
        });
      await page.goto(base + "district-review.html");
      await page.waitForFunction(() => window.__DISTRICT__?.ready);
      await page.waitForTimeout(250);
      const png = await page.locator("canvas").screenshot();
      renders.push(png);
      if (base === portable) {
        const p = await page.evaluate(
          () =>
            new Promise((resolve) => {
              const begin = performance.now(),
                first = window.__PIXEL_METRICS__.frameCount,
                samples = [];
              const timer = window.setInterval(
                () => samples.push(window.__PIXEL_METRICS__.fps),
                100,
              );
              setTimeout(() => {
                window.clearInterval(timer);
                resolve({
                  elapsedMs: performance.now() - begin,
                  frames: window.__PIXEL_METRICS__.frameCount - first,
                  phaserActualFpsSamples: samples,
                  renderer: window.__PIXEL_METRICS__.renderer,
                  visibleProps: window.__DISTRICT__.visibleProps,
                  totalProps: window.__DISTRICT__.totalProps,
                });
              }, 2200);
            }),
        );
        performance.push({
          viewport: mobile
            ? "390x844 DPR2 Canvas emulation"
            : "1440x1200 SwiftShader WebGL",
          ...p,
        });
      }
      if (base === portable && !mobile) {
        await page.locator("canvas").focus();
        await page.keyboard.down("Shift");
        for (const [key, field, target, positive] of [
          ["ArrowRight", "x", 1280, true],
          ["ArrowUp", "y", 544, false],
          ["ArrowRight", "x", 1536, true],
          ["ArrowUp", "y", 475, false],
        ]) {
          await page.keyboard.down(key);
          try {
            await page.waitForFunction(
              ({ field, target, positive }) =>
                positive
                  ? window.__DISTRICT__[field] >= target
                  : window.__DISTRICT__[field] <= target,
              { field, target, positive },
              { timeout: 23000 },
            );
          } finally {
            await page.keyboard.up(key);
          }
          await page.waitForTimeout(170);
        }
        await page.keyboard.up("Shift");
        await page.locator("#interact").click();
        await page.waitForFunction(() => window.__DISTRICT__?.area === "room");
        await page.waitForTimeout(250);
        await page
          .locator("canvas")
          .screenshot({ path: `${out}/package-reading-room.png` });
        await page.locator("#interact").click();
        await page.waitForFunction(
          () => window.__DISTRICT__?.area === "outdoor",
        );
        await page.goto(base);
        await page.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
        assert.equal(
          await page.evaluate(() => window.__PIXEL_METRICS__.guests.length),
          4,
        );
      }
      await context.close();
    }
    assert(
      renders[0].equals(renders[1]),
      "source vs exact extracted portable render must match",
    );
    comparison.push({
      mobile,
      sha256: createHash("sha256").update(renders[0]).digest("hex"),
      byteIdentical: true,
    });
  }
  assert.deepEqual(errors, []);
  const p = JSON.parse(readFileSync(`${out}/package.json`, "utf8"));
  p.status = "HTTP_BROWSER_VERIFIED";
  writeFileSync(`${out}/package.json`, JSON.stringify(p, null, 2) + "\n");
  writeFileSync(
    `${out}/package-verification.json`,
    JSON.stringify(
      {
        status: "PASS",
        zipSha256: p.zip_sha256,
        errors,
        comparison,
        realExtractedPackageMovement: true,
        reciprocalEntryExit: true,
        oldTownFourGuests: true,
        method:
          "Exact extracted Python launcher, real Chromium, reduced-motion deterministic canvas comparison and keyboard traversal. No public loopback link supplied to user.",
      },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(
    `${out}/performance.json`,
    JSON.stringify(
      {
        status: "MEASURED_EMULATED_ONLY",
        method:
          "2200ms wall-time/Phaser frame count + actualFps sampling, no recording, software Chromium. Stationary reduced-motion comparison; NOT representative physical mobile or worst-case exploration FPS.",
        samples: performance,
        limits: [
          "No physical phone or 60FPS guarantee",
          "Legacy hidden controller atlases retained for compatibility",
          "Outdoor repeated art shares textures; image culling uses camera bounds",
          "Only room PNGs lazy-loaded; this two-chunk proof is not a full open-world streaming engine",
        ],
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    JSON.stringify({
      status: "PASS",
      comparison,
      performance: performance.map((x) => ({
        renderer: x.renderer,
        measuredFramesPerSecond: x.frames / (x.elapsedMs / 1000),
      })),
    }),
  );
} finally {
  await browser.close();
}
