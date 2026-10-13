# Studio decisions

- 2026-10-13: The latest supplied STUDIO_MASTER_PROMPT.md authorizes continuing beyond environment setup. Keep the existing app and isolate work from Korean Arena production.
- Preserve compatible stack: React/React DOM 19.3.0, Three 0.186.1, R3F 9.8.1, Drei 10.7.9, Vite 8.3.4, TypeScript 5.9.3. npm lockfiles are authoritative; no dependency reinstall/upgrade without need.
- Art direction: Hanji Craft × Celadon Ceramics × Miniature Seoul × gentle magic. Follow existing ART_DIRECTION.md palette: ink #15243A, cream #F5EFE1, jade #72BEAC, coral #E57B69, brass #CFAC67, haze #AFC7E0.
- Selected A, Ceramic Seed Spirit, through concepts/DESIGN_REVIEW.md (29/30 vs 24/30 for B/C). Technical/art selection, not user approval. Preserve the three-direction sheet. Pear silhouette, scalloped rim, asymmetric paper/ceramic leaf ornaments and brass inlay; lightweight transform clips.
- Modeling: reproducible Blender Python scripts and editable .blend sources; export Y-up glTF in meter-equivalent units, stable names, real geometry and clips. Lightweight transform animations are preferred to unnecessary rig complexity.
- Export: retain existing exports/v1 contract; no required Draco/meshopt decoders for the first delivery. Verify original/optimized clip names, durations, topology and rendering.
- Use available native image generation for concept exploration only. Do not configure a paid external provider or optional sprite forge in this first slice.
- Progress: GitHub checkpoints plus four persistent records, before expensive operations and after meaningful verified subtasks. Never depend only on chat history.
