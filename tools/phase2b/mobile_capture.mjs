import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const rows = [];
try {
  for (const [w, h] of [
    [844, 390],
    [667, 375],
  ]) {
    const c = await b.newContext({
        viewport: { width: w, height: h },
        deviceScaleFactor: 3,
        isMobile: true,
        hasTouch: true,
      }),
      p = await c.newPage();
    await p.goto("http://127.0.0.1:4325/3D-pharse5-/?renderer=canvas");
    await p.locator("#character-selection").waitFor();
    await p.waitForTimeout(300);
    await p.screenshot({
      path: `docs/phase2b/mobile-${w}x${h}-gallery-top.jpg`,
      type: "jpeg",
      quality: 82,
    });
    for (const id of ["sori", "jiwon", "nari", "taeyang", "yuna", "hyunwoo"])
      await p.locator(`[data-character="${id}"]`).tap();
    await p.locator('[data-action="run"]').tap();
    await p.waitForTimeout(300);
    await p.screenshot({
      path: `docs/phase2b/mobile-${w}x${h}-gallery-bottom.jpg`,
      type: "jpeg",
      quality: 82,
    });
    const fit = await p.evaluate(() => ({
      viewport: [window.innerWidth, window.innerHeight],
      count: document.querySelectorAll("[data-character]").length,
      scrollTop: document.querySelector(".studio-gallery-column").scrollTop,
      overflow:
        document.querySelector("#character-selection").scrollWidth >
        document.querySelector("#character-selection").clientWidth,
      preview: (() => {
        const r = document
            .querySelector("#character-preview")
            .getBoundingClientRect(),
          a = document.querySelector("#character-art").getBoundingClientRect();
        return {
          width: r.width,
          height: r.height,
          inside:
            r.x >= a.x &&
            r.y >= a.y &&
            r.right <= a.right &&
            r.bottom <= a.bottom,
        };
      })(),
    }));
    if (
      fit.count !== 12 ||
      fit.overflow ||
      !fit.preview.inside ||
      fit.preview.width !== 96 ||
      fit.preview.height !== 112
    )
      throw Error("Mobile geometry");
    await p.locator("#character-confirm").tap();
    await p.waitForFunction(
      () =>
        window.__GATE3__?.ready && window.__GATE3__.characterId === "hyunwoo",
    );
    const start = await p.evaluate(() => window.__GATE3__.x),
      cdp = await c.newCDPSession(p),
      box = await p.locator("#joystick").boundingBox(),
      x = box.x + box.width / 2,
      y = box.y + box.height / 2;
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [{ x, y, id: 1 }],
    });
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: x + 30, y, id: 1 }],
    });
    await p.waitForFunction((x) => window.__GATE3__.x > x + 8, start);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    rows.push({ fit, actualTouchJoystick: "PASS", physicalHardware: false });
    await c.close();
  }
  await fs.writeFile(
    "docs/phase2b/mobile-browser.json",
    JSON.stringify(
      {
        rows,
        method:
          "Chromium touch emulation at DPR3; no actual Android/iPhone device evidence",
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
