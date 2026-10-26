# Korean Arena — Phase 1 character foundation

Read [PROJECT_STATE](docs/current/PROJECT_STATE.md) and [Phase 1 directive](docs/current/PHASE1_DIRECTIVE.md). These supersede historical Gate3 STOP instructions.

- Work on `feature/phase1-character-foundation`. No delegation unless explicitly requested by the user.
- Approved world baseline `checkpoint/world-art-approved-phase1-20261026` is immutable. Canonical world is `palace-cleanup-world`, never V10 graybox.
- No map art/coordinates/collision/camera/tour changes. Preserve Juni source/native atlas/animations/movement. Verify `docs/phase1/protected-world.json` and `protected-juni.json`.
- Build one shared character registry/manager/controller, selection UI and versioned local preferences. New art must pass native animation/identity gates; unfinished characters stay explicitly incomplete and unplayable, never placeholders or Juni recolors.
- Preserve original source art, Sprite Forge/animation tooling, tests, licenses and all checkpoints. Cleanup only via documented inventory, unknown ownership means KEEP.
- No paid external artwork APIs, separate learning-app changes, Phase2 gameplay, main merge or public deployment. Stop after the Phase1 playable package and honest QA for human review.
- Historical engineering/instruction records live in docs/history/pre-phase1 and Git. They are not current authority.
