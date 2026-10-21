# Southern reset cleanup — V9

The user explicitly authorized removal of failed V6/V7/V8 and earlier southern implementations from the active branch. Complete current work was committed and pushed before deletion. Recovery tag `recovery/before-v9-total-southern-reset-20261021` was pushed and independently remote-peeled to `0b809ee883231fcfe46af6330a93e2142c98c299` before any deletion. Tag object `af3f3bb397b763418d731d7682463b1aade16a1b` remains intact. V8 is REJECTED; the recovery is not artwork approval or deployment.

The dependency inventory in [docs/v9-world/dependency-inventory.json](docs/v9-world/dependency-inventory.json) separates fixed north, reusable source artwork, character assets, shared controller/animation/UI/learning systems and obsolete southern layers. [deleted-files.json](docs/v9-world/deleted-files.json) lists every removed tracked path with original Git blob and byte count: **4,931 files /4,087,341,729bytes**. Unknown/untracked work was not selected. `.git`, recovery tags, main and the separate learning application were untouched.

Removed active roots include old revision entry HTML/configs; old southern scene adapters, road masks, composite grounds, map bundles, obsolete coordinate/nav/collision data and their abandoned exports; historical screenshot/video/ZIP/report collections; and generators/tests tied only to removed map entries. The4,931-file inventory is the exact audit, not a claim that all character/art resources were deleted. The current `.gitignore` now excludes generated media and allows only the eventual V9 review ZIP/video. Existing user-approved source assets remain tracked.

Preserved/rebased:

- `assets-src/protected-north`: literal4352×2240approved northern image, land mask,273original placements, bodies/anchors/stops and immutable hash proof. No north layout changes.
- `assets-src/library`:110reusable native art kinds, original masters/prop sheets/prompts/provenance, and artwork-local physical templates. No old southern global coordinates, roads or plot data are retained as planning input.
- Entire approved Juni144-frame source/generation/registration/palette and Bori/Juni/Nari master sources; original physics/legacy actor assets and original creator tooling where needed.
- Shared Phaser movement, JuniMotion, occlusion, analog joystick/mobile UI, dialogue, Academy lesson/interior and guest content. Shared module moves/import rebasing are recorded; movement and animation logic remain protected by source checks.
- Licenses, package lock, build/test infrastructure and mandatory Forge/Juni production records under `docs/pipeline/`.
- One actual V8 engine image under `docs/v9-world/V8_BEFORE_ENGINE.png` solely for honest before/after comparison. It must NEVER feed V9 layout or terrain generation.

Old southern runtime tests were archived with their removed entries. Current tests must cover the new geometry and preserved behavior; no old collision counts/coordinate hashes are frozen and no equivalent working behavior is claimed from a passing source-only check.

Restore the COMPLETE old working tree into a separate recovery directory, without changing the current branch/history:

```bash
mkdir -p /workspace/recovery-v8
 git archive recovery/before-v9-total-southern-reset-20261021 | tar -x -C /workspace/recovery-v8
```

Read an individual old file without restoring it into the active project:

```bash
git show recovery/before-v9-total-southern-reset-20261021:docs/v8-city/RECOVERY_ARCHIVE.md
```

The archive contains the complete source, native screenshots, final75310320byteMP4 and exact14171740byteHTTP-tested ZIP. To inspect old V8, extract its ZIP and run `python3 start.py`; never open raw HTML/file://. Its source CI39443356059 actually passed12unit/65browser cases; recovery annotation distinguishes that source result from subsequent archive-only additions. No V8 independent fresh-clone claim is added. V9 will receive its own final verification after actual implementation.

No Git history rewrite, force push, tag removal, main merge, website deployment or paid API occurred.
