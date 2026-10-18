# Landscape mobile review

The new living-korea-review entry uses a full-viewport landscape Phaser canvas below a translucent safe-area-aware HUD. Native pixel rendering caps high-DPI cost; artwork proportions are preserved. Existing desktop and older review entries are unchanged.

Portrait shows an explicit rotate-device screen and pauses physics/input. Rotation resumes only orientation-induced pause; manual pause survives. A user-gesture button requests fullscreen and landscape lock when available. Unsupported/rejected requests leave clear manual-rotation instructions. No iOS Safari lock support is assumed.

Left D-pad, right hold-run/explore/wave/celebrate use captured multi-pointer input, with56/68pxcontrols. Real CDP simultaneous direction/run and partial release are checked. Dialogues scroll, Korean/Vietnamese text remains visible, minimap and prompts adapt. DOM controls cannot fall through into world clicks.

Actual Chromium emulation:568x320,640x360,844x390,932x430, DPR3cost cap, simulated safe-area variables, portrait↔landscape, reduced-motion/manual pause, dialogue and unsupported-orientation mock. Whole-browser screenshot files distinguish HUD from native canvas images. These are not physical Android/iOS or real Safari tests. Touchscreen hardware, browser chrome, notches and thermal performance still need device review.

To review on a phone on the same network, extract the ZIP and explicitly run `python3 start.py --lan`; open the printed path using the computer LAN IP. This binds your local review server only when requested. Plain LAN HTTP may not support orientation/fullscreen APIs; manual rotation still works. Default launcher binds127.0.0.1. For slow software-GPU rendering use `--canvas`, or choose the Canvas fallback in settings. No automatic public hosting is performed.
