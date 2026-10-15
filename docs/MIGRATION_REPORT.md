# Migration report — Pixel v3.1

Gate0: remotely verified archive f1f13f2b4aebcc2659d94cde84800cef17ad7a4e, exact branch/tag + fresh independent HTTPS clone; all2738 file hashes matched. No LFS. Full restore commands and per-file inventory: migration/3d-archive-proof.md/json. Pending v0.6 work saved honestly unfinished.

2718 tracked obsolete paths removed from active working branch only, grouped in migration/deletion-manifest.json: old3D runtime/builds/tests, Blender generator/export pipelines, GLB/texture/source art, archived renders/media, old concepts/packages and superseded art docs. Git history/archive/main are not rewritten or deleted. Retain general-purpose provenance/checkpoint policy and historical exact user requests; original versions accessible through archive. Two immutable v0.5 release files kept as deployment hold and excluded from Vite dist. Ignored duplicate builds/dependency directories moved outside active checkout; no unique untracked source destroyed.

Removed active legacy runtime deps: Three, React, ReactDOM, React Three Fiber, Drei and React plugin/type packages. Old Studio glTFTransform, gltfjsx, glTFValidator/Blender pipeline removed from branch. Active lock has Phaser/Zod and required TypeScript/Vite/Vitest/Playwright/ESLint/formatter tools only. No GLB/Three/R3F/Drei/Blender import in active app.

New default root index.html/src/main.ts launches original 2D Phaser4.2.1 tilemap/sprite/Arcade scene; strict typed domains, original editable indexed art, atlas/export/map validation, local progress and Vietnamese HTML shell. Three art candidates; no final art approval. Working branch rebuild/pixel-social-rpg-v3, not merged to main.

Old Pages workflow removed on pixel branch, replaced with read-only test CI (no Pages deploy permission/job). Main/public v0.5 unchanged and independently HTTP-hash checked082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f. No replacement deployment authorization or claim.

Tool versions/limitations: TOOLCHAIN.md, INSTALLATION_MATRIX.md, SKILL_REGISTRY.md. Native Tiled/LibreSprite GUI absent; verified permitted editable PNG/TiledJSON workflow. No paid providers/cloud resources/account integration, ads or free-text chat. Clean remote-clone verification and measured candidate report are referenced in quality-reports/pixel-v3.1/VERIFICATION_SUMMARY.json after completion; do not confuse source push with remote CI success.
