# Phase 3A — approved 26-NPC development baseline

The owner approves the 26 NPC identities, artwork, animations and gameplay foundation reviewed at `831022a8533c1d2126f77724d6eea8aeca2e8e30`. All approved art is preserved. The before-change approval tag is `checkpoint/phase3a-26-npc-art-approved-20261029-831022a8`; the final development tag is `checkpoint/phase3a-26-npc-development-approved-20261029`. Branch: `feature/phase3a-approved-roster-lock`; exact original base and hashes are in APPROVED_BASELINE.json.

Ordinary development gameplay now registers **26 unique NPCs: 14 residents + 6 original modern visitors + 6 historical archive reconstructions**. No QA flag is needed for archive access. The original 20-person living collection and legacy resident count of 14 remain compatible. The existing registry, state machine, navigation, dialogue and bounded texture pool are reused.

All six historical names are retained; there are **zero fictional replacements and zero artwork edits**. The documented art inputs identify no copied museum portrait, photograph, standardized portrait or film actor. This input-chain finding is not comprehensive legal clearance. HTTP 403 is a transport failure, not a rights denial. Commercial release still requires applicable generation terms, jurisdiction and depiction review. See the required [rights and identity matrix](../phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md).

Public KO/VI names are now separate from stable IDs. Neutral reconstruction notices replace obsolete art-preview wording. All 36 archive node IDs, links, vocabulary and hooks remain compatible. Detailed historical facts and six separate modern real-person fact cards remain unverified and excluded from factual release. No authentic portrait, quotation, endorsement, account or lesson completion is invented.

- [QA](QA.md): 153 unit tests passed; E2E: PASS: 67 original full-suite cases + the corrected 26-record case on rerun.
- [Approved roster and hashes](APPROVED_ROSTER_26.json), [protected audit](PROTECTED_AUDIT.md), [exact scope](MIGRATION.md).
- [Native screenshots and actual gameplay](REVIEW.html), [Phase 3B architectural handoff](PHASE3B_HANDOFF.md).
- [Playable ZIP](PHASE3A_APPROVED_26NPC_DEVELOPMENT.zip), [checksum and extraction proof](PACKAGE_PROOF.json).

Extract the ZIP, run `python3 start_review.py`, and open the printed local review URL. No Node installation or network is needed for gameplay. Fresh storage shows the unchanged Character Studio: choose a character, then enter the world. Optional full-resolution online source links are distinct from local native crops.

Physical Android, iPhone and hardware-GPU validation remain **NOT TESTED**. Previous art-validator and world-planning warnings remain documented. Phase 3B is an architectural handoff only: **no implementation, main merge or public deployment**.
