# Skill registry — current Codex session

States are independent: REFERENCED, DOWNLOADED, INSTALLED, DISCOVERABLE_IN_THIS_CODEX_SESSION, FUNCTIONALLY_VERIFIED. npm packages and executables are not Codex skills. File existence alone does not establish runtime discovery. No runtime restart API or skill-installer tool is exposed in this session.

| Skill | Referenced | Downloaded | Installed | Discoverable | Functionally verified | Result |
|---|---|---|---|---|---|---|
| cloud-environment-onboarding:setup | yes | provider-delivered | provider-managed | yes, cloud skills.list/read | yes, actual npm installation + Phaser HTTP/browser/build workflow | APPLIED; current cloud package c0/setup, provider exposes no version SHA |
| Agent Sprite Forge generate2dsprite/generate2dmap/video2dsprite/generate2dmedia | yes | yes, pinned5324342fdfab72430f4e9604f3fe427009f8596d | no | no | no | SKIPPED optional provider workflow; README/SKILL/license/code inspected, no provider invoked |
| pixel-art-qa | planned | no | no | no | no | DEFERRED as a Codex wrapper; actual equivalent tools/check_art.py and browser QA run directly |
| phaser-tilemap-integration | planned | no | no | no | no | DEFERRED wrapper; exporter/Tiled validator/real scene smoke implemented as repository tools |
| korean-game-content-qa | planned | no | no | no | no | DEFERRED Gate3; no expert-certified curriculum claim |
| social-game-safety | planned | no | no | no | no | DEFERRED Gate4/5; no real chat/accounts |
| rewarded-ads-integrity | planned | no | no | no | no | DEFERRED Gate8; no ad SDK/revenue |

Gate1/2 selected skill is the available/discoverable onboarding skill; its functional test is the genuine setup+launch+browser validation, not installing a duplicate skill. Custom wrappers are not needed to execute the small existing tools and are not claimed installed. No hundreds-of-skills install or pretend activation. If future gates choose new project-local skills, verify supported discovery/restart first; BLOCKED discovery must remain explicit, never inferred from .agents/skills directories.

Forge source: https://github.com/0x0funky/agent-sprite-forge, MIT; cache `/workspace/tooling-cache/agent-sprite-forge` outside production, not vendored or declared a project checkout. Its generation routing/video requirements do not make paid use necessary for our original code-authored pixel pipeline. Existing skill inventory cloud: onboarding only; executor: empty. Checked project and user .agents/.codex locations; legacy builtins/remote-skills dirs are not invocation evidence. No raw credential values inspected.

Session update after successful skill application: developer later removed the cloud skill catalog. Onboarding was discoverable/read/invoked during setup (evidence above); it is not claimed currently invocable from the updated catalog. No custom skill is claimed installed or activated. Tested repository tools/start instructions remain runnable independently of skill inventory.
