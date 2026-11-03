# Reproduce this private review

Source branch feature/phase3b-d-farm-shop-cleanup; baseline d54117c0958724276b98a131dbcb90a9af24e0fc. checkpoint/phase3bd-before-20261103 is immutable. Native runtime first implementation521f3a0d; final source commit in PUBLIC_CANDIDATE_PROOF.json. Final build equality report binds unchanged tested play bytes to the final source build; handoff-only documentation may follow.

Use Node24, Python3/Pillow and project locked dependencies. npm run typecheck; npm run assets:check; npm run lint; npm run format:check; npm test; npm run build. Start npm run preview on port4330 for configured browser scenarios; npm run test:e2e uses installed Chromium (or PIXEL_CHROMIUM_PATH). Full and targeted reports retain separate counts/failures; do not sum them into a fake clean run. test:e2e raw historical evidence remains in .cache locally; concise source reports are versioned here.

Source guard: python3 tools/phase3bd/world_guard.py. Build+transport: python3 tools/phase3bd/ci_artifacts.py. Actual candidate guard: world_guard.py --artifact <candidate>. Actual final ZIP guard: world_guard.py --artifact <candidate> --zip <zip>. Source history is required for exact deleted-file preimage assertions (CI checkout fetch-depth0). CI contains no deployment permission.

Private builder: REVIEW_OUT=.cache/<fresh-candidate> node tools/phase3bd/build_review.mjs. Finalization/packaging take the same fresh candidate path; never overwrite earlier checkpoints. Approved20/26 public snapshots are copied unchanged; private3BC rollback remains independently recoverable. New exact public exposure stays PENDING in manifest/receipt. Historical donor archive and raw art/prompt sources are excluded.

Gameplay recording: QUEST_REVIEW_URL=<local-candidate>/play/ node tools/phase3bd/gameplay.mjs. Uses canonical native floor route planner, real WASD/Shift, real elapsed growth, original Juni, wrong/different/right questions and persistent readback. No state/time override for completion. Optional review-only NPC clock is set to morning to make existing shopkeeper available, not to accelerate crop growth. SciPy/NumPy are capture-only route-analysis dependencies, not shipped or imported by game. Cached path fields are keyed by exact native floor SHA.

If Playwright FFmpeg download is unavailable, use an already installed FFmpeg via a workspace-local executable link with PLAYWRIGHT_BROWSERS_PATH; no restriction bypass needed. Actual captures, source SHA, codec/duration/size and absent audio are recorded in VIDEO_PROOF.json. PNG is native clarity evidence; lossy review video is not pixel-exact.

Offline review: extract the one delivered PHASE3BD_REVIEW.zip, run python3 start-review.py, then open http://127.0.0.1:4483/review/ . The launcher hashes every manifest entry and only binds loopback; no npm/internet/auth required. Stop server with Ctrl+C.

No remote source/artifact push, Pages dispatch, v0.5 change, main merge, paid service or Phase3B-E is authorized by this private review package. A new exact owner approval is required before the existing protected GitHub Pages workflow may publish. Physical Android/iPhone/hardware GPU remain NOT TESTED.
