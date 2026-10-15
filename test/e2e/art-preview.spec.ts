import { test, expect, type Page } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const out = process.env.PIXEL_REPORT_DIR ?? "quality-reports/pixel-v3.1";
mkdirSync(out, { recursive: true });
const metrics = (p: Page) => p.evaluate(() => window.__PIXEL_METRICS__!);
async function ready(p: Page) {
  await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
}
async function walk(p: Page, key: string, ms: number) {
  await p.locator("canvas").focus();
  await p.keyboard.down(key);
  await p.waitForTimeout(ms);
  const m = await metrics(p);
  await p.keyboard.up(key);
  return m;
}
function watch(p: Page) {
  const errors: string[] = [];
  const missing: string[] = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  p.on("response", (r) => {
    if (r.status() >= 400) missing.push(`${r.status()} ${r.url()}`);
  });
  return { errors, missing };
}
test("actual three-direction art, animation, collision, HTML dialogue and settings", async ({
  page,
  context,
}) => {
  const observed = watch(page);
  await page.goto("./");
  await ready(page);
  await page.screenshot({ path: out + "/desktop-B.png", fullPage: true });
  await page.locator("canvas").screenshot({ path: out + "/engine-B.png" });
  const first = await metrics(page);
  expect(first.animationFrames).toBe(48);
  expect(first.colliders).toBe(13);
  const movement = [];
  for (const [key, direction] of [
    ["ArrowDown", "down"],
    ["ArrowUp", "up"],
    ["ArrowLeft", "left"],
    ["ArrowRight", "right"],
  ]) {
    const initial = await metrics(page);
    const m = await walk(page, key, 550);
    expect(m.direction).toBe(direction);
    expect(Math.hypot(m.x - initial.x, m.y - initial.y)).toBeGreaterThan(10);
    movement.push(m);
    await page
      .locator("canvas")
      .screenshot({ path: `${out}/walk-${direction}.png` });
  }
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(70);
  const a = await page
    .locator("canvas")
    .screenshot({ path: out + "/moving-a.png" });
  await page.waitForTimeout(220);
  const b = await page
    .locator("canvas")
    .screenshot({ path: out + "/moving-b.png" });
  await page.keyboard.up("ArrowRight");
  expect(createHash("sha256").update(a).digest("hex")).not.toBe(
    createHash("sha256").update(b).digest("hex"),
  );
  await page.keyboard.down("Shift");
  const run = await walk(page, "ArrowLeft", 350);
  await page.keyboard.up("Shift");
  expect(run.speed).toBe(126);
  await walk(page, "ArrowUp", 2200);
  const wallA = await metrics(page);
  await walk(page, "ArrowUp", 500);
  const wallB = await metrics(page);
  expect(wallB.y).toBeCloseTo(wallA.y, 0);
  expect(wallA.y).toBeGreaterThan(257);
  await page.keyboard.press("e");
  await expect(page.locator("#dialog-copy")).toContainText("Mira");
  await expect(page.locator("#dialog-copy")).toContainText("우체국");
  await page.screenshot({ path: out + "/dialogue-hangul.png" });
  await page.getByRole("button", { name: "Đóng lời nhắn" }).click();
  await page.getByRole("button", { name: "Tạm dừng", exact: true }).click();
  await page.waitForTimeout(100);
  const pausedA = await metrics(page);
  await page.waitForTimeout(400);
  const pausedB = await metrics(page);
  expect(pausedB.environmentFrame).toBe(pausedA.environmentFrame);
  expect(pausedB.x).toBe(pausedA.x);
  await page.getByRole("button", { name: "Tiếp tục", exact: true }).click();
  for (const zoom of ["2", "3", "1"]) {
    await page.locator("#zoom").selectOption(zoom);
    await page.waitForTimeout(150);
    await page
      .locator("canvas")
      .screenshot({ path: `${out}/pixel-zoom-${zoom}.png` });
    expect(
      await page
        .locator("canvas")
        .evaluate((e) => getComputedStyle(e).imageRendering),
    ).toBe("pixelated");
  }
  await page
    .getByRole("button", { name: "Ánh chiều dịu", exact: true })
    .click();
  await page.waitForTimeout(200);
  await page.locator("canvas").screenshot({ path: out + "/evening.png" });
  for (const style of ["A", "C", "B"]) {
    await page.locator("#direction").selectOption(style);
    await page.waitForFunction(
      (s) => window.__PIXEL_METRICS__?.style === s,
      style,
    );
    await page
      .locator("canvas")
      .screenshot({ path: `${out}/engine-${style}.png` });
  }
  await page.reload();
  await ready(page);
  expect((await metrics(page)).style).toBe("B");
  expect(
    await page.evaluate(
      () => JSON.parse(localStorage.getItem("hangeul-pixel-guest-v1")!).metMira,
    ),
  ).toBe(true);
  await context.setOffline(true);
  await expect(page.locator("#offline")).toContainText("Đang offline");
  const offBefore = await metrics(page);
  const offAfter = await walk(page, "ArrowDown", 300);
  expect(offAfter.y).toBeGreaterThan(offBefore.y);
  await page.screenshot({ path: out + "/offline-loaded.png" });
  await context.setOffline(false);
  expect(observed.errors).toEqual([]);
  expect(observed.missing).toEqual([]);
  writeFileSync(
    out + "/desktop-verification.json",
    JSON.stringify(
      {
        status: "PASS",
        initial: first,
        movement,
        run,
        closedWall: [wallA, wallB],
        pause: [pausedA, pausedB],
        ...observed,
        offline: "Loaded assets continue; no cold-offline caching claim",
      },
      null,
      2,
    ),
  );
});
test("OS reduced motion, actual touch, mobile layout and DPR", async ({
  browser,
}) => {
  const reports = [];
  for (const dpr of [1, 2]) {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      deviceScaleFactor: dpr,
      isMobile: true,
      hasTouch: true,
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const observed = watch(page);
    await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
    await ready(page);
    expect((await metrics(page)).reduced).toBe(true);
    await expect(page.locator("#motion")).toBeChecked();
    const stillA = await metrics(page);
    await page.waitForTimeout(300);
    const stillB = await metrics(page);
    expect(stillB.environmentFrame).toBe(stillA.environmentFrame);
    const button = page.getByRole("button", { name: "Đi xuống", exact: true });
    await button.scrollIntoViewIfNeeded();
    const box = (await button.boundingBox())!;
    const cdp = await context.newCDPSession(page);
    const before = await metrics(page);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: box.x + box.width / 2, y: box.y + box.height / 2 }],
    });
    await page.waitForTimeout(450);
    const after = await metrics(page);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    expect(after.y).toBeGreaterThan(before.y + 5);
    await page.waitForTimeout(100);
    const stopped = await metrics(page);
    await page.waitForTimeout(200);
    expect((await metrics(page)).y).toBeCloseTo(stopped.y, 1);
    expect(after.frame).toContain("walk-down");
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({
      path: `${out}/mobile-dpr-${dpr}.png`,
      fullPage: true,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    expect(observed.errors).toEqual([]);
    expect(observed.missing).toEqual([]);
    reports.push({ dpr, before, after, ...observed });
    await context.close();
  }
  writeFileSync(
    out + "/mobile-verification.json",
    JSON.stringify(
      {
        status: "PASS",
        reports,
        limitation:
          "Cloud Chromium touch emulation; physical-device FPS unmeasured",
      },
      null,
      2,
    ),
  );
});
test("genuine WebGL-unavailable Canvas fallback", async ({ browser }) => {
  const context = await browser.newContext();
  await context.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (
      this: HTMLCanvasElement,
      type: string,
      ...args: unknown[]
    ) {
      if (type.includes("webgl")) return null;
      return Reflect.apply(original, this, [type, ...args]);
    } as typeof original;
  });
  const page = await context.newPage();
  const observed = watch(page);
  await page.goto("http://127.0.0.1:4201/3D-pharse5-/");
  await ready(page);
  expect((await metrics(page)).renderer).toBe("Canvas");
  const a = await metrics(page);
  const b = await walk(page, "ArrowDown", 300);
  expect(b.y).toBeGreaterThan(a.y);
  await page
    .locator("canvas")
    .screenshot({ path: out + "/canvas-fallback.png" });
  expect(observed.errors).toEqual([]);
  expect(observed.missing).toEqual([]);
  writeFileSync(
    out + "/fallback-verification.json",
    JSON.stringify(
      { status: "PASS", renderer: "Canvas", a, b, ...observed },
      null,
      2,
    ),
  );
  await context.close();
});
