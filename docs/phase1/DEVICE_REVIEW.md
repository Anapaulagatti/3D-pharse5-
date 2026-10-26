# Physical-device handoff — NOT TESTED

Android Chrome/iPhone Safari and hardware WebGL performance have no recorded device evidence. Chromium844×390/DPR3 touch emulation is a regression check only.

1. Extract ZIP, run `python3 start_review.py`, open localhost. Use its `--lan` option only on trusted private Wi-Fi for a phone; no public deployment.
2. Record device/model, OS/browser, landscape viewport/DPR, power/thermal state, checkpoint and actual screen video.
3. First launch must show four gallery cards. Only Juni is playable. Haneul/Bomi/Minjun are clearly incomplete; their confirmation stays disabled. Do not record them as completed characters.
4. Select Juni with “Bắt đầu hành trình”, check four-direction walk/run, Space/wave, C/celebrate or mobile emote buttons. Check building occlusion, original joystick isolation, exploration key/button and native sharpness.
5. Reopen selection from `···` → Chọn nhân vật, browse incomplete references, return to Juni without moving the player or losing world state. Reload: saved Juni restores directly. Try blocked storage: session play must remain possible.
6. Preserve Scenic/Tour Pause/Skip/collapse/Return and reduced motion. Visit station/bridges and record any collisions or missing chunks. Current known inherited world issues remain separate; do not change the map.
7. `···` → Export test report downloads the existing `gate3a-test-report.json` workflow, now including characterId/player count in state. Save JSON with device details, video, UTC time and PASS/FAIL/NOT TESTED notes. The cache budget is not a measured device memory/fps guarantee.

No different-avatar switch can be tested until another complete native atlas exists. Phase1 four-character acceptance remains INCOMPLETE. No Phase2 authorization is implied.
