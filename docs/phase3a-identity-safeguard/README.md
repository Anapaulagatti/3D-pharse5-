# Phase 3A — final fictional identity safeguard

The owner requests fictional public identities while preserving the approved artwork at `8a2dbe6f`. This targeted continuation starts from `c6b805cb` on `feature/phase3a-fictional-identity-safeguard`. It does not rebuild Phase 3A or begin Phase 3B.

| Public Vietnamese display | Korean display | Fictional role |
|---|---|---|
| Han Yeonhwa | 한연화 | Cultural keeper |
| Baek Junseo | 백준서 | Writing scholar |
| Nam Gyeongu | 남경우 | Artisan researching tools |
| Yun Hwayeon | 윤화연 | Artist |
| Kang Muyeong | 강무영 | Coastal guide |
| Seo Daeun | 서다은 | Culture-loving student |

Names, occupations, archive introductions, interaction labels, 36 dialogue nodes, gallery captions and accessibility text use the fictional presentation. Internal NPC IDs and source provenance remain stable. The six are not presented as real historical people or credited with real achievements. Detailed unverified biographies stay disabled.

[Current native gallery and actual gameplay](REVIEW.html) · [QA](QA.md) · [Protected hash audit](PROTECTED_AUDIT.json) · [Individual depiction review](DEPICTION_REVIEW.md) · [Rights matrix](../phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md) · [Phase 3B handoff](PHASE3B_HANDOFF.md).

All 26 NPCs remain operational through the existing registry, movement and dialogue systems. No source pixel, atlas, animation mapping, collision, route, world asset, playable character or cosmetic is edited. There is no new actor engine or save migration. Twelve playable characters and 28 cosmetics remain protected.

[Playable ZIP](PHASE3A_FICTIONAL_IDENTITIES_REVIEW.zip): extract, run `python3 start_review.py`, open its printed local URL. Fresh storage uses the original Character Studio. [Package checksum and extraction proof](PACKAGE_PROOF.json) records what was actually checked.

Fictionalization is an owner-directed precaution, not a finding that historical names are prohibited and not commercial depiction clearance. The individual review records visual associations and its limits. Any substantiated art concern requires an independent review; approved art is not silently changed. Physical Android/iPhone and hardware-GPU tests remain NOT TESTED. Prior art-validator and spatial warnings are retained.

Stop after the new recoverable checkpoint and handoff. No Phase 3B implementation, main merge, public deployment or separate learning-website changes.
