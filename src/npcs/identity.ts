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
    role: nameSchema,
    publicName: nameSchema,
    identityKind: z.enum(["historical-reconstruction", "original-fictional"]),
    eraLabel: z.string().min(1),
    fictionalAlias: nameSchema.nullable(),
    identityDecision: z.enum([
      "retain-approved-independent-reconstruction",
      "fictional-fallback-approved",
      "owner-directed-fictional-identity",
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
        depictionStatus: z.enum([
          "independent-reviewed",
          "reviewed-no-specific-copy-identified-not-legal-clearance",
        ]),
      })
      .nullable(),
  })
  .superRefine((value, context) => {
    if (value.identityKind === "original-fictional") {
      if (
        !value.fictionalAlias ||
        !value.fallbackEvidence ||
        ![
          "fictional-fallback-approved",
          "owner-directed-fictional-identity",
        ].includes(value.identityDecision)
      )
        context.addIssue({
          code: "custom",
          message:
            "Fictional fallback requires a documented identity AND depiction decision; renaming is insufficient",
        });
      if (
        value.identityDecision === "fictional-fallback-approved" &&
        value.fallbackEvidence?.depictionStatus !== "independent-reviewed"
      )
        context.addIssue({
          code: "custom",
          message:
            "Rights-based fallback still requires an independently reviewed depiction; owner precaution is a different decision",
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
        ? `${identity.role.vi} · nhân vật hư cấu · cảm hứng ${identity.eraLabel}`
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
          ko: `안녕하세요. 저는 ${identity.publicName.ko}입니다. 게임 속 가상 인물로서 옛 문화를 함께 살펴봐요.`,
          vi: `Xin chào! Tôi là ${identity.publicName.vi}, ${identity.role.vi.toLocaleLowerCase("vi")}, một nhân vật hư cấu trong game. Cùng khám phá văn hóa xưa nhé.`,
        }
      : {
          ko: "안녕하세요. 옛 문화를 살펴보는 교육용 재구성입니다.",
          vi: "Xin chào! Cùng khám phá văn hóa xưa qua một hình tượng tái hiện nhé.",
        },
    notice: fictional
      ? {
          ko: "이 인물은 게임 속 가상 인물이며 실제 역사 인물이 아닙니다. 이야기와 대사는 게임을 위해 창작했습니다. 자세한 역사 자료는 별도로 검증 중입니다.",
          vi: "Đây là nhân vật hư cấu trong game, không phải một nhân vật lịch sử có thật. Câu chuyện và lời thoại được sáng tác cho game. Tư liệu lịch sử chi tiết đang được kiểm chứng riêng.",
        }
      : {
          ko: "교육용으로 재구성한 모습입니다. 실제 초상이나 발언을 그대로 옮긴 것이 아닙니다. 자세한 역사 자료는 검증 중입니다.",
          vi: "Đây là hình tượng tái hiện phục vụ giáo dục, không phải bản sao chân dung hay lời nói thật của nhân vật. Tư liệu lịch sử chi tiết đang được kiểm chứng.",
        },
    art: {
      ko: "천천히 둘러보고 한국어 낱말도 함께 배워 보세요.",
      vi: "Bạn cứ thong thả khám phá và cùng học vài từ tiếng Hàn nhé.",
    },
    return: fictional
      ? {
          ko: "다음에 또 만나요. 즐겁게 둘러보세요!",
          vi: "Hẹn gặp lại! Chúc bạn khám phá thật vui nhé.",
        }
      : node.content,
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
        ? {
            ...node.hint,
            ko: fictional
              ? "함께 배우는 한국어 낱말 · 게임 속 가상 인물"
              : node.hint.ko,
          }
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
