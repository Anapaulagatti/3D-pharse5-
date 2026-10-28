from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]; D=R/'docs/phase3a-finalization'
ids=json.loads((R/'assets-src/npcs/phase3a-finalization/identity-presentations.json').read_text())['identities']
audit=json.loads((D/'protected-audit.json').read_text())
def write(name, text): (D/name).write_text(text.strip()+'\n')
corrected=(D/'corrected-e2e.log').read_text() if (D/'corrected-e2e.log').exists() else ''
e2e='PASS: 67 original full-suite cases + the corrected 26-record case on rerun' if '1 passed' in corrected else '67 passed; one obsolete 20-record expectation corrected, rerun pending'
write('README.md',f'''# Phase 3A — approved 26-NPC development baseline

The owner approves the 26 NPC identities, artwork, animations and gameplay foundation reviewed at `831022a8533c1d2126f77724d6eea8aeca2e8e30`. All approved art is preserved. The before-change approval tag is `checkpoint/phase3a-26-npc-art-approved-20261029-831022a8`; the final development tag is `checkpoint/phase3a-26-npc-development-approved-20261029`. Branch: `feature/phase3a-approved-roster-lock`; exact original base and hashes are in APPROVED_BASELINE.json.

Ordinary development gameplay now registers **26 unique NPCs: 14 residents + 6 original modern visitors + 6 historical archive reconstructions**. No QA flag is needed for archive access. The original 20-person living collection and legacy resident count of 14 remain compatible. The existing registry, state machine, navigation, dialogue and bounded texture pool are reused.

All six historical names are retained; there are **zero fictional replacements and zero artwork edits**. The documented art inputs identify no copied museum portrait, photograph, standardized portrait or film actor. This input-chain finding is not comprehensive legal clearance. HTTP 403 is a transport failure, not a rights denial. Commercial release still requires applicable generation terms, jurisdiction and depiction review. See the required [rights and identity matrix](../phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md).

Public KO/VI names are now separate from stable IDs. Neutral reconstruction notices replace obsolete art-preview wording. All 36 archive node IDs, links, vocabulary and hooks remain compatible. Detailed historical facts and six separate modern real-person fact cards remain unverified and excluded from factual release. No authentic portrait, quotation, endorsement, account or lesson completion is invented.

- [QA](QA.md): 153 unit tests passed; E2E: {e2e}.
- [Approved roster and hashes](APPROVED_ROSTER_26.json), [protected audit](PROTECTED_AUDIT.md), [exact scope](MIGRATION.md).
- [Native screenshots and actual gameplay](REVIEW.html), [Phase 3B architectural handoff](PHASE3B_HANDOFF.md).
- [Playable ZIP](PHASE3A_APPROVED_26NPC_DEVELOPMENT.zip), [checksum and extraction proof](PACKAGE_PROOF.json).

Extract the ZIP, run `python3 start_review.py`, and open the printed local review URL. No Node installation or network is needed for gameplay. Fresh storage shows the unchanged Character Studio: choose a character, then enter the world. Optional full-resolution online source links are distinct from local native crops.

Physical Android, iPhone and hardware-GPU validation remain **NOT TESTED**. Previous art-validator and world-planning warnings remain documented. Phase 3B is an architectural handoff only: **no implementation, main merge or public deployment**.
''')
write('PROTECTED_AUDIT.md',f'''# Protected-baseline audit

Human approval: `831022a8`; working base: `6e90d287`. Complete pre-edit SHA256 inventory: APPROVED_BASELINE.json.

| Check | Result |
|---|---|
| Previously tracked files checked | {audit['checkedFiles']} |
| Byte-identical files | {audit['unchangedFiles']} |
| Frozen NPC, character, cosmetic and world asset files | {audit['all26ApprovedArtSourceAndRuntimeAssetFilesUnchanged']} unchanged |
| Public assets for all 26 NPCs | {audit['all26PublicNPCFilesExact']} unchanged |
| Authorized non-pixel edits | {len(audit['authorizedChanges'])} |
| Art exceptions / regeneration / fictional replacements | 0 / 0 / 0 |
| Unexpected modifications | 0 |

Every authorized change has exact before/after hashes and its reason in protected-audit.json. Changes are limited to authority documents, approved roster availability and identity presentation, two explanatory comments, and three tests with superseded roster/notice expectations. Existing movement, preservation, cache, touch and state assertions are retained.

APPROVED_ROSTER_26.json records all 26 stable IDs, 2,704 native animation cells, 96×112 registration, anchor (48,100), atlas hashes, animation mappings and route digests. The twelve playable characters, 28 cosmetics, 46 variants, world, collision, camera and tour are unchanged. Historical sources and checkpoints are not overwritten.
''')
write('MIGRATION.md','''# Exact scope and compatibility

- `src/npcs/identity.ts` and `identity-presentations.json` add a typed public-name layer for the six archive figures. All current names are retained. A future fictional fallback requires separate documented identity and depiction decisions, new KO/VI aliases and rewritten fictional narration. A name-only substitution cannot establish image clearance. These checks are not a legal certification service.
- `history.ts` composes the 26 approved definitions using the existing NPCRegistry. The original living `npcCatalog` stays at 20. Art availability and verified historical facts are counted separately. Existing review URLs and DOM identifiers remain compatible.
- `manager.ts` enables the existing archive selector in ordinary development gameplay and reports 26/14/6/6, zero unapproved art candidates and zero verified historical claims. Population, movement, cache, depth and collision behavior remain unchanged.
- Only neutral reconstruction presentation changes. Original source definitions remain frozen; the runtime overlay preserves all 36 node IDs, next links, conditions, vocabulary and null future hooks. These graphs are not verified biographies.
- Three existing test files update superseded 20/0 availability or art-preview notice expectations. New tests cover stable identity mapping, safe fallback contracts and ordinary non-QA access. Existing behavioral assertions remain.

NPC IDs remain the save keys in `korean-arena-npc-world-v1`; display names are presentation only. Existing records survive, with missing records initialized by the existing mechanism. World position, player appearance, presets, visited state and learning progress are not migrated or reset.

No costume, hairstyle, approved pixel, anchor, gait, speed, footprint, route, world coordinate, approach point, interaction distance or quest identifier changes. No art exception is needed. A future depiction-specific legal issue must use independently reviewed artwork and a new approval reference, preserving this baseline.
''')
write('QA.md',f'''# Phase 3A finalization QA

| Check | Status | Evidence |
|---|---|---|
| Unit suite | PASS, 153 tests | final-test.log; 147 previous + 6 identity tests |
| Full E2E coverage | {e2e} | final-e2e.log and corrected-e2e.log; initial failure preserved |
| Focused archive / touch / ordinary access | PASS, 5 tests | focused-e2e.log |
| Typecheck / assets / lint / formatting | PASS | final-*.log; no checks suppressed |
| Production build | PASS | initial-build.log; tested runtime unchanged |
| Six literal native readbacks | PASS, zero pixel mismatches | native-readback-qa.json |
| Protected assets | PASS, byte-identical | protected-audit.json; zero art exceptions |
| Registry and graph | 26 unique IDs, 136 reachable nodes | existing registry validation |
| KO/VI identities | PASS, six historical names retained | native-runtime-evidence.json |
| Fictional fallback | Zero active; migration contract tested | identity.test.ts |
| Portable package | See extraction and runtime proof | PACKAGE_PROOF.json, package-smoke.json |
| Commercial / legal clearance | PENDING; not certified | required rights/identity matrix |
| Detailed history and real-person fact cards | Zero verified; excluded | unchanged source receipts |
| Physical Android / iPhone / hardware GPU | NOT TESTED | no physical evidence |
| Prior art and world issues | WARN / FAIL retained | prior 13 Forge FAIL / 11 WARN, Creator limitations, Harin and spatial issues |

The sole original full-suite failure was an overlooked `records.length === 20` expectation. The approved canonical roster now has 26 records; only that expected count changed. Movement and cache checks stayed intact. The original failed run is retained rather than represented as a clean 68-test run.

A registry count of 26 does not mean 26 simultaneous actors. Existing limits remain four active actors, four loaded textures and two pending loads. One contextual historical reconstruction temporarily replaces a canonical host slot; leaving restores living schedules. Legacy `registered=14` remains compatible. Art approval does not certify factual or commercial release.
''')
html=['''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase 3A · 26 NPC đã duyệt</title><style>body{max-width:1000px;margin:auto;padding:16px;background:#1d1b24;color:#f4e7cc;font:16px system-ui;line-height:1.5}a{color:#efca80}img,video{max-width:100%}img{image-rendering:pixelated}a.play{display:inline-block;min-height:44px;margin:5px;padding:8px;background:#3a3248}article{padding:18px 0;border-top:1px solid #88745b}</style><h1>Phase 3A · 26 NPC đã duyệt làm baseline phát triển</h1><p>Giữ nguyên tranh, atlas và animation. Sáu hình tượng lịch sử phục vụ giáo dục, không phải chân dung hay lời nói được xác thực. Tư liệu chi tiết và điều kiện phát hành thương mại còn chờ rà soát. Thiết bị thật: CHƯA KIỂM THỬ.</p><a class="play" href="../../index.html">Vào thế giới · 26 NPC</a><p><a href="../phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md">Ma trận quyền và danh tính</a> · <a href="QA.md">QA</a> · <a href="PHASE3B_HANDOFF.md">Bàn giao kiến trúc Phase 3B</a></p><h2>Archive trong thế giới thường, không cần cờ QA</h2><img src="ordinary-world-archive-menu.jpg" alt="Menu archive thật"><video preload="none" controls src="approved26-ordinary-world-actual.mp4"></video><p>Video ghi thao tác game thật với Sejong, không có QA/historyArtReview trong URL.</p>''']
for r in ids:
 id=r['npcId'];html.append(f'''<article><h2>{r['publicName']['vi']} · {r['publicName']['ko']}</h2><p>Giữ tên lịch sử và tranh đã duyệt. Cảm hứng thời kỳ: {r['eraLabel']}; chi tiết lịch sử đang kiểm chứng.</p><a class="play" href="../../index.html?qa&renderer=canvas&npcReview={id}">Lối vào kiểm tra · {id}</a><p>QA chỉ đặt Juni tại lối tiếp cận đã kiểm tra, không mở khóa roster.</p><a href="native/{id}-phaser-native.png">Ảnh Phaser gốc 1:1</a> · <a href="native/{id}-body-native.png">Crop nhân vật native</a><p><img loading="lazy" src="native/{id}-context-native.png" alt="Crop thế giới native"><img loading="lazy" src="native/{id}-dialogue.jpg" alt="Tên KO/VI và thông báo nguồn"></p></article>''')
html.append('<p>Chỉ bàn giao kiến trúc Phase 3B; chưa triển khai. Không merge main hoặc deploy.</p></html>');write('REVIEW.html',''.join(html))
print('Readable review docs generated:',e2e)
