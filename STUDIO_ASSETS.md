# Pixel asset registry

3D archive: docs/migration/3d-archive-proof.json inventory2738paths; exact archive f1f13f2, full Blender/GLB/textures/sources/previous releases/v0.6concepts+unfinished work preserved. Legacy release hold showcase-v0.5 excluded from pixel build.

Sources: assets-src/directions.json (editable32colour ramps), layout.json, plaza.tmj (editable Tiled4layers/13colliders), A/B/C indexed PNG masters and tools/export_art.py. atlas sources use48x64canvas,4directions×(2idle+6walk+4wave)=48frames/style. All candidates REVIEW_CANDIDATE_NOT_APPROVED. Original code-authored,MIT; no provider imagery/audio. Source edits contract: assets-src/README.md.

Derived: public/assets/{A,B,C}/{avatar.png,avatar.json,house/tiles/tree/lamp/mailbox/bench/market/bridge/flowers/fence.png}, plaza.json and direction sheets. Production license notices public/licenses. No GLB/runtime3D dependency. All atlas pixels checked against master, binary alpha/2pxgutter/palette/hash/reachability PASS.

Visual: quality-reports/pixel-v3.1 source-vs-engine sheets, native game screenshots, mobile/canvas/evening/zoom/dialogue, original17JPEG/compositor capture JSON and103314byte6.55sMP4 +decoded frames. Actual capture, not concept-as-proof; sparse capture not FPS measurement.

Portable view: downloads/pixel-v3.1 ZIP480147bytes, manifest exactSHA; verified actual extracted HTTP desktop/mobile.

| Production path | Bytes | SHA256 |
|---|---|---|
| public/assets/A/avatar.json | 16304 | 96e40d47e38f4ad179d5b3243efeec981fe03e83279b7983e401084b88d68111 |
| public/assets/A/avatar.png | 11795 | 559ab933dd45809c973a23a4079b96a8d32f749f2b38794abe9a2d747b43aea3 |
| public/assets/A/bench.png | 326 | b24e502bfe5d88c460bb429f24b9e0f8486b0975b281f2a4e92e36bd9d8f6a56 |
| public/assets/A/bridge.png | 481 | 6023662198e66afdd37aa7768aa8833c8ebc99e0e8389c5c896ce2a3e1f83e9c |
| public/assets/A/fence.png | 215 | 5d62e48c84735160ceaf7a2bfa8a906ea5d16e4f30fe3ae4cd254cc793ce21d5 |
| public/assets/A/flowers.png | 282 | 7637e410c8c61ff374698c94f62d8f53c5081ec115349d7c92738b7502a51e25 |
| public/assets/A/house.png | 2736 | 2e90b29a6645856a30dc9ea5917ebd401dd6d465ffa4187fb49f7273b3e40820 |
| public/assets/A/lamp.png | 326 | 3663ac9b193063208b32433621ffdbaa5868f491d39a790d2e21f71c98789bd1 |
| public/assets/A/mailbox.png | 395 | 1006cc1e82f2b8835b0ff40a6d62149da24ff7528dee1c59bffd7eed6e19246b |
| public/assets/A/market.png | 788 | 97fe5a05fc98d6daa88dd74b4eef967b7a8b5d82c0b954619f4bbc662560d721 |
| public/assets/A/tiles.png | 922 | 8076581aa5dee426a67f9d1a46bd364f7229ad109f56d30107ce0d6582d3f776 |
| public/assets/A/tree.png | 1678 | 23a566b616c0021e16c3589ab9e429183420d6825e6c57e6114a94cd92ca9928 |
| public/assets/B/avatar.json | 16304 | 96e40d47e38f4ad179d5b3243efeec981fe03e83279b7983e401084b88d68111 |
| public/assets/B/avatar.png | 12529 | 404be839adcbf96c9938e533d864c5aa848a672cb492821abba26d3d4960c66a |
| public/assets/B/bench.png | 328 | 712876c7aecf27f635b5e8ddc177a7fd2579283b3f6430258978d2a373837c69 |
| public/assets/B/bridge.png | 476 | 5da1259f064d944cb3a0479885e50aff94b507d57e62417e557924b4793cb199 |
| public/assets/B/fence.png | 215 | 90b996731934873688cf9003dcdf340cc145ee62f4670b8f7be5a1b951dde2e7 |
| public/assets/B/flowers.png | 282 | cc24e17dd8164c2c224e036b56a8d797130448625d8343d93a43468b5ecfd4a6 |
| public/assets/B/house.png | 3200 | 5198065ddb306d6a61b430140bb7177a050e07499829001d648a225058f192d9 |
| public/assets/B/lamp.png | 327 | e2a6a17ebb051e07369d3c217a82483b844a6e97627bdf7088a268ebfe3e05d4 |
| public/assets/B/mailbox.png | 396 | 6bdd4ee1c60f86210861582bb95a27067d071a452f9443b52523ad9e8c1689ca |
| public/assets/B/market.png | 797 | 6a551c8043eccafdfa00b09078ec7bd61625d3f8ae20754bc18d13c75916c32e |
| public/assets/B/tiles.png | 920 | 10ac9098f3cf105101f0cd95f0a9f19a55bc0ea7447c04dec9d0e8d2abd141a4 |
| public/assets/B/tree.png | 1698 | 0ea9e68a6e8aaf6a54e46fbd6c2fe33ad60d5e1389c04dd79473bd8a2e479c3c |
| public/assets/C/avatar.json | 16304 | 96e40d47e38f4ad179d5b3243efeec981fe03e83279b7983e401084b88d68111 |
| public/assets/C/avatar.png | 12195 | e02f2c52560b68c8ac05da2d92a1afd319b08f51bb3155f88ed1a15c1d0c4029 |
| public/assets/C/bench.png | 338 | c5eec3bb499b6646491b041b1c4b1c5221cb83e785fd8a5753ae69ba9a37bc0e |
| public/assets/C/bridge.png | 477 | d9e9db8ea9ffcb5d739f682a0d061c5632e0078d1c33a81499cf5bc31e9744a5 |
| public/assets/C/fence.png | 241 | 0649ff1570d35bb4792148aabb135abaefa7fbca5c0c58f1f2282aaeca4cc5b4 |
| public/assets/C/flowers.png | 283 | e243a2e556969c2e5e03b1352ace11eb9de538bee8a261f608f7300772800b88 |
| public/assets/C/house.png | 3572 | dd3f01157b6a63d039f346686fba6768ba160f94ef5deccbce4d6348b0c2670c |
| public/assets/C/lamp.png | 319 | b041a1bccc250898320bcf65127ea5adf5ff1349cae96339ce9263941c2446b7 |
| public/assets/C/mailbox.png | 391 | 35eb1aaec0a8629fc80f3e9e066a11a6dd58f400a6f0ea22d8ef2bb53f6223a8 |
| public/assets/C/market.png | 788 | 4b295716c481b086d466d75fdfeb82d730d00b6566320833719a7e2aded9418a |
| public/assets/C/tiles.png | 917 | 4df7a8983b71de5773cdded6a13fcd93024f215d278bd2943cd645deeda8d709 |
| public/assets/C/tree.png | 1691 | da52faa31e3aef248b3625d8c50a6eba7ecd5d8f28f1701c892ff771c61570a5 |
| public/assets/direction-A.png | 7822 | 887275dd52651a3f32f069f114b35e9a1e57cb09aeb9fc202decf4c61366a4fa |
| public/assets/direction-B.png | 8416 | 37c288661530d60d021cf669e4ed7e29c23d2b1d7b503943e1e4b985a38fe84c |
| public/assets/direction-C.png | 8718 | 2eae0d93ea569c53b2bc2ba0a6f2d5d456c5ce182a11a16d64058eae689229e7 |
| public/assets/plaza.json | 3763 | 319d5f6a1df1529f8b3da8503eb22c4d935b903f241c393a6f22154f2240f821 |

Remote content checkpoint519fa74941698b3b3f253f282fd2df841d4707f4 independently matched origin. Actions0dd7550 run38668885824 succeeded (actual remote tests). Later519fa74 CI exposed formatting of new delivery helper; local formatter/lint now PASS, no runtime/art change. Proof checkpoint will rerun CI and retain observed outcomes.

FINAL VERIFIED HANDOFF: d7570bc31df8fe858d46748b67bf3b85bec80660 independently remote-matched; Actions38669691060 SUCCESS after formatter fix. tools/setup.sh actually executed full validation PASS (5unit,3browser), reporting to ignored .cache/setup-qa without changing source art or accepted evidence. Final proof/setup-only checkpoint saved with checkpoint/pixel-v3.1-art-review-20261015. Runtime/ZIP unchanged. STOP for explicit new pixel A/B/C selection.

## PIXEL-ART-RESET-002 — user rejected previous Gate2
New authoritative reset review: docs/reviews/pixel-reset-v2/USER_REVIEW.md; audit explains palette/layout/scale/form failures. Previous035d4cd/tag preserved as rejected baseline. Reuse working Phaser/packages; new assets use reset-v2 versioned paths and independent scene data. No Gate3/public deployment. Next: produce three substantially distinct original world/character directions, inspect actual gameplay rendering, then STOP for new approval.
