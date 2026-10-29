import fs from "node:fs/promises";
import { spawnSync } from "node:child_process";
const rows = [];
for (const [name, args, env, output] of [
  [
    "portal-public-exposure",
    ["tools/review-portal/build.mjs"],
    { REVIEW_EXPOSURE: "public", REVIEW_OUT: ".cache/blocked-review-public" },
    ".cache/blocked-review-public",
  ],
  [
    "canonical-public-rights",
    [
      "node_modules/vite/bin/vite.js",
      "build",
      "--mode",
      "public",
      "--outDir",
      ".cache/blocked-game-public",
    ],
    {},
    ".cache/blocked-game-public",
  ],
  [
    "unsafe-review-base",
    ["tools/review-portal/build.mjs"],
    {
      VITE_REVIEW_BASE: "https://unapproved.invalid/",
      REVIEW_OUT: ".cache/blocked-review-base",
    },
    ".cache/blocked-review-base",
  ],
]) {
  const r = spawnSync(process.execPath, args, {
    env: { ...process.env, ...env },
    encoding: "utf8",
  });
  const exists = await fs.access(output).then(
    () => true,
    () => false,
  );
  if (r.status === 0 || exists)
    throw Error("Gate emitted unauthorized output: " + name);
  rows.push({
    name,
    exitCode: r.status,
    outputExists: exists,
    diagnostic:
      (r.stderr + r.stdout).slice(0, 2200) +
      "\n…\n" +
      (r.stderr + r.stdout).slice(-300),
    status: "PASS expected rejection",
  });
}
await fs.writeFile(
  "docs/review-portal/EXPOSURE_GATES.json",
  JSON.stringify(
    {
      status: "PASS",
      rows,
      publicExposure: "NOT_APPROVED",
      commercial: "BLOCKED_PENDING_REVIEW",
    },
    null,
    2,
  ) + "\n",
);
