import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
const b = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const p = await b.newPage({
    viewport: { width: 1280, height: 1000 },
    deviceScaleFactor: 1,
  });
  await p.goto("http://127.0.0.1:4325/3D-pharse5-/?renderer=canvas");
  await p.locator("#character-selection").waitFor();
  await p.waitForTimeout(300);
  await p.screenshot({
    path: "docs/phase2b/studio-desktop-top.jpg",
    type: "jpeg",
    quality: 85,
  });
  await p.locator('[data-character="hyunwoo"]').click();
  await p.locator('[data-action="run"]').click();
  await p.waitForTimeout(300);
  await p.screenshot({
    path: "docs/phase2b/studio-desktop-bottom.jpg",
    type: "jpeg",
    quality: 85,
  });
  await fs.writeFile(
    "docs/phase2b/studio-desktop.json",
    JSON.stringify(
      {
        actualBrowser: true,
        viewport: [1280, 1000],
        galleryEntries: await p.locator("[data-character]").count(),
        selected: "hyunwoo",
        artApproval: "PENDING",
        physicalDevices: "NOT TESTED",
      },
      null,
      2,
    ),
  );
} finally {
  await b.close();
}
