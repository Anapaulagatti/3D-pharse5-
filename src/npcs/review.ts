import { npcRegistry } from "./registry";
/** Only an explicit QA URL selects a declared, mask-validated approach. Normal spawn is untouched. */
export function npcReviewSpawn(
  query: URLSearchParams,
): [number, number] | undefined {
  if (!query.has("qa")) return;
  const id = query.get("npcReview");
  const d = id && npcRegistry.get(id);
  return d ? [...d.reviewSpawn] : undefined;
}
