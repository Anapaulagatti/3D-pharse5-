import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
const dir = ".cache/gate1/video-frames";
await fs.mkdir(dir, { recursive: true });
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-gpu-compositing"],
});
const page = await browser.newPage({
  viewport: { width: 1280, height: 980 },
  deviceScaleFactor: 1,
  reducedMotion: "reduce",
});
const frames = [],
  writes = [],
  visits = [],
  errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(r.url());
});
try {
  await page.goto(
    "http://127.0.0.1:4230/3D-pharse5-/gate1-street.html?renderer=canvas",
  );
  await page.waitForFunction(() => window.__GATE1__?.ready);
  if (await page.evaluate(() => !!window.__GATE1_TEST__))
    throw Error("QA placement exposed");
  const cdp = await page.context().newCDPSession(page);
  cdp.on("Page.screencastFrame", (e) => {
    const name = String(frames.length).padStart(6, "0") + ".jpg";
    frames.push({ name, t: e.metadata.timestamp });
    writes.push(fs.writeFile(dir + "/" + name, Buffer.from(e.data, "base64")));
    void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
  });
  await cdp.send("Page.startScreencast", {
    format: "jpeg",
    quality: 86,
    maxWidth: 1280,
    maxHeight: 980,
    everyNthFrame: 3,
  });
  async function axis(a, t) {
    let v = await page.evaluate((a) => window.__GATE1__[a], a);
    if (Math.abs(t - v) < 5) return;
    const sign = Math.sign(t - v),
      k =
        a === "x"
          ? sign > 0
            ? "ArrowRight"
            : "ArrowLeft"
          : sign > 0
            ? "ArrowDown"
            : "ArrowUp";
    await page.keyboard.down("Shift");
    await page.keyboard.down(k);
    try {
      await page.waitForFunction(
        ({ a, t, sign }) => (window.__GATE1__[a] - t) * sign >= -9,
        { a, t, sign },
        { polling: "raf", timeout: Math.max(6000, Math.abs(t - v) * 25) },
      );
    } finally {
      await page.keyboard.up(k);
      await page.keyboard.up("Shift");
      await page.waitForTimeout(140);
    }
    for (let n = 0; n < 16; n++) {
      v = await page.evaluate((a) => window.__GATE1__[a], a);
      if (Math.abs(t - v) < 5) return;
      const key =
        a === "x"
          ? t > v
            ? "ArrowRight"
            : "ArrowLeft"
          : t > v
            ? "ArrowDown"
            : "ArrowUp";
      await page.keyboard.down(key);
      await page.waitForTimeout(
        Math.max(20, Math.min(80, Math.abs(t - v) * 9)),
      );
      await page.keyboard.up(key);
      await page.waitForTimeout(140);
    }
    throw Error("Input steering " + a + " " + t + " " + v);
  }
  await page.locator("canvas").focus();
  await page.waitForTimeout(1200);
  for (const x of [242, 598, 888, 1288]) {
    await axis("x", x);
    await page.keyboard.press("e");
    await page.waitForFunction(() => !document.querySelector("#dialog").hidden);
    await page.waitForTimeout(1000);
    await page.locator("#close-dialog").click();
    visits.push(await page.evaluate(() => ({ ...window.__GATE1__ })));
  }
  await axis("x", 992);
  await axis("y", 928);
  await axis("x", 1120);
  await page.keyboard.press("e");
  await page.waitForFunction(() => !document.querySelector("#dialog").hidden);
  await page.waitForTimeout(1300);
  await page.locator("#close-dialog").click();
  await page.keyboard.press("Space");
  await page.waitForTimeout(1500);
  visits.push(await page.evaluate(() => ({ ...window.__GATE1__ })));
  await cdp.send("Page.stopScreencast");
  await Promise.all(writes);
  await browser.close();
  await fs.writeFile(
    dir + "/frames.txt",
    frames
      .map(
        (f, i) =>
          `file '${f.name}'\nduration ${Math.max(0.001, (frames[i + 1]?.t ?? f.t + 0.1) - f.t)}`,
      )
      .join("\n") + "\n",
  );
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
      dir + "/frames.txt",
      "-fps_mode",
      "vfr",
      "-c:v",
      "libx264",
      "-threads",
      "2",
      "-preset",
      "fast",
      "-crf",
      "27",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "docs/gate1/GATE1_GAMEPLAY.mp4",
    ],
    { timeout: 120000 },
  );
  const proof = {
    source:
      "Actual normal-entry Phaser, no QA URL/hook/teleport/frame injection. Real keyboard at unchanged60/100 speeds, doors via E, crossing into public court, Space greeting. CDP actual timestamps, VFR, no speedup.",
    frames: frames.length,
    duration: frames.at(-1).t - frames[0].t,
    visits,
    errors,
  };
  await fs.writeFile(
    "docs/gate1/video-provenance.json",
    JSON.stringify(proof, null, 2) + "\n",
  );
  if (errors.length) throw Error(JSON.stringify(errors));
  console.log(
    JSON.stringify({ frames: frames.length, duration: proof.duration, errors }),
  );
} finally {
  await browser.close();
}
