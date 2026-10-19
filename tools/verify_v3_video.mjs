import { chromium } from "playwright";
import fs from "node:fs/promises";
import crypto from "node:crypto";
import { spawn } from "node:child_process";
const dir = "docs/v3-final/quality";
const server = spawn(
  "python3",
  ["-m", "http.server", "4210", "--bind", "127.0.0.1", "--directory", dir],
  { stdio: "ignore" },
);
let browser;
const errors = [],
  results = [];
try {
  for (let i = 0; i < 100; i++) {
    try {
      if (
        (
          await fetch(
            "http://127.0.0.1:4210/mobile-gameplay-video-verification.json",
          )
        ).ok
      )
        break;
    } catch {
      /* owned server readiness */
    }
    if (i === 99) throw Error("Video server not ready");
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  for (const file of ["mobile-gameplay.mp4", "multi-district-traversal.mp4"]) {
    const p = await browser.newPage({ viewport: { width: 844, height: 390 } });
    p.on("pageerror", (e) => errors.push(e.message));
    p.on("console", (m) => {
      if (m.type() === "error") errors.push(m.text());
    });
    await p.route("**/favicon.ico", (route) => route.fulfill({ status: 204 }));
    await p.goto("http://127.0.0.1:4210/");
    await p.evaluate(async (file) => {
      document.body.style = "margin:0;background:black";
      document.body.innerHTML = "";
      const v = document.createElement("video");
      v.id = "video";
      v.muted = true;
      v.playsInline = true;
      v.style = "width:844px;height:390px;object-fit:contain";
      v.src = URL.createObjectURL(await (await fetch(file)).blob());
      document.body.append(v);
    }, file);
    await p.waitForFunction(
      () => document.querySelector("video").readyState >= 2,
    );
    const start = await p.evaluate(async () => {
      const v = document.querySelector("video");
      v.currentTime = 5;
      await new Promise((r) => v.addEventListener("seeked", r, { once: true }));
      if (Math.abs(v.currentTime - 5) > 0.1)
        throw Error("Video seek5 did not reach actual time: " + v.currentTime);
      await v.play();
      return v.currentTime;
    });
    const firstPixels = await p.evaluate(() => {
      const c = document.createElement("canvas");
      c.width = 844;
      c.height = 390;
      c.getContext("2d").drawImage(document.querySelector("video"), 0, 0);
      return c.toDataURL();
    });
    await p.waitForTimeout(2200);
    const lastPixels = await p.evaluate(() => {
      const c = document.createElement("canvas");
      c.width = 844;
      c.height = 390;
      c.getContext("2d").drawImage(document.querySelector("video"), 0, 0);
      return c.toDataURL();
    });
    if (firstPixels === lastPixels)
      throw Error("Decoded video pixels do not move");
    const state = await p.evaluate(() => {
      const v = document.querySelector("video");
      return {
        currentTime: v.currentTime,
        duration: v.duration,
        width: v.videoWidth,
        height: v.videoHeight,
        paused: v.paused,
        error: v.error?.message ?? null,
        quality: v.getVideoPlaybackQuality().totalVideoFrames,
      };
    });
    if (state.currentTime < start + 1.5 || state.error || state.paused)
      throw Error("Actual video playback failed " + JSON.stringify(state));
    await p.evaluate(() => document.querySelector("video").pause());
    if (file.endsWith(".mp4"))
      for (const sec of file.startsWith("mobile")
        ? [2, 8, 15, 20]
        : await p.evaluate(() =>
            [0.1, 0.35, 0.65, 0.9].map(
              (q) =>
                Math.round(
                  document.querySelector("video").duration * q * 1000,
                ) / 1000,
            ),
          )) {
        await p.evaluate(async (sec) => {
          const v = document.querySelector("video");
          v.currentTime = sec;
          await new Promise((r) =>
            v.addEventListener("seeked", r, { once: true }),
          );
          if (Math.abs(v.currentTime - sec) > 0.1)
            throw Error(
              "Seek actual time differs: " + v.currentTime + " vs " + sec,
            );
        }, sec);
        await p.evaluate(() => {
          const v = document.querySelector("video");
          let c = document.querySelector("#decoded");
          if (!c) {
            c = document.createElement("canvas");
            c.id = "decoded";
            c.width = 844;
            c.height = 390;
            c.style = "position:fixed;inset:0;width:844px;height:390px";
            document.body.append(c);
          }
          c.getContext("2d").drawImage(v, 0, 0);
        });
        await p.screenshot({ path: `${dir}/decoded-${file}-${sec}s.png` });
      }
    results.push({
      file,
      ...state,
      decodedPixelsChanged: true,
      firstPixelHash: crypto
        .createHash("sha256")
        .update(firstPixels)
        .digest("hex"),
      lastPixelHash: crypto
        .createHash("sha256")
        .update(lastPixels)
        .digest("hex"),
    });
    await p.close();
  }
  if (errors.length) throw Error(JSON.stringify(errors));
  await fs.writeFile(
    `${dir}/video-playback.json`,
    JSON.stringify(
      {
        status: "PASS",
        method:
          "Actual Chromium HTMLVideoElement decoding, seek and >1.5s of observed playback for both new H264 real-gameplay clips. Decoded frame pixels must differ during actual playback. MP4 screenshots draw the HTMLVideoElement into Canvas because headless video overlay screenshots stayed stale; these are decoded frames, not source stills. Harness favicon is explicitly served204; full HTTP-downloaded Blob enables seeking without requiring Python-server Range support. Every requested seek checks actual currentTime.",
        results,
        errors,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(JSON.stringify({ results, errors }));
} finally {
  if (browser) await browser.close();
  server.kill("SIGINT");
}
