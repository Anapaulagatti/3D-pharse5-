# Studio asset inventory

| Asset | Source | Output / format | Status | Usage / milestone | Validation / provenance |
|---|---|---|---|---|---|
| Initial hanok/mascot prototype | preview/src/SceneView.tsx | Runtime JSX geometry | Existing study; preserve until replacement verified | Foundation / M2 | Five historical browser checks in d355dca; original procedural source |
| Static fallback study | preview/src/Poster.tsx | Inline SVG | Existing fallback | Foundation / M2 | Browser fallback checked in d355dca; original source |
| Toolchain fixture | Studio/scripts/create-smoke-fixture.py | Ignored Studio/.cache/smoke/*.blend, *.glb | Tooling test, not production art | Pipeline / M2 | Saved Validator reports; 0 errors/0 warnings; original procedural |
| Baseline screenshots | preview/tests/studio.spec.ts | quality-reports/preview-*.png | Historical evidence | Foundation / M2 | Actual Chromium captures; not current golden-slice output |

Production assets are listed below as they are saved and verified; inspect current manifest for exact sizes/checksums. Do not list planned files as delivered. Preserve successful concept-generation outputs before any retry.

| Three mascot/world directions | Original text specification, native image_gen | concepts/mascot-directions-v1.png / PNG, metadata JSON | Saved concept; A selected by technical rubric | Art direction / M3 | Actual generated image inspected; original AI generation, no external source images; not a mesh |

| Hanok arena source | Studio/modeling/arena.py and common.py | assets/source-blend/arena-hero.blend; assets/models/arena-hero.glb; exports/v1/models/arena-hero.glb | Saved geometry/export; visual review pending | Arena / M4 | Blender exported, Validator 0 errors/0 warnings, LanternSway clip, instance topology/bounds parity; original procedural |
| Ceramic Seed Spirit source | Studio/modeling/mascot.py and common.py | assets/source-blend/mascot-base.blend; assets/models/mascot-base.glb; exports/v1/models/mascot-base.glb | Six exported clips; browser playback review pending | Mascot / M5 | Validator 0 errors/0 warnings; six clip names/durations and node topology/bounds preserved; original procedural |

| Original grain textures | Studio/modeling/common.py | assets/textures/{hanji-grain,courtyard-stone}.png; embedded in GLB; exports/v1/textures/ | Saved 256×256 original textures | Materials / M4–M5 | Actual PNG headers checked; original procedural, no downloaded textures |
