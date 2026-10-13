# Portable first slice — v0.2.0

This is an independent art/preview handoff. No Korean Arena production code, backend, auth, user progress, exams, payments or QR features were accessed or changed.

- `models/arena-hero.glb`: curved-roof arena, timber/screens, courtyard, garden, bridge and skyline; `LanternSway` is a 3-second ambient clip.
- `models/mascot-base.glb`: Ceramic Seed Spirit; `Idle`, `Happy`, `Thinking`, `Celebration`, `Disappointed`, `Greeting`, each 2 seconds.
- Model axes: exported Y-up, original Blender Z-up; meter-equivalent units. Arena origin is the nominal courtyard ground plane; collectible plinth extends to Y=-0.7 and paving is slightly raised above Y=0. Mascot local origin is at its feet. Actual bounds are in the manifest.
- Preview placement: mascot at [-0.4, 0.48, 1.0], scale 0.82 in the arena; isolated showcase scale 1.35. These are preview choices, not required application transforms.
- No required Draco/meshopt/texture decoders. PNG textures are embedded; separate originals are provided. Base-color maps use sRGB. Materials are glTF PBR, opaque; no transmission or postprocessing is required.
- Clone scenes before independent per-instance animation/material changes. Do not dispose geometry/textures still owned by a shared GLTF cache. Use an AnimationMixer for the actual embedded clips.
- Preserve stable node names if consuming clips. Optimization retains every scene node's topology/bounds and exact animation sampler arrays. One deterministic Celebration pose is checked pixel-identical in raw vs optimized GLB browser renders; this does not replace testing all animation on a target device.
- Reduced motion: select a static pose (the preview uses clip time 0.8s), freeze decorative motion and render on demand. A pause toggle preserves current animation time.
- Use `posters/arena-desktop.png`, `arena-mobile.png` and `mascot-transparent.png` for WebGL failure and low-resource presentations. These are actual renders, not concept artwork.

Proposed visual API only:

```ts
type MascotState = 'Idle' | 'Happy' | 'Thinking' | 'Celebration' | 'Disappointed' | 'Greeting';
type SceneQuality = 'low' | 'medium' | 'high';
type ArenaVisualProps = { mascotState?: MascotState; quality?: SceneQuality; reducedMotion?: boolean; lighting?: 'day' | 'evening' | 'night' };
```

The standalone preview uses React 19 / R3F 9 / Drei 10. The eventual application must use its own compatible renderer versions; this handoff does not authorize upgrading its dependency tree. Lazy-load model assets and keep core learning UX available without WebGL. Physical-phone GPU/FPS is not yet verified. Six learning districts are not delivered in this version; see manifest missing_assets and STUDIO_TASKS.md.
