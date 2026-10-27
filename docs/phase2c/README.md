# Korean Arena · Phase2C Fashion Studio

TECHNICAL PASS — ARTISTIC APPROVAL PENDING. Phase2B is human-approved and locked; Phase3 is locked. This is a review candidate, not an artistic-acceptance claim.

[Playable ZIP](PHASE2C_FASHION_STUDIO_REVIEW.zip) · [visual gallery](REVIEW.html) · [QA](QA.md) · [native default/customized12](twelve-default-fashion-native.png) · [enlarged2×](twelve-default-fashion-review-2x.png) · [device handoff](DEVICE_REVIEW.md).

Branch `feature/phase2c-fashion-studio`. Approved source `8ef1980131cc743b304b21742cabc6ea4e9bb251` (`checkpoint/phase2b-walkfront-hotfix-review-20261027`), preserved as `checkpoint/phase2b-twelve-characters-approved-20261027`. Intermediate checkpoints: `checkpoint/phase2c-foundation-20261027` (5d79429), `checkpoint/phase2c-fashion-catalog-20261027` (f3954af). Final review reference: `checkpoint/phase2c-fashion-studio-review-20261027`. Exact commit can be resolved from the annotated tag; tags are never overwritten.

## Delivered

- Existing12 approved identities, native atlases, motion order/anchors/speeds preserved. Frozen world, collision, camera, tour, controls and unrelated engine remain byte-identical.
- Existing10 item IDs remain; their original sources are immutable. Derived paint/erase revisions bind to approved poses and repair old front-walk garment ownership before expansion.
- 18 newly authored designs (6hair/6outfits/6accessories);28 total items,46 character-specific variants,12 complete curated looks. Availability is truthful, not universal.
- Existing Studio extended with Vietnamese/Korean names, animated native previews, visible loading/selection, per-item equipment, reset, save/apply/enter/cancel, named local preset rename/delete and bounded persistence. No competing engine or UI framework.
- Current v1/v2 stores remain readable. Progress, visited markers and world position survive switches and reload. Up to12 personal presets, names trimmed to32characters; existing names/looks are not evicted by a full list. Curated presets remain protected.
- Lazy requested-only atlas composition, deterministic pose/revision-bound keys, base cache2, composite cache2, character textures3. No eagerly generated runtime permutation library.

## Review locally

Extract the ZIP and run `python3 start_review.py`. Open `http://127.0.0.1:4342/REVIEW.html`. The actual compiled game and assets work locally without Node or an external service. Five representative videos and actual native sheets are included; individual crops, remaining per-character videos and full authoring evidence link to the immutable Git checkpoint. Use `--lan` only when intentionally testing on your own LAN device. LAN HTTP works without SubtleCrypto via a verified SHA256 fallback.

Choose a character, select a suggested fashion look or individual compatible items, inspect all directions/actions, enter the world, move, then reopen Studio. Save a named preset, rename/delete it, cancel an uncommitted draft and reload. The12 original appearances always remain available through Reset.

[Catalog](COSMETIC_CATALOG.md) · [matrix](COMPATIBILITY_MATRIX.md) · [animation](ANIMATION_COMPATIBILITY.md) · [performance](PERFORMANCE.md) · [protected audit](PROTECTED_AUDIT.md) · [visual review](VISUAL_REVIEW.md).

No map rebuild, character regeneration, shops/economy/learning integration, paid API, main merge or public deployment. Stop for human Phase2C review; Phase3 remains locked.
