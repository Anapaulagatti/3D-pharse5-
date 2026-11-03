import { describe, it, expect } from "vitest";
import { execFileSync, spawnSync } from "node:child_process";
import {
  readFileSync,
  existsSync,
  mkdtempSync,
  writeFileSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
const cleanup = JSON.parse(
  readFileSync("docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json", "utf8"),
) as {
  base: string;
  removed: { path: string; sha256: string; classification: string }[];
  retained: { path: string; sha256: string }[];
};
describe("approved world allowlist and real active-tree cleanup", () => {
  it("actually removes every confirmed unused rejected path while preserving documented approved-source exceptions", () => {
    expect(cleanup.removed.length).toBeGreaterThan(0);
    for (const r of cleanup.removed) {
      expect(r.classification).toBe("CONFIRMED_REJECTED_UNUSED");
      expect(existsSync(r.path), r.path).toBe(false);
    }
    for (const r of cleanup.retained)
      expect(
        createHash("sha256").update(readFileSync(r.path)).digest("hex"),
        r.path,
      ).toBe(r.sha256);
  });
  it("does not select a world by directory/query, copy all public assets, or build retired entrypoints", () => {
    const main = readFileSync("src/gate3/main.ts", "utf8"),
      vite = readFileSync("vite.config.ts", "utf8");
    expect(main).toContain('const id = "palace-cleanup-world"');
    expect(main).not.toContain('query.get("scene")');
    expect(vite).toContain("publicDir: false");
    expect(vite).not.toContain("v10-city-review");
  });
  it("rejects reintroduced old map content even renamed and placed in a different artifact location", () => {
    const d = mkdtempSync(join(tmpdir(), "pixel-world-guard-"));
    try {
      const image = cleanup.removed.find(
        (r) => r.path.includes("docs/v9-world/") && r.path.endsWith(".png"),
      )!;
      writeFileSync(
        join(d, "renamed-old-map.png"),
        execFileSync("git", ["show", cleanup.base + ":" + image.path], {
          maxBuffer: 128 * 1024 * 1024,
        }),
      );
      const r = spawnSync(
        "python3",
        ["tools/phase3bd/world_guard.py", "--artifact", d],
        { encoding: "utf8" },
      );
      expect(r.status).not.toBe(0);
      expect(r.stderr).toContain("rejected content hash");
    } finally {
      rmSync(d, { recursive: true, force: true });
    }
  });
});
