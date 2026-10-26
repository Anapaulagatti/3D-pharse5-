import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase1",
  base = "http://127.0.0.1:4324/",
  errors = [],
  rows = [];
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const c = await b.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  const p = await c.newPage();
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("response", (r) => {
    if (r.url().startsWith(base) && r.status() >= 400)
      errors.push(`${r.status()} ${r.url()}`);
  });
  await p.goto(base + "?native&entry=station-all&pixelAudit");
  await p.locator("#character-selection").waitFor();
  if (!(await p.locator("#character-confirm").isVisible()))
    throw Error("Native first-launch selection blocked");
  await p.locator("#character-confirm").click();
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 45000 },
  );
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  await fs.writeFile(
    `${D}/package-station-native-1x.png`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  rows.push({ case: "native-first-launch", audit: a });
  for (const entry of [
    "palace-axis-local",
    "station-all",
    "bridge-a-full",
    "bridge-b-full",
    "retail",
    "namsan",
    "amusement",
    "market",
    "jeju-culture",
  ]) {
    await p.goto(base + `?entry=${entry}`);
    await p.waitForFunction(
      () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
      {},
      { timeout: 45000 },
    );
    const state = await p.evaluate(() => window.__GATE3__);
    if (
      state.playerSprites !== 1 ||
      state.characterId !== "juni" ||
      state.scene !== "palace-cleanup-world" ||
      state.chunks.errors
    )
      throw Error("Invalid canonical package entry " + entry);
    rows.push({
      entry,
      characterId: state.characterId,
      sprites: state.playerSprites,
      scene: state.scene,
      errors: state.chunks.errors,
    });
    console.log("ZIP entry", entry, "PASS");
  }
  await fs.writeFile(
    `${D}/package-smoke.json`,
    JSON.stringify(
      {
        rows,
        errors,
        physicalDevices: "NOT TESTED",
        roster: "Juni only;3incomplete",
      },
      null,
      2,
    ),
  );
  if (errors.length) throw Error(errors.join(";"));
} finally {
  await b.close();
}
