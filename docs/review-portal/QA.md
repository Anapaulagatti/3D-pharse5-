# One-link portal QA

Fresh task run on Node24.19.0 / Python3.12 / Pillow12.3.0. Canonical game code/assets/tests byte-identical to the accepted3B-A foundation; no UI/map/animation changes there. New review-only bridge/source and static hosting tools are separate.

| Check | Result | Evidence |
|---|---|---|
| npmci (writablecache), assets, typecheck, lint, format, build | PASS | COMMAND_PROOF.json |
| Unit | PASS171 /24files | COMMAND_PROOF.json |
| Complete original E2E | PASS72;0skipped/flaky/fail;15.6minutes | QA_RESULT.json / COMMAND_PROOF.json |
| Portal realPhaser26approaches/dialogue/return, clock, caps | PASS | PORTAL_SMOKE.json |
| Normal Doyun selection and normal local/session state protected from QA | PASS | PORTAL_SMOKE.json |
| All26nativePOST_RENDER cells vs approvedatlas | PASS;0unexplainedmismatch | NATIVE_QA.json |
| Anonymous homepage/game/JSON/JS/snapshots | PASS401 | PORTAL_SMOKE.json |
| Secret-shapedfiles/rawauditexcluded;deniedpaths | PASS | EXTRA_SMOKE.json |
|4localcheckpointvideos actually play | PASS | EXTRA_SMOKE.json |
| Subdirectory + nested snapshot game/lazyassets/return | PASS | EXTRA_SMOKE.json |
| Mobile portrait390×844 / landscape667×375, touchcontrols | PASS browseremulation | PORTAL_SMOKE.json / screenshots |
| Localpromotion,oldsyntheticsnapshotretention,rollback,nounlistedfile | PASS localfixture only | PROMOTION_QA.json |
| Publicexposuregate + canonicalpublicrights + badbase | PASS expectedfailure;0output | EXPOSURE_GATES.json |
| Existing23277trackedfiles audited | PASS23274unchanged;3authorizeddoc/configedits | PROTECTED_AUDIT.json |
| RemotePages/API/currentpublishedartifact | BLOCKED transport403 / CLIForbidden | PAGES_INSPECTION.json |
| RemoteHTTPS/authentication/deployment | NOTDEPLOYED / NOTTESTED | Ownerhostingdecisionrequired |
| PhysicalAndroid/iPhone/GPU/thermal/battery | NOTTESTED | No physicaldeviceevidence |
| Phase3B-Aartisticapproval | PENDING | Ownerreviewrequired |
| Publicexposure / commercialrelease | NOTAPPROVED / BLOCKED_PENDING_REVIEW |26unresolvedNPCrecords;otherassetrightsnotcleared |

The4videos are genuine earlier3B-Acheckpointrecordings, labeledas such; they are not falsely represented as newlyrecordedportalgameplay. Currentportalrendering/interaction/nativepixels have separatefreshreceipts. The4before/afterpairs deliberately show unchangedapprovedsprites, with source3AatlasSHA256equalto3B-A; there was no newart. Finalcandidatebuild/snapshotmetadata and finalreplay are recorded inFINAL_HANDOFF.json beforedelivery.

KnownWARN: ~1.94MBminifiedmainPhaserchunk exceedsreportthreshold; nosuppressionorhardwareFPSclaim. Existingartheuristicandspatialwarningsof3A/3B-Aretained. TechnicalPASSisnotownerartacceptance,rightspermission,realdevicecertificationorapprovalforfuturephases.

One-timegate: choose an owner-controlled access-controlled staginghost/hostname, provisionTLS andprivateorigincredentials; run the exactREADMEsetupandanonymous/authenticatedchecks. No publicURL is invented; no existingPagesreplacement or repo creation occurred. Source/checkpointsremainlocalbecause this environmenthas no currentauthenticatedGitHubwritechannel; no publicart/screenshots were pushed as a workaround.
