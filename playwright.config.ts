import { defineConfig } from "@playwright/test";
import { existsSync } from "node:fs";
const previewPort = Number(process.env.PIXEL_PREVIEW_PORT ?? 4201);
export default defineConfig({
  testDir: "tests/e2e",
  workers: 1,
  timeout: 120000,
  reporter: [
    ["list"],
    [
      "json",
      {
        outputFile: `${process.env.PIXEL_REPORT_DIR ?? ".cache/browser"}/e2e-results.json`,
      },
    ],
  ],
  use: {
    baseURL: `http://127.0.0.1:${previewPort}/3D-pharse5-/`,
    headless: true,
    launchOptions: {
      executablePath:
        process.env.PIXEL_CHROMIUM_PATH ??
        (existsSync("/usr/bin/chromium") ? "/usr/bin/chromium" : undefined),
      args: [
        "--no-sandbox",
        "--disable-gpu-compositing",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader",
      ],
    },
    screenshot: "only-on-failure",
    video: "off",
  },
  webServer: {
    command: `npm run preview -- --port ${previewPort}`,
    url: `http://127.0.0.1:${previewPort}/3D-pharse5-/`,
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
