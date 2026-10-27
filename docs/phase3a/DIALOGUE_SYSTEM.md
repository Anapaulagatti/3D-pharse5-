# Contextual Korean/Vietnamese dialogue

42 authored nodes (3perNPC),all present in the shipped registry. Every resident has welcome/context/care content,2simple topic choices and an optional next link. Text is authored and deterministic; no AI API,quiz,reward or shop action is invoked.

Nodes carry stable ID,NPC ownership,KO/VI content,locale-aware hint/choice labels,next references,conditions and future topic/hook metadata. Startup validation rejects duplicates,missing/cross-owned links,unreachable nodes and cycles. A defensive8-step cap closes invalid runtime sequences and releases movement safely.

Approach a resident and press E,use the proximity button or the supported Explore control. Eligible visible actors require a valid canonical-ground line and≤92px range. Closest distance and stable ASCII ID resolve priority; a14px hysteresis window prevents near-equal targets flickering. Current routes keep residents apart. TALK pins the selected actor and only one modal can open.

The panel shows VI/KO name,occupation,Korean text,Vietnamese translation,topic choices,Next and Close/Return,plus a native preview from the resident’s actual atlas. It uses its own scoped classes,44px controls and safe-area insets,not the legacy HUD footer’s pointer policy. Keyboard Enter follows focused choices/next; Escape/close always release the lock. Touch/keyboard events stay inside the modal. Movement/analog state is reset through the existing host pause/reset mechanism; no player controller is replaced. Closing returns the NPC to its prior valid activity.

Korean wording was manually checked for polite register,grammar and location/occupation context; translations retain the meaning. These are short beginner-friendly introductions,not authenticated lesson content. Native Korean editorial/human acceptance remains part of final review; automatic Hangul/text-integrity checks do not grant linguistic or artistic approval.

Future NPCLearningContextProvider accepts only an authenticated learning context/curriculum identifiers. No provider is connected now; no lesson completion is invented. Future content should use a beginner curriculum when verified data is absent. Quest/shop IDs are null; equipped cosmetics,owned inventory and future server authorization remain separate. The existing Korean-learning website is untouched.

NPC-only storage: korean-arena-npc-world-v1. Existing korean-arena-player-preferences-v1,korean-arena-appearance-preferences-v2 and world/progress stores are unchanged. [Real landmark visit→NPC dialogue→reload proof](extra-evidence.json) is separate from test sentinels and does not claim external learning-account verification.
