# Native forecourt restoration — isolated playable candidate

The soft station floor has actually been repaired in a new candidate. The approved default world, station artwork, corrected planters, independent shadow sources, Juni, collision data and renderer remain unchanged. **Human visual approval is pending; G3-B remains blocked.**

Open [source / current / restored comparison](SOURCE_CURRENT_RESTORED_1X.png). Every crop is at exactly 1:1, without enlargement, sharpening or recoloring. The earlier source column deliberately shows retired props as provenance; those objects were not brought into the candidate.

- [Before: native Phaser frame](before-auto-native.png)
- [After: native Phaser frame](after-auto-native.png)
- [Complete station frontage with Juni, native crop](station-with-juni-1x.png)
- [Entrance paving before/after](entrance-ground-comparison-1x.png)
- [Tactile material before/after](tactile-strip-comparison-1x.png)
- [Left planter pavement before/after](left-planter-pavement-comparison-1x.png)
- [Right planter pavement before/after](right-planter-pavement-comparison-1x.png)
- [Real keyboard gameplay video](forecourt-walk.mp4)
- [Playable ZIP](G3A_FORECOURT_RESTORATION.zip)
- [Technical QA and remaining issues](QA.md)

All native PNGs are preserved separately. The contact sheets only arrange native crops on a labelled background. Browser previews may fit images to the screen; download/open at 100% for pixel evaluation. The video is compressed gameplay evidence, not a substitute for the lossless PNGs.

## Local review

Extract the ZIP, run `python3 -m http.server 4286 --bind 127.0.0.1` inside it, and open `http://127.0.0.1:4286/`. Choose the restoration or unchanged comparison. WASD/arrows, Shift run, and the existing mobile joystick remain available. Native evidence mode holds the camera for matching comparisons; normal play retains the existing follow camera.

Candidate URL: `gate3-review.html?scene=registration-forecourt&entry=station`.
Before URL: `gate3-review.html?scene=registration-refined&entry=station`.
Add `&native&pixelAudit` for fixed 1280×900 native readback, or `&renderer=canvas` for the unchanged fallback.

## Ownership and provenance

Recovery source: `assets-src/gate25-reconstruction/original-ground.png`. Approved current source: `assets-src/gate25-station-planters/final-clean-ground.png`. Both remain immutable. The new derived assets live under `assets-src/gate3/forecourt-restoration/`; only two runtime ground chunks are new under `public/assets/gate3/registration-forecourt/`.

The native floor patch remains 684×210, source rectangle `[2500,690,3184,900]`, raster world origin `[2274,2603]`. Binary masks separate editable ground, tactile material, retired-source objects/shadows, changed pixels and current owned shadows. `native-source-map.npz` records original-source reference coordinates for every repaired pixel before the unchanged current shadow composite. `provenance.json` records exact counts and policy.

Clean original paving is recovered at its original coordinates. Ground obscured by retired benches, planter bodies, bollards or their shadows uses documented clean native material from the same perspective row, translated by integer pixels. There is no resizing, interpolation, global filter, whole-scene replacement or old-prop overlay. Small native material repetitions in those reconstructed areas remain subject to human review.

The current tactile route is recorded in `tactile-locked-mask.png`; only its material is replaced, including native studs/ridges. Original gold source geometry is not pasted wholesale. The current curb begins at source y812 and remains pixel-exact. Current planter shadow RGBA is applied once over the clean repaired ground; the two independent shadow files and foreground sprites are unchanged.

The candidate clones the existing registration comparison, retaining all other registrations and their unresolved spatial status. It does not approve or change the bakery/masterplan proposal. No G3-B production, merge or public deployment was performed.
