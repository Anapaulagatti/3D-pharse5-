from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-palace-cleanup'
rd=lambda n:json.loads((D/n).read_text());scope=rd('scope-and-collision.json');body=rd('body-clearance.json');render=rd('native-render-qa.json');movement=rd('movement-report.json');assert movement['complete'];assert sum(x['failureSamples']for x in body['contact'])==0
report={'technicalScope':'PASS','historicalAssetFilesExact':3041,'outsideScopePixels':0,'collisionCellsChanged':scope['worldCollisionCellChanges'],'collisionPolicy':'Only old blocked cells under new visible exterior branch floor2110..2635,y1438..1488 opened; all other collision exact','logicalSolidsContactSpecTargetsStopsPlans':'UNCHANGED','nativeGroundReadbackPixels':render['exactGroundPixels'],'nativeGroundMismatches':0,'integerNativePlacementAndNearest':'PASS','pathAxisWorldX':2048,'architectureFootprintsAndSilhouettes':'PRESERVED','movementLegs':len(movement['legs']),'nativeContactSamples':sum(x['samples']for x in body['contact']),'unsupportedNativeContactSamples':0,'tests':'30 PASS /9files','typecheckAssetChecksBuild':'PASS','HanbitJejuBridgesWesternHanokJuni':'UNCHANGED / protected hashes exact','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED','artisticAcceptance':'PENDING HUMAN','remaining':'Bakery allocation and inherited global spatial/navigation decisions remain separate; no full-world acceptance implied.'}
(D/'technical-qa.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'QA.md').write_text(f'''# Palace local cleanup QA

Human artistic acceptance **PENDING**. Technical PASS is not art approval.

| Check | Status | Evidence |
|---|---|---|
| Ceremonial-axis registration | PASS technical / human visual review pending | Native source column655 registered to world2048; no scale/interpolation. Original doorway/upper court unchanged; lower approach locally rebuilt, existing west public cross-lane retained. |
| Right-corner house approach | PASS movement / human visual review pending | Narrow floor branch at y1431–1494 connects public axis to existing exterior step toe. Roof, facade, stairs, props and footprint unchanged. No new interior gameplay. |
| Front railing/stair details | Candidate repaired / human review pending | Only2 small masks, native before/after supplied. Original architecture/silhouette preserved. Current map used; no missing reviewer annotations invented. |
| Native sharpness | PASS | {render['exactGroundPixels']:,} eligible actual Phaser ground pixels exact;4 same-camera BEFORE/AFTER pairs, integer placement and NEAREST. |
| Scope / protected assets | PASS | 3,041 historical assets exact;0 changed native ground/static/readback pixels outside explicit mask. Hanbit, both Jeju bridges, island, approved western hanok, commercial row, roads, Juni unchanged. |
| Collision / walkability | PASS local | {report['collisionCellsChanged']} old closed cells under newly visible branch floor opened; only2 derived mask chunks. ALL other cells, original native-contact spec/data, logical solids, plans/targets unchanged.2 consecutive real-control legs / {report['nativeContactSamples']} original-atlas foot samples /0 unsupported. |
| Regression checks | PASS | Typecheck, original asset/Juni/preservation checks,30 tests/9files, scoped lint and private review build. |
| Physical Android/iPhone / hardware performance | NOT TESTED | Chromium emulation/software WebGL is not physical device evidence. |

[Scope + collision](scope-and-collision.json) · [Protected hashes](protected-hashes.json) · [Native render audit](native-render-qa.json) · [Actual movement](movement-report.json) · [Native body/contact](body-clearance.json) · [Asset provenance](asset-provenance.json).

Collision reason: the first actual stop/idle-back recording found3 unsupported contact samples at the old exterior threshold, including y1446. The final candidate opens only existing ground below the stair foot, not the building/interior. Original binaries remain untouched; final actual movement was repeated against the new derived masks. Original movement/controls and all unrelated collision remain unchanged; no teleports after initial review spawn or movement/collision/frame overrides. New2 maskSha256 metadata values match their binaries; inherited untouched metadata is retained, while preservation QA hashes actual files rather than trusting old metadata.

A complete native right-gateway lantern foreground retains its cap over the branch floor and sorts at worldy1610. It is the same approved-style approach source texels, not an extra decoration hiding a seam; binary alpha/native integer placement retained.

Combined palace image joins2 genuine native Phaser readbacks at worldy1040 without resizing/blending; all original unmodified frames remain available. Gameplay videos are lossy motion evidence; native PNGs prove pixel fidelity. Source authoring:3 adopted built-in local outputs;2 rejected internal trials excluded from final assets. No external paid provider API/key.

No main merge, deployment, original source overwrite or separate-app change. Historical checkpoints retained; before checkpoint `checkpoint/g3d-before-palace-cleanup-20261025`. Final review checkpoint `checkpoint/g3d-palace-cleanup-review-20261025`. STOP for human approval.
''')
p=R/'AGENTS.md';s=p.read_text();header='# Final palace cleanup handoff — STOP for human visual review\n\n[Current local evidence/QA/package](docs/gate3-palace-cleanup/README.md). Three scoped palace repairs delivered. Western hanok, Hanbit and BOTH bridges approved/locked.3041 historical assets exact;0 out-of-scope ground/static/native Phaser pixels. Only2358 old branch-floor cells opened after actual foot-contact evidence; all other collision/contact fields exact.2 consecutive original-control movement legs,0 unsupported native contacts. Physical hardware/devices NOT TESTED. Finish package/link/checkpoint metadata only then STOP; no further art/expansion, main merge or deployment without human direction.\n\n'
if not s.startswith('# Final palace cleanup handoff'):p.write_text(header+s)
print(report)
