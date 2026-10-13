# Asset provenance

All delivered 3D geometry, animation, material definitions, texture grain and rendered posters were created for this Studio from original procedural Blender Python source. No asset store model, scraped image, downloaded texture, HDRI, branded character or paid font was used.

The project uses the asset provenance label `project-owned-original` defined in EXPORT_CONTRACT.md. This is ownership/provenance metadata for these Studio outputs, not a new open-source license applied to the entire repository.

| Output | Source / provenance |
|---|---|
| Arena, lantern geometry/animation | Studio/modeling/arena.py, common.py; original Korean-inspired construction |
| Ceramic Seed Spirit and six clips | Studio/modeling/mascot.py, common.py; original procedural interpretation of selected concept A |
| Hanji / stone texture PNGs | Deterministic original grain from common.py; 256×256, packed and embedded |
| Arena posters | Actual Chromium capture of delivered GLB scene |
| Transparent mascot portrait | Native Blender/Cycles render of the saved model; RGBA 800×1000 |
| Three-direction concept sheet | Native image_gen from an original text specification, no external reference images; metadata in concepts/mascot-directions-v1.json |

Dependencies retain their respective upstream licenses. They are installed through npm and are not copied into the portable asset export. The preview remains a separate development app. No external asset attribution requirements were introduced.
