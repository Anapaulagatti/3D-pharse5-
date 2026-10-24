# Physical-device review / report export

Android Chrome and iPhone Safari are **NOT TESTED**. Chromium touch emulation is a separate regression check, not physical-device acceptance. Hardware WebGL performance is unresolved.

1. Extract the complete ZIP. Run `python3 start_review.py`. For a trusted private Wi-Fi test only, use `python3 start_review.py --lan`; open the machine's private LAN address and printed port on the phone. This is local review, not a public deployment.
2. Record device/model, OS, browser/version, landscape orientation, DPR/viewport, build/checkpoint identifier, battery/power mode and test duration. Capture actual screen video; do not infer a PASS from desktop emulation.
3. Follow the ten region links. Check native Juni size/animation, crisp/stable pixels, visible entrances, street/bridge joins, foreground fade and collision contact. Bakery is intentionally unplaced; the8px strip and listed route/projection issues remain known failures.
4. Test joystick movement without moving the camera, diagonal walking/running, Scenic drag/pinch, tour Pause/Skip, collapsed controls/restoration and Return to Juni. Verify the original Juni position is retained during the tour. Repeat with reduced motion enabled.
5. Walk for at least10 minutes through historical, retail, station, amusement, harbor and Jeju regions. Record stalls, missing chunks, memory reloads, heat, browser termination and visible cadence. A managed64MiB cache budget is not actual total GPU/browser memory. Do not claim60fps from average update intervals.
6. Open `···` → **Export test report**. Keep the downloaded JSON together with device details, UTC time, actual screen video and issue notes. Name them `DEVICE_OS_BROWSER_CHECKPOINT_UTC.*`.
7. Report each item as PASS, FAIL or NOT TESTED with its evidence filename. Preserve failed attempts. Hardware/device PASS requires recorded evidence on that actual device.

This package uses the accepted controls. Extracted-package emulation below checks selected behavior only; it does not close physical-device or performance P1s.

Extracted-package regression: [ten-region smoke report](package-smoke.json) and [downloaded session](package-emulated-session.json). Normal-motion Pause/Resume/Skip and reduced-motion static-tour/disabled Pause were checked separately. Use [device report template](DEVICE_REPORT_TEMPLATE.json) for actual hardware results.

Review checkpoint: `checkpoint/g3d-spatial-reconciliation-review-20261024`. The final world remains a candidate; confirm current evidence against the exact artifact tag. Physical-device results require actual device recordings and exported sessions, not the headless smoke report.
