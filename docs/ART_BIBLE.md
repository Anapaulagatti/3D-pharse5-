> Historical Gate2 baseline. User rejected its art. Current art pass: docs/PIXEL_RESET_ART_BIBLE.md; tool versions remain unchanged.

# Pixel style proof — selection pending

32×32 world tile. 48×64 character canvas; roughly49px visible height, foot anchor bottom centre; 16×10 grounded collision footprint. House224×208 with~30px door compared with~24px-wide character. Perspective: orthogonal top-down 3/4 baked art; no3D renderer/imported GLB.

A Celadon Morning: jade student/bob, low sweeping roof with honey ridge ornament. B Coral Courier (recommended): coral messenger, paper hair pin, envelope satchel, raised secondary roof, warm timber/celadon contrast. C Indigo Festival: capped jade artisan, indigo roof/purple blossom ramps, lantern banners. One deliberately small shared plaza tests composition rather than mass-producing three towns. Three directions are editable production-format pixel candidates, not approved art.

All geometric raster operations land on integer source pixels, no anti-aliased image rendering, no painterly downsampling. At most32 opaque colours per indexed source. RGBA atlas has binary alpha, transparent RGB0, two-pixel gutters and untrimmed48×64 anchors. Four directions each have two idle, six walk, four wave frames; run reuses the walk frames at15fps versus10fps and is explicitly not a separately authored run sheet. Left is a mirrored authored side view. Head, collar, satchel and feet stay consistent.

Phaser nearest-neighbour/pixelArt/roundPixels and integer camera1×/2×/3×. Mobile viewport uses a smaller camera crop and upward framing, never scales world pixels fractionally to fit. HTML text remains smooth Unicode; Korean words are not drawn into low-resolution graded UI. Optional evening is a restrained cool overlay, not full polished day/night system. Reduced-motion OS setting is read initially and live; idle/ambient freezes, explicit movement remains available.

Original cultural cues: curved tiled eaves, timber/lattice, hanji envelope, courtyard stepping paths, blossom clusters, lantern posts and small market. Inspired by hanok/Bukchon architecture as general cultural forms; no traced photos/game art, trademarks, copied map or licensed asset pack. Code-authored source and editable indexed PNGs; no image model used. Human cultural/Korean content review still pending.

Source contact sheets and real engine shots are compared in quality-reports/pixel-v3.1/REVIEW.md. Source layout is not a screenshot. No “approved sheet” exists until the user's explicit A/B/C selection.
