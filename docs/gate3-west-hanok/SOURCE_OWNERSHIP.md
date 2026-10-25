# Native source provenance

Baseline: current `jeju-bridges-world` at official human visual bridge approval. New namespaces only: `assets-src/gate3/west-hanok-v1` and `public/assets/gate3/west-hanok-world`.

One built-in `image_gen.imagegen` local-edit job used the current native western context and exact two-polygon guide. The whole house and enclosed garden were coherently authored together; no rejected southern quality reference, whole-world generation or external paid provider API/key was used. Raw output and input paths are recorded in `authoring-jobs.json`; the original1536×1024 source is retained.

Source pixels are selected at integer origin320,750 inside `edit-scope-mask.png`; no scaling, interpolation, sharpening or blur. Old target-only fragment/foreground ownership is removed inside the masks, while any original alpha outside remains exact. New roof/garden foreground mattes copy the SAME native RGB with binary alpha; no facade or tree fragments are reassembled from old pieces.

ALL original sources and approved Hanbit/Jeju art remain immutable. Collision arrays, logical solids and native-contact guard are unchanged. No new land, route amendment, interior system or neighboring architecture was introduced.

Reproduce: freeze with `g3wh_prepare.py`, retain authoring master, `g3wh_build.py`, actual `g3wh_capture.mjs`, `g3wh_audit.py`, original-control `g3wh_walk.mjs` and `g3wh_movement_audit.py`. Documentation/review derivative generation is separate from source artwork.
