# Active-tree cleanup — current source checkpoint

Before: **5948 tracked files /744800556bytes**, at3b62e9b772e9d1e542d13b951ba67a0744c38c35. Final active tree: **193 tracked files**, a **96.76% reduction**. Fresh-clone verification is complete; exact final metadata SHA/CI are recorded in the final checkpoint tag.

Removed5937obsolete or duplicate tracked paths after verified backups, including some consolidated current-runtime paths. Removed whole historical active directories: assets/ (remaining Blenderbackupfiles), showcase-v0.5/, public-reset/, public-unified/, quality-reports/, downloads/, rejected A/B/C/reset and superseded chibi/unified source sets, oldmigration/review docs and obsolete generation/capture/package/check scripts. All remain recoverable in Git. Currentworld/actors were copied and hash-verified before duplicatepaths were removed; acceptedworld pixels were NOT regenerated/deleted.

Retained: one src/public/assets/{world,actors}/assets-src/{world,actors}/tools/tests/docs structure, exact lockedPhaser/TS/Vite toolchain, original/Phaser/ZodMIT notices,24unchangedworldsourcefiles+originalsourceatlas/provenance, editable currentactoratlases/JSON/masterframes+nativeauthors, allrequired animationpixels, currenttests/CI and roadmap. No3Dpackages existed in the selected runtime lock, so none were needlessly reinstalled; exact package-lockbytes unchanged. Superseded individual frame duplicates are replaced by current editable native atlases and deterministicauthors; derived per-frame/QA/capture outputs are ignored.cache. OldunusedGuest A/B/C storage was replaced with actualvalidatedavatarpreferences, retaining corrupt-state/reload/input/Koreantext testcoverage.

Immutable remote recovery:
- recovery/pixel-before-anim-cleanup-20261015 ->3b62e9b…: actualfreshHTTPSclone/readhash of5948files PASS.
- recovery/historical-3d-20261015 ->f1f13f2…: actualfreshHTTPSclone/readhash of2738files PASS.
- recovery/historical-guests-before-cleanup-20261015 ->bd241a9…: currentNPC/animation backup pushed and remotepeeledSHAverified before deletion.

Exact commands and proof docs/RECOVERY.md/current/recovery-verification.json. No forcepush, tagretargeting, historyrewriting or destruction of unknown/untrackeduserfiles. Gitfullhistorydownload stilllarge bydesign; a shallowclone ofcleanedtip excludesobsoleteactive files.

Assetgraph checks: runtimeworldkindfiles/Tiled/manifest/imports traced; everyactorframe matchesgenerator/source/runtime; palette/alpha/gutter/clipping pass; map77colliders/11reachablelandmarks andall4patrolfootprints clear. Single43file runtimeasset tree, notices/favicon additionally. Build/type/lint/8unit and all5nativeflows pass from a fresh remote clone after consolidation. Exact currentZIP HTTP desktop/mobile/input/nativepixels/no404criticalerrors PASS. Latestonlyreviewboard/town/mobile/beforeafterMP4/ZIP/manifest/verification retained; rawvideo/temp/failedtakes ignored. .gitignore preventsold3D/build/cache/media clutter, with explicitexceptions for the onecurrentreviewMP4/ZIP.

Main/publicboundary: newtipcontainsreadonlyverificationCI onmain/reviewbranch, noPagespublishworkflow/permission. Oldmainf1f13f2isancestor. Pages workflow build type and unchanged old public HTML were verified before/after safe main promotion. No unfinished game deployment was authorized or performed. Final source/CI evidence is referenced below and in the final checkpoint tag.

Current source checkpoint after staging: **193 tracked files**, compared with5948baseline (**96.76% fewer**). Counts include source/runtime/licenses/tools and latestreviewevidence.

## Completed verification and source promotion

Fresh HTTPS clone of source commit3a22e62de62abd598f0ad0d24b95ddbb9f1fd98c: npm ci, typecheck, lint, formatting, eight unit tests, build, complete actor/world source checks and all five native browser flows PASS (30.53 seconds total browser run; no retries). Every built file matches the existing review ZIP manifest. Source CI38720697542 SUCCESS. See docs/current/clean-clone-verification.json. Earlier timing-only assertion failures are documented, not presented as successful runs.

Main was fast-forwarded from historicalf1f13f2 to the verified cleaned source. Before promotion, workflow383196743 (legacy 3D Pages publishing) was disabled and its disabled_manually state verified. Pages uses workflow artifacts; the cleaned tree contains only read-only pixel CI. The public HTML SHA256 remained082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f before/after promotion. No new game deployment occurred. The final documentation checkpoint is published to both source branches; its exact SHA and final CI are independently verified in tag checkpoint/pixel-animation-history-cleanup-20261015.

The ZIP's actual extracted HTTP/browser checks pass desktop and emulated mobile DPR2. Final 40.28-second before/after footage was decoded and inspected; natural blink and visible walk/run/gestures are present. No physical-device performance guarantee or final user visual approval is claimed.
