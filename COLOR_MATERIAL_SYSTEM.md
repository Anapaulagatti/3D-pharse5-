# Color and material system

| Role | Color | Material behavior |
|---|---|---|
| Structural ink / roof | #293C55 / #15243A | Roughness 0.60–0.80, low metalness; curved ceramic ribs |
| Paper / courtyard stone | #F5EFE1 | Hanji roughness 0.92; stone 0.85; subtle original 256px grain |
| Signature ceramic | #72BEAC | Roughness 0.26–0.38, metalness 0.05; sculpted readable volumes |
| Blossom / cheek accents | #E57B69 | Matte, small deliberate areas |
| Inlaid brass / lantern frames | #CFAC67 | Metalness 0.65, roughness 0.34; restrained borders |
| Skyline / distant structures | #AFC7E0 | Opaque muted blue; no costly transparent layer stack |
| Lantern cores | warm amber | Hanji emissive material; low-cost lighting accent |

Use sRGB for base color images. Blender procedural grain is generated into actual PNGs, packed into .blend and embedded into GLB where used. Normals/roughness are geometric/material values, not falsely claimed texture maps. No downloaded textures, HDRIs, proprietary fonts or paid assets.

Materials are shared and static environment meshes merged by material. Movable lantern nodes and mascot parts remain separate for animation. Avoid transmission, heavy bloom, giant textures and required compressed-mesh decoders for this first slice.
