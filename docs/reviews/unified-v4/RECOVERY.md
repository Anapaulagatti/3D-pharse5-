# Exact recovery without resetting current work

Old3D: clone archive/3d-final-before-pixel-v3-20261015 into a different directory; HEAD must be f1f13f2b4aebcc2659d94cde84800cef17ad7a4e. Fresh remote clone executed again for V4;2738file SHA256s match docs/migration/3d-archive-proof.json. See quality-reports/unified-v4/gate0-recovery.json.

Rejected pixel: clone repository into a different directory, checkout checkpoint/pixel-art-reset-v2-review-20261015; HEAD must be2554327606b046db79a4be04668d935d4bc74639. Old sources/ZIP/evidence also remain in the active tree, but Vite public-unified excludes them from the current runtime. Do not overwrite uncommitted work or force push. Current previous-review-preservation.json records1923file hashes before V4 work.

Gate0–1 readiness checkpoint03473c434506f96ca6f9925bf8adbc176bd41174. No additional3D files/dependencies were removed: the migration was already complete. Frozen showcase-v0.5 and existing public Pages are untouched. No main changes or website deployment jobs.
