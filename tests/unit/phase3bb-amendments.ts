import amendments from "../../docs/phase3bb-hotfix/AUTHORIZED_AMENDMENTS.json";
/** Exact successor hashes, not an ignore list. Old authority manifests are immutable. */
export function expectedAmendedHash(path: string, original: unknown): unknown {
  const row = (
    amendments.files as Record<
      string,
      { beforeSHA256: string; afterSHA256: string }
    >
  )[path];
  if (!row) return original;
  if (row.beforeSHA256 !== original)
    throw Error("Amendment predecessor mismatch: " + path);
  return row.afterSHA256;
}
