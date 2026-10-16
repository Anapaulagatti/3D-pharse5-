# Actual tool use — URBAN-PLAN-002 refinement gate

Read AGENTS.md, mandatory registry, four STUDIO records and actual upstream `generate2dmap/SKILL.md` / `generate2dsprite/SKILL.md` at Forge5324342fdfab72430f4e9604f3fe427009f8596d before authoring. Consulted proven Forge and Juni production reports. Existing Juni144frames/creator workflow, all runtime art/controller/UI/test/lock/workflows are preserved. No upstream tool update, new production dependency or new asset generator was installed.

## Executed now

```sh
FORGE_MAX_PAID_REQUESTS=0 python3 /workspace/tooling-cache/agent-sprite-forge/skills/generate2dmedia/scripts/forge_doctor.py --host-tools image_gen --save .cache/urban-refinement/forge-doctor.json
python3 tools/check_urban_zoning.py
python3 tools/render_urban_zoning.py
CI=true bash tools/setup.sh
```

- `forge_doctor` is a non-generating diagnostic: host image tool available, video NO_ROUTE, CLI proof UNKNOWN/PRESENT,7optionalMISSING. Missing API credentials/Grok/resvg are not blockers for planning or existing game validation; no key values were printed. Raw [doctor JSON](forge-doctor.json). User's no-paid-routes rule overrides any upstream key-as-consent suggestion.
- Geometry/diagram tools use existing Python3.12.14, Pillow12.3.0 and numpy2.3.5; exported SVG is ordinary editable XML with semantic groups, not resvg output. They draw **schematics only**, never replacement pixel game artwork, runtime bundles, Tiled data or colliders. Normal setup/build do not call these authoring tools or regenerate art.
- Official research used read-only HTTPS text retrieval from KHS and UNESCO. Four response contents were checked, own-word observations and original translations retained with URL/hash in references.json. Two false Bukchon lookups were rejected (404 / wrong actual content despite200), not claimed as researched evidence. No external photos, maps, game art or provider services were copied.
- The first schematic check FAIL found five roads touching expanded building/gate corners and a disconnected instrument platform. Raw report retained at history/refinement-first-clearance-fail.json. Real geometry was changed: wider setback at workshop entry, shifted book/tea lanes, lower residential bend, exterior gate stopping point and added platform-to-court apron. Thresholds, bridges and building collision masks were not weakened.
- Final preliminary check:41targets /37022walk cells connected,0inter-building overlaps,0road intrusions into masses/protected banks outside decks,one closed classified palace perimeter,0palace-wall cells in market/homes,2aligned bridges across actual planned water. Compare footprint silhouettes independently of colors; distinct multi-mass homes/program buildings, not simple recolors. Roofless monument/ceremonial gate are intentionally simple landmark shapes. These checks do not approve final art or imply a game has been built.

## Not executed / production still gated

No image-generation tool, paid API/provider, master_still, sprite_set, frame synthesis, prop/terrain extraction, finish_frames, palette generation, map_bundle, map_nav, official scene marker preview or Tiled export was executed for this refinement. No final buildings, replacement sprites, NPCs, quests or playable district assembly. Existing actual Forge/Juni generation/processing evidence and strict WARN/FAIL records remain unchanged in their historical production reports.

After this masterplan receives explicit approval, use the proven real Forge layered-map/prop/terrain/nav/linked-room/Tiled workflows and test the actual Phaser result at native Juni scale. The planning JSON is not map_bundle.v2; its footprint bounding boxes must not become solid rectangles closing U/L courts. Source pixels, roof/canopy/eaves/platform envelope, depth, foot collision and runtime accessibility/mobile performance remain future checks, not delivered proof.

Relevant regression uses the existing exact npm lock/Node24.19.0/Phaser4.2.1/Vite/TypeScript/Chromium. `tools/setup.sh` validates stored assets, type/lint/format/unit/build/browser checks; it never generates art. Exact observed final CI/clean-clone SHA/results belong in verification.json and the actual annotated checkpoint/urban-refinement-review-20261016 after verification. No website deployment/main promotion.
