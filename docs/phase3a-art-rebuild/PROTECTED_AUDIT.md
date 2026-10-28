# Preservation and rollback

Baseline `a9defb9a2151016f2177e25229becdecf6190538`;beforecheckpoint `checkpoint/phase3a-npc-art-before-rebuild-20261028`;rejected4ed5a53 and all previous checkpoints retained. [Exact frozen manifest](protected-baseline.json),[current audit and9before/after hashes](protected-audit.json).

**6591existing source/runtime/asset/tool/test files unchanged.** Allappsrc including NPC Registry/FSM/navigation/dialogue/population/persistence/culling/assets/camera/player engine are byte-identical. All14NPC IDs,names,occupations,spawns,route points,interaction radii,frame registrations/clip timings unchanged. Approved world,masks,geometry,collision,12players/28cosmetics/Studio/speeds/progress code unchanged.

Only9existing derived asset files change: `atlas.png`, `preview-native.png`, `provenance.json` forSeoyeon/Minseo/Harin. All3oldatlases remain recoverable;exact baseline copies serve the labelled BEFORE inspector. Elevenother rejected NPC illustrations remain byte-identical and await the human pilot gate.

New own illustrated masters,raw generation prompts,turnarounds,native finishes,retouches,PNGmasks,joints,occlusion patches,frames and build/QA tools are separate under `assets-src/npcs/phase3a-art-rebuild`, `tools/phase3a-art-rebuild` and this documentation directory. The review clip utility lives under tools and does not enter production gameplay. No original player or source illustration is re-exported.

`AGENTS.md` and `docs/current/PROJECT_STATE.md` record the explicit rejection,new3pilot authorization and review STOP. No historical source/tag/checkpoint overwrite,no main merge,no publicdeployment,no separate learning-site changes. Reproduce `python3 tools/phase3a-art-rebuild/audit.py`.
