# Station planter repair candidate — human quality approval pending

The user's latest decision is **NOT fully approved**. Earlier approval/checkpoint records remain historical and recoverable; they do not approve this repair. Only the two low station planters, their old painted shadows/underpainting and local foot reservations were changed. No Gate3, merge, deployment, building redesign or full-street replacement.

## Source diagnosis

| Stage | Finding |
| --- | --- |
| Current source | The objects are baked in `district-refinement/east.png`, inherited from `assets-src/gate25-reconstruction/ground-revised-host.png`. They are not foreground sprites or duplicates among the seventeen existing objects. |
| Resolution | That clean-environment host image is2030×775, nearest-finished to3184×1214. **96.43% of the left sample and97.27% of the right sample match those enlarged host pixels exactly**. Soft painted foliage and diffuse shadows already exist in the source; enlargement exposes coarse clusters. |
| Original station | The original station texture has sharply defined flowers/stone and benches in this area. Its older720px authoring finish is a separate historical operation; the defective current objects predominantly come from the later environment plate. |
| Interpolation | Current Phaser uses pixelArt=true, antialias=false, roundPixels=true. Chunks are mounted at integer world origins without scaling. Nearest sampling preserves the bad source detail; it cannot recover missing detail. No evidence identifies GPU interpolation as the original cause. |
| Alpha | Existing ground is opaque RGB. There is no foreground planter alpha mask to produce an edge halo. The old soft fringe/shadow is painted into that RGB ground. |
| Compositing / depth | Architecture was restored separately above this foreground area; the two low planters/shadows remained flattened in the environment and could not Y-sort independently of Juni. |

[Measured source fractions, authoring transforms and actual native readback](sampling-and-alpha.json) · [Immutable source snapshot](protected-before.json).

## Restricted repair

The complete old low objects and their diffuse shadows were removed into a clean derived floor, with binary masks limited to their two reservations. The central tactile corridor and lower tactile branches are protected explicitly. Station facade/doors, Muneum, bakery, crosswalk and all original textures remain unchanged.

Two separately authored native planters replace them: left190×87 at(2545,695), right190×83 at(2908,699), each with root depth778. White/yellow flowers and fern-dominant foliage vary from the right's smaller white/mauve blossoms and lower fine-leaf silhouette. Stone rims, faces and supports use one perspective/light/material family. These are replacements with removed underpainting, not extra decorative overlays covering old defects.

The host sprites were deliberately finished **once** from their high-resolution crops using NEAREST downsampling and a128-color/no-dither palette; no upscaling is used for them in Phaser. Source crops, dimensions, prompts and exact transforms are retained. This intentional source-authoring finish must not be confused with a claim that no resampling ever happened.

Body alpha is0/255 with transparent RGB cleared. A light/dark inspection caught the first shadow classifier treating cool granite pixels as shadow; the final mask protects stone geometry and asserts an opaque stone-face core. Final light/dark boards show the corrected assets. Their small owned cast/contact shadows use controlled native64/96 alpha in source, baked once onto clean floor below actors. No old shadow, gray matte or duplicated planter layer remains in the repair pipeline.

Only the eastern ground texture changes; the west/center runtime textures are reused directly. Existing native chunk boundaries1512/2488, source artwork, Juni atlas/scale, camera/tour/control code and seventeen earlier foreground objects remain intact. [Asset/geometry proof](asset-proof.json) · [Source preservation](preservation.json) · [Art provenance](../../assets-src/gate25-station-planters/provenance.json).

## Validation judgments

| Check | Result / evidence |
| --- | --- |
| Both planter bounding boxes in native Phaser vs final source composite | **PASS**, exact RGB equality, including opaque body edges; no unwanted native runtime resampling observed |
| Body alpha/transparent RGB and stone-face opacity | **PASS**, binary alpha, zero RGB outside mask, opaque core and corrected light/dark inspection |
| Central strip / tactile / crosswalk / station entrance coordinates | **PASS**, exact preserved RGB/collision;89px continuous clear strip, unchanged Juni walk/run visible width at most49px |
| Actual station approach / both clearance edges / both planter foot collisions | **PASS**, normal-entry input/video; no QA placement or speed override |
| Depth / existing layers | **PASS** state/input checks, new opaque Y-sorted planters; screenshots show Juni behind them. Final visual interpretation remains human review |
| Existing source/checkpoints / unrelated architecture | **PASS**, original inputs unchanged, historical tag retained |
| Typecheck, lint, formatting, actor/source checks, unit tests | **PASS**,18 tests /5 files. A comment-only fix in the existing handoff QA retry handler resolves an empty-catch lint issue; no game behavior changes |
| Visual craftsmanship, natural detail/material/light equivalence to Muneum | **NOT TESTED by human / PENDING**. Replacement, pixel equality and passing tests do not grant art acceptance |
| Physical Android Chrome / iPhone Safari | **NOT TESTED** |

Actual captures: unannotated native district, both before/after close-ups, complete station frontage with Juni, behind-planter gameplay and collision/traversal video. The frontage is a native crop of a1280×900 normal gameplay canvas after actual movement, not a concept render; original canvas/state are retained. [Review index](README.md).

The surrounding painted environment remains its existing source quality; this task does not rebuild other landscaping or convert the world into a tilemap/asset system. Judge the two repaired objects directly in the native crops and complete frontage, alongside the Muneum reference. **STOP for explicit human visual approval. Gate3 remains LOCKED.**
