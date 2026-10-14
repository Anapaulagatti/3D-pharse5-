# Studio progress

- Current milestone: BIG-UPDATE-004 — Living Hanok Showcase v0.4 COMPLETE as a verified review candidate. STOP for user visual feedback.
- Latest scope: uploaded v0.4 major overhaul prompt; mascot/full-body/face, richer Hanok, life/material/light/camera/UI polish only. No Hangul Garden or new district.
- Last verified checkpoint before final complete-evidence handoff: 7bd2ada (production, source, inspected movie/visual proof) pushed and independently matched origin/main; final docs/candidate evidence save follows in history.
- Verified at: 2026-10-14T04:52:37.822903+00:00.
- Main deliverables: quality-reports/v0.4/REVIEW.md, VERIFICATION_SUMMARY.json, desktop/day/evening/night/hero/detail/12 poses+live pairs/mobile/fallback, 44.92s real motion capture, versioned Blender/GLB sources, standalone HTML/review/static ZIPs and manifest.
- Mascot: original approved body/identity retained; independent leg/arm/head/ear transform pivots, twelve authored GLB/NLA clips (Idle, Walk, Run, Jump, Greeting, Happy, Thinking, Celebration, Disappointed, Curious, ClickReaction, ReturnToIdle); clear exported eye/brow/mouth/cheek states, runtime blink/gaze/camera awareness, one-shot natural ReturnToIdle/Idle. Editable mascot-living.blend and 696,568-byte GLB (11,074 triangles/47 source primitives).
- Hanok: original arena and v0.3 detail layer retained; additional roof crests, entrance/railings/steps, patterned promenade/lotus pedestal edge, vessels/plants/flowers/cushions/bridge finials/city windows and 3 fuller swaying plum crowns. Versioned hanok-living.blend/GLB, 799,860 bytes/18,112 triangles/20 primitives/CanopyWind. Small bands optimized 64→24 segments.
- Presentation: larger hero mascot, closer portrait/full jump fit, corrected portrait ground shadow; warmer evening and readable cool/warm night, original palette/materials. Five clear action shortcuts, dropdown comparison, mesh feedback; low/medium/high, optional cinematic camera yielding to orbit, pause/OS/offscreen and PNG fallback retained.
- Verification COMPLETE: production typecheck/build PASS; five GLBs Validator 0 errors/0 warnings; 10 production + 10 exact extracted-static repository-subpath checks PASS, no critical page/console errors or missing resources. Human actual hero/lighting/face/locomotion/mobile/fallback and decoded movie frames inspected.
- Exact candidate: showcase-v0.4/index.html, 10,213,265 bytes, SHA cd238a4c79f378d05eea098ec3f55c207c24c91444afce459d1345c012572846; JS/CSS/10 verified original GLB/texture/PNG assets embedded, strict static allowlist index.html/.nojekyll, dependency notices included. Provenance/known-secret/private-content audit PASS; downloads/v0.4 ZIP hashes in package-manifest.json.
- Source preservation: 43 baseline .blend/GLB/texture/animation/export/showcase/download/workflow/lockfile files exactly match 9c3c373 baseline. App dependencies unchanged; no paid service, external HDRI/large texture/audio/backend.
- Measured costs: Low 115 draw calls /131,121 triangles; Medium/High 228 /262,175 incl shadow passes. World exports total4,707,444 bytes exceeds old4MB goal explicitly; Low exceeds old provisional80draw goal but fits v0.4 QA ceiling135/155k. Physical device GPU/FPS unmeasured (QA-004); cloud software video may stutter, no60FPS claim.
- Movie: actual CDP compositor frames after GLB readiness, 52 JPEGs/original timestamps, VFR H.2641280×660/44.92s/641,340 bytes. No synthetic or accelerated motion. Removed only bottom60px asynchronous film-caption strip; raw/uncropped capture retained, decoded keyframes human-inspected.
- Historical QA: failed constant face export caught by real mouth/eye assertions and human images, corrected with supported Blender keep-constant-channel flag; per-clip body/face reset channels now validated. Cloud transport/server interruption and default5s soft-render polling failure retained; supported server restart/60s deadlines, all assertions kept. Final reports supersede failed/interrupted runs.
- Public site: https://anapaulagatti.github.io/3D-pharse5-/ remains exact approved v0.3 HTML SHA0ce49e58. Confirmed real origin200; deployment workflow and its inputs unchanged. V0.4 not publicly deployed; candidate STOP policy and publication approval still apply.
- Viewing: extract downloads/v0.4/living-hanok-v0.4-review.zip and run START_WINDOWS.cmd or python3 start.py (Python3 required); browser opens actual app through HTTP. Source viewers do not render raw index.html. No user-facing cloud localhost link.

## NEXT SESSION HANDOFF

**Current milestone:** BIG-UPDATE-004 COMPLETE. STOP for v0.4 visual feedback.

**Current task ID:** VISUAL-REVIEW-004 pending user. PUBLIC-RELEASE-004 only if explicitly requested. WORLD tasks unstarted.

**Last verified checkpoint:** 7bd2ada pushed and independently matched remote before the final complete-evidence handoff. The final docs/candidate-evidence commit follows; verify origin/main after push.

**Completed work:** All v0.4 rig/12 native clips/face/Hanok/life/light/material/camera/UI work, production/build and five Validator0/0, twenty real browser stages, human image/movie inspection, exact ZIP/subpath/preservation/privacy/provenance audit.

**Unfinished work:** User visual feedback; optional later publication. Physical device profiling QA-004 remains unavailable. No extra environment or optional audio work authorized.

**Files to inspect:** quality-reports/v0.4/REVIEW.md, VERIFICATION_SUMMARY.json, final-render/verification.json, candidate-render/verification.json, capture/media-report.json; exports/v0.4/asset-manifest.json, versioned Blender sources and showcase-v0.4/build-info.json; package-manifest and PERFORMANCE_REPORT.

**Known blockers:** None for reviewing candidate. Physical GPU/phone FPS unmeasured. Original fallback poster intentionally retained.

**Exact next command or action:** Review the before/after gallery, 45s movie and ZIP; await user feedback. Do not rebuild assets/setup, add districts or deploy v0.4 automatically. If later explicitly publishing, stage only the reviewed candidate and verify actual public render again.

**Verification required:** All relevant checks complete for HTML SHAcd238a4c79f378d05eea098ec3f55c207c24c91444afce459d1345c012572846. Repeat only for a new authorized change or concrete failure. Source/export/asset preservation must continue.

**Remote GitHub save status:** Prior checkpoints through7bd2ada verified. Final docs/candidate proof save follows in history; compare origin/main to HEAD after push before claiming persistence. V0.4/doc/evidence paths do not trigger scoped v0.3 Pages deployment.
