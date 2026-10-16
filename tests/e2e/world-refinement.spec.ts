import { test, expect, type Page } from "@playwright/test";
import { createHash } from "node:crypto";

async function ready(page: Page, suffix = "") {
  await page.goto(`./refinement-review.html?qa&renderer=canvas${suffix}`);
  await page.waitForFunction(() => window.__SEOUL__?.ready);
}
async function place(page: Page, x: number, y: number) {
  await page.evaluate(([x, y]) => window.__SEOUL_TEST__!.place(x, y), [x, y]);
  await page.waitForTimeout(120);
}
async function move(
  page: Page,
  key: string,
  axis: "x" | "y",
  target: number,
  positive = false,
) {
  await page.locator("canvas").focus();
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      ({ axis, target, positive }) =>
        positive
          ? window.__SEOUL__![axis] >= target
          : window.__SEOUL__![axis] <= target,
      { axis, target, positive },
      { timeout: 20000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.waitForTimeout(140);
}

test("compact palace: real leaf collision, safe closing, open inner gate and royal interaction", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  await ready(page);
  expect((await page.evaluate(() => window.__SEOUL__!)).world).toEqual([
    2304, 1920,
  ]);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(1900);
  await page.keyboard.up("ArrowUp");
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    739,
  );
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.gateOpen);
  await page.locator("#close-dialog").click();
  await move(page, "ArrowUp", "y", 660);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("ngưỡng cửa");
  await page.locator("#close-dialog").click();
  await move(page, "ArrowUp", "y", 380);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeLessThan(400);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("궁궐");
  await page.locator("#close-dialog").click();
  await place(page, 1456, 404);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog-copy")).toContainText("Hanji");
  expect(errors).toEqual([]);
});

test("Academy east shortcut, wall collision, lazy room and unchanged Hangul lesson/return", async ({
  page,
}) => {
  await ready(page);
  await place(page, 1008, 1392);
  await move(page, "ArrowLeft", "x", 864);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeLessThan(880);
  await place(page, 1008, 1248);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowLeft");
  await page.waitForTimeout(1600);
  await page.keyboard.up("ArrowLeft");
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThanOrEqual(
    976,
  );
  await place(page, 544, 1152);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "room");
  await place(page, 385, 392);
  await page.locator("#interact").click();
  await expect(page.locator(".hangul-letter")).toBeVisible();
  for (const answer of ["giyeok", "nieun", "mieum"]) {
    await page
      .locator("#dialog-copy")
      .getByRole("button", { name: answer, exact: true })
      .click();
    await page
      .locator("#dialog-copy")
      .getByRole("button", {
        name: answer === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  await expect(page.locator("#dialog-copy")).toContainText("Hoàn thành");
  await page.locator("#close-dialog").click();
  await place(page, 384, 490);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__SEOUL__?.area === "outdoor");
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeCloseTo(544, 0);
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeCloseTo(1152, 0);
});

test("workshop service gap, independent wing collision and open museum/modern frontages", async ({
  page,
}) => {
  await ready(page);
  await place(page, 1440, 1264);
  await move(page, "ArrowRight", "x", 1584, true);
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(1568);
  await place(page, 1938, 1232);
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(1400);
  await page.keyboard.up("ArrowUp");
  expect(await page.evaluate(() => window.__SEOUL__!.y)).toBeGreaterThanOrEqual(
    1186,
  );
  for (const [x, y, copy] of [
    [1632, 1536, "Khoa học"],
    [1984, 1744, "Lịch sử"],
    [512, 1872, "Cà phê"],
  ] as const) {
    await place(page, x, y);
    await page.locator("#interact").click();
    await expect(page.locator("#dialog-copy")).toContainText(copy);
    await page.locator("#close-dialog").click();
  }
});

test("cached opaque cue matches the reference pixels and never re-reads textures during movement", async ({
  page,
  context,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await ready(page);
  const ref = await context.newPage();
  await ref.emulateMedia({ reducedMotion: "reduce" });
  await ready(ref, "&occlusion=reference");
  const reads = await page.evaluate(
    () => window.__REFINEMENT__!.maskReadsAtLoad,
  );
  let occluded = 0;
  for (const [x, y] of [
    [1152, 748],
    [1440, 1504],
    [2256, 1724],
    [544, 1152],
  ]) {
    await place(page, x, y);
    await place(ref, x, y);
    const n = await page.evaluate(
      () => window.__PLAZA_REVIEW__!.occludedPixels,
    );
    occluded += n;
    expect(n).toBe(
      await ref.evaluate(() => window.__PLAZA_REVIEW__!.occludedPixels),
    );
    expect(
      createHash("sha256")
        .update(await page.locator("canvas").screenshot())
        .digest("hex"),
    ).toBe(
      createHash("sha256")
        .update(await ref.locator("canvas").screenshot())
        .digest("hex"),
    );
    expect(
      await page.evaluate(() => window.__REFINEMENT__!.maskReadsAtLoad),
    ).toBe(reads);
  }
  expect(occluded).toBeGreaterThan(100);
  await ref.close();
});

test("mobile real touch, reduced-motion and settled pause remain usable", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("./refinement-review.html?renderer=canvas");
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  expect(await page.evaluate(() => !!window.__SEOUL_TEST__)).toBe(false);
  await expect(page.locator("#motion")).toBeChecked();
  const clock = await page.evaluate(() => window.__SEOUL__!.ambientClock);
  const right = page.locator('[data-x="1"]');
  await right.scrollIntoViewIfNeeded();
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setTouchEmulationEnabled", { enabled: true });
  const touch = async () => {
    const b = (await right.boundingBox())!;
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x: b.x + b.width / 2, y: b.y + b.height / 2 }],
    });
  };
  const release = () =>
    cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  const x = await page.evaluate(() => window.__SEOUL__!.x);
  await touch();
  await page.waitForTimeout(500);
  await release();
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBeGreaterThan(
    x + 15,
  );
  expect(await page.evaluate(() => window.__SEOUL__!.ambientClock)).toBe(clock);
  await page.locator("#pause").click();
  const f = await page.evaluate(() => window.__PIXEL_METRICS__!.frameCount);
  await page.waitForFunction(
    (f) =>
      window.__PIXEL_METRICS__!.paused &&
      window.__PIXEL_METRICS__!.frameCount >= f + 2,
    f,
  );
  const frozen = await page.evaluate(() => window.__SEOUL__!.x);
  await touch();
  await page.waitForTimeout(250);
  await release();
  expect(await page.evaluate(() => window.__SEOUL__!.x)).toBe(frozen);
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(390);
});
