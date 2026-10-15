import { test, expect } from "@playwright/test";

test("Juni renders eight real gait frames per direction, transitions and social gestures in the actual district", async ({
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
  await page.goto("./plaza-review.html");
  await page.waitForFunction(() => window.__PLAZA_REVIEW__?.ready);
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.evaluate(() => {
    const log: { action: string; frame: string; direction: string }[] = [];
    (window as unknown as { juniSamples: typeof log }).juniSamples = log;
    function sample() {
      const r = window.__PLAZA_REVIEW__;
      if (r)
        log.push({ action: r.action, frame: r.frame, direction: r.direction });
      requestAnimationFrame(sample);
    }
    requestAnimationFrame(sample);
  });
  await page.waitForFunction(
    () => window.__PLAZA_REVIEW__!.frame === "idle-front-5",
  );
  for (const run of [false, true]) {
    if (run) await page.keyboard.down("Shift");
    for (const [key, view] of [
      ["ArrowRight", "right"],
      ["ArrowUp", "back"],
      ["ArrowLeft", "left"],
      ["ArrowDown", "front"],
    ]) {
      await page.locator("canvas").focus();
      await page.keyboard.down(key);
      try {
        await expect
          .poll(
            () =>
              page.evaluate(
                ({ action, view }) => {
                  const samples = (
                    window as unknown as {
                      juniSamples: {
                        action: string;
                        frame: string;
                        direction: string;
                      }[];
                    }
                  ).juniSamples;
                  return new Set(
                    samples
                      .filter(
                        (s) => s.action === action && s.direction === view,
                      )
                      .map((s) => s.frame),
                  ).size;
                },
                { action: run ? "run" : "walk", view },
              ),
            { timeout: 5000 },
          )
          .toBe(8);
      } finally {
        await page.keyboard.up(key);
      }
      await page.waitForFunction(
        () => window.__PLAZA_REVIEW__!.action === "idle",
      );
    }
    if (run) await page.keyboard.up("Shift");
  }
  for (const [id, action] of [
    ["wave", "wave"],
    ["celebrate", "celebrate"],
    ["pose", "social"],
  ]) {
    await page.locator(`#${id}`).click();
    await page.waitForFunction(
      (action) => window.__PLAZA_REVIEW__!.action === action,
      action,
    );
    await page.waitForFunction(
      () => window.__PLAZA_REVIEW__!.action === "idle",
    );
  }
  const samples = await page.evaluate(
    () =>
      (
        window as unknown as {
          juniSamples: { action: string; frame: string }[];
        }
      ).juniSamples,
  );
  for (const action of [
    "idle",
    "start",
    "stop",
    "turn",
    "wave",
    "celebrate",
    "social",
  ])
    expect(
      new Set(samples.filter((s) => s.action === action).map((s) => s.frame))
        .size,
      action,
    ).toBeGreaterThan(1);
  await page.locator("#pause").click();
  await page.waitForFunction(() => window.__PIXEL_METRICS__!.paused);
  const frozen = await page.evaluate(() => window.__PLAZA_REVIEW__!);
  await page.waitForTimeout(250);
  expect(await page.evaluate(() => window.__PLAZA_REVIEW__!.frame)).toBe(
    frozen.frame,
  );
  expect(
    await page.evaluate(() => window.__PLAZA_REVIEW__!.environmentClock),
  ).toBe(frozen.environmentClock);
  await page.locator("#pause").click();
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.waitForFunction(
    () => window.__PLAZA_REVIEW__!.frame === "idle-front-0",
  );
  await page.waitForTimeout(350);
  expect(await page.evaluate(() => window.__PLAZA_REVIEW__!.frame)).toBe(
    "idle-front-0",
  );
  expect(errors).toEqual([]);
});
