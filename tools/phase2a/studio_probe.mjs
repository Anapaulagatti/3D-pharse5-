import { chromium } from "@playwright/test";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  for (const [name, w, h] of [
    ["desktop", 1280, 900],
    ["mobile", 844, 390],
    ["small", 667, 375],
  ]) {
    const c = await b.newContext({
      viewport: { width: w, height: h },
      deviceScaleFactor: 1,
    });
    const p = await c.newPage();
    p.on("pageerror", (e) => console.log("ERROR", e.message));
    await p.goto("http://127.0.0.1:4320/3D-pharse5-/");
    await p.locator("#character-selection").waitFor();
    await p.locator('[data-character="ara"]').click();
    await p.waitForTimeout(1600);
    await p.screenshot({ path: `/tmp/phase2a-studio-${name}.png` });
    console.log(
      name,
      await p
        .locator("#character-selection")
        .evaluate((d) => ({
          width: d.clientWidth,
          height: d.clientHeight,
          scroll: d.scrollHeight,
          screen: [innerWidth, innerHeight],
        })),
    );
    await c.close();
  }
} finally {
  await b.close();
}
