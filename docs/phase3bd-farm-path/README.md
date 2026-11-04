# Farming lifecycle + path hotfix · 2026-11-04

Playable: PHASE3BD_FARM_PATH_REVIEW.zip (701,140,647 bytes). Unzip, run `python3 start-review.py`, then open http://127.0.0.1:4483/farm-path-review/ . No npm/network required. Browser launch and actual harvested produce verified from the extracted ZIP, not only from dev.

Source build: 79f290581434306371ee892cf411c3d9766aebea
Artifact: 5b5ce278596520efd520f6af63266e57c49c3fd8 (review/phase3bd-farm-path-20261104)
Manifest: d170ee180c4743ab8bee4b4a952c7bf1b7f69c2c8083e1b2eb84cf6846beea58 ·4301files
ZIP SHA256: 50615405a33656861a5f30ba210ca29bd5899f2c55c56b76ffd719bbab4b2ae7
Prepared release controls: 5179fb2203231e69735bd50d863591812a706834 (review/phase3bd-farm-path-controls-20261104)
Checkpoint: checkpoint/phase3bd-farm-path-review-20261104

Two crops now show empty/prepared soil, sown, sprout, young, growing, mature and harvested/prepared states. Wet soil differs visibly from dry; crop sprites disappear after harvest. All18plants in each of6managed beds use actual native state frames; approved source terrain/fences remain immutable. The starter quest earns its seed in-world and yields produce/reward with reload persistence. No remote farming action modal.

Navigation: western modern planter clear-paving strip [455,2350,30,130],23→30px visible public lane,910new passable anchor cells. Existing planter throughx454 stays blocked. Farm aisles/exit, Cheolsu approach, farm→shop and bookshop approach were traversed; other sound corridors remain unchanged. Cardinal corner assistance searches at most4px and only takes valid <=1px swept steps, preserving analog magnitude/speed/facing. Logical solids, source masks, camera, original player collision registration and protected coordinates unchanged. No generic map dilation.

Evidence: index.html gallery; native1:1PNG/crops; videos/ two actual silent Phaser captures; SCALLION_QA.json (90real seconds); PATH_BEFORE_AFTER.json; PIXEL_READBACK.json; OFFLINE_BROWSER_PROOF.json; QA.md,DEFECTS.md.10479original artwork/source hashes unchanged;26NPC/12players/24cosmetics preserved.209unit/71broader regression/14final relevant tests PASS, with revision qualification and historical snapshot warnings documented. Android/iPhone/hardwareGPU NOT TESTED.

Rollback: source checkpoint/phase3bd-before-farm-path-20261104; exact previous physical artifact9fce709a/manifest17306fc4. Earlier publicfff156b6/543ccd32 and all prior snapshots preserved byte-exact.

## Public review gate

The hotfix has NOT been deployed to Pages. Existing approval binds only9fce709a/17306fc4. The exact new manifest above requires one consolidated owner decision. Prepared controls are on a separate branch with a PENDING receipt; local receipt/integrity checks block solely missing owner approval/date, while all hashes/source/pins/history checks pass. No review-main, officialv0.5, production deployment or Phase3BE changes. Do not approve the obsolete waiting9fceworkflow as this new hotfix. After exact approval, use the prepared controls and existing protected Pages workflow, with actual HTTPS verification before claiming success.
