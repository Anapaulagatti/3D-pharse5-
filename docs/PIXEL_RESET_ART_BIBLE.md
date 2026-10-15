# Pixel Art Direction Reset v2 — review candidate

The previous Gate2 is REJECTED BY USER. It is preserved at035d4cd / checkpoint/pixel-v3.1-art-review-20261015 and previous ZIP. No style is approved. This pass is an art proof, not Gate3 or a full town release.

| Direction | Character / silhouette | Architecture / road | Foliage / props / social mood |
|---|---|---|---|
| A Moonletter Garden | Arin, long split celadon riding coat, coral scarf tails, folded-paper hairpin, asymmetric mail satchel, envelope wave | Intimate L-wing timber hanok, thick giwa planes, veranda/stairs, irregular stone garden paths and water crossing | Branching plum + broad tiered pine; tea pavilion, lantern noticepost, koi/reed pond; calm pen-pal garden |
| B Ginkgo Commons | Seoha, wide navy beret, glasses, broad ivory academic coat over pleats, book/backpack; raised open-book emote | Two-storey Korean seowon library on stone plinth with glazed reading wing, broad civic stair, formal slab courtyard and diamond borders | Golden ginkgo + narrow sculpted pine; book fountain, clock kiosk, hydrangea seating; study/social hub |
| C Hanji Afterhours | Jun, asymmetric ponytail, headphones, cropped layered jacket, loose cyan trousers, camera pouch and lightsticks | Split-height workshop/terrace, right exterior stair, deep awning/shop window; zigzag brick pedestrian lane | Cascading willow + open orange street tree; festival stall, busking stage, lantern arch/banners; youthful makers' lane |

Three independent Tiled maps/object placements and source sheets. Reused small furniture/anchors intentionally share one engine/art family; identity differences are not established by colour hashes alone. Actual native screenshots are the visual gate.

World tiles32x32, fixed hero48x64, four directions,4idle/8walk/6emote frames per direction,72frames/style. Default integer camera2x produces124–126visible CSS-pixel idle height versus53–54previously. Optional1x map overview and3x close view; phone2x focuses on character/frontage and naturally crops distant roofs,1x shows composition. Native canvas pixels equal CSS dimensions; DPR2 verified separately.

Source art: original native image_gen object masters, no reference image, exact prompts + immutable source PNGs/provenance. Independently code-authored new character silhouettes/outfits/animation frames, tiles, curbs and small fixtures. Object export has explicit annotated crops, alpha threshold/connected-component separation, nearest game-size sampling, up to128opaque colours/object. Character frames use up to64colours, binary alpha,2pxatlas gutters. This is not a claim that every generated master pixel was hand-placed. Accepted source edits must be preserved before export; raw masters are never overwritten.

Upper-left light is baked into front/right walls, eave thickness/undersides, recessed windows/doors, layered stone bases, canopy clusters/trunks and foliage highlights. Native ground curb/corner tiles add low raised edges/shadows without new physics. Small planters were revised to match material scale. First academy master had European royal motifs and is explicitly rejected, kept as history; corrected Korean source is active.

Idle timing is1800/120/350/1100ms. Installed Phaser4.2.1 Animation.getNextTick uses currentFrame.duration || msPerFrame (absolute override, not addition). The earlier additive assumption was incorrect, made blink20ms, and was corrected after native movie inspection. One-pixel breathing/cloth follow-through; explicit input animates under reduced motion, ambient/idle freezes. Emote overlay was redrawn outside head silhouette after actual movie review found occlusion. No retimed motion or overwritten OS preference.

Keep environment and framing review separate from production approval. No physical-device FPS claim, new gameplay district, production backend, wardrobe, learning quest, ads or replacement deployment.
