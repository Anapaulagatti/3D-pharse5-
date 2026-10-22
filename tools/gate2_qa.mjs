import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import assert from "node:assert/strict";
import { ready, state, grid, walk, capture } from "./gate2_browser_lib.mjs";
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--disable-gpu-compositing",
    "--disable-background-timer-throttling",
  ],
});
const rows = process.argv[2]
    ? JSON.parse(
        await fs.readFile("docs/gate2/browser-qa.json", "utf8"),
      ).rows.filter((r) => r.scene !== process.argv[2])
    : [],
  errors = [],
  requests = new Set();
async function page(extra = {}) {
  const p = await browser.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
    ...extra,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(r.url());
  });
  p.on("request", (r) => requests.add(new URL(r.url()).pathname));
  return p;
}
try {
  for (const id of process.argv[2]
    ? [process.argv[2]]
    : ["a", "b", "c", "transition", "station"]) {
    const p = await page();
    await ready(p, id);
    assert.equal(
      await p.evaluate(() => typeof window.__GATE2_TEST__),
      "undefined",
    );
    assert.equal((await state(p)).samplingMode, 1);
    const x = (await state(p)).x;
    await p.keyboard.down("ArrowRight");
    await p.waitForTimeout(300);
    await p.keyboard.up("ArrowRight");
    assert((await state(p)).x > x + 7);
    rows.push({
      case: "Normal entry/no placement hook/keyboard/native sampling",
      scene: id,
      pass: true,
    });
    await ready(p, id, "&qa");
    const d = JSON.parse(
        await fs.readFile(`public/assets/gate2/${id}/scene.json`, "utf8"),
      ),
      g = await grid(p),
      routes = [];
    for (const t of d.targets) {
      routes.push({ target: t.id, ...(await walk(p, g, [t.x, t.y])) });
      await p.keyboard.press("e");
      await p.waitForFunction(() => !document.querySelector("#dialog").hidden);
      await p.waitForFunction(
        (id) => window.__GATE2__.visited.includes(id),
        t.id,
      );
      await p.locator("#close").click();
    }
    rows.push({
      case: "All destinations reached with continuous actual input and E interactions",
      scene: id,
      pass: true,
      routes,
    });
    await p.locator("#pause").click();
    const before = await state(p);
    await p.keyboard.down("ArrowLeft");
    await p.waitForTimeout(300);
    await p.keyboard.up("ArrowLeft");
    const after = await state(p);
    assert(Math.hypot(after.x - before.x, after.y - before.y) < 0.1);
    await p.locator("#pause").click();
    rows.push({ case: "Pause freezes movement", scene: id, pass: true });
    const scalePoint = {
      a: [730, 750],
      b: [888, 580],
      c: [410, 1210],
      transition: [850, 630],
      station: [360, 430],
    }[id];
    await p.evaluate(([x, y]) => window.__GATE2_TEST__.place(x, y), scalePoint);
    await p.waitForTimeout(100);
    await capture(p, `docs/gate2/${id.toUpperCase()}_ARCHITECTURE_1X.png`);
    await p.close();
    const m = await page({
      viewport: { width: 844, height: 390 },
      isMobile: true,
      hasTouch: true,
    });
    await ready(m, id);
    const start = await state(m),
      box = await m.locator("#joystick").boundingBox(),
      cdp = await m.context().newCDPSession(m);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchStart",
      touchPoints: [
        { x: box.x + box.width / 2 + 32, y: box.y + box.height / 2 },
      ],
    });
    await m.waitForTimeout(900);
    await cdp.send("Input.dispatchTouchEvent", {
      type: "touchEnd",
      touchPoints: [],
    });
    assert((await state(m)).x > start.x + 15);
    await capture(m, `docs/gate2/${id.toUpperCase()}_MOBILE.png`);
    rows.push({
      case: "Mobile landscape actual CDP joystick touch",
      scene: id,
      pass: true,
    });
    await m.close();
  }
  for (const [id, pairs] of [
    [
      "b",
      [
        [1216, 848],
        [1216, 896],
      ],
    ],
    [
      "c",
      [
        [780, 880],
        [780, 1005],
      ],
    ],
  ]) {
    const p = await page();
    await ready(p, id, "&qa");
    const values = [];
    for (const pt of pairs) {
      await p.evaluate(([x, y]) => window.__GATE2_TEST__.place(x, y), pt);
      await p.waitForTimeout(100);
      values.push(await state(p));
    }
    assert(values[0].behind.length > 0);
    assert.notDeepEqual(values[0].behind, values[1].behind);
    rows.push({
      case: "Native support-root Y-sort and sensible occlusion transition",
      scene: id,
      pass: true,
      values,
    });
    await p.close();
  }
  assert.equal(errors.length, 0, JSON.stringify(errors));
  assert(![...requests].some((r) => /assets\/(v[0-9]|world)\//.test(r)));
  await fs.writeFile(
    "docs/gate2/browser-qa.json",
    JSON.stringify(
      {
        rows: [
          ...new Map(rows.map((r) => [r.scene + "/" + r.case, r])).values(),
        ],
        errors,
        requests: [...requests].sort(),
        limits: [
          "Headless software Canvas and emulated mobile, no hardware performance claim",
          "QA starts only after normal-entry checks; destination traversal uses actual keys",
          "Independent slices; no approved full-world integration or human artistic approval claimed",
        ],
      },
      null,
      2,
    ) + "\n",
  );
  console.log(JSON.stringify({ cases: rows.length, errors }));
} finally {
  await browser.close();
}
