# Scope and preserved foundation

The existing registry, CharacterSelection dialog, local preference key/schema, PlayerCharacterManager, Phaser asset loader and shared scene controller remain in use. Each existing Haneul/Bomi/Minjun entry now points to its own actual native atlas. No new avatar engine, duplicated movement controller, map generation, asset cleanup or world integration was introduced.

RegistryMotion only gained optional authored start/stop/turn playback. Distance phase still advances from actual accepted travel, and paused/blocked input cannot advance it. Juni still uses the original immutable JuniMotion and144-frame atlas.

The reload test exposed an existing foundation limitation: character choice persisted, but scene position and existing visited markers restarted. A small per-tab version1 session checkpoint now saves those two existing fields on pagehide and restores them only on actual browser reload of the identical pathname/query and canonical scene. A deliberate new review-entry navigation keeps its declared spawn. Restore validates schema, world bounds, logical solids and the original native ground mask. Corrupt/denied storage safely falls back. This adds no accounts, quests, learning progress, inventory or Phase2 services, and leaves the character-preference key untouched.

Main scene changes are imports, validated reload seed, visited seed and pagehide listener. Movement sweep, world geometry, NativeContact, FoundationCamera/Tour, depth policy, joystick, native viewport and sampling remain unchanged. Protected source/hash reports and actual paired native world readbacks verify preservation independently.

Physical Android/iPhone testing and hardware WebGL performance remain NOT TESTED. Browser touch/DPR emulation and software WebGL smoke evidence are labelled separately. The canonical outdoor world has no implemented room/interior transition; no historical V10 interior was substituted to manufacture a production PASS.

## Historical test input synchronization

The unchanged legacy V10 runtime exposed a test-harness defect: `axis()` began the next direction while original Juni still decelerated. The diagnostic trace records ~8px perpendicular drift after release; the suite and unchanged isolated retry timed out on the leisure route, while a state-observed diagnostic completed it. Only the unprotected E2E helper was corrected: wait for the real exposed velocity to reach zero, use the existing walking key for the last few pixels, restore Shift, and assert each waypoint within4px. Original routes,8s minimum movement timeout, final16px gate, obstacle checks and production code remain unchanged. This strengthens registration checking; it does not relax collision/animation validators or move the actor through a test hook between waypoints. The original full-suite failure, isolated failure and diagnostics remain under initial-attempt/ and legacy-recheck/.
