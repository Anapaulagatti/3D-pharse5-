# Studio decisions

- 2026-10-13: The latest supplied STUDIO_MASTER_PROMPT.md authorizes continuing beyond environment setup. Keep the existing app and isolate work from Korean Arena production.
- Preserve compatible stack: React/React DOM 19.3.0, Three 0.186.1, R3F 9.8.1, Drei 10.7.9, Vite 8.3.4, TypeScript 5.9.3. npm lockfiles are authoritative; no dependency reinstall/upgrade without need.
- Art direction: Hanji Craft × Celadon Ceramics × Miniature Seoul × gentle magic. Follow existing ART_DIRECTION.md palette: ink #15243A, cream #F5EFE1, jade #72BEAC, coral #E57B69, brass #CFAC67, haze #AFC7E0.
- Mascot is not selected yet. Compare exactly three substantially different designs; choose through a documented technical/art rubric. Do not label the choice user-approved without an explicit user decision.
- Modeling: reproducible Blender Python scripts and editable .blend sources; export Y-up glTF in meter-equivalent units, stable names, real geometry and clips. Lightweight transform animations are preferred to unnecessary rig complexity.
- Export: retain existing exports/v1 contract; no required Draco/meshopt decoders for the first delivery. Verify original/optimized clip names, durations, topology and rendering.
- Use available native image generation for concept exploration only. Do not configure a paid external provider or optional sprite forge in this first slice.
- Progress: GitHub checkpoints plus four persistent records, before expensive operations and after meaningful verified subtasks. Never depend only on chat history.
