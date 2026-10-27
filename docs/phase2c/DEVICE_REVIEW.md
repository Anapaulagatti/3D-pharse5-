# Physical-device handoff

Status: Android Chrome NOT TESTED. iPhone Safari NOT TESTED. Hardware GPU, thermal stability and sustained mobile memory NOT TESTED.

1. Unzip PHASE2C_FASHION_STUDIO_REVIEW.zip. Run `python3 start_review.py`; open REVIEW.html locally. For your own LAN test explicitly use `python3 start_review.py --lan`, then open the host LAN IP and port4342 from the phone. No public hosting is required or authorized.
2. Record the actual device model, OS/browser versions, viewport/DPR, checkpoint and ZIP SHA256. Open DEVICE_REVIEW.html in the package and keep a native screenshot plus screen recording.
3. Test both landscape orientations, notches/safe areas, gallery scrolling, all three categories, preview directions/actions, named presets (save/rename/delete/cancel), reset, return, reload and joystick isolation. Verify progress and original world position.
4. Repeat60actual character changes and100preview/apply operations. Record resource counts, visible stutter, warm-up, thermal behavior and browser crash/reload, separately from estimated texture bytes. Do not infer GPU memory from atlas dimensions.
5. Enter PASS/FAIL/WARN only for observed checks. Leave unrun checks NOT TESTED. Export the local JSON report with actual screenshot/video filenames. The form requires recorded evidence to accept PASS. It does not transmit data or authenticate evidence.

Desktop Chromium Canvas and software SwiftShader checks are technical smoke evidence only. No physical-device PASS has been claimed.
