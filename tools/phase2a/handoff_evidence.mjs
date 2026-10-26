import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2a",
  BASE = "http://127.0.0.1:4325/3D-pharse5-/",
  V1 = "korean-arena-player-preferences-v1",
  V2 = "korean-arena-appearance-preferences-v2";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox", "--enable-precise-memory-info"],
});
const ready = (p) =>
  p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
const state = (p) =>
  p.evaluate(
    ({ V1, V2 }) => ({
      actor: window.__GATE3__.characterId,
      appearance: window.__GATE3__.appearance,
      position: [window.__GATE3__.x, window.__GATE3__.y],
      visited: window.__GATE3__.visited,
      players: window.__GATE3__.playerSprites,
      caches: window.__GATE3__.characterAssets,
      v1: localStorage.getItem(V1),
      v2: localStorage.getItem(V2),
      lessonFixture: localStorage.getItem("phase2a-lesson-sentinel"),
      heap: performance.memory
        ? {
            used: performance.memory.usedJSHeapSize,
            total: performance.memory.totalJSHeapSize,
            limit: performance.memory.jsHeapSizeLimit,
          }
        : null,
    }),
    { V1, V2 },
  );
async function open(p) {
  if (!(await p.locator("#character-open").isVisible()))
    await p.locator("#settings summary").click();
  await p.locator("#character-open").click();
  await p.locator("#character-selection").waitFor();
}
async function apply(p, enter = false) {
  await p.locator(enter ? "#character-confirm" : "#appearance-save").click();
  if (enter)
    await p.locator("#character-selection").waitFor({ state: "hidden" });
  else
    await p.waitForFunction(() =>
      document
        .querySelector("#character-feedback")
        .textContent.includes("Đã lưu"),
    );
  await p.waitForFunction((V2) => {
    const saved = JSON.parse(localStorage.getItem(V2)),
      a = window.__GATE3__;
    return (
      a?.ready &&
      saved &&
      a.characterId === saved.selectedCharacterId &&
      JSON.stringify(a.appearance) ===
        JSON.stringify(saved.appearances[a.characterId])
    );
  }, V2);
}
try {
  const c = await b.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await c.addInitScript(
    ({ V1 }) => {
      if (!localStorage.getItem(V1)) {
        localStorage.setItem(
          V1,
          JSON.stringify({ version: 1, characterId: "haneul" }),
        );
        localStorage.setItem("phase2a-lesson-sentinel", "KEEP_FIXTURE_ONLY");
      }
    },
    { V1 },
  );
  const p = await c.newPage();
  await p.goto(BASE + "?renderer=canvas&pixelAudit");
  await ready(p);
  const legacy = await state(p);
  if (legacy.v2 !== null || legacy.actor !== "haneul")
    throw Error("v1 read altered");
  await p.keyboard.press("e");
  await p.locator("#dialog").waitFor();
  await p.locator("#close").click();
  const before = await state(p);
  if (!before.visited.length) throw Error("No real visit");
  await open(p);
  await p.locator("#appearance-preset").selectOption("review-ara-harbor");
  await p.locator("#appearance-preset-name").fill("Dạo biển · local");
  await apply(p, true);
  const applied = await state(p);
  await p.reload();
  await ready(p);
  const restored = await state(p);
  if (
    JSON.stringify(applied.appearance) !==
      JSON.stringify(restored.appearance) ||
    JSON.stringify(before.position) !== JSON.stringify(restored.position) ||
    JSON.stringify(before.visited) !== JSON.stringify(restored.visited) ||
    restored.lessonFixture !== "KEEP_FIXTURE_ONLY"
  )
    throw Error("State restore failure");
  await fs.writeFile(
    `${D}/persistence-evidence.json`,
    JSON.stringify(
      {
        method:
          "Real v1-only startup, real E exploration visit, Studio preset applied through UI, actual reload; sentinel is only a fixture, no real learning service/account is connected.",
        legacy,
        before,
        applied,
        restored,
        status: "PASS",
      },
      null,
      2,
    ),
  );
  await open(p);
  const client = await c.newCDPSession(p);
  await client.send("HeapProfiler.collectGarbage");
  const memoryBefore = await state(p),
    observations = [];
  for (let i = 0; i < 24; i++) {
    if (i % 6 === 5)
      await p
        .locator(
          `[data-character="${["juni", "haneul", "bomi", "minjun"][Math.floor(i / 6)]}"]`,
        )
        .click();
    else
      await p
        .locator("#appearance-preset")
        .selectOption(
          [
            "review-ara-harbor",
            "review-ara-sunlit",
            "review-doyun-field",
            "review-doyun-varsity",
          ][i % 4],
        );
    await apply(p);
    const s = await state(p);
    if (
      s.players !== 1 ||
      s.caches.textures.length > 3 ||
      s.caches.composition.baseImages > 2 ||
      s.caches.composition.compositeImages > 2 ||
      JSON.stringify(s.position) !== JSON.stringify(before.position)
    )
      throw Error("Unbounded cache/state");
    observations.push(s);
  }
  await client.send("HeapProfiler.collectGarbage");
  const memoryAfter = await state(p);
  await fs.writeFile(
    `${D}/memory-observations.json`,
    JSON.stringify(
      {
        environment:
          "Desktop headless Chromium, Canvas, Studio open (world paused); precise-memory flag and explicit GC used before/after. Values do not certify mobile hardware or WebGL performance.",
        memoryBefore,
        observations,
        memoryAfter,
        steadyActorTextureCap: 3,
        temporaryLoadAllowance: 1,
        compositeCacheCap: 2,
        basePreviewCacheCap: 2,
        estimates:
          "width*height*4 RGBA bytes per owner, not a complete VRAM/browser-memory measurement. CanvasTexture readback buffers, patch decode, browser image cache and frozen-world resources add overhead.",
        physicalAndroid: "NOT TESTED",
        physicalIPhoneSafari: "NOT TESTED",
      },
      null,
      2,
    ),
  );
  await c.close();
  for (const [name, width, height] of [
    ["mobile-landscape", 844, 390],
    ["small-landscape", 667, 375],
  ]) {
    const m = await b.newContext({
      viewport: { width, height },
      deviceScaleFactor: 3,
      isMobile: true,
      hasTouch: true,
    });
    await m.addInitScript(
      (V1) =>
        localStorage.setItem(
          V1,
          JSON.stringify({ version: 1, characterId: "ara" }),
        ),
      V1,
    );
    const page = await m.newPage();
    await page.goto(BASE + "?renderer=canvas");
    await ready(page);
    await open(page);
    await page.locator("#appearance-preset").selectOption("review-ara-sunlit");
    await apply(page);
    await page.locator('[data-action="run"]').tap();
    await page.waitForTimeout(300);
    await page.screenshot({
      path: `${D}/${name}-studio-browser.jpg`,
      type: "jpeg",
      quality: 84,
      scale: "css",
    });
    const geometry = await page.evaluate(() => ({
      viewport: [window.innerWidth, window.innerHeight],
      preview: [
        document.querySelector("#character-preview").width,
        document.querySelector("#character-preview").height,
      ],
      buttons: [
        ...document.querySelectorAll(
          "#character-confirm,#appearance-save,#appearance-reset,#character-preview-direction",
        ),
      ].map((e) => ({
        id: e.id,
        x: e.getBoundingClientRect().x,
        y: e.getBoundingClientRect().y,
        w: e.getBoundingClientRect().width,
        h: e.getBoundingClientRect().height,
      })),
      physicalDevice: false,
    }));
    await fs.writeFile(
      `${D}/${name}-browser-geometry.json`,
      JSON.stringify(geometry, null, 2),
    );
    await m.close();
  }
} finally {
  await b.close();
}
