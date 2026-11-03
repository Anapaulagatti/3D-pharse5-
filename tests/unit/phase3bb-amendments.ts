import newest from "../../docs/phase3bd/AUTHORIZED_AMENDMENTS.json";
import cleanup from "../../docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json";
import { existsSync, readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import latest from "../../docs/phase3bc/AUTHORIZED_AMENDMENTS.json";
import amendments from "../../docs/phase3bb-hotfix/AUTHORIZED_AMENDMENTS.json";
/** Exact successor hashes, not an ignore list. Old authority manifests are immutable. */
function priorAmendedHash(path: string, original: unknown): unknown {
  const row = (
    amendments.files as Record<
      string,
      { beforeSHA256: string; afterSHA256: string }
    >
  )[path];
  if (!row) {
    const next = (
      latest.files as Record<
        string,
        { beforeSHA256: string; afterSHA256: string }
      >
    )[path];
    if (next && next.beforeSHA256 !== original)
      throw Error("Phase3BC predecessor mismatch: " + path);
    return next?.afterSHA256 ?? original;
  }
  if (row.beforeSHA256 !== original)
    throw Error("Amendment predecessor mismatch: " + path);
  const next = (
    latest.files as Record<
      string,
      { beforeSHA256: string; afterSHA256: string }
    >
  )[path];
  if (next && next.beforeSHA256 !== row.afterSHA256)
    throw Error("Phase3BC predecessor mismatch: " + path);
  return next?.afterSHA256 ?? row.afterSHA256;
}

export function expectedAmendedHash(path: string, original: unknown): unknown {
  const prior = priorAmendedHash(path, original);
  const next = (
    newest.files as Record<
      string,
      { beforeSHA256: string; afterSHA256: string }
    >
  )[path];
  if (next && next.beforeSHA256 !== prior)
    throw Error("Phase3BD predecessor mismatch: " + path);
  return next?.afterSHA256 ?? prior;
}
const historicalBatch = new Map<string, Buffer>();
function loadHistoricalBatch() {
  const rows = cleanup.removed.filter(
    (r) => r.path.startsWith("public/assets/") || r.path.startsWith("src/"),
  );
  const data = execFileSync("git", ["cat-file", "--batch"], {
    input: rows.map((r) => cleanup.base + ":" + r.path + "\n").join(""),
    maxBuffer: rows.reduce((n, r) => n + r.bytes + 256, 1024 * 1024),
  });
  let offset = 0;
  for (const row of rows) {
    const end = data.indexOf(10, offset);
    const header = data.subarray(offset, end).toString().split(" ");
    if (header[1] !== "blob")
      throw Error("Missing preserved blob: " + row.path);
    const size = Number(header[2]);
    const bytes = data.subarray(end + 1, end + 1 + size);
    if (createHash("sha256").update(bytes).digest("hex") !== row.sha256)
      throw Error("Historical preimage mismatch: " + row.path);
    historicalBatch.set(row.path, bytes);
    offset = end + 1 + size + 1;
  }
}
export function readPreservedBytes(path: string): Buffer {
  if (existsSync(path)) return readFileSync(path);
  const removed = cleanup.removed.find((r) => r.path === path);
  if (!removed) {
    const moved = cleanup.archiveMoves.find((r) => r.from === path);
    if (!moved) throw Error("Missing unapproved path: " + path);
    const bytes = readFileSync(moved.to);
    if (createHash("sha256").update(bytes).digest("hex") !== moved.sha256)
      throw Error("Moved approved donor changed: " + path);
    return bytes;
  }
  if (!historicalBatch.size) loadHistoricalBatch();
  const old =
    historicalBatch.get(path) ??
    execFileSync("git", ["show", cleanup.base + ":" + path], {
      maxBuffer: 128 * 1024 * 1024,
    });
  if (createHash("sha256").update(old).digest("hex") !== removed.sha256)
    throw Error("Historical removed blob mismatch: " + path);
  return old;
}
