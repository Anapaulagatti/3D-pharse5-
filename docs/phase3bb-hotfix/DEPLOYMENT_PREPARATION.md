# Same review Pages workflow; exact exposure gate retained

Destination remains Anapaulagatti/3D-pharse5-review. Productionv0.5/source-main are untouched. No new public artifact push, approval receipt or deployment run is created for this candidate before its exact owner decision.

The original20 release's recorded hosted QA failed an asset URL, not a gameplay rebuild: `phases/3b-a/contemporary20-e0f9db0d/play/.vite/manifest.json` returned404. Upstream `actions/upload-pages-artifact@v4` was successfully fetched from its official GitHub action source during this task. Its tar step explicitly excludes `.[^/]*`, dropping the approved dot-directory metadata even though the exact source manifest included it. Evidence is saved as UPSTREAM_PAGES_ACTION.yml. This is distinct from the input/camera movement defect.

The controlled transport correction retains the same workflow/jobs, owner receipt, hash gate, protected github-pages environment and deploy-pages action. Only the archive step is replaced with a regular-file allowlist tar and upload-artifact using the required github-pages/artifact.tar format. Every manifest file is rehashed, unmanifested files/symlinks/Git metadata rejected, and tar member set compared with the allowlist. No artwork or manifest bytes are edited. This preserves the old20 snapshot byte-for-byte, including its approved metadata, and avoids reproducing404 in the retained snapshot after the new release.

The new game compilation does not request a Vite build manifest; its live runtime has no hidden-directory dependency. Existing approved snapshot bytes remain canonical. No old checkpoint is overwritten.

The local new26 candidate has already passed actual Phaser, dialogue, clock, mobile emulation and resource checks. Hosted verification after an authorized release must additionally prove the new exact live manifest, all26 catalog IDs, actual interaction/movement/touch and resource/console status. Physical Android/iPhone/GPU remain NOT TESTED.

Transport-only control fix committed and pushed to the separate review repository as `77cd925`. It changes no approval receipt and therefore does not match the workflow release trigger; no game deployment was requested.

Public export uses the existing identity presentation functions before bundling. It removes obsolete real-name/date/source-URL proposals from the six original canonical JSON inputs in the derived build only. It retains stable IDs, native atlases, routes and all displayed fictional dialogue; canonical source/provenance is unchanged. This is data minimization, not an assertion that renaming grants rights.
