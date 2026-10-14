# REFORGE-005 — pre-production audit

Target: Korean Arena 3D Studio v0.5 — Joseon Fantasy Reforge. Gate A is concept review, not a completed playable release.

## Recoverable public baseline

- Local and independently read origin/main: `9cc1381792b768f1e973d45b3421d24eb514c0d5`, clean at entry.
- Public v0.4: HTTPS 200, text/html, 10,213,265 bytes, SHA `cd238a4c79f378d05eea098ec3f55c207c24c91444afce459d1345c012572846`.
- Pages run 38530210414 completed successfully; the latest three runs are completed. No active deployment to interrupt.
- `preserved-v04.json` records 75 approved source/model/texture/export/package/modeling/deployment files. Existing source snapshots are also recoverable from the baseline Git tree.
- Pages workflow watches only its own file, the existing staging script and showcase-v0.4 HTML/metadata. This Gate A changes none of them. v0.5 publication is not authorized.

## Actual implementation findings

| Area | Observed source/export | Consequence for v0.5 |
|---|---|---|
| Building envelope | `arena.py:pavilion` creates four columns, two crossbeams, two side beams and three rear paper screens; front/left/right have no complete wall/door envelope | Rebuild an actual four-sided building; do not hide missing walls behind scenery |
| Roof support | `roof` generates thin sampled roof sheets/ribs/ridge; no purlin/rafter/underside framing. Columns top at z1.90; beam tops z1.985; curved roof surface starts above this | Build a continuous roof-to-rafter-to-purlin-to-beam-to-column-to-stone load path; close the visible support gaps |
| Additive detail | v0.3/v0.4 scripts add carved accents, railings, valances, planters, canopy and skyline | These layers do not provide missing structural walls or roof support. A new structure must replace the old pavilion in the candidate rather than stack more decorations on it |
| Character rig | Actual v0.4 GLB: zero skins, zero JOINTS_0/WEIGHTS_0 attributes, zero morph targets; 12 node-transform clips | Keep it as the legacy companion; create a genuinely skinned humanoid after concept approval |
| Movement | `LivingMascot.tsx` samples authored clips in a fixed display location; Walk/Run have oscillating root displacement; no input controller, collision or world locomotion | Implement world movement and synchronized in-place gait, contact and collision. Do not represent current showcase loops as playable humanoid locomotion |
| Face | v0.4 switches actual alternate mouth/eye geometry and supports gaze/blink | Preserve this asset, but author new facial controls with the new humanoid, including ten reviewable expressions |
| Preview | Existing React19/R3F9/Drei10 scene, orthographic OrbitControls, three light presets, quality tiers, OS motion preference, visibility handling and PNG fallback | Reuse this working shell and dependency tree. Add isolated candidate modes only after gates allow implementation |
| Cost | Saved v0.4 Low115 draws/131,121 triangles; medium/high228/262,175 incl shadows; world GLBs4,707,444 bytes | Rebuild with a new measured budget; do not load all legacy/additive models alongside the candidate by default |

Five exported GLBs were directly parsed in `existing-glb-inspection.json`; all original clip names and actual skin attributes are recorded. This structural inspection does not replace render review or a new Validator run. Existing five-GLB Validator0/0 and ten-stage public browser evidence remain in v0.4 reports.

## Reference consulted

[Seoul Metropolitan Government — Structure of Hanok](https://hanok.seoul.go.kr/front/eng/info/infoHanok.do?tab=2), fetched with TLS validation, HTTP200, 33,031 bytes, SHA `c419a612e75c5e50672b516c1eaa400bd52c867fa09599c8594e60d07704bddd`.

The page describes a timber framework of columns, crossbeams, purlins, rafters, supports and connectors, with regional and functional variation. It describes raised wooden maru and straight-line, L, U and square layouts. The proposed small straight-line scholarly house is a stylized fantasy interpretation, not a certified historical reconstruction. No website photos, diagrams or third-party textures are copied into the asset library.

## Current scope and gate

Archive the exact request, inspect saved Blender sources and existing actual rendered evidence, produce three genuinely different original humanoid concepts and a dimensioned architecture/controller plan. Save and verify checkpoints. Stop for the user's concept choice before the expensive final character build, as requested in section15 Gate A. Gates B–E and the v0.5 milestone remain unfinished.
