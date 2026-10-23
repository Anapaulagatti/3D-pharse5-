# Physical-device review handoff — NOT TESTED

The existing Android/iPhone workflow remains available. This package adds a touch-emulation report; it is not physical-device evidence.

1. Extract the ZIP on a computer, run `python3 start_review.py --lan`, and connect the phone to the same private Wi-Fi. Open the printed LAN URL using Android Chrome or iPhone Safari. The default command binds only localhost; no public deployment is provided.
2. Record model, OS/browser version, landscape CSS size/DPR, thermal/power state and orientation. Record a short screen video of native movement, region transitions, station approach and Jeju arrival/house path.
3. Check joystick release, diagonal movement, Run, Explore, scenic dragging, pinch/preset zoom, tour titles/Pause/Skip/Return, collapsed controls and reduced-motion settings. Verify tour return preserves Juni's position; joystick movement must not start camera gestures.
4. Open Options(···) → Export test report. Save its JSON with the device record and screenshots/video. Repeat after a longer traversal to observe cache eviction and heat/frame pacing.
5. Mark individual results PASS/FAIL with recorded evidence; otherwise keep NOT TESTED. A report exported by a desktop emulator does not grant a physical-device PASS.

Known world defects remain in GATE3_MASTER_DEFECT_REGISTER.md. Do not confuse expected unresolved route/geometry defects with a successful device controls test.
