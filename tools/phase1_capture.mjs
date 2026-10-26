import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase1",
  key = "korean-arena-player-preferences-v1",
  rows = [],
  errors = [];
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const c = await browser.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await c.addInitScript(
    (key) =>
      localStorage.setItem(
        key,
        JSON.stringify({ version: 1, characterId: "juni" }),
      ),
    key,
  );
  const p = await c.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  for (const renderer of ["canvas", "webgl"])
    for (const entry of ["palace-front-local", "station-all", "bridge-a-full"])
      for (const phase of ["before", "after"]) {
        const url =
          phase === "before"
            ? `http://127.0.0.1:4321/gate3-review.html?scene=palace-cleanup-world&entry=${entry}&native&pixelAudit&renderer=${renderer}`
            : `http://127.0.0.1:4320/3D-pharse5-/?entry=${entry}&native&pixelAudit&renderer=${renderer}`;
        await p.goto(url);
        await p.waitForFunction(
          () =>
            window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
          {},
          { timeout: 45000 },
        );
        const audit = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
        const file = `${entry}-${renderer}-${phase}-native-1x.png`;
        await fs.writeFile(
          `${D}/${file}`,
          Buffer.from(audit.png.split(",")[1], "base64"),
        );
        delete audit.png;
        rows.push({ entry, renderer, phase, file, audit });
        console.log(file);
      }
  await c.close();
  const ui = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
  });
  const page = await ui.newPage();
  await page.goto("http://127.0.0.1:4320/3D-pharse5-/");
  await page.locator("#character-selection").waitFor();
  await page.screenshot({
    path: `${D}/selection-desktop.jpg`,
    type: "jpeg",
    quality: 85,
  });
  for (const id of ["haneul", "bomi", "minjun"]) {
    await page.locator(`[data-character="${id}"]`).click();
    await page.locator("#character-master").waitFor();
    await page.waitForFunction(
      () => document.querySelector("#character-master").complete,
    );
    await page.screenshot({
      path: `${D}/selection-${id}-incomplete.jpg`,
      type: "jpeg",
      quality: 85,
    });
  }
  await ui.close();
  const mobile = await browser.newContext({
    viewport: { width: 844, height: 390 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
  });
  const m = await mobile.newPage();
  await m.goto("http://127.0.0.1:4320/3D-pharse5-/");
  await m.locator("#character-selection").waitFor();
  await m.screenshot({
    path: `${D}/selection-mobile-landscape.jpg`,
    type: "jpeg",
    quality: 75,
  });
  await mobile.close();
  await fs.writeFile(
    `${D}/native-captures.json`,
    JSON.stringify(
      {
        rows,
        errors,
        method:
          "Actual Phaser POST_RENDER native1x before accepted ZIP /after actual production index, same entry/camera/DPR1, Canvas and WebGL. Browser JPEGs separately labelled UI reviews.",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join(";"));
} finally {
  await browser.close();
}
