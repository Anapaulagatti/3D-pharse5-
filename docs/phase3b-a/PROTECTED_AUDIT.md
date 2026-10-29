# Protected content audit

Base: `4d8162282a340f2b87ca6309973a959bb005a4e8`; approved art/identity reference: `6dbee381fcf1adf79f3f96c931b7170cea2ba076`. BASELINE.json was recorded before recovery edits to tracked source. Exactly 23111 preexisting tracked files checked; 23105 remain byte-identical. Every authorized code/authority exception has before/after SHA256 and purpose in PROTECTED_AUDIT.json.

- 9083 preexisting NPC/player/cosmetic/world asset files unchanged.
- 36 original test source files unchanged; 15 unit and3 E2E cases are additive.
- All26 IDs, native96×112/48,100 registration, 104cells/actor, atlas pixels/JSON and NPCDefinition route/speed/footprint remain.
- Twelve playable characters,28cosmetics/Studio, world masks, collision, camera, tour and old storage contracts protected.
- package.json, lockfile and preservation validators unchanged.
- Zero image-generation calls, actor-art edits, world-art edits or silent candidate promotions.
- 28 prior historical fixture files copied at their already-approved hashes and versioned; see ARCHIVAL_RECOVERY.json. These are exact recovery dependencies, not authored replacement art.

No historical tag or branch is overwritten. The original older checkout was preserved; recovery used a separate worktree. Rollback uses the approved base and removal of only the additive life-clock key if desired. No destructive reset or blanket checkout is required.
