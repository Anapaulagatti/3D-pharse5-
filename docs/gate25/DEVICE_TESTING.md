# Physical mobile validation — NOT TESTED

No connected Android/iPhone or device-control connector is exposed to this cloud environment. `adb` is absent and `/dev/bus/usb` is absent. Chromium touch emulation is the automated environment; it is not Android Chrome or iPhone Safari. No physical model/OS/FPS/temperature/battery results are invented.

## Reproducible handoff

1. Download/extract `GATE25_PLAYABLE.zip` on a computer on the same trusted Wi-Fi as the phone. Python3 is the only server prerequisite. Run `python3 start.py --lan`. This binds to the local network for your private test; there is no public hosting or deployment. Stop with Ctrl-C when finished.
2. Find that computer's LAN IP, allow its Python server through the local firewall if needed, and open `http://COMPUTER_LAN_IP:8065/3D-pharse5-/gate2-review.html?scene=c` on the phone. Do not use `127.0.0.1` on the phone: it would refer to the phone itself. The game needs no native app or account. HTTP suffices for these Canvas/pointer features; a browser's download behavior may differ.
3. Rotate to landscape. Test at least one real Android/Chrome and one real iPhone/Safari. Record exact device model, OS build, browser version, CSS viewport, DPR, screen resolution, browser bars/orientation-lock state and reduced-motion setting. Avoid claiming equivalence from user-agent strings alone.
4. Open Options(···) → **Export test report** before and after each scene's session. It downloads JSON with user agent/screen/DPR, player/camera state, raw update cadence, texture inventory and chunk request/ready timings. If iOS offers a share/download sheet, save it to Files. Also record external observations and screenshots/video in the form below.

## Short session — 3–5 minutes per device

| Check | Procedure | PASS/FAIL/NOT TESTED + evidence |
| --- | --- | --- |
| Native movement/run | Jeju: joystick in all directions, hold Run with second finger, release both; Juni stops correctly, no accidental tour | NOT TESTED |
| Scenic controls | Scenic → one-finger drag, two-finger pinch at25/33/50/100%; boundaries stay inside source; joystick does not drag camera | NOT TESTED |
| Full overview | Full scene includes entire Jeju, Juni, landmarks and previous viewport; scale labelled; Return restores1:1 without teleport | NOT TESTED |
| Tour | Scenic → Start Tour; coast→oreum→orchard→house at50%; meaningful detail/composition; smooth motion/pauses | NOT TESTED |
| Pause / manual / Resume | Pause mid-tour, drag/pinch, Resume; no camera fight; paused view stays still | NOT TESTED |
| Skip / Exit / movement cancel | Skip advances; Return restores native view; joystick/keyboard intent safely exits auto control, then movement works | NOT TESTED |
| Reduced motion | Enable OS reduced motion, reload. Tour uses static selection; Skip changes frame immediately; no auto-pan | NOT TESTED |
| Landscape/safe areas | Test landscape left/right with browser chrome visible and collapsed. Joystick, Run, Scenic, captions and Return fit; no critical overlap | NOT TESTED |
| Readability | Juni and entrances clear at1×;50% tour landmarks attractive; overview is orientation only, small text need not remain readable | NOT TESTED |
| District | Select Gate2.5 district. Walk from Muneum across bakery to station doorway and back. Watch both joins, Y-sort, sidewalk contact, prefetch and no flicker | NOT TESTED |
| Jeju working plan | Select Gate2.5 approved Jeju expansion. Cross technical connector to native bridge, approach both landing paths; sea is blocked, no ferry/teleport | NOT TESTED |

## Long session — at least 15 minutes per device

Use the district and Jeju in separate sessions. Repeatedly walk/run both joins; switch Follow→Scenic→Overview→Tour→Return at least20times; include pause/resume, browser background/foreground and landscape reversal. Export separate reports after5and15minutes. Note any blank chunks, image loss, browser reload, touch lag, scroll escape, camera stutter or crashes. Note battery percentage before/after only if accessible and test conditions known. Record warmth subjectively; do not invent a temperature. Use OS/native tools if actual temperature or memory is accessible and state the tool.

Session interval histogram is per scene/document; changing scenes reloads the document and starts fresh. It measures raw browser update cadence with0.5ms bins, not actual display presentation FPS. Samples from hidden frames are excluded; the first foreground interval can still contain suspension time and must be identified as such. JS heap is Chromium-only when exposed; texture RGBA-equivalent is a dimension estimate, not total resident browser/GPU memory. Long-session diagnostics must not be presented as thermal/FPS certification.

## Result form — fill one per real device

- Tester/date/location and physical device/model:
- OS/browser/version:
- CSS viewport/DPR/screen/browser-bar/safe-area conditions:
- Duration/route/repeated-mode count:
- Exported JSONs and screenshots/recording:
- Mean/p95/p99 raw update interval, spikes; any independently measured average/low FPS and tool:
- Chunk request→ready times, visible stalls or reloads:
- Measured memory (tool, or unavailable), battery change (conditions, or unavailable), thermal observation:
- Control, composition and readability PASS/FAIL, exact localized fixes:
- Mobile UX decision by human tester: can move, recognize architecture, enjoy tour, orient with Overview, return clearly and explore district comfortably?

**Physical acceptance is NOT TESTED until these real-device reports exist. Gate3 remains locked.**
