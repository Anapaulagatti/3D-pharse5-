# Korean Arena — V10 clean-room graybox review

The current user request is docs/current/V10_CLEANROOM_REQUEST.md. It supersedes V9 production directives. Read that file, docs/ART_SKILL_REGISTRY.md and all four STUDIO records.

Work on rebuild/southern-city-cleanroom-v10 in /workspace/southern-city-v10. This is a fresh clone of V9 ed007df73dac31ed834cb3fbb85a3cc80bdf26a0. Remote-verified recovery/before-v10-cleanroom-20261021 protects that exact commit; never retarget tags, rewrite history, force push, merge into main or deploy the website.

MANDATORY STOP: deliver the new urban masterplan and playable graybox, then wait for explicit USER approval before final environment artwork or phases D–F. No paid APIs, separate-app edits, delegation, or worktrees. No claim that numeric tests approve the design.

V10 planning/build inputs: tools/v10_plan.py, assets-src/v10-city/plan/city.json, assets-src/protected-north and its north-only native library references. No V9/V8/V7/V6 southern plan, mask, atlas, coordinates or screenshots may feed the V10 planner/compiler. tools/v10_compare.py alone reads V9 geometry for a labeled diagnostic AFTER the independent plan commit. Never use its output as generation input. V9 source originals remain inactive for recovery/diagnosis; generated public/assets/world and its entry page have been removed.

Protect the north 0..2239, its273placements/253solids/native art, Juni144frames, Academy, shared engine/controller/joystick/UI and existing source/license/tooling. assets-src/v10-city/protected-files.json and tools/v10_validate.py enforce stored integrity; preserve lockfiles. Native1024x768 north render matches V9 at the documented camera/DPR/reduced-motion settings.

Runtime uses public/assets/v10-city only for the outdoor map. New southern volumes/materials are explicitly requested geometric placeholders, not final pixel artwork. Setup never generates art: npm ci --ignore-scripts, bash tools/setup.sh validates stored source/runtime and browser flows. Node24+/Python3.12/Pillow12.3/Chromium are required. npm run dev:4200; npm run preview:4201, base /3D-pharse5-/. Loopback is internal, never a public preview. Use docs/v10-city/V10_GRAYBOX_REVIEW.zip for a local HTTP review.

Rebuild graybox only when authorized: python3 tools/v10_plan.py then python3 tools/v10_build.py. Freshness checks deliberately fail until hashed Forge/nav proofs are refreshed in new output directories. Forge remains optional for setup, pinned5324342fdfab72430f4e9604f3fe427009f8596d. All mandatory reports, actual captures, comparison limitations and test evidence are in docs/v10-city. Do not regenerate approved art or expand production past the approval gate.
