# Physical-device review — Android Chrome / iPhone Safari NOT TESTED

The district artistic prototype is human-approved at checkpoint/gate25-refinement-approved-20261022 (868aa60). This handoff authorizes device review only. Gate3, production integration, main merge, deployment and large expansion remain locked.

## Launch the frozen package

1. Extract `GATE25_DEVICE_REVIEW.zip` on a computer with Python3. On the same trusted Wi-Fi as the phone, run `python3 start.py --lan`. Keep that terminal open; stop with Ctrl-C when finished. Allow the local Python server through the computer firewall if required. No public hosting is needed.
2. Substitute the computer's LAN IP in `http://COMPUTER_LAN_IP:8065/3D-pharse5-/gate2-review.html?scene=district-refinement`. Open with actual **Chrome on Android** and actual **Safari on iPhone**. `127.0.0.1` on a phone refers to that phone, not the computer.
3. Rotate to landscape. Record exact device/model, OS/browser version, viewport/DPR, browser bars, orientation and OS reduced-motion state. The archived picker still says approval pending because the approved runtime is frozen; the approval document/checkpoint records its accepted visual status.

## Short review — 3–5 minutes per device

| Check | What to do | Initial status |
| --- | --- | --- |
| Loading / native appearance | Open district; inspect sharp pixels, Juni identity/scale and full-size facades. Look for blank chunks, flicker or lost textures. | NOT TESTED |
| Controls | Use joystick through all directions, Run with a second finger, then release; confirm movement stops. Joystick gestures must not pan Scenic camera. | NOT TESTED |
| Two district joins | Move Muneum → bakery → station doorway and back. Inspect sidewalk contact, entrances, foreground occlusion and chunk transitions. | NOT TESTED |
| Pedestrian connectors | Enter west alley and east station-garden passage from sidewalk, continue toward rear promenade, then return. Inspect roots, lamps, contact shadows and circulation at native scale. | NOT TESTED |
| Foreground | Inspect four varied planting pockets and unchanged lower paths/borders. Record any localized issue with screenshot and position. | NOT TESTED |
| Camera | Scenic drag/pinch, Full scene and Return; Return restores native view and preserves Juni's world position. | NOT TESTED |
| Jeju tour regression | Open scene `c`; run coast → oreum → orchard → house at50%. Check landmark titles, idle collapse/restore, Pause/manual view/Resume, Skip, Return and joystick cancellation. | NOT TESTED |
| Safe areas | Landscape left/right; browser bars visible/collapsed. Verify joystick, Run/Explore, Scenic, titles, Skip/Pause/Return remain accessible. | NOT TESTED |
| Reduced motion | Enable OS reduced motion, reload; use static tour selections and immediate Return without automatic panning. | NOT TESTED |

## Sustained review — at least15 minutes per device

Keep district and Jeju as separate scene sessions. Repeat joins, walk/run, camera modes and background/foreground restoration; do20 mode cycles. Export at start,5minutes and15minutes. Record visible stutter, touch lag, texture loss, unexpected reload, crash and orientation problems. A scene change reloads the document and resets its session, so save exports before switching.

## Export and submit evidence

1. Return to Juni → Options(···) → **Export test report**. Save `gate25-test-report.json`; on iPhone use Download/Share → Files if offered.
2. Rename each file with platform, device, scene and elapsed minutes, e.g. `iphone-model-district-15min.json`. Keep the original JSON contents. Reports include user agent/viewport/DPR, raw update intervals, player/camera state and chunk diagnostics; they do not prove physical-device identity.
3. Complete `DEVICE_REPORT_ANDROID.json` or `DEVICE_REPORT_IPHONE.json`. Attach exported JSON paths plus real screenshots and screen recordings. Record memory/battery/temperature only when actually observed or measured; name the tool/conditions, otherwise leave null/unavailable.
4. Mark a check PASS or FAIL only after running it on the named physical device. Unperformed checks remain NOT TESTED. Browser update cadence and texture-size estimates are not certified display FPS or total GPU memory. Human device acceptance stays pending until evidence is reviewed.

No fixes, production expansion or Gate3 work begin automatically after a device result. Stop and return the reports for human review; explicit Gate3 authorization is still required.
