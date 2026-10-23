import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const port = Number(process.env.G3_PORT || 4271),
  variant = process.env.G3_VARIANT || "optimized";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  headless: true,
  args: ["--no-sandbox"],
});
const rows = [];
const errors = [];
for (let repeat = 0; repeat < 2; repeat++)
  for (const renderer of repeat ? ["canvas", "auto"] : ["auto", "canvas"]) {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 1000 },
      deviceScaleFactor: 1,
    });
    const page = await context.newPage();
    page.on("pageerror", (e) => errors.push(e.message));
    async function open(search) {
      const t = Date.now();
      await page.goto(
        `http://127.0.0.1:${port}/gate3-review.html?profile&${variant === "baseline" ? "baseline&" : ""}renderer=${renderer}&${search}`,
      );
      await page.waitForFunction(() => window.__GATE3__?.ready);
      await page.waitForFunction(() => window.__GATE3__?.chunks.inflight === 0);
      return Date.now() - t;
    }
    async function snap(phase, extra = {}) {
      rows.push({
        repeat,
        requestedRenderer: renderer,
        phase,
        ...extra,
        ...(await page.evaluate(() => ({
          state: window.__GATE3__,
          profile: window.__GATE3_PROFILE__.snapshot(),
        }))),
      });
    }
    async function reset() {
      await page.evaluate(() => window.__GATE3_PROFILE__.reset());
    }
    const coldMs = await open("scene=district&entry=station");
    await snap("cold", { navigationToWarmMs: coldMs });
    await reset();
    await page.waitForTimeout(4000);
    await snap("warm-stationary");
    await open("scene=district&entry=alley");
    await reset();
    await page.keyboard.down("Shift");
    await page.keyboard.down("d");
    await page.waitForTimeout(6000);
    await page.keyboard.up("d");
    await page.keyboard.up("Shift");
    await snap("movement-across-chunks");
    await open("scene=world");
    await page.locator("#scenic").click();
    await page.mouse.move(500, 500);
    await page.mouse.wheel(0, 100);
    await page.waitForTimeout(500);
    await reset();
    await page.locator("#start-tour").click();
    await page.waitForTimeout(10000);
    await snap("scenic-and-tour");
    await open("scene=world&stress");
    await reset();
    await page.locator("#scenic").click();
    await page.locator("#start-tour").click();
    await page.waitForTimeout(8000);
    await snap("stress24MiB");
    await context.close();
    console.log(variant, repeat, renderer, "done");
  }
await fs.writeFile(
  `docs/gate3a-corrections/diagnostics-${variant}.json`,
  JSON.stringify(
    {
      variant,
      conditions: {
        repeats: 2,
        order: "WebGL/Canvas, then Canvas/WebGL",
        viewport: [1280, 1000],
        dpr: 1,
        recording: false,
        concurrency: "one page at a time",
        cold: "fresh browser context, cache shared only within this renderer/repeat",
        timing: "CPU and API calls; asynchronous GPU execution not measured",
      },
      errors,
      rows,
    },
    null,
    2,
  ),
);
await browser.close();
if (errors.length) throw Error(errors.join("\n"));
