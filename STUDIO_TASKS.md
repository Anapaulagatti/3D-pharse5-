# Studio task checklist

Statuses: TODO, IN_PROGRESS, DONE, BLOCKED. DONE requires outputs and verification. Milestones follow the persistent-progress prompt (nine milestones).

| Milestone | Stable ID | Deliverable | Status | Evidence |
|---|---|---|---|---|
| 1 Environment | ENV-001 | Audit existing checkout, tools and version compatibility | DONE | d355dca baseline; Node 24.19, React 19.3/R3F 9.8/Drei 10.7, Blender 4.3.2 |
| 1 Environment | ENV-002 | Preserve recovery records and supplied master prompt | DONE | Four root STUDIO files, AGENTS.md, STUDIO_MASTER_PROMPT.md |
| 2 Pipeline | PIPE-001 | Blender export, Validator, glTF Transform, gltfjsx tooling | DONE | quality-reports/toolchain-validation*.json; existing smoke fixtures |
| 2 Pipeline | PIPE-002 | Load exported production GLB in the existing React preview | TODO | Requires actual arena and mascot GLBs |
| 3 Art direction | ART-001 | Three distinct mascot/world explorations and selection rubric | IN_PROGRESS | |
| 3 Art direction | ART-002 | Color, materials, silhouettes and camera standards | TODO | Existing ART_DIRECTION.md is the starting point |
| 4 Hanok Arena | ARENA-001 | Editable curved roof, timber, courtyard, garden and skyline | TODO | |
| 4 Hanok Arena | ARENA-002 | Export GLB, inspect, optimize and validate | TODO | |
| 5 Mascot | MASCOT-001 | Selected original character model and editable Blender source | TODO | |
| 5 Mascot | MASCOT-002 | Six distinct exported animation clips | TODO | Idle, Happy, Thinking, Celebration, Disappointed, Greeting |
| 6 Animation/polish | PREVIEW-001 | Lighting, camera, POIs, animated lanterns and restrained atmosphere | TODO | |
| 6 Animation/polish | PREVIEW-002 | Real asset info, loading, failure states and reduced motion | TODO | Existing accessible controls/fallback are preserved |
| 7 Optimization/QA | QA-001 | GLB stats, clip parity, checksums and provenance manifest | TODO | |
| 7 Optimization/QA | QA-002 | Build, desktop/phone viewport, animation and fallback browser checks | TODO | Baseline five tests passed in d355dca; rerun after changes |
| 7 Optimization/QA | QA-003 | Render review, fallback posters, transparent mascot portrait | TODO | |
| 8 Districts | WORLD-001 | Hangul Garden, Vocabulary Café, Grammar Library | TODO | Start only after golden slice is reviewed |
| 8 Districts | WORLD-002 | Listening Subway, TOPIK Academy, EPS Workshop | TODO | Start only after golden slice is reviewed |
| 9 Handoff | EXPORT-001 | Versioned portable exports, licenses and integration notes | TODO | No production integration |
| 9 Handoff | SAVE-001 | Verify remote checkpoint and session-end recovery instructions | TODO | |
