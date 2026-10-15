import { defineConfig } from "@playwright/test";
import { existsSync } from "node:fs";
export default defineConfig({
  testDir: "test/e2e",
  workers: 1,
  timeout: 45000,
  reporter: [
    ["list"],
    ["json", { outputFile: "quality-reports/pixel-v3.1/e2e-results.json" }],
  ],
  use: {
    baseURL: "http://127.0.0.1:4201/3D-pharse5-/",
    headless: true,
    launchOptions: {
      executablePath:
        process.env.PIXEL_CHROMIUM_PATH ??
        (existsSync("/usr/bin/chromium") ? "/usr/bin/chromium" : undefined),
      args: [
        "--no-sandbox",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader",
      ],
    },
    screenshot: "only-on-failure",
    video: "off",
  },
  webServer: {
    command: "npm run preview",
    url: "http://127.0.0.1:4201/3D-pharse5-/",
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
