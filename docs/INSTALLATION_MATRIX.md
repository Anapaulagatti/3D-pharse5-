> Historical Gate2 baseline. User rejected its art. Current art pass: docs/PIXEL_RESET_ART_BIBLE.md; tool versions remain unchanged.

# Installation matrix

`checkpoint_sha` identifies source/evidence checkpoint, not a package version. Later media/build/clean-clone results are in VERIFICATION_SUMMARY.json. Distinguish optional native executables from the verified permitted headless contracts.

| tool_id | source | pinned_version_or_SHA | license | mandatory_for_gate | installed | executable/discovered | test_command_or_invocation | actual_result | limitations | checkpoint_sha |
|---|---|---|---|---|---|---|---|---|---|---|
| phaser | npm registry / package.json | 4.2.1 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| typescript | npm registry / package.json | 5.9.3 | Apache-2.0 | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| vite | npm registry / package.json | 8.3.4 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| vitest | npm registry / package.json | 5.0.4 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| @playwright/test | npm registry / package.json | 1.64.1 | Apache-2.0 | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| eslint | npm registry / package.json | 10.12.0 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| typescript-eslint | npm registry / package.json | 8.71.2 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| prettier | npm registry / package.json | 3.9.10 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| zod | npm registry / package.json | 4.6.7 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| @types/node | npm registry / package.json | 24.19.2 | MIT | 1 | yes | yes | build/browser or typecheck/lint/tests | VERIFIED_LOCAL | Chromium cloud only | 0dd7550 |
| Node / npm | official environment | 24.19.0 / 11.9.0 | Node/npm notices | 1 | yes | yes | --version, npm ci | VERIFIED_LOCAL | not a desktop host | 0dd7550 |
| Pillow source editor/exporter | python Pillow | 12.3.0 | HPND | 1/2 | yes | yes | npm run assets; assets:check | VERIFIED_LOCAL | open indexed PNG + scripts; no GUI claim | 0dd7550 |
| Tiled | mapeditor/tiled | 1.12.2 release inspected | GPL2+ | headless equivalent | no | no | generated .tmj loaded in Phaser, collisions tested | VERIFIED_LOCAL equivalent | native editor not installed; official local method TOOLCHAIN.md | 0dd7550 |
| LibreSprite | LibreSprite/LibreSprite | 1.3 release inspected | GPL2 | editable workflow equivalent | no | no | indexed PNG source round-trip equality | VERIFIED_LOCAL equivalent | GUI not installed | 0dd7550 |
| Chromium | existing system executable | see browser-version.json | Chromium notices | 1 | yes | yes | npm run test:e2e | VERIFIED_LOCAL | SwiftShader/touch emulation | 0dd7550 |
| ffmpeg | existing system executable | see browser-version.json | FFmpeg build license | evidence | yes | yes | tools/finish_capture.py | capture verification pending | local-only encoder, not runtime | 0dd7550 |
| Agent Sprite Forge | 0x0funky/agent-sprite-forge | 5324342fdfab72430f4e9604f3fe427009f8596d | MIT | optional | downloaded only | no Codex discovery | README/SKILL/source inspection only | SKIPPED | no provider/paid video calls | 0dd7550 |
| cloud-environment-onboarding:setup | c0/setup | provider-managed/no SHA exposed | provider skill | 1 | yes | yes cloud inventory | applied setup, installation, actual scene/browser | FUNCTIONALLY_VERIFIED | new saved config pending | 0dd7550 |

All five skill states and deferred custom wrappers are in SKILL_REGISTRY.md. No claimed install based merely on a reference/download.
