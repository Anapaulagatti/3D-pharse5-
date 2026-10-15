import { test, expect, type Page } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const out = process.env.PIXEL_REPORT_DIR ?? ".cache/browser";
mkdirSync(out, { recursive: true });
const metrics = (p: Page) => p.evaluate(() => window.__PIXEL_METRICS__!);
async function ready(p: Page) {
  await p.waitForFunction(() => window.__PIXEL_METRICS__?.ready);
}
async function walk(p: Page, key: string, ms: number) {
  await p.locator("canvas").focus();
  const initial = await metrics(p);
  await p.keyboard.down(key);
  // Wait elapsed simulation time, not a frame count: high-refresh and software
  // renderers can advance a different amount of game time per presented frame.
  await p.waitForFunction(
    ({ start, duration }) =>
      (window.__PIXEL_METRICS__?.environmentFrame ?? 0) >= start + duration,
    { start: initial.environmentFrame, duration: ms },
    { timeout: Math.max(12000, ms * 12) },
  );
  const m = await metrics(p);
  await p.keyboard.up(key);
  return m;
}
async function moveAxis(p: Page, axis: "x" | "y", target: number) {
  await p.locator("canvas").focus();
  const current = (await metrics(p))[axis];
  if (Math.abs(current - target) < 3) return;
  const sign = target > current ? 1 : -1;
  const key =
    axis === "x"
      ? sign > 0
        ? "ArrowRight"
        : "ArrowLeft"
      : sign > 0
        ? "ArrowDown"
        : "ArrowUp";
  await p.keyboard.down(key);
  try {
    await p.waitForFunction(
      ({ axis, target, sign }) =>
        ((window.__PIXEL_METRICS__?.[axis] ?? 0) - target) * sign >= 0,
      { axis, target, sign },
      { timeout: 20000 },
    );
  } finally {
    await p.keyboard.up(key);
  }
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
test("unified plaza native movement, collision, layered outfits, distinct run and social emotes", async ({
  page,
  context,
}) => {
  const observed = watch(page);
  await page.goto("./");
  await ready(page);
  const first = await metrics(page);
  expect(first.style).toBe("unified");
  expect(first.animationFrames).toBe(284);
  expect(first.colliders).toBe(77);
  await page.locator("canvas").focus();
  await page.keyboard.press("e");
  await expect(page.locator("#dialog-copy")).toContainText("Sejong");
  await expect(page.locator("#dialog-copy")).toContainText("글자");
  await page.getByRole("button", { name: "Đóng lời nhắn" }).click();
  const movement = [];
  for (const [key, direction] of [
    ["ArrowDown", "down"],
    ["ArrowUp", "up"],
    ["ArrowLeft", "left"],
    ["ArrowRight", "right"],
  ]) {
    const initial = await metrics(page);
    const m = await walk(page, key, 350);
    expect(m.direction).toBe(direction);
    expect(Math.hypot(m.x - initial.x, m.y - initial.y)).toBeGreaterThan(10);
    expect(m.frame).toContain("walk-");
    expect(m.layerFrames.every((f) => f === m.frame)).toBe(true);
    movement.push(m);
  }
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(80);
  const a = await page.locator("canvas").screenshot();
  await page.waitForTimeout(220);
  const b = await page.locator("canvas").screenshot();
  await page.keyboard.up("ArrowRight");
  expect(createHash("sha256").update(a).digest("hex")).not.toBe(
    createHash("sha256").update(b).digest("hex"),
  );
  await page.keyboard.down("Shift");
  const run = await walk(page, "ArrowLeft", 250);
  await page.keyboard.up("Shift");
  expect(run.speed).toBe(100);
  expect(run.frame).toMatch(/^run-left-/);
  expect(run.layerFrames.every((f) => f === run.frame)).toBe(true);
  await moveAxis(page, "y", 560);
  await moveAxis(page, "x", 512);
  await walk(page, "ArrowUp", 1800);
  const wallA = await metrics(page);
  await walk(page, "ArrowUp", 400);
  const wallB = await metrics(page);
  expect(wallB.y).toBeCloseTo(wallA.y, 0);
  expect(wallA.y).toBeGreaterThan(470);
  expect(wallA.y).toBeLessThan(500);
  await walk(page, "ArrowDown", 250);
  await page.waitForFunction(() => !window.__PIXEL_METRICS__?.moving);
  const emotes = [];
  for (const action of ["wave", "celebrate", "pose", "think"]) {
    await page.locator("#" + action).click();
    await page.waitForFunction(
      (a) =>
        window.__PIXEL_METRICS__!.frame.startsWith(a + "-") &&
        Number(window.__PIXEL_METRICS__!.frame.split("-").at(-1)) >= 2,
      action,
    );
    const m = await metrics(page);
    expect(m.layerFrames.every((f) => f === m.frame)).toBe(true);
    emotes.push(m);
    await page
      .locator("canvas")
      .screenshot({ path: out + "/" + action + ".png" });
    await page.waitForFunction(() =>
      window.__PIXEL_METRICS__!.frame.startsWith("idle-"),
    );
  }
  for (const hair of ["0", "1"])
    for (const outfit of ["0", "1"]) {
      await page.locator("#hair").selectOption(hair);
      await page.locator("#outfit").selectOption(outfit);
      await page.waitForFunction(
        ({ h, o }) =>
          window.__PIXEL_METRICS__!.hair === +h &&
          window.__PIXEL_METRICS__!.outfit === +o,
        { h: hair, o: outfit },
      );
      const m = await metrics(page);
      expect(m.layerFrames.every((f) => f === m.frame)).toBe(true);
    }
  await page.locator("#accessory").uncheck();
  await page.reload();
  await ready(page);
  expect((await metrics(page)).hair).toBe(1);
  expect((await metrics(page)).outfit).toBe(1);
  expect((await metrics(page)).accessory).toBe(false);
  await page.locator("#pause").click();
  await page.waitForFunction(() => window.__PIXEL_METRICS__!.paused);
  const pausedA = await metrics(page);
  await page.waitForTimeout(250);
  const pausedB = await metrics(page);
  expect(pausedB.environmentFrame).toBe(pausedA.environmentFrame);
  expect(pausedB.x).toBe(pausedA.x);
  await page.locator("#pause").click();
  for (const zoom of ["1", "2", "3"]) {
    await page.locator("#zoom").selectOption(zoom);
    await page.waitForFunction(
      (z) => window.__PIXEL_METRICS__!.cameraZoom === +z,
      zoom,
    );
    expect(
      await page
        .locator("canvas")
        .evaluate((e) => getComputedStyle(e).imageRendering),
    ).toBe("pixelated");
    await page
      .locator("canvas")
      .screenshot({ path: out + "/zoom-" + zoom + ".png" });
  }
  await context.setOffline(true);
  await expect(page.locator("#offline")).toContainText("Đang offline");
  const before = await metrics(page);
  const after = await walk(page, "ArrowDown", 250);
  expect(after.y).toBeGreaterThan(before.y);
  await context.setOffline(false);
  expect(observed.errors).toEqual([]);
  expect(observed.missing).toEqual([]);
  writeFileSync(
    out + "/desktop-verification.json",
    JSON.stringify(
      {
        status: "PASS",
        first,
        movement,
        run,
        closedWall: [wallA, wallB],
        emotes,
        pause: [pausedA, pausedB],
        ...observed,
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

test("new chibi hero renders four visibly different moods at the same pixel crop", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 1100 });
  const observed = watch(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("./");
  await ready(page);
  const initial = await metrics(page);
  expect(initial.avatarVersion).toBe("chibi-motion-v2");
  expect(initial.heroCssHeight).toBe(112);
  expect(initial.layerFrames).toHaveLength(5);
  const hashes = new Set<string>();
  for (const mood of ["neutral", "happy", "focused", "surprised"]) {
    await page.locator("#expression").selectOption(mood);
    await page.waitForFunction(
      (e) => window.__PIXEL_METRICS__!.expression === e,
      mood,
    );
    const start = await metrics(page);
    await page.waitForFunction(
      (f) => window.__PIXEL_METRICS__!.frameCount > f + 3,
      start.frameCount,
    );
    const m = await metrics(page);
    expect(m.frame).toBe("idle-down-0");
    expect(m.x).toBe(initial.x);
    expect(m.y).toBe(initial.y);
    const canvas = (await page.locator("canvas").boundingBox())!;
    const pixels = await page.screenshot({
      clip: {
        x: canvas.x + m.screenFoot.x - 40,
        y: canvas.y + m.screenFoot.y - 112,
        width: 80,
        height: 112,
      },
    });
    hashes.add(createHash("sha256").update(pixels).digest("hex"));
  }
  expect(hashes.size).toBe(4);
  expect(observed.errors).toEqual([]);
  expect(observed.missing).toEqual([]);
});

test("four historical guests greet, teach a word and visibly move without pretending to be online players", async ({
  page,
}) => {
  const observed = watch(page);
  await page.goto("./");
  await ready(page);
  const first = await metrics(page);
  expect(first.guests.map((g) => g.id)).toEqual([
    "sejong",
    "jang",
    "saimdang",
    "yi",
  ]);
  for (const [id, ko, word] of [
    ["sejong", "세종대왕", "글자"],
    ["jang", "장영실", "물"],
    ["saimdang", "신사임당", "나무"],
    ["yi", "이순신", "함께"],
  ]) {
    await page.locator(`[data-guest="${id}"]`).click();
    await expect(page.locator("#dialog-copy")).toContainText(ko);
    await expect(page.locator("#dialog-copy")).toContainText(word);
    await expect(page.locator("#dialog-copy")).toContainText(
      "những thời kỳ khác nhau",
    );
    await page.waitForFunction((id) => {
      const g = window.__PIXEL_METRICS__!.guests.find((g) => g.id === id);
      return (
        !!g &&
        /^(wave|think|pose)-/.test(g.frame) &&
        +g.frame.split("-").at(-1)! >= 2
      );
    }, id);
    await page.getByRole("button", { name: "Đóng lời nhắn" }).click();
  }
  // Observe each patrol actually move. A single wall-clock snapshot can catch
  // a guest resting or returning to its start and does not prove inactivity.
  await Promise.all(
    first.guests.map((old) =>
      page.waitForFunction(
        (old) => {
          const g = window.__PIXEL_METRICS__!.guests.find(
            (g) => g.id === old.id,
          );
          return !!g && Math.hypot(g.x - old.x, g.y - old.y) > 1;
        },
        old,
        { timeout: 20000 },
      ),
    ),
  );
  expect(observed.errors).toEqual([]);
  expect(observed.missing).toEqual([]);
});
