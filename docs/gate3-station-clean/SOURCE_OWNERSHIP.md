# Source provenance — no old Hanbit art reuse

[Authoring jobs and exact references](../../assets-src/gate3/station-clean-v1/authoring-jobs.json) · [Build ownership](../../assets-src/gate3/station-clean-v1/integration-provenance.json) · [Changed files](changed-assets.json).

1. Historical `final-world` is frozen for comparison/checkpointing. Its station artwork is not an authoring reference.
2. All six station foreground owners are removed. The entire old station ground region is replaced with a neutral engineering placeholder, including old floor, shadows and props. Non-station neighbors stay in place. Road/entry coordinates are drawn as planning-only vectors without copying old art pixels.
3. `fresh-empty-site-authored.png` is a new native1536×1024 ground master authored from this genuinely purged guide plus Muneum's original non-station Gate1 reference. Only the fixed station parcel and tree-remnant area are installed.
4. Actual Phaser clean-site evidence is captured BEFORE any new station architecture is authored.
5. The new architecture is authored from the clean map and abstract new massing geometry, with Muneum as craftsmanship reference. The first fresh design was too large and was rejected, not rescaled. Final fresh source is a new full native painting with a different silhouette, material hierarchy, window/arch design, central clock and sign.
6. Fresh source crop354,220,684,500 is registered at2274,2140. Its explicit pivot39.5,56 retains the logical anchor2313.5,2196 while producing an integer raster origin. All source texels remain1:1. Roof/upper/facade masks partition this ONE new painting, not old component art. Source alpha is binary; every opaque architectural texel is directly verified against actual Phaser readback.
7. New contact-shadow pixels come only from this new architecture painting, selected over the fresh empty floor. No old canonical floor or old baked shadow is a possible donor. The entire old lot is checked underneath the building, not just the pixels visible around it.

Historical files remain unchanged for recovery and provenance. Preserving history does not mean retaining its artwork in the active composition. The active manifests contain no old station object/image dependency and all four ground chunks touching the old lot are replaced. The default live renderer requests zero old station textures.

Scope: main lot2274,2140,684,673; right tree remnant2958,2490,38,208; retirement of old canopy terminal2946,2244,82,274. Ground changes occur only in the first two masks. Old terminal retirement is foreground-only. Original non-station objects/coordinates and all outside pixels are exact.

No full-world generation, no global material/filter/color pass, no half-pixel resampling, no old-mask patch workflow, no source deletion, no main merge/deployment. Built-in host image authoring only; no new paid external API. Actual native PNGs are distinguished from source masters, engineering guides and enlarged JPEG review copies.
