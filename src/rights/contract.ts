import { z } from "zod";
export const riskSchema = z.enum([
  "LOW_CONCERN",
  "NEEDS_REVIEW",
  "CONCRETE_CONCERN",
]);
export const publicationSchema = z.enum([
  "DEV_ONLY",
  "BLOCKED_PENDING_REVIEW",
  "LICENSE_DOCUMENTED",
  "LEGAL_REVIEWED",
]);
export const rightsAssetSchema = z.looseObject({
  stableId: z.string(),
  publicName: z.object({ ko: z.string(), vi: z.string() }),
  status: z.string(),
  approvedForDevelopment: z.boolean(),
  approvedForCommercialRelease: z.boolean(),
  risk: riskSchema,
  publication: publicationSchema,
  creatorTool: z.looseObject({
    creationTerms: z.string(),
    termsAtCreationEvidence: z.array(z.string()),
  }),
  sourceEvidence: z
    .array(
      z.object({
        path: z.string(),
        sha256: z.string().regex(/^[a-f0-9]{64}$/),
        inspection: z.string(),
      }),
    )
    .min(1),
  beforeAtlasSHA256: z.string().regex(/^[a-f0-9]{64}$/),
  afterAtlasSHA256: z.string().regex(/^[a-f0-9]{64}$/),
  artModified: z.boolean(),
  candidate: z.unknown(),
});
export const rightsInventorySchema = z.object({
  schemaVersion: z.literal(1),
  scope: z.string(),
  assets: z.array(rightsAssetSchema),
  excludedReferences: z.array(
    z.object({
      id: z.string(),
      includedInGame: z.boolean(),
      risk: riskSchema,
      publication: publicationSchema,
      reason: z.string(),
    }),
  ),
});
export type RightsInventory = z.infer<typeof rightsInventorySchema>;
export function validateRightsInventory(
  input: unknown,
  requiredIds: readonly string[],
) {
  const q = rightsInventorySchema.parse(input),
    ids = new Set(q.assets.map((a) => a.stableId));
  if (
    ids.size !== q.assets.length ||
    ids.size !== requiredIds.length ||
    requiredIds.some((id) => !ids.has(id))
  )
    throw Error(
      "Rights inventory must cover every required stable NPC ID exactly once",
    );
  for (const a of q.assets) {
    if (!a.artModified && a.beforeAtlasSHA256 !== a.afterAtlasSHA256)
      throw Error("Undocumented art change " + a.stableId);
    if (
      a.approvedForCommercialRelease &&
      (!["LICENSE_DOCUMENTED", "LEGAL_REVIEWED"].includes(a.publication) ||
        !a.creatorTool.termsAtCreationEvidence.length ||
        /UNKNOWN/i.test(a.creatorTool.creationTerms))
    )
      throw Error(
        "Commercial approval needs actual terms/review evidence, not a fictional name: " +
          a.stableId,
      );
  }
  return q;
}
export function assertReleaseAllowed(
  q: RightsInventory,
  profile: "private-review" | "public",
) {
  const bad = q.assets.filter((a) =>
      profile === "public"
        ? !a.approvedForCommercialRelease ||
          !["LICENSE_DOCUMENTED", "LEGAL_REVIEWED"].includes(a.publication)
        : !a.approvedForDevelopment,
    ),
    refs =
      profile === "public"
        ? q.excludedReferences.filter(
            (r) =>
              r.includedInGame &&
              ["DEV_ONLY", "BLOCKED_PENDING_REVIEW"].includes(r.publication),
          )
        : [];
  if (bad.length || refs.length)
    throw Error(
      `Asset rights gate: ${profile} build BLOCKED. Required assets: ${bad.map((a) => a.stableId + " [" + a.publication + "]").join(", ")}. References: ${refs.map((r) => r.id).join(", ")}. Obtain applicable creation/account terms and independent distribution-jurisdiction review; see docs/phase3b-a/RIGHTS_REVIEW_QUEUE.md. No substitution or actor deletion is permitted.`,
    );
}
