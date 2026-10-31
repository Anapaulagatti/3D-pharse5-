import latest from "../../docs/phase3bc/AUTHORIZED_AMENDMENTS.json";
import amendments from "../../docs/phase3bb-hotfix/AUTHORIZED_AMENDMENTS.json";
/** Exact successor hashes, not an ignore list. Old authority manifests are immutable. */
export function expectedAmendedHash(path: string, original: unknown): unknown {
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
