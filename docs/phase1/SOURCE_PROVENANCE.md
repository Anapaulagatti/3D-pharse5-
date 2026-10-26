# Art and engine provenance

Approved world/Juni: exact baseline SHA `a183b1a69f08571acea1a35b4d70185ad95a2257`, checkpoint `checkpoint/world-art-approved-phase1-20261026`. [World hashes](protected-world.json), [Juni hashes](protected-juni.json), [paired actual Phaser preservation](preservation-qa.json). No world image generation, geometry, collision, source-art overwrite or Juni revision.

Five ACTUAL built-in imagegen calls:3original full-body design references (Haneul/Bomi/Minjun),1front-walk pilot,1targeted opposite-leg repair. External paid provider API/key calls0. Model/cost not exposed by host. Full retained files, visual references, prompt summaries and SHA256 in [run manifest](../../assets-src/characters/phase1/run-manifest.json) and [asset provenance](asset-provenance.json). Summaries are labelled summaries, not a claim of retained byte-exact prompt transcripts.

Applicable skills read in full:
- [Forge generate2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/generate2dsprite/SKILL.md)
- [Forge video2dsprite](https://github.com/0x0funky/agent-sprite-forge/blob/5324342fdfab72430f4e9604f3fe427009f8596d/skills/video2dsprite/SKILL.md)
- [Character Animation Creator](https://github.com/tachikomared/character-animation-creator-skill/blob/9ce98dffb98c84488fe7b99b62c49fabee20abd6/SKILL.md)

Actually executed: Forge doctor (host-image available, AI-video route absent),3binary-key clean jobs for reference portraits, Creator key helper plus2diagnostic motion audits, native fixed integer4 extraction for DIAGNOSIS ONLY. No paid video synthesis, full sprite_set, code-drawn character art, static-image sliding, procedural hero substitution or new accepted gameplay atlas. Pinned optional tool clones remain in `/workspace/tooling-cache`; neither tool code nor AGPL dependencies are vendored into production. Re-clone exact pinned Creator commit there if reproducing optional diagnostics; setup/build never generate artwork.

Both Haneul pilots fail visual gait: the leading shoe stays on the same side in all8poses. Measured leading-toe x offset has the same positive sign in every pose. Requested source size/root guides were not respected. The rectangular96×112 diagnostic also encounters the Creator square-cell validator mismatch (`atlas is 768x112; expected 768x96`); that tool limitation is separate from the independently observed visual rejection. Raw warnings/errors retained, no thresholds weakened.

All3new designs remain INCOMPLETE. High-resolution keyed reference portraits retain matte key-ring warning metrics ([verbatim values](asset-provenance.json)); these are not final native sprites or approved alpha/animation artwork. They are never spawned into the world. Original raw masters, keyed previews, failed trial/repair and exact processing stdout/stderr remain recoverable. Bomi/Minjun animations are NOT AUTHORED, rather than implicitly passed. Juni alone has the original complete144-frame atlas and actual native gameplay evidence.

Renderer uses installed Phaser4.2.1/TypeScript5.9/Vite8 and existing Zod. Package files/dependencies unchanged; no upgrade. All actual game sprites retain native scale1, nearest sampling and original Juni feet/origin. Portable review bundle changes asset base URLs only; final extracted-package checks verify it independently.
