import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
const dir = ".cache/v10-production/walkthrough-frames";
await fs.mkdir(dir, { recursive: true });
const routes = JSON.parse(
  await fs.readFile("docs/v10-production/walkthrough-routes.json", "utf8"),
);
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const page = await browser.newPage({
  viewport: { width: 1200, height: 1000 },
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
});
const errors = [],
  visits = [],
  frames = [],
  writes = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
try {
  await page.goto(
    "http://127.0.0.1:4220/3D-pharse5-/v10-city-review.html?renderer=canvas",
  );
  await page.waitForFunction(() => window.__SEOUL__?.ready);
  if (await page.evaluate(() => !!window.__SEOUL_TEST__))
    throw Error("QA hook exposed");
  const cdp = await page.context().newCDPSession(page);
  cdp.on("Page.screencastFrame", (e) => {
    const name = `${String(frames.length).padStart(6, "0")}.jpg`;
    frames.push({ name, t: e.metadata.timestamp });
    writes.push(fs.writeFile(`${dir}/${name}`, Buffer.from(e.data, "base64")));
    void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
  });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 80,
    maxWidth: 1200,
    maxHeight: 1000,
    everyNthFrame: 4,
  });
  async function axis(axis, target) {
    let current = await page.evaluate((a) => window.__SEOUL__[a], axis);
    const keyFor = (delta) =>
      axis === "x"
        ? delta > 0
          ? "ArrowRight"
          : "ArrowLeft"
        : delta > 0
          ? "ArrowDown"
          : "ArrowUp";
    if (Math.abs(target - current) > 24) {
      const sign = Math.sign(target - current),
        key = keyFor(target - current);
      await page.keyboard.down("Shift");
      await page.keyboard.down(key);
      try {
        await page.waitForFunction(
          ({ axis, target, sign }) =>
            (window.__SEOUL__[axis] - target) * sign >= -12,
          { axis, target, sign },
          {
            polling: "raf",
            timeout: Math.max(6000, Math.abs(target - current) * 30),
          },
        );
      } catch (e) {
        console.log(
          JSON.stringify({
            axis,
            target,
            actual: await page.evaluate(() => [
              window.__SEOUL__.x,
              window.__SEOUL__.y,
            ]),
          }),
        );
        throw e;
      } finally {
        await page.keyboard.up(key);
        await page.keyboard.up("Shift");
        await page.waitForTimeout(150);
      }
    }
    await page.keyboard.up("Shift");
    // Correct stopping drift with actual short walking inputs before each turn.
    for (let attempt = 0; attempt < 24; attempt++) {
      current = await page.evaluate((a) => window.__SEOUL__[a], axis);
      const delta = target - current;
      if (Math.abs(delta) < 5) return;
      const key = keyFor(delta);
      await page.keyboard.down(key);
      await page.waitForTimeout(
        Math.min(90, Math.max(20, Math.abs(delta) * 9)),
      );
      await page.keyboard.up(key);
      await page.waitForTimeout(140);
    }
    throw Error(
      "Input steering did not settle at " +
        axis +
        "=" +
        target +
        " actual " +
        current,
    );
  }
  for (let g = 0; g < routes.length; g++) {
    await page.locator("canvas").focus();
    await page.keyboard.down("Shift");
    for (const leg of routes[g]) {
      for (const [x, y] of leg.points) {
        await axis("x", x);
        await axis("y", y);
      }
      visits.push({
        target: leg.destination,
        actual: await page.evaluate(() => [
          window.__SEOUL__.x,
          window.__SEOUL__.y,
        ]),
        elapsed: frames.at(-1)?.t - frames[0]?.t,
      });
      console.log(JSON.stringify(visits.at(-1)));
      await page.waitForTimeout(450);
    }
    await page.keyboard.up("Shift");
    await page.locator("#interact").click();
    await page
      .getByRole("button", {
        name: g === 0 ? "Lên phà đến Jeju" : "Lên phà về bờ biển",
      })
      .click();
    await page.waitForTimeout(1500);
  }
  await cdp.send("Page.stopScreencast");
  await Promise.all(writes);
  const concat = frames
    .map(
      (f, i) =>
        `file '${f.name}'\nduration ${Math.max(0.001, (frames[i + 1]?.t ?? f.t + 0.1) - f.t)}`,
    )
    .join("\n");
  await fs.writeFile(`${dir}/frames.txt`, concat + "\n");
  await browser.close();
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-hide_banner",
      "-loglevel",
      "error",
      "-f",
      "concat",
      "-safe",
      "0",
      "-i",
      `${dir}/frames.txt`,
      "-fps_mode",
      "vfr",
      "-c:v",
      "libx264",
      "-threads",
      "2",
      "-preset",
      "fast",
      "-crf",
      "30",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "docs/v10-production/V10_GAMEPLAY_WALKTHROUGH.mp4",
    ],
    { timeout: 180000 },
  );
  const result = {
    source:
      "Actual normal-entry Phaser Canvas via keyboard at unchanged run speed100, reciprocal ferry UI; CDP real timestamps, no speedup/no QA placement",
    visits,
    errors,
    frames: frames.length,
    duration: frames.at(-1).t - frames[0].t,
  };
  await fs.writeFile(
    "docs/v10-production/walkthrough.json",
    JSON.stringify(result, null, 2) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
} finally {
  await browser.close();
}
