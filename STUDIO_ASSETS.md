# Korean Arena — reset asset inventory

Active review candidate: **reset-v2; no direction approved**. All paths below are relative to this repository.

| Direction | Character / distinct form | Environment |
| --- | --- | --- |
| A Moonletter Garden | Arin courier; split celadon coat, coral scarf, paper hairpin, satchel; envelope-wave | L-wing giwa hanok, timber porch/plinth, plum and pine, tea pavilion and koi pond |
| B Ginkgo Commons | Seoha scholar; broad beret, glasses, ivory coat/pleats, book/backpack; book-lift | Two-storey Korean seowon library, stone stair, diamond-edged civic slabs, ginkgo/narrow pine, book fountain and kiosk |
| C Hanji Afterhours | Jun performer; side ponytail/headphones, cropped purple jacket, cyan trousers, camera pouch; overhead lightsticks | Split-height workshop/roof terrace/stair, brick lane, willow/orange tree, market stall/stage/lantern arch |

Editable originals and exact prompts: assets-src/reset-v2/{A,B,C}. Native object master provenance: SOURCE_PROVENANCE.json. B object-master.png is retained but rejected for European architectural drift; active corrected source is object-master-korean.png. The other active object masters are A/object-master.png and C/object-master.png. Do not accidentally restore the rejected B master to production.

Characters/tiles/small props: tools/export_reset.py, per-frame PNG originals, manifest.json and worlds.json. Fixed48×64 character anchors,72frames/style, atlas512×1024 with2px gutters;32px tiles and three independent30×24 maps. Objects are separate depth-sorted/collidable sprites, not a whole rendered backdrop. Production objects use binary alpha and at most128 colours; characters at most64. Generated masters are not claimed manually pixel-placed. Export uses explicit crops/alpha connected components and nearest-neighbour scaling; originals untouched.

Runtime: public-reset/assets/reset-v2,52 files, approx1.46MB. Map objects A25/B24/C25; colliders23/20/21. Vite publicDir selects public-reset only. New build excludes old rejected public/assets/A/B/C, master prompts/PNGs, Blender/GLB archive and private data. Original/dependency license records are in LICENSES.md and public-reset/licenses.

Review media: quality-reports/pixel-reset-v2/REVIEW.md; DIRECTIONS_IN_ENGINE.png, OLD_VS_NEW.png, ACTUAL_CHARACTER_READABILITY.png, SOURCE_VS_ENGINE_A/B/C.png; final-render native idle/walk/emote/overview/mobile; blink real natural blink retained by normal Pause control. Final movie premium-pixel-reset-motion.mp4 has413 CDP compositor frames over46.55s with original Chrome timestamps, plus decoded stills. Raw current frames/timestamps in motion/. Historical attempts and VIDEO_BLINK_EVIDENCE/VIDEO_IDLE_LIFE boards are retained as earlier attempts, not the final natural-blink proof.

Portable static ZIP: downloads/pixel-reset-v2/premium-pixel-reset-review.zip; exact per-file hashes and size in package-manifest.json; extracted HTTP checks/screenshots in quality-reports/pixel-reset-v2/package/. The package contains runtime only and Python launcher; no Node required for viewing.

Preserved rejected baseline: assets-src/A,B,C; public/assets/A,B,C; tools/export_art.py; downloads/pixel-v3.1 and quality-reports/pixel-v3.1. Verification214protected files +110review files in preservation.json. Original3D archive/tag at f1f13f2; frozen showcase-v0.5 remains excluded from new build. No approved originals deleted or regenerated.
