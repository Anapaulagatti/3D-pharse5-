# Accepted Gate2.5 prototype — real-device handoff only

**Human artistic approval recorded.** The approval covers the current district prototype refinement only. **Android Chrome: NOT TESTED. iPhone Safari: NOT TESTED. Gate3: LOCKED.**

[User approval](../current/GATE25_REFINEMENT_APPROVAL.md) · [Recoverable checkpoint](https://github.com/Anapaulagatti/3D-pharse5-/tree/checkpoint/gate25-refinement-approved-20261022) · [Checkpoint metadata](checkpoint.json).

- Approved commit: `868aa60acce297253c555f994ecac60276a830b3`.
- Annotated tag: `checkpoint/gate25-refinement-approved-20261022`.
- [Original approved ZIP](../gate25-refinement/GATE25_COMPOSITION_PLAYABLE.zip) is unchanged and recoverable at that checkpoint.
- [Accepted native image](../gate25-refinement/AFTER_NATIVE_1X.png) and [prototype review evidence](../gate25-refinement/README.md) are retained. Earlier approval-pending reports describe the capture-time state; the new user approval supersedes that status only for this prototype's artistic refinement.

## Handoff

**[Download the device-review ZIP](GATE25_DEVICE_REVIEW.zip)**. It is prepared from the approved existing archive, with byte-identical game files. Only handoff documentation, approval/checkpoint metadata, report templates and the package manifest differ. No rebuild, new artwork or runtime modification.

Extract and run `python3 start.py --lan`. On the same trusted Wi-Fi, open:

`http://COMPUTER_LAN_IP:8065/3D-pharse5-/gate2-review.html?scene=district-refinement`

Use your computer's LAN IP. Test with real Android Chrome and real iPhone Safari, landscape in both orientations. Start with the district; the existing Jeju tour remains available as scene `c`. The frozen build's historical picker labels are unchanged.

Follow the [device checklist and export workflow](DEVICE_CHECKLIST.md). Use **Options(···) → Export test report**, save JSON before switching scenes, attach actual device model/OS/browser and real screen recordings. Fill [Android report](DEVICE_REPORT_ANDROID.json) and [iPhone report](DEVICE_REPORT_IPHONE.json); all checks start NOT TESTED.

[ZIP integrity and runtime equivalence](package.json) · [Packaging/export smoke test](handoff-qa.json) · [Published downloads and remote checkpoint verification](published-verification.json). Automated desktop checks are packaging checks, not physical-device acceptance.

## Recovery

Create an isolated checkout without disturbing current work:

```sh
git fetch origin tag checkpoint/gate25-refinement-approved-20261022
git worktree add --detach ../gate25-approved checkpoint/gate25-refinement-approved-20261022
```

The checkpoint pins source, artwork, coordinates, native captures, original package and prior QA. [Original package hash](checkpoint.json) and runtime manifest hashes allow exact comparison.

**STOP after handoff. No Gate3, full-world production, merge to main, deployment or large-scale expansion. Wait for explicit Gate3 authorization.**
