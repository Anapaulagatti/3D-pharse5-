import { test, expect, type Page } from "@playwright/test";
async function axis(
  page: Page,
  key: string,
  field: "x" | "y",
  target: number,
  positive = true,
) {
  await page.locator("canvas").focus();
  await page.keyboard.down(key);
  try {
    await page.waitForFunction(
      ({ field, target, positive }) => {
        const d = window.__DISTRICT__;
        return d && (positive ? d[field] >= target : d[field] <= target);
      },
      { field, target, positive },
      { timeout: 22000 },
    );
  } finally {
    await page.keyboard.up(key);
  }
  await page.waitForTimeout(170);
}
test("first district is genuinely connected, interior loads on entry, letter activity saves and reciprocal return works", async ({
  page,
}) => {
  const errors: string[] = [],
    requests: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  page.on("request", (r) => requests.push(r.url()));
  await page.goto("./district-review.html");
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  expect(requests.some((u) => u.includes("/living-seoul/room/"))).toBe(false);
  await page.keyboard.down("Shift");
  await axis(page, "ArrowRight", "x", 1280);
  await axis(page, "ArrowUp", "y", 544, false);
  await axis(page, "ArrowRight", "x", 1536);
  await axis(page, "ArrowUp", "y", 475, false);
  await page.keyboard.up("Shift");
  expect(
    await page.evaluate(() => window.__DISTRICT__!.camera.x),
  ).toBeGreaterThan(900);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__DISTRICT__?.area === "room");
  expect(
    requests.some((u) => u.includes("/living-seoul/room/room-base.png")),
  ).toBe(true);
  await axis(page, "ArrowUp", "y", 397, false);
  await page.locator("#interact").click();
  await expect(page.locator("#dialog")).toBeVisible();
  const position = await page.evaluate(() => window.__DISTRICT__!.y);
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(200);
  await page.keyboard.up("ArrowUp");
  expect(await page.evaluate(() => window.__DISTRICT__!.y)).toBeCloseTo(
    position,
    1,
  );
  await page
    .locator("#dialog-copy")
    .getByRole("button", { name: "mieum", exact: true })
    .click();
  await expect(page.locator("#dialog-copy")).toContainText("Chưa đúng");
  for (const name of ["giyeok", "nieun", "mieum"]) {
    await page
      .locator("#dialog-copy")
      .getByRole("button", { name, exact: true })
      .click();
    await page
      .locator("#dialog-copy")
      .getByRole("button", {
        name: name === "mieum" ? "Hoàn thành" : "Chữ tiếp theo",
        exact: true,
      })
      .click();
  }
  await expect(page.locator("#quest-progress")).toContainText("Đã ghép đúng");
  await page.locator("#close-dialog").click();
  await axis(page, "ArrowDown", "y", 490);
  await page.locator("#interact").click();
  await page.waitForFunction(() => window.__DISTRICT__?.area === "outdoor");
  expect(await page.evaluate(() => window.__DISTRICT__!.x)).toBeCloseTo(
    1536,
    0,
  );
  // Blocked facades really collide: do not let the actor walk through the building.
  await page.locator("canvas").focus();
  await page.keyboard.down("ArrowUp");
  await page.waitForTimeout(1800);
  await page.keyboard.up("ArrowUp");
  expect(
    await page.evaluate(() => window.__DISTRICT__!.y),
  ).toBeGreaterThanOrEqual(413.5);
  await page.reload();
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  await expect(page.locator("#quest-progress")).toContainText("Đã ghép đúng");
  expect(errors).toEqual([]);
});
test("district preserves mobile Canvas touch and reduced-motion, and survives unavailable local storage", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    const get = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (
      this: HTMLCanvasElement,
      type: string,
      ...args: unknown[]
    ) {
      if (type.includes("webgl")) return null;
      return get.call(this, type, ...(args as []));
    } as typeof get;
    Storage.prototype.getItem = () => {
      throw Error("Private storage");
    };
    Storage.prototype.setItem = () => {
      throw Error("Private storage");
    };
  });
  await page.goto("./district-review.html");
  await page.waitForFunction(() => window.__DISTRICT__?.ready);
  expect(await page.evaluate(() => window.__PIXEL_METRICS__!.renderer)).toBe(
    "Canvas",
  );
  await expect(page.locator("#storage-status")).toContainText("Không truy cập");
  const x = await page.evaluate(() => window.__DISTRICT__!.x);
  const b = page.locator('[data-x="1"]');
  await b.scrollIntoViewIfNeeded();
  const box = (await b.boundingBox())!;
  const cdp = await context.newCDPSession(page);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x: box.x + box.width / 2, y: box.y + box.height / 2 }],
  });
  await page.waitForTimeout(650);
  await cdp.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
  await page.waitForTimeout(250);
  expect(await page.evaluate(() => window.__DISTRICT__!.x)).toBeGreaterThan(
    x + 12,
  );
  const frozen = await page.evaluate(
    () => window.__PLAZA_REVIEW__!.environmentClock,
  );
  await page.waitForTimeout(250);
  expect(
    await page.evaluate(() => window.__PLAZA_REVIEW__!.environmentClock),
  ).toBe(frozen);
  await context.close();
});
