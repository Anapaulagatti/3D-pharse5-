import type { NPCDefinition } from "./types";
/** Content metadata only. All collections use the existing NPC model/asset pool/FSM. */
export type NPCCollection =
  "resident" | "historical-archive" | "modern-fictional";
export interface VerifiedContentSource {
  url: string;
  accessedAt: string;
  claimReferences: readonly string[];
  status: "verified";
}
export interface HistoricalArchiveMetadata {
  id: string;
  category: "historical-archive";
  era: string;
  dateLabel: string;
  hostResidentId: string;
  sources: readonly VerifiedContentSource[];
  interpretation: "original educational reconstruction, not a verbatim quotation";
}
export interface ModernVisitorMetadata {
  id: string;
  category: "modern-fictional";
  hostResidentId: string;
  homeZone: NPCDefinition["homeZone"];
  rights: "original-fictional";
  realPerson: false;
  licensedCameo: false;
}
export interface ModernIconFactCard {
  id: string;
  name: { ko: string; vi: string };
  neutralFacts: { ko: string; vi: string };
  sources: readonly VerifiedContentSource[];
  likenessAssets?: never;
  endorsement: false;
}
/** A failed fetch must never unlock factual history/biographical content.
 * Approved reconstruction actors are a separate development-art decision. */
export function hasVerifiedSources(sources: readonly VerifiedContentSource[]) {
  return (
    sources.length > 0 &&
    sources.every(
      (s) =>
        s.status === "verified" &&
        /^https:\/\//.test(s.url) &&
        Number.isFinite(Date.parse(s.accessedAt)) &&
        s.claimReferences.length > 0,
    )
  );
}
