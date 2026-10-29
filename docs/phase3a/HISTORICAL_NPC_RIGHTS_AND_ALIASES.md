# Historical provenance and fictional public identities

Current owner decision: 2026-10-29. This supersedes the earlier decision to retain historical public names. All six now use **original fictional game identities** as a precautionary design choice while commercial depiction rights remain unverified. It is not a legal finding that historical names are copyrighted or prohibited.

This document is internal provenance/release documentation, not a public game gallery. Original source records are preserved. All approved artwork remains byte-identical to `8a2dbe6f`; original internal NPC IDs remain compatible.

| Internal historical reference / stable ID | Public identity (VI / KO) | Public role and status | Individual depiction concern | Decision, migration and remaining rights status |
|---|---|---|---|---|
| Seondeok / `npc-history-seondeok` | Han Yeonhwa / 한연화 | Fictional cultural keeper; Silla-inspired | Branching crown and formal silhouette evoke Silla royalty; no specific copied museum portrait identified in inspected inputs. | Owner-directed fictionalization, not legal denial. New KO/VI name, fictional introduction and accessibility label; same IDs, art, routes and save keys. Commercial depiction and generation terms remain REVIEW REQUIRED. |
| Sejong / `npc-history-sejong` | Baek Junseo / 백준서 | Fictional writing scholar; early Joseon-inspired | Red ceremonial robe, gold motif and black headwear retain strong royal association; standardized-portrait similarity not comprehensively checked. | New identity does not clear that visual association. No factual claim of creating Hangul or real royal achievements. Preserve pixels; independent depiction comparison pending. |
| Jang Yeong-sil / `npc-history-jang` | Nam Gyeongu / 남경우 | Fictional artisan researching tools; early Joseon-inspired | Workwear and technical prop; no museum reconstruction or actor image supplied. Exact prop authenticity not established. | Fictional occupation, not a real inventor's biography. Same atlas, animations, interaction and save references. Commercial review remains pending. |
| Shin Saimdang / `npc-history-saimdang` | Yun Hwayeon / 윤화연 | Fictional artist; Joseon-inspired | No banknote portrait or specific painting supplied; modern portrait/costume comparison remains unverified. | No real paintings, quotations or family biography attributed. KO/VI presentation changed; approved pixels unchanged. Rights not certified. |
| Yi Sun-sin / `npc-history-yi` | Kang Muyeong / 강무영 | Fictional coastal guide; Joseon-inspired | Helmet and armor may evoke naval-command depictions; no film actor/statue photograph input recorded. | No real battle, rank, quote or military achievement attributed. A rename does not resolve possible costume/likeness issues. Independent commercial review pending. |
| Yu Gwan-sun / `npc-history-yu` | Seo Daeun / 서다은 | Fictional culture-loving student; early-twentieth-century Korea-inspired | Student silhouette can evoke historical photographs; no actual photograph or actor reference supplied. | No real independence activity or biography attributed. Same ID and approved sprites; commercial depiction review remains open. |

## Provenance and actual review

[Original generation provenance and hashes](../phase3a-final-six/ART_PROVENANCE.json) records the original 13 image-generation calls: six masters, six turnarounds and a prop board. Those prompts explicitly used historical inspiration. This task generates no artwork and makes no retroactive claim that the original prompts were fictional. The recorded visual reference was fictional Seoyeon, not a museum portrait or film actor. Input-chain provenance does not guarantee that an output has no similarity to any third-party work.

[Individual depiction review](../phase3a-identity-safeguard/DEPICTION_REVIEW.md) identifies residual concerns and its inspection limits. No specific copied third-party source is established by the reviewed materials; no artwork is therefore silently edited. If a particular depiction requires changes, preserve this baseline and seek independent art review for that case.

Historical facts and names are distinct from copyright in a particular portrait, photograph, film portrayal or expression. Likeness, endorsement, trademark and commercial-use issues depend on actual depiction, context and jurisdiction. The project MIT notice does not independently establish applicable AI-generation terms, output copyrightability or third-party clearance. Commercial publication remains pending review. Prior CONNECT 403 results are transport failures, not permissions denials. No new successful source verification or license is invented.

## Runtime, localization and saved data

`assets-src/npcs/phase3a-finalization/identity-presentations.json` holds only the six public fictional names, occupations and decision metadata. Historical name mapping is retained in internal provenance at `docs/phase3a-identity-safeguard/INTERNAL_REFERENCE_MAP.json` and original immutable source records. It is not rendered as an NPC identity.

`src/npcs/identity.ts` applies names, roles and fictional KO/VI narration through the existing registry and dialogue renderer. Welcome, notice, return, archive introduction, interaction labels, gallery captions and accessibility labels identify fictional characters. Unverified biographies remain disabled. All 36 dialogue node IDs, links, vocabulary, future hooks, assets, coordinates, schedules and NPC save keys remain compatible. No duplicate actor or invented lesson completion is created.

Owner-directed precaution and a rights-based fallback are separate decision types. The owner-directed record explicitly says that the reviewed depiction is not legally cleared. Existing rights-based fallback validation still requires its independent review status. Neither mode turns a name into a license.

## Release status

26 development NPCs remain available: 14 residents, six original modern visitors and six fictional era-inspired archive inhabitants. The legacy `historicalArchiveCount=6` is a compatible collection name, not a claim that the actors are actual historical people. Detailed historical content and separate real-person fact cards remain zero verified and excluded. No celebrity cameo is added. Twelve playable characters, 28 cosmetics and world pixels are protected.

Physical Android, iPhone and hardware-GPU testing remain NOT TESTED. Existing art-validator and spatial warnings remain recorded. Phase 3B is prepared for a separately authorized implementation task; it is not started here. No main merge or public deployment.
