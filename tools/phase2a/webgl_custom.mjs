import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const D = "docs/phase2a",
  catalog = JSON.parse(
    await fs.readFile(
      "assets-src/characters/phase2a/cosmetics/catalog.json",
      "utf8",
    ),
  ),
  look = catalog.presets[0].appearance;
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: [
    "--no-sandbox",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
try {
  const c = await browser.newContext({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await c.addInitScript((look) => {
    localStorage.setItem(
      "korean-arena-player-preferences-v1",
      JSON.stringify({ version: 1, characterId: "ara" }),
    );
    localStorage.setItem(
      "korean-arena-appearance-preferences-v2",
      JSON.stringify({
        version: 2,
        selectedCharacterId: "ara",
        appearances: { ara: look },
        presets: [],
      }),
    );
  }, look);
  const p = await c.newPage();
  await p.goto(
    "http://127.0.0.1:4325/3D-pharse5-/?native&pixelAudit&renderer=webgl&entry=transition",
  );
  await p.waitForFunction(
    () => window.__GATE3__?.ready && window.__GATE3__.chunks.inflight === 0,
    {},
    { timeout: 60000 },
  );
  const a = await p.evaluate(() => window.__GATE3_PIXEL_AUDIT__());
  if (
    a.state.renderer !== "WebGL" ||
    !a.state.characterAssets.activeKey.startsWith("studio-")
  )
    throw Error("No actual custom WebGL atlas");
  const file = "custom-ara-webgl-native.png";
  await fs.writeFile(
    `${D}/${file}`,
    Buffer.from(a.png.split(",")[1], "base64"),
  );
  delete a.png;
  const q = JSON.parse(await fs.readFile(`${D}/actual-gameplay.json`, "utf8"));
  q.rows = q.rows.filter((r) => r.mode !== "review-ara-harbor-webgl");
  q.rows.push({
    mode: "review-ara-harbor-webgl",
    id: "ara",
    action: "idle",
    view: "front",
    file,
    sourcePath: `${D}/${file}`,
    audit: a,
    observedFrames: [a.state.frame],
    trace: [],
  });
  q.softwareWebGL =
    "SwiftShader render smoke only; not hardware/mobile performance certification";
  await fs.writeFile(`${D}/actual-gameplay.json`, JSON.stringify(q, null, 2));
  await c.close();
  console.log(
    "Actual customized WebGL native screenshot captured; software only",
  );
} finally {
  await browser.close();
}
