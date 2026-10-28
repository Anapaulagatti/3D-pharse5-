import { z } from "zod";
import source from "../../assets-src/npcs/phase3a-finalization/identity-presentations.json";
import type { DialogueNode, NPCDefinition } from "./types";

const nameSchema = z.object({
  ko: z.string().regex(/[가-힣]/),
  vi: z.string().min(1),
});
export const identityPresentationSchema = z
  .object({
    npcId: z.string().regex(/^npc-history-/),
    historicalReference: nameSchema,
    publicName: nameSchema,
    identityKind: z.enum(["historical-reconstruction", "original-fictional"]),
    eraLabel: z.string().min(1),
    fictionalAlias: nameSchema.nullable(),
    identityDecision: z.enum([
      "retain-approved-independent-reconstruction",
      "fictional-fallback-approved",
    ]),
    decisionReason: z.string().min(1),
    artworkAction: z.literal("preserve-byte-identical"),
    commercialReleaseStatus: z.literal("review-required"),
    generatedAssetTermsStatus: z.literal("not-independently-confirmed"),
    likenessStatus: z.literal("not-legally-certified"),
    verifiedHistoricalContent: z.literal("pending-excluded"),
    factCardIds: z.array(z.string()).max(0),
    fallbackEvidence: z
      .object({
        identityDecisionReference: z.string().min(1),
        depictionDecisionReference: z.string().min(1),
        depictionStatus: z.literal("independent-reviewed"),
      })
      .nullable(),
  })
  .superRefine((value, context) => {
    if (value.identityKind === "original-fictional") {
      if (
        !value.fictionalAlias ||
        !value.fallbackEvidence ||
        value.identityDecision !== "fictional-fallback-approved"
      )
        context.addIssue({
          code: "custom",
          message:
            "Fictional fallback requires a documented identity AND depiction decision; renaming is insufficient",
        });
      if (
        value.publicName.ko === value.historicalReference.ko ||
        value.publicName.vi === value.historicalReference.vi
      )
        context.addIssue({
          code: "custom",
          message:
            "Fictional identity must not retain the historical public name",
        });
      if (
        value.fictionalAlias &&
        (value.publicName.ko !== value.fictionalAlias.ko ||
          value.publicName.vi !== value.fictionalAlias.vi)
      )
        context.addIssue({
          code: "custom",
          message:
            "Both public locales must match the approved fictional alias",
        });
    } else if (
      value.fictionalAlias ||
      value.fallbackEvidence ||
      value.identityDecision !== "retain-approved-independent-reconstruction"
    ) {
      context.addIssue({
        code: "custom",
        message:
          "Retained historical reconstruction cannot silently carry a fictional replacement",
      });
    }
  });
export type NPCIdentityPresentation = z.infer<
  typeof identityPresentationSchema
>;
export const historicalIdentities = source.identities.map((row) =>
  identityPresentationSchema.parse(row),
);
if (new Set(historicalIdentities.map((row) => row.npcId)).size !== 6)
  throw Error("Exactly six unique historical identity presentations required");

/** Presentation only: never replace IDs, assets, animations, routes or saved keys.
 * This validates migration evidence, not legal clearance or generated-art ownership.
 */
export function presentNPCIdentity(
  definition: NPCDefinition,
  presentation?: NPCIdentityPresentation,
): NPCDefinition {
  if (!presentation) return definition;
  const identity = identityPresentationSchema.parse(presentation);
  if (identity.npcId !== definition.id)
    throw Error("Identity cannot replace a stable NPC ID");
  return {
    ...definition,
    names: { ...identity.publicName },
    occupation:
      identity.identityKind === "original-fictional"
        ? `Nhân vật hư cấu · cảm hứng ${identity.eraLabel}`
        : `Tái hiện giáo dục · cảm hứng ${identity.eraLabel}`,
  };
}

/** No sourced biography is shipped here. Historical and fictional presentations
 * both use neutral narrator text, with independent pending factual information.
 */
export function presentArchiveDialogue(
  node: DialogueNode,
  identity: NPCIdentityPresentation,
): DialogueNode {
  if (node.npcId !== identity.npcId)
    throw Error("Cross-owned identity dialogue");
  const suffix = node.id.slice(identity.npcId.length + 1);
  const fictional = identity.identityKind === "original-fictional";
  if (
    !["welcome", "notice", "words", "art", "sources", "return"].includes(suffix)
  )
    throw Error(
      fictional
        ? "Fictional fallback requires an independently rewritten narrative, not inherited biography"
        : "Historical facts require a separately verified content registry",
    );
  const content: Record<string, { ko: string; vi: string }> = {
    welcome: fictional
      ? {
          ko: "안녕하세요. 저는 게임 속 가상 안내인입니다. 옛 문화를 함께 살펴봐요.",
          vi: "Xin chào! Tôi là người dẫn chuyện hư cấu trong game. Cùng khám phá văn hóa xưa nhé.",
        }
      : {
          ko: "안녕하세요. 옛 문화를 살펴보는 교육용 재구성입니다.",
          vi: "Xin chào! Cùng khám phá văn hóa xưa qua một hình tượng tái hiện nhé.",
        },
    notice: fictional
      ? {
          ko: "이 인물은 게임 속 가상 인물입니다. 실제 역사 인물의 초상이나 발언이 아닙니다. 역사 자료는 별도로 검증합니다.",
          vi: "Đây là nhân vật hư cấu trong game, không phải hình tượng hay lời nói của một nhân vật lịch sử có thật. Tư liệu lịch sử được kiểm chứng riêng.",
        }
      : {
          ko: "교육용으로 재구성한 모습입니다. 실제 초상이나 발언을 그대로 옮긴 것이 아닙니다. 자세한 역사 자료는 검증 중입니다.",
          vi: "Đây là hình tượng tái hiện phục vụ giáo dục, không phải bản sao chân dung hay lời nói thật của nhân vật. Tư liệu lịch sử chi tiết đang được kiểm chứng.",
        },
    art: {
      ko: "천천히 둘러보고 한국어 낱말도 함께 배워 보세요.",
      vi: "Bạn cứ thong thả khám phá và cùng học vài từ tiếng Hàn nhé.",
    },
    sources: {
      ko: "검증된 자료를 확보한 뒤 자세한 역사 설명을 제공합니다.",
      vi: "Phần giới thiệu lịch sử chi tiết sẽ được mở khi tư liệu đã được kiểm chứng.",
    },
  };
  return {
    ...node,
    content: content[suffix] ?? node.content,
    hint:
      suffix === "words"
        ? node.hint
        : {
            ko: fictional
              ? "게임 속 가상 인물 · 역사 자료는 별도 검증"
              : "교육용 재구성 · 자세한 역사 자료는 검증 중",
            vi: fictional
              ? "Nhân vật hư cấu · tư liệu lịch sử được kiểm chứng riêng"
              : "Tái hiện giáo dục · tư liệu lịch sử chi tiết đang được kiểm chứng",
          },
  };
}
