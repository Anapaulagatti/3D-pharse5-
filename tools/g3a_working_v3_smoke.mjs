import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const errors = [],
  b = await chromium.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto("http://127.0.0.1:4290/");
  const links = await p.locator("a").evaluateAll((a) => a.map((x) => x.href));
  for (const u of links) {
    const r = await p.request.get(u);
    if (!r.ok()) throw Error(u);
  }
  await p.goto(
    "http://127.0.0.1:4290/gate3-review.html?scene=registration-working-v3&entry=station&native&pixelAudit",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  await p.keyboard.down("s");
  await p.waitForFunction(() => window.__GATE3__.y >= 2855);
  await p.keyboard.up("s");
  const audit = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    "/tmp/working-v3-package-native.png",
    Buffer.from(audit.png.split(",")[1], "base64"),
  );
  delete audit.png;
  const checks = await p.evaluate(() => ({
    scene: window.__GATE3__.scene,
    renderer: window.__GATE3__.renderer,
    transferGuardClosed: !window.__GATE3_TEST__.walkable(2954, 2690),
    stationAisle: window.__GATE3_TEST__.walkable(2598.5, 2610),
  }));
  if (
    checks.scene !== "registration-working-v3" ||
    !checks.transferGuardClosed ||
    !checks.stationAisle
  )
    throw Error(JSON.stringify(checks));
  await p.goto(
    "http://127.0.0.1:4290/gate3-review.html?scene=registration-working-v3&entry=platform&native",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
  );
  await p.keyboard.down("w");
  await p.waitForFunction(() => window.__GATE3__.y < 2600);
  await p.keyboard.up("w");
  if (errors.length) throw Error(errors.join("\n"));
  await fs.writeFile(
    "docs/g3a-controlled-finalization/package-smoke.json",
    JSON.stringify(
      {
        status: "PASS",
        linksChecked: links.length,
        errors,
        checks,
        audit,
        actualPlatformMovement: "PASS original W key",
        physicalDevices: "NOT TESTED",
        stationTransfer: "BLOCKED / retained source edge",
      },
      null,
      2,
    ),
  );
  console.log(
    "PASS extracted-package links, native WebGL load, original platform movement and retained collision lock",
  );
} finally {
  await b.close();
}
