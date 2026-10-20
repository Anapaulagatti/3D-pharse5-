# Final map-lock polish

Target: approved V6 at2df01bf215e0355cc1fed20b58779d5d0b740683. Recovery before work:recovery/before-final-map-lock-20261020, remote tag66057ae9394f8f624ebf20a582b5d2223ae3bfb6 peeled to2df01bf before edits. This is a narrowly edited ground-material pass, not a reconstructed district or a release to the public website.

## What changes

- A small warm-to-cool stone treatment on the already straight central connector joins the traditional upper half to the contemporary paving without moving its alignment. Northern ground above2240 is frozen.
- Existing modern streets have consistent low-contrast outer edges. Edges follow the union of paved areas, so they do not cross junctions.
- Nine existing venue aprons receive restrained native-texture color variations and4px flush inlays, with wide gaps on every existing circulation axis. Station/cafe/discovery-hall materials lean cool jade/blue; library/carousel/kiosk remain a little warmer. These are ground inlays, not walls or new collision claims.
- Jeju keeps its approved route centerlines and width. Only the outer8native pixels of existing convex/concave sand bends are eased, reusing literal original grass/sand tile pixels. Court thresholds and required route cores are protected.
- Paired3px stone-tone guides on existing harbor and island-arrival walking material identify the boarding approach. Sea, shoreline, pier artwork, triggers, arrivals and ferry operation stay unchanged.
- Pixel color adjustments use the original pixel at the same coordinate, with small integer RGB/material adjustments. No blur, image tracing, generator, image upscaling or soft sampling. Buildings/Juni/trees/prop images remain byte-exact.

## Preservation and editable source

assets-src/final-map-lock/polish.json records all permitted material/edge settings. tools/final_map_lock.py runs AFTER the original V6 palette finish, before literal32px tile extraction in the existing exporter. It always starts from the exact approved source, never from its own already-adjusted output. Processing receipt, binary changed-pixel mask, preserved geometry/file hashes and independent Pillow-only offline guard are retained. Every actual edit is inside the prior V6 repair mask. tools/setup.sh only validates saved files and never authors or generates artwork.

497prop placements,108original prop images,552collision rectangles,world4352x5312,144Juni frames,land/walk/forest masks,all route centerlines/widths,spawns,portals,anchors,interactions,camera/controller/UI,dependency lock and GitHub workflows remain unchanged. No new landmark,building,physical boundary or gameplay. Native overview and matched1:1 comparisons use actual Phaser renders, not a source composition claimed as gameplay. BEFORE images are inherited verbatim from the approved2df01bf review and recorded with hashes; AFTER images are newly captured from production Phaser.

## Actual toolchain

Pinned Agent Sprite Forge5324342fdfab72430f4e9604f3fe427009f8596d: relevant map,sprite and media SKILL.md read; proven Gwanghwamun/Juni records reused. forge_doctor is a local diagnostic, not generation. The real map_bundle hash/validate,linked world/room navigation,Tiled export and layered composition are executed through the existing exporter; commands/stdout/stderr/exits are retained in assets-src/final-map-lock/forge-commands.json. The original palette finish is reused from its content-addressed cache, not falsely counted as a fresh palette command. No extraction of new prop artwork,master-still,sprite_set,animation synthesis,host-image or paid-provider calls.

Inherited northern edge-canopy clipping/compose footprint skips/Juni weak side-idle/small-wave warnings remain visible in quality/inherited-forge-warnings.json; optional missing keys/Grok/resvg remain in the doctor report. Numeric/source integrity does not establish user art approval. Physical Android/iOS/Safari/hardware GPU performance is unmeasured. No60FPS claim.

## Final verification

Read quality/verification.json for executed local results and the ACTUAL checkpoint/final-map-lock-verified-20261020 annotation after creation for exact final GitHub CI/independent-clone/tag facts. A planned tag name is not a success claim. No main merge or deployment. Stop after source checkpoint for user visual review.
