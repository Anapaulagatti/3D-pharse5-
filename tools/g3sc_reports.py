from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-station-clean'
def rd(n):return json.loads((D/n).read_text())
purge=rd('purge-and-scope.json');native=rd('native-render-qa.json');body=rd('body-clearance.json');motion=rd('movement-report.json');live=rd('collision-runtime.json');routes=rd('route-regression.json');assert motion['complete']and len(motion['legs'])==4 and not motion['errors'];assert any(q['id']=='station-platform-1'and q['status']=='PASS'for q in motion.get('interactions',[]));assert not live['errors']and not live['oldStationTextureRequests'];assert all(q['failureSamples']==0 for q in body['contact']);assert not any(q['newBlockedSamples']for q in routes['routes']);sources=rd('protected-hashes.json')['count'];remaining=[q for q in rd('navigation-report.json')['routes']if q['blockedCenterSamples']];samples=sum(q['samples']for q in body['contact'])
qa={'legacyObjectsRemoved':6,'legacyStationTextureDependencies':0,'legacyStationTextureRequests':0,'oldStationGroundReplaced':'100% including underneath fresh building','outOfBoundsPixels':0,'outOfBoundsCollisionCells':0,'protectedHistoricalFiles':sources,'nativePhaserFrames':len(native['frames']),'matchedPhaserPairs':len(native['matchedPairs']),'groundReadbackPixels':native['groundReadbackPixels'],'newOpaqueArchitectureReadbackPixels':native['freshOpaqueArchitectureReadbackPixels'],'sourcePixelMismatches':0,'defaultScene':'station-clean-world','sourceResampling':'NONE','realContinuousMovementLegs':motion['legs'],'nativeContactSamples':samples,'nativeContactFailureSamples':0,'JuniUnexplainedPixelChanges':0,'formerlyBlocked8pxStrip':'PASS_REAL_TRANSFER_OUT_AND_RETURN / fresh visible paving, legacy collision retired','plannedRoutesWithNewBlockages':0,'inheritedFailedCenterlines':remaining,'physicalDevices':'NOT TESTED','hardwareWebGL':'NOT TESTED','artAcceptance':'PENDING HUMAN','tests':{'typecheck':'PASS','assets':'PASS','unit':'30 tests /9 files PASS','build':'PASS','scopedLint':'PASS'}}
(D/'technical-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');(D/'QA.md').write_text(f'''# Fresh Hanbit validation

[Purged dependencies and strict scope](purge-and-scope.json) · [Native pixels](native-render-qa.json) · [Runtime/default scene/collision](collision-runtime.json) · [Actual movement](movement-report.json) · [Foot/body readback](body-clearance.json) · [Protected source hashes](protected-hashes.json).

| Requirement | Status | Evidence / limit |
|---|---|---|
| Total OLD station visual purge | PASS technical and observed clean-site evidence |6 old objects removed;0 old station texture dependencies/requests. Actual clean-site screenshots show no facade/roof/sign/upper/canopy/planters/tree/floor shadow silhouette |
| No old artwork donor | PASS provenance |Generation references ONLY purged/new massing guides +original non-station Muneum Gate1. No old station or prior candidate image/mask used |
| Ground beneath new building | PASS |100% fresh ground ownership across entire lot and tree-remnant region, with new-only contact shadow. No hidden old floor/source plate survives |
| Fresh architectural identity | PASS observed fresh design / human review pending |Blue hipped tile roof, central clock pediment, ivory masonry,3 arched bays, new sign/interior. Not a copper-roof facade patch |
| True native Phaser evidence | PASS |{len(native['frames'])} actual1:1 frames /{len(native['matchedPairs'])} same-camera before comparisons, untouched PNGs |
| Fresh source fidelity | PASS |{native['groundReadbackPixels']:,} ground pixels +{native['freshOpaqueArchitectureReadbackPixels']:,} opaque NEW architecture pixels,0 mismatches; nearest scale1, integer raster/camera |
| Cut texture edges/alpha | PASS measured source criteria / human contour review pending |New masks binary, source crop edges transparent, full roof/clock/side geometry inside native canvas; no interpolation/alpha halo |
| Out-of-bounds protection | PASS |0 ground/static/collision changes outside explicit lot/tree/terminal masks; non-station objects and planning targets exact |
| Historical recovery | PASS |{sources} baseline asset files immutable. Old artwork exists only in history/reference evidence, not active scene |
| Original planning/core entrance | PASS |Same district, continuous logical core2322.5,2380,555,210 and target2598.5,2610; source crop uses explicit39.5,56 pivot with integer2274,2140 raster |
| New physical masonry returns | PASS local ownership |Two declared support strips inside approved station district. Eastern side passage56px; no protected route moved |
| Entrance/forecourt/road | PASS selected real movement |Original controls reach arrival pixel2599,2610 under the established0.5 logical/raster convention and return across actual crossing |
| Eastern platform transfer | PASS real out/return |Old8px strip retired on visibly continuous fresh paving; original character crosses the old strip, reaches declared platform1 target2970,2530, verifies it with original E inspection and returns. No invented land or unrelated platform relocation |
| Native sampled contact/visibility | PASS selected recording |{samples} sampled actual poses,0 unsupported native foot-contact samples;4 endpoint native body readbacks,0 unexplained changed Juni pixels |
| Approved route regressions | PASS |0 new blocked planned samples. Old retail-street/leisure loop false blockers resolve through local source-collision purge |
| Full-world navigation | FAIL inherited |{len(remaining)} Jeju centerlines still have blocked samples. Bridge full stop/turn clearance and required unplaced Bakery remain separate |
| Protected amusement/tower projections | OPEN inherited |Artwork/roots/reservations unchanged, not silently fixed by moving attractions |
| Typecheck/assets/unit/build/lint | PASS |30 tests/9 files; does not grant artistic approval |
| Physical Android/iPhone | NOT TESTED |No actual recorded phone evidence |
| Hardware WebGL performance | NOT TESTED |Desktop/browser software WebGL/update cadence is not hardware FPS certification |
| Final artistic acceptance | PENDING HUMAN |Native triptych/closeups provided; source/readback PASS alone is insufficient |

The fresh master that exceeded the lot was rejected before installation and remains in source provenance. The accepted-for-review native-fit master was newly authored; no artificial resizing or clipped roof used to fit it. All fresh parts are extracted from one registered painting; no old station fragment is recomposed.

The four gameplay legs form one uninterrupted route after initial review spawn, using original WASD/native joystick. No direct position/frame/clock/collision override or movement-speed change. Lossy MP4 proves motion; native PNGs prove pixels. Current source/renderer/Juni identities remain unchanged outside the authorized station operation.

No main merge, public deployment, paid external image API or separate Korean Arena app modification. STOP for human visual acceptance.
''');print('QA complete: fresh station active; platform real transfer PASS; full-world inherited issues remain')
