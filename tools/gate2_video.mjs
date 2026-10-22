import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { ready, state, grid, walk } from "./gate2_browser_lib.mjs";
const proofs = process.argv[2]
  ? JSON.parse(
      await fs.readFile("docs/gate2/video-provenance.json", "utf8"),
    ).filter((r) => r.scene !== process.argv[2])
  : [];
for (const id of process.argv[2] ? [process.argv[2]] : ["a", "b", "c"]) {
  const dir = `.cache/gate2/video-${id}`;
  await fs.mkdir(dir, { recursive: true });
  const browser = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-gpu-compositing",
      "--disable-background-timer-throttling",
    ],
  });
  const p = await browser.newPage({
    viewport: { width: 1280, height: 980 },
    deviceScaleFactor: 1,
  });
  const frames = [],
    writes = [],
    routes = [],
    errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  try {
    await ready(p, id);
    if (await p.evaluate(() => !!window.__GATE2_TEST__))
      throw Error("QA exposed");
    const g = await grid(p),
      cdp = await p.context().newCDPSession(p);
    cdp.on("Page.screencastFrame", (e) => {
      const name = String(frames.length).padStart(6, "0") + ".jpg";
      frames.push({ name, t: e.metadata.timestamp });
      writes.push(
        fs.writeFile(dir + "/" + name, Buffer.from(e.data, "base64")),
      );
      void cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId });
    });
    await cdp.send("Page.startScreencast", {
      format: "jpeg",
      quality: 90,
      maxWidth: 1280,
      maxHeight: 980,
      everyNthFrame: 3,
    });
    await p.waitForTimeout(900);
    const points = {
      a: [
        [730, 750],
        [1408, 290],
      ],
      b: [
        [598, 580],
        [888, 580],
        [1288, 580],
        [1120, 928],
      ],
      c: [
        [460, 570],
        [780, 880],
        [410, 1210],
      ],
    }[id];
    for (const target of points) {
      routes.push(await walk(p, g, target));
      await p.keyboard.press("e");
      await p.waitForTimeout(750);
      await p.locator("#close").click();
    }
    await p.keyboard.press("Space");
    await p.waitForTimeout(1400);
    const end = await state(p);
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
        "23",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        `docs/gate2/${id.toUpperCase()}_GAMEPLAY.mp4`,
      ],
      { timeout: 120000 },
    );
    proofs.push({
      scene: id,
      frames: frames.length,
      duration: frames.at(-1).t - frames[0].t,
      routes,
      end,
      errors,
      source:
        "Actual normal-entry Phaser; real keys; 60/100 px/s; no QA hook, placement, frame injection or speedup; CDP timestamps retained; VFR encoding",
    });
    await fs.writeFile(
      "docs/gate2/video-provenance.json",
      JSON.stringify(proofs, null, 2) + "\n",
    );
    console.log(JSON.stringify(proofs.at(-1)));
  } finally {
    await browser.close();
  }
}
