# Originality, fit and full-world feasibility

This is a review assessment, not authorization or implementation of Gate3. Human artistic approval remains pending. The approved Gate1 plan and checkpoints are unchanged.

## Slice B: what is reused and what is new

| Component | Actual provenance |
| --- | --- |
| Four commercial buildings: café, bookshop, learning venue and convenience store | Reused approved Muneum foundation at1:1, including elevations, roof gardens, balconies, storefront glass, interiors, doors and Korean signs. No newly authored commercial building in B. |
| Sidewalks, asphalt, crossing, planting, baked shadows and furniture already present in that foundation | Reused pixels from Muneum, not new Gate2 southern art. |
| Ten foreground placements using seven unique prop images | Reused Muneum bench, flower box, planter/tree, light, bikes and heritage-tree assets. Y-sort and softening are presentation behavior, not new artwork. |
| Collision reservation and destination positions | Derived from the approved Muneum bundle/venues; B’s layout is retained. |
| Gate2 review controller, shared scene loading, native exports, tests and packaging | Newly authored technical review work. These do not establish architectural originality. |
| Railway station | Newly generated/finished supporting architecture in its separate study; not one of B’s four storefronts. It proves a station study, not a new commercial-building production pipeline. |
| Transition | Newly generated background using the approved visual references; its modern motifs resemble Muneum. Not a reusable original southern building kit. |

**FAIL / not demonstrated:** successful production of additional original modern commercial buildings. Reusing Muneum demonstrates retention of the benchmark only. The prior Gate2 scale/material PASS judgments for B apply to that retained sample, not originality or production readiness.

If a later, explicit authorization permits Gate3, the proposed method is to define distinct building briefs and full-sized footprints first, then author original elevations with different massing, rooflines, materials and shop identities. Use Muneum as a craftsmanship reference, not as pixels to rearrange. Each candidate needs a source/provenance record, native Juni comparison, doorway and sidewalk clearance, matching perspective/light, readable Korean signage, collision/occlusion review and a human artistic check. Only approved candidates would become modular building assets. No such buildings are being generated now, and future production quality is not guaranteed by this plan.

## Jeju and station fit: unresolved proposals

- **Jeju world fit: FAIL.** Approved land720×1260 versus approximately910×1380 painted land in a1024×1536 native study. Proposed study origin[3180,3200]; approximate land[3280,3240,910,1380]; proposed canvas4352×4864. Land extent is an estimate, not a final shoreline polygon. No art downscale or masterplan edit.
- **Bridge/ferry integration: FAIL / unproven.** The bridge diagram uses the approved bridge corridor and its centerline shore crossing as the baseline; the proposed art endpoint[3180,3560] needs a local connector from[3160,3480]. Ferry mainland[2560,4100] stays fixed; proposed island arrival[3180,4020] shifts(-60,-80) from[3240,4100]. Bridge supports, vertical clearance, shore joins and engineering have not been designed or validated. The ferry is still future gameplay.
- **Station exact fit: FAIL.** Approved building560×210; study collision555×220. Holding the north/west edge fixed for comparison puts the south edge10px farther toward the forecourt. The forecourt starts20px beyond the approved south edge; this assumption would leave10px. This is not proof of a usable threshold corridor or final registration. Resolve the collision/entrance geometry locally after review, without shrinking architecture. No station/rail/forecourt geometry was changed.

The diagrams are dimensioned schematics from retained planning data, not rendered gameplay and not an applied after-state.

## Can painted plates become coherent reusable world assets?

**Feasible in principle, not yet production-ready.** Current ground images can be retained as fixed image-layer chunks at native scale, with collision and semantic foreground layers registered to each chunk. That is sufficient for isolated scene review. It is not equivalent to a reusable modular world kit.

The foreground masks duplicate pixels that are also baked into the ground. Moving a masked tree, bench or roof leaves the original painted copy underneath. Similarly, baked shadows belong to their original placements. Extracted masks currently support occlusion at fixed positions; they are not independent movable props. Reuse would need clean ground plates, complete transparent objects, correct back/side silhouettes, separate contact shadows where appropriate, native anchors and footprints. All new source preparation would require subsequent authorization; none is done here.

| Area | Current limit | Proposed later resolution / evidence needed |
| --- | --- | --- |
| Tilemap compatibility | Bundles use image layers and positioned objects; no seamless terrain tileset, tile adjacency rules or verified Tiled round-trip. Painted pavers, vegetation and shadows are not automatically tileable. | Use fixed image chunks where appropriate. Separately author genuinely repeatable terrain tiles/edge variants, then verify Tiled/Phaser readback and collision alignment. Do not cut arbitrary painted squares and claim a tileset. |
| Perspective and scale | The scenes have a compatible illustrative camera convention, not a calibrated shared3D projection. Doorways and apparent floor depth still need per-asset review. | Establish asset guides and anchor/pixel measurements; review Juni at each entrance and seam. No silent nonuniform scaling. |
| Collision alignment | Path masks and building rectangles are authored approximations. Forge navigation proves the supplied geometry, not visual agreement with every painted wall/step. The new approach is tested locally; old Forge snapshots predate that amendment. | Inspect wall/step silhouettes and collision overlays at1:1; test doorway clearance and narrow corners in the actual engine. Keep polygon/footprint source and registration versioned together. |
| Texture memory | Disk PNG size is not decoded memory. A1536×1024 RGBA8 image costs6MiB; a1024×1536 image also costs6MiB. Five foundations total about25.98MiB before walk masks, objects and Juni. Inventory totals approximately61MiB RGBA8 equivalent for all current PNGs together; each scene currently loads separately. CPU collision arrays and canvas/backing stores add overhead. This is not a measured GPU/RAM result. | Stream a small set of512/1024px chunks with margins, release unused caches, avoid loading the whole world at once, and measure actual memory. A proposed4352×4864 monolithic RGBA8 image alone would cost80.75MiB; matching masks/copies multiply that. |
| Rendering performance | Actual evidence uses Canvas/headless Chromium. Large painted images plus duplicated foreground masks cause overdraw. No physical-mobile FPS, WebGL batching, texture-limit or memory-pressure proof. | Profile representative joined chunks and moving actors on target devices; measure frame time, overdraw and cache churn. Choose atlases/chunks after measurement. No performance PASS is claimed now. |
| Scene seams | Each scene has baked framing, landscaping and lighting. Placing image rectangles beside one another can reveal terrain, road-width, shadow and perspective discontinuities. A transition crop alone does not prove all joins. | Plan overlaps/connector strips at native scale, reconcile path edges and shared material/light conventions, then inspect and walk every seam. No automatic seam-free stitching claim. |

## Concise checkpoint judgments

| Item | Judgment |
| --- | --- |
| Lightweight previews and lossless native crops | PASS — all preview JPEGs and448×336 native crops below1MB; original PNGs retained. |
| Local Jeju exterior approach | Technical PASS after real-input traversal; visual/human approval pending. Source house silhouette protected; only the entrance corridor patch and local walk mask change. No interior gameplay claim. |
| Native source/masterplan preservation | PASS — retained-image and plan hashes checked; checkpoints untouched. |
| B reuse disclosure | PASS — explicit, hash-backed disclosure. |
| New original modern commercial-building production | FAIL / not demonstrated. |
| Jeju reservation fit | FAIL / proposal needs review. |
| Bridge and ferry alignment readiness | FAIL / proposal and engineering unproven. |
| Station exact collision-depth fit | FAIL /10px discrepancy unresolved. |
| Modular/tilemap readiness and full-world seams | FAIL / not yet demonstrated. |
| Full-world rendering/memory performance | FAIL / not tested on an integrated world or physical devices. |
| Human artistic approval | NOT GRANTED; no technical PASS changes this. |

STOP. Gate3 is locked. No full-world integration, merge, deployment or protected-checkpoint alteration.
