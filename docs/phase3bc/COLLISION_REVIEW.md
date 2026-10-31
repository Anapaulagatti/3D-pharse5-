# Collision review

All4352×4864 canonical native mask cells, continuous logical building footprints and local native contact guard are inspected. Global movement uses a swept ground-anchor sample, not the sprite's96×112 transparent rectangle or an Arcade physics body. The existing western-house local native footprint guard remains direction-dependent. Do not infer a new global36px body from an illustration.

Four visible doorstep pads were rejected by legacy collision padding: cafe, bookshop, learning building and Maru. `src/gate3/Accessibility.ts` opens only four named lanes, outside the unchanged protected building solids. No doorway/facade/world-coordinate movement. Foreground/chunk readiness checks still apply. Door triggers retain canonical target coordinates.

Two native collision-only chunks additionally restore practical lanes on existing Jeju stone bridge decks: `COLLISION_AMENDMENTS.json` records source/current hashes, exact paths and changed cell counts. Initial conservative4px driver-grid planning exposed narrow lanes; the original full-resolution anchor mask was connected, so this was not proof the whole bridge was impassable. Visible-deck21px lanes remove unnecessary collision padding; no rail posts, sea, pier faces or vegetation sources are repainted. Actual controls must validate these changes separately.

`NAVIGATION_AUDIT.json`:110 canonical review/target/plot anchors; radial margin is diagnostic, not proof of art or real movement. Several legacy markers lie in blocked scenery:

- Jeju arrival/bridge-island `(3500,3610)` is on planted/railing ownership; approach uses the existing stone lane, not that plant.
- Old Jeju ferry-landing marker `(3180,4020)` is off the approved bridge deck. Ferry gameplay remains future; no water opened.
- Palace-west review marker `(1740,1090)` falls inside the retained side-garden collision ownership. Main ceremonial, archive and eastern paths are separate. A specific side-garden entry still needs a local visual/route decision; no wholesale garden/wall removal.
- BridgeB's old mainland marker has6.4px radial margin; the functional deck lane is tested separately.

These are retained WARN/FAIL metadata entries, not silently moved checkpoints. Closed building interiors, cultivated bed interiors, water, cliffs, fences and decorative bases stay blocked. Bakery remains unplaced; W0 rejected and Q1 unapproved. The rejected station90×36 visual connector remains absent. Station/platform access is tested through existing eastern public circulation, not claimed through the old blocking strip.

Read-only `?qa&collisionDebug` overlay: green actual ready walkable anchor samples; amber<8px local neighbor clearance; red blocked/unready cells; white actual global anchor plus local native-contact pixels when in that field; blue approved doorstep amendments. It never mutates collision. A red chunk before loading is a readiness block, not a permanent terrain diagnosis.

Actual traversal results, failures and corrected driver issues are retained in TRAVERSAL_QA/RUNTIME_QA and their INITIAL records. A screenshot alone is not counted as traversal.
