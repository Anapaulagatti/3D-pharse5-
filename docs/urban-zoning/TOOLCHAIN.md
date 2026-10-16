# Actual tools used in this zoning gate

Read mandatory project registry and complete actual upstream `generate2dmap/SKILL.md` and `generate2dsprite/SKILL.md` at Agent Sprite Forge `5324342fdfab72430f4e9604f3fe427009f8596d`. Reused installed Node24.19.0, Python3.12.14, Pillow12.3.0, exact Phaser/Vite/TypeScript/npm lock and Chromium. No new dependencies or globally registered skills were installed; the upstream skill sources exist in the documented external tooling cache.

Executed:

```sh
FORGE_MAX_PAID_REQUESTS=0 python3 /workspace/tooling-cache/agent-sprite-forge/skills/generate2dmedia/scripts/forge_doctor.py --host-tools image_gen --save .cache/urban-zoning/forge-doctor.json
python3 tools/render_urban_zoning.py
CI=true bash tools/setup.sh
```

The diagnostic reports host_image available, FFmpeg ready, no video generation route; optional missing API credentials/Grok/resvg remain missing. CLI image route proof is UNKNOWN/PRESENT, not verified. It made **no media/API/provider call**. See [raw doctor result](forge-doctor.json). User's paid-route prohibition overrides any upstream suggestion that a key grants spending consent.

The diagram renderer draws a **planning diagram only**, from editable zoning JSON, and samples reserved circulation on a16px grid. It produces PNG/SVG plus planning-check.json. It does not create runtime pixels, procedural replacement map art, map_bundle.v2, a Tiled export or game colliders. Nineteen proposed approach/NPC locations are connected in this approximation; final ground/roof/canopy geometry, art/collision alignment and native Phaser traversal of the proposed map are **UNRUN** until zoning approval.

No image generation, master_still, prop extraction, terrain extraction, finish_frames, map_bundle, map_nav, scene marker preview, export_tiled or character-animation production was executed for this gate. Earlier actual pipelines and raw WARN/FAIL records remain unchanged in docs/gwanghwamun, docs/juni-animation and docs/living-seoul. No claim of a new playable district or visual artwork approval.

After zoning approval, use the actual documented layered-map/prop/terrain/nav/linked-room/Tiled workflows and original generated art sources; preserve the current game and verify native rendered scale, routes, collision, occlusion, entry/exit, mobile/touch/Canvas and accessibility. Do not substitute the zoning diagram for that production evidence.
