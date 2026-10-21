# V10 masterplan + playable graybox — awaiting approval

This is the first A–C review delivery. Southern buildings, terrain and attractions are simple spatial placeholders; they are not finished pixel art. Approved north and Juni remain original.

1. [New urban masterplan](V10_NEW_URBAN_MASTERPLAN.png)
2. [Actual Phaser full-world graybox](V10_GRAYBOX_OVERVIEW.png)
3. [Same-origin V9/V10 geometry comparison](V9_V10_GEOMETRY_COMPARISON.png)
4. [Road hierarchy and plot/entrance layout](V10_ROAD_AND_PLOT_LAYOUT.png)
5. [Clean workspace audit](V10_CLEAN_WORKSPACE_AUDIT.md)
6. [Source dependency graph](V10_SOURCE_DEPENDENCY_GRAPH.md)
7. [Playable graybox ZIP](V10_GRAYBOX_REVIEW.zip)

Extract the ZIP, enter Korean-Arena-V10-Graybox, run `python3 start.py` (Windows `py start.py`). Python3 required; Node is unnecessary for viewing. Use the printed local HTTP address. WASD/arrows walk, Shift runs, E interacts; landscape touch joystick remains available. This local launcher does not publish the game.

The plan is a compact east–west high street with paired street-facing blocks and a civic courtyard. Transit anchors the eastern end; the western hill has a connected scenic trail. A southwest leisure circuit has a deliberate arrival from the market/coastal spine. Coastal shops lead to the southeast ferry terminal; Jeju sits east of the lower coast with an arrival trail, village lane and olle loop. This changes the spatial hierarchy and district relationships, not just paving colors. Twenty-three venue/landmark lots are reserved across the whole plan; final architecture/material variation remains subject to approval.

Technical evidence:12unit and15browser cases pass;32Forge targets,19clear authored road centerlines,23interactable entrances, both ferry directions, mobile joystick/portrait pause, Academy and forced WebGL. Package extraction/normal-entry desktop and mobile touch pass;125build files match. Matched native north frame is pixel-identical to V9. See validation.json, package-verification.json and north-render-proof.json.

Road-envelope overlap with V9 is8.9%; plot-envelope overlap9.3%; no exact road arrays or plot rectangles copied. These are diagnostic geometry quantities, with V9 curve approximation disclosed; they do not approve the design. Pixels/Terravilla sites were blocked403, and no firsthand study of unavailable content is claimed. Main chunk-size warning remains. Physical-phone/Tiled/WindowsGUI testing remains unperformed.

Final artwork, premium asset generation and phasesD–F are on hold for explicit USER approval of this plan and graybox. No main merge or website release.
