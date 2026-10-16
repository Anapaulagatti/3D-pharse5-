import { chromium } from "playwright";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
const server = spawn(
  "python3",
  [
    "-m",
    "http.server",
    "4203",
    "--bind",
    "127.0.0.1",
    "--directory",
    "docs/world-refinement/quality",
  ],
  { stdio: "ignore" },
);
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch("http://127.0.0.1:4203/capture.json")).ok) break;
    } catch {
      /* Owned HTTP startup. */
    }
    await new Promise((r) => setTimeout(r, 50));
  }
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const p = await browser.newPage({ viewport: { width: 1100, height: 850 } });
  const errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  await p.setContent(
    '<video muted controls width="1024" src="http://127.0.0.1:4203/gameplay-walkthrough.mp4"></video>',
  );
  await p.locator("video").evaluate((v) => v.play());
  await p.waitForFunction(
    () => document.querySelector("video").currentTime > 2,
  );
  const result = await p.locator("video").evaluate((v) => ({
    readyState: v.readyState,
    width: v.videoWidth,
    height: v.videoHeight,
    duration: v.duration,
    playedSeconds: v.currentTime,
    error: v.error?.message ?? null,
    quality: v.getVideoPlaybackQuality().toJSON?.() ?? {
      totalVideoFrames: v.getVideoPlaybackQuality().totalVideoFrames,
      droppedVideoFrames: v.getVideoPlaybackQuality().droppedVideoFrames,
    },
  }));
  if (
    result.error ||
    result.width !== 1024 ||
    result.height !== 768 ||
    result.quality.totalVideoFrames < 10
  )
    throw Error(JSON.stringify(result));
  await p.locator("video").evaluate((v) => {
    v.pause();
    v.currentTime = 12;
  });
  await p.waitForFunction(() => !document.querySelector("video").seeking);
  await p.locator("video").screenshot({
    path: "docs/world-refinement/quality/video-browser-playback.png",
  });
  await fs.writeFile(
    "docs/world-refinement/quality/video-browser-playback.json",
    JSON.stringify({ status: "PASS", ...result, errors }, null, 2),
  );
  console.log(result);
  if (errors.length) throw Error(JSON.stringify(errors));
} finally {
  if (browser) await browser.close();
  server.kill("SIGINT");
}
