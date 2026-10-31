import { chromium } from "playwright";
import fs from "node:fs/promises";
import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
const root = process.cwd() + "/docs/v9-world/quality/video";
const server = createServer(async (req, res) => {
  if (req.url === "/favicon.ico") {
    res.writeHead(204);
    res.end();
    return;
  }
  if (req.url !== "/v9-gameplay.mp4") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end("<!doctype html><title>Actual video playback verification</title>");
    return;
  }
  const path = root + "/v9-gameplay.mp4",
    stat = await fs.stat(path),
    range = req.headers.range;
  let start = 0,
    end = stat.size - 1;
  if (range) {
    const match = /bytes=(\d+)-(\d*)/.exec(range);
    if (!match) {
      res.writeHead(416);
      res.end();
      return;
    }
    start = Number(match[1]);
    end = match[2] ? Number(match[2]) : end;
  }
  const headers = {
    "Content-Type": "video/mp4",
    "Accept-Ranges": "bytes",
    "Content-Length": end - start + 1,
  };
  if (range) headers["Content-Range"] = `bytes ${start}-${end}/${stat.size}`;
  res.writeHead(range ? 206 : 200, headers);
  createReadStream(path, { start, end }).pipe(res);
});
await new Promise((resolve) => server.listen(4284, "127.0.0.1", resolve));
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch("http://127.0.0.1:4284/")).ok) break;
    } catch {
      /* task-owned server starting */
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    executablePath: process.env.PIXEL_CHROMIUM_PATH ?? "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu-compositing"],
  });
  const page = await browser.newPage({
    viewport: { width: 1280, height: 960 },
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("http://127.0.0.1:4284/");
  await page.setContent(
    '<video id="v" src="http://127.0.0.1:4284/v9-gameplay.mp4" controls muted playsinline style="width:1280px;height:960px"></video><canvas id="c" width="1280" height="960" hidden></canvas>',
  );
  await page.waitForFunction(
    () => document.querySelector("video").readyState >= 2,
  );
  const duration = await page.locator("video").evaluate((v) => v.duration);
  await page.locator("video").evaluate((v) => v.play());
  await page.waitForTimeout(1800);
  const played = await page.locator("video").evaluate((v) => v.currentTime);
  assert(played > 1);
  await page.locator("video").evaluate((v) => v.pause());
  const rows = [];
  for (const fraction of [0.03, 0.24, 0.5, 0.77, 0.94]) {
    const time = duration * fraction;
    await page.locator("video").evaluate((v, t) => {
      v.currentTime = t;
    }, time);
    await page.waitForFunction((t) => {
      const v = document.querySelector("video");
      return (
        !v.seeking && Math.abs(v.currentTime - t) < 0.15 && v.readyState >= 2
      );
    }, time);
    const png = await page.evaluate(() => {
      const v = document.querySelector("video"),
        c = document.querySelector("canvas");
      c.getContext("2d").drawImage(v, 0, 0);
      return c.toDataURL();
    });
    const bytes = Buffer.from(png.split(",")[1], "base64");
    const name = `decoded-${Math.round(fraction * 100)}.png`;
    await fs.writeFile(root + "/" + name, bytes);
    rows.push({
      fraction,
      time,
      file: name,
      sha256: createHash("sha256").update(bytes).digest("hex"),
    });
  }
  assert.equal(new Set(rows.map((r) => r.sha256)).size, rows.length);
  assert.deepEqual(errors, []);
  const proof = {
    status: "PASS",
    method:
      "Actual Chromium HTMLVideo playback, elapsed playback>1s,5real seeks and different decoded frame pixels. Representative frames inspected separately; no every-frame visual-review claim.",
    duration,
    playedSeconds: played,
    rows,
    errors,
  };
  await fs.writeFile(
    root + "/browser-playback.json",
    JSON.stringify(proof, null, 2),
  );
  const encoding = JSON.parse(
    await fs.readFile(root + "/encoding-verification.json", "utf8"),
  );
  encoding.playbackVerified = true;
  await fs.writeFile(
    root + "/encoding-verification.json",
    JSON.stringify(encoding, null, 2) + "\n",
  );
  console.log(
    "Actual video playback/5seeks/moving decoded pixels PASS",
    duration,
  );
} finally {
  if (browser) await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
