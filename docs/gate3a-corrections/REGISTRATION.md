# Individual-building registration proposal — human approval required

The approved 3184×1214 district remains an immutable reference and frozen playable package. It is **not** the world-coordinate layout. The candidate retains the 4352×4864 canvas and protected station logical coordinates; the current masterplan and default world scene are unchanged. A separate `registration` scene demonstrates the proposed placements using original native pixels and engineering paving only.

[Current versus proposed diagram](CURRENT_VS_PROPOSED.png) · [Footprint comparison](FOOTPRINT_COMPARISON.png) · [Original/proposed entrances](ENTRANCE_COORDINATES.md) · [Exact proposal data](registration-proposal.json)

| Building | Native facade ownership crop in original district | Candidate raster origin | Contact footprint | Existing planning reservation |
| --- | --- | --- | --- | --- |
| Muneum cafe |(35,200)–(450,756),415×556 |(510,2035) |(510,2380,415,210) |cafe390×210; **25px east width amendment needed** |
| Munjang bookshop |(450,235)–(780,756),330×521 |(980,2070) |(980,2380,330,210) |Part of existing books720×210 |
| Learning |(780,195)–(1080,756),300×561 |(1310,2030) |(1310,2380,300,210) |Shares books slot with bookshop, not a second invented reservation |
| Maru convenience store |(1080,245)–(1501,757),421×512 |(220,2608) |(220,2910,421,210) |**New unassigned candidate** at western Namsan approach |
| Original 오월제과 bakery |(1537,0)–(2442,763),905×763 |(1353,3060) |(1380,3370,875,442) |**New unassigned candidate** in waterfront zone |
| Hanbit station / canopy envelope |(2539,283)–(3184,736),645×453 |(2313,2196) |**(2322.5,2380,555,210), unchanged** |civic; logical full-source anchor remains(2238.5,2180) |

Crop dimensions include owned facade/context pixels and are not claims about new architectural ground dimensions. The bookshop/learning pair keeps its shared source party wall. No building is resized, regenerated or recolored. The station platform canopy is an independent source-owned foreground object with its own support depth 2649; the station body retains2590, and corrected planters retain 2691. This allows the canopy to occlude independently rather than flattening it into the facade root.

## Exact reservation conflicts and proposed public realm

- Cafe contact width415 exceeds its390px slot by25px east, consuming part of the former80px gap. The remaining55px gap is a **non-public service recess**, closed in the candidate foot field; it is not presented as an accessible premium alley. Future side elevations/service treatment need source-preserving art after registration approval.
- Native visual envelopes exceed the500px facade-reserve heights: cafe556, bookshop521, learning561. They project55/20/60px north of the current2090 facade top and1px past the2590 bottom. They visually intrude45/10/50px into the transition zone ending2080. No historical building or northern geometry moves. Approval of these projection easements is required.
- Bookshop and learning contact widths sum630px within the720px books reservation. Their two source entrances branch to the retained public approach node(1350,2690). Cafe retains its public approach node(700,2690); its native threshold is(717,2605). These are distinct public approach and facade threshold coordinates, not silently moved protected doors.
- Convenience store contact plot is140px west of the tower-zone edge, on unassigned mainland, with60px to the mainland planning boundary. No old protected commercial reservation is asserted. The tower and southwest Namsan position remain fixed. A localized western Namsan-path bypass through(760,3140) and(760,2920) preserves the(750,2800) destination; a clear front connection reaches the new native threshold(428,3133). Existing park zoning/route amendment needs human approval.
- Bakery contact875×442 fits entirely inside the waterfront zone(330,3360,2700,520), intersects **no approved building contact footprint**, and retains the original875×442 bakery solid rather than shortening the building to fit. Its plot is a proposed public-land allocation, not a previously protected bakery reservation. It conflicts with five named planning paths: `urban-avenue`, `island-arrival`, `harbor-link`, `promenade`, `market-waterfront-shortcut`.
- Bakery circulation proposal: retain the northern spine to its3308 approach plaza, provide60px pedestrian links around the sides, preserve80px physical clearance to the market and75px to the ferry terminal, and move the local promenade segment to3900 with a96px reservation before returning to3790. A64px entrance connection links promenade3900 to bakery threshold3840. Juni's measured49px maximum visible width leaves15.5/13px per side at the market/ferry midlines. This is a pedestrian diversion proposal; it does not claim continuation of a176px vehicular avenue through those narrow side corridors.
- The bakery's905px facade projection extends above its contact footprint. Its conservative projection envelope overlaps the future carousel reservation by38×90px at(2220,3060), although contact footprints do not intersect. Depth composition and future attraction visibility must be reviewed before new art; this is not permission to move the carousel.
- Station contact fits the existing civic contact region. Native facade/roof context projects outside its560px facade reservation, and the retained platform canopy covers part of the planned western platform. These are explicit visual overhangs; platform navigation, canopy occlusion and future railway composition require further district-level review. No train operation is introduced.

`connectingRoutes` in the proposal records exact route points/widths. The current approved paths remain in the immutable source plan; candidate paving displays proposed circulation for evaluation. These strips are pedestrian/planning geometry, not a completed asphalt/sidewalk streetscape. Final road cross-sections, curb/crossing continuity and safe public-realm allocation need art/engineering review before G3-B; no painted production street is claimed here.

## Pixel phase: explicit convention, not hidden coordinate rounding

Protected station source reference stays **(2238.5,2180)**, protected collision stays **(2322.5,2380,555,210)** and threshold stays **(2598.5,2610)**. There was no approved native full-world station raster at that half-pixel source edge; the prior working plan supplied the reference geometry.

The candidate declares a source pivot **(0.5,0)**, giving an integer raster edge **(2238,2180)**. Cropped station foreground uses the corresponding anchor(2313.5,2196) and the same pivot. The0.5px delta from the old source-edge interpretation is explicitly recorded and **requires final human approval**. This is a proposed anchor/raster convention, not a claim that the old literal image-edge convention and new raster edge are numerically identical. The protected reference/collider are never passed through rounding or written back to the masterplan.

Native pixel column84 is rendered over[2322,2323], whose centre2322.5 lies on the unchanged logical collision edge. Column360 has centre2598.5, matching the entrance axis. Collision checks retain continuous world coordinates before sampling the conservative foot-clearance field; that field can reject points outside the body hull to preserve player clearance. Juni's existing pixel-rounded visual pose can differ from its continuous position by at most0.5px; its atlas/scale are unchanged.

[Pixel-grid/collision diagram](PIXEL_PHASE_AND_COLLISION.png) · [Native RGB readback](native-pixel-and-phase.json) · [Static routes](static-validation.json).

## Craftsmanship and seam strategy

The intact approved district remains the artistic benchmark. The proof copies its owned facade pixels at scale 1 and demonstrates anchors/entrances/occlusion. It does **not** establish that polygon cutouts are finished modular environment art: exposed party-wall ends, rooftop vegetation ownership and ground-context cut boundaries remain visible on engineering terrain.

After registration approval, G3-B must author missing side elevations and the connecting public realm around these fixed native facades, preserve protected facade pixels with hashes, retain whole foreground vegetation/props with proper support roots, and validate every seam at1:1 with actual traversal. Use coherent paving/curbs, modest lighting and planted setbacks outside the clear paths; do not hide cuts behind oversized vegetation. This task creates no new southern building and does not treat reused Muneum as proof of original architecture production.

**No proposal in this document is applied to the approved masterplan or accepted as final registration. Stop for human approval.**
