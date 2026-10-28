# Verified Phase 3A development checkpoint

- Human artistic review: `831022a8533c1d2126f77724d6eea8aeca2e8e30`.
- Permanent before-change reference: `checkpoint/phase3a-26-npc-art-approved-20261029-831022a8`.
- Completed development checkpoint: `checkpoint/phase3a-26-npc-development-approved-20261029`.
- Exact checkpoint commit: `8a2dbe6f8077c3263f1280311e3673899f3d37f9`.
- Working branch: `feature/phase3a-approved-roster-lock`.

Both references were published without replacing an existing ref. The checkpoint above remains immutable; this later receipt records its external verification.

All 26 NPCs are available in ordinary development gameplay. Approved artwork and animations, twelve playable characters, cosmetics and world assets remain unchanged. All 26 actors passed movement, interaction and return-control checks in an independently extracted offline ZIP. Actual Phaser native readback matched approved opaque pixels for all 26 with no mismatch or foreground occlusion.

Current validation: 153 unit tests passed; the full E2E run passed 67 cases and exposed one obsolete 20-record expectation. After changing that expectation to the approved 26 records, the single affected case passed on rerun. The original failed run remains recorded. Typecheck, asset validation, lint, formatting and build passed.

[Publication receipt](published-verification.json) verifies 46 immutable file URLs, a complete remote ZIP download with matching SHA256, all 291 preexisting remote refs unchanged, and untouched main at `33360ed1989e4db9fc3fc4e3686ca385e0b00908`.

ZIP: `PHASE3A_APPROVED_26NPC_DEVELOPMENT.zip` (77,804,987 bytes).
SHA256: `2c9c6a14057c4398192c539ca802e843d21dbc1cdd8dae2905a63c0adbc140b4`.

All six historical public names are retained; zero fictional substitutions or art exceptions were required. Commercial rights, applicable generation terms, detailed historical facts and modern real-person fact cards remain pending, as described in the required rights matrix. Physical Android, iPhone and hardware-GPU validation remain NOT TESTED. These limitations are not waived by artistic approval.

**Phase 3B foundation: READY after the verified checkpoint. Phase 3B implementation: NOT STARTED. No main merge or public deployment.**
