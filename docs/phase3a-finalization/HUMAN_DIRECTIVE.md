# CODEX — FINALIZE PHASE 3A & LOCK 26 NPCs
## Additional Task: Historical NPC Identity & Rights-Safe Fallback

The human project owner officially approves the current 26-NPC roster, visual quality, animation style and gameplay foundation as the development baseline.

**PHASE 3A ARTISTIC APPROVAL: GRANTED.**

Use review checkpoint `831022a8` as the reference, after verifying the exact commit and working tree.

## TASK 1 — LOCK APPROVED CONTENT

1. Create an immutable, recoverable Phase 3A approval checkpoint.
2. Lock all 26 approved NPC identities, artwork, sprite atlases and animations, except changes explicitly required by the rights-safety task below.
3. Preserve all 12 playable characters, 28 cosmetics and approved world artwork.
4. Preserve NPC registry, dialogue, navigation and interaction systems.
5. Record protected asset hashes and update project documentation.
6. Do not regenerate or redesign approved NPCs without a documented legal or technical requirement.

## TASK 2 — HISTORICAL NPC IDENTITY & RIGHTS-SAFE FALLBACK

Review the six historical NPCs:

- Seondeok (선덕여왕)
- Sejong (세종대왕)
- Jang Yeong-sil (장영실)
- Shin Saimdang (신사임당)
- Yi Sun-sin (이순신)
- Yu Gwan-sun (유관순)

### A. Verify legal and source status

For every NPC, distinguish:

- Historical names and public-domain historical facts.
- Copyright in specific source illustrations, photographs or other artwork.
- Rights relating to recognizable likenesses or commercially protected identities, where applicable.
- Ownership and permitted use of the actual AI-generated or illustrated NPC assets.

Do not interpret an inaccessible reference URL or HTTP 403 as proof that rights are unavailable.

Do not invent licenses, permissions or legal clearance.

### B. Fictional identity fallback

If a proposed NPC identity or its depiction cannot be cleared for its intended commercial use, replace that NPC's public-facing identity with an original fictional Korean character.

Requirements:

1. Create a new Korean name and Vietnamese display name.
2. Avoid names, titles, aliases or identifying combinations that closely imitate a protected identity.
3. Preserve the character's historical-era role and educational theme where appropriate.
4. Remove or independently redesign protected or excessively recognizable likeness elements when needed.
5. Keep the character's approved visual quality at Juni level.
6. Do not downgrade art quality or replace the NPC with generic procedural sprites.
7. Maintain the same total NPC count.
8. Maintain navigation, dialogue and interaction functionality.

Do not assume renaming alone resolves copyright, likeness or other intellectual-property risks.

### C. Preserve gameplay compatibility

Do not change stable internal NPC IDs unnecessarily.

Use a separate display-name and fictional-identity mapping so existing:

- NPC registry references.
- Dialogue IDs.
- World coordinates.
- Interaction points.
- Animation registrations.
- Future quest hooks.
- Saved player data.

remain compatible.

Update Korean and Vietnamese dialogue consistently.

Remove any claims that a fictional NPC is the actual historical person.

### D. Educational integrity

Verified historical facts may remain in a separate educational information system with appropriate sourcing.

Do not fabricate historical biographies or present fictional events as documented history.

Distinguish clearly between fictional game inhabitants and historical information.

If facts remain unverified, mark the educational material as pending and exclude it from public release until verification.

### E. Deliver a rights and identity matrix

Create:

`docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md`

Include for each NPC:

- Original historical reference.
- Public-facing game identity.
- Original or fictional status.
- Artwork provenance.
- Rights/permission status.
- Reason for retaining or changing the identity.
- Dialogue and localization migration.
- Remaining release blockers.

## TASK 3 — PRESERVE THE APPROVED ROSTER

Keep all 26 NPCs available.

Do not create replacement duplicates.

Do not modify unaffected characters.

Do not touch the approved world map, Character Studio, cosmetic system or player animations.

Any authorized modifications to historical NPC artwork must be individually documented and regression tested.

## TASK 4 — FINAL QA & HANDOFF

Run existing project validation and relevant regression tests.

Confirm:

- 26/26 NPCs remain registered.
- All NPC interactions work.
- No broken dialogue references.
- Korean/Vietnamese names display correctly.
- No navigation regressions.
- Sprite atlas compatibility remains intact.
- All protected artwork outside authorized scope remains unchanged.
- Historical and celebrity rights issues are recorded accurately.
- Physical-device testing is not falsely marked PASS.

Create an immutable approval checkpoint after the changes.

Update `AGENTS.md` and `docs/current/PROJECT_STATE.md`.

Prepare the architectural handoff for Phase 3B.

No main merge or public deployment without separate authorization.

**PHASE 3A: APPROVED AS DEVELOPMENT BASELINE.**

**PHASE 3B: READY AFTER CHECKPOINT VERIFICATION.**

Do not start Phase 3B in this task.