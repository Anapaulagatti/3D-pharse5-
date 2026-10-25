# Hanbit Station — full clean rebuild / human review

[BEFORE / CLEAN / AFTER gallery](VISUAL_REVIEW.md) · [Complete gallery and video](VISUAL_REVIEW.html) · [Playable ZIP](HANBIT_CLEAN_REBUILD_REVIEW.zip) · [QA](QA.md) · [Purge and scope audit](purge-and-scope.json).

**The active review world now uses the entirely new station.** The old station is not kept active or patched underneath it. This human override supersedes previous station-art preservation decisions. Historical source files/checkpoints remain recoverable; none is a station-art donor.

## Purge completed before new construction

Six legacy renderer objects are removed: facade, both corrected old planter sprites, old canopy, old canopy terminal and old potted tree. Every pixel of station-owned ground in2274,2140,684,673 and the right tree-remnant extension2958,2490,38,208 is freshly authored, including paving, old prop shadows and road-edge texture. The retired canopy terminal beyond the lot is removed; its correct neighboring platform remains.

The [actual Phaser clean-site screenshot](station-all-clean-native.png) was captured before authoring the fresh station. It shows a finished neutral paved plot without the old station silhouette, roof, facade, upper floor, sign, props or shadows. A flat technical purge guide was only an authoring input; it is never the final game ground.

## Fresh construction

The new design has an ivory masonry facade, slate-blue hipped roof, central clock pediment, three arched public/ticket-hall bays, warm interior depth and newly painted 한빛역 signage. It was painted directly for the cleaned map using ONLY that clean site, abstract planning solids and the approved non-station Muneum Gate1 reference. No old station, prior copper-roof candidate, old roof mask, old windows, sign, planters or canonical floor supplied its artwork.

One fresh painting supplies the roof, upper architecture and facade at the same native origin. Contact shadows come only from that painting. Original-scale pixels are selected through new masks; no artwork is stretched or resampled. The first fresh design exceeded the parcel and is retained as REJECTED/NOT INSTALLED. The final native-fit source is not a shrunk version of that image.

## Planning and gameplay

World location, district reservation, original continuous logical core2322.5,2380,555,210 and entrance2598.5,2610 remain unchanged. The native painted masonry returns receive explicit local support rectangles2294,2380,29,210 and2878,2380,24,210 inside the same approved district; no route is moved. The eastern public passage remains56px wide beside these returns.

Legacy source/planter collision ownership is removed on the visible fresh paved parcel. The formerly closed8px strip is now real connected pavement: actual original controls cross onto the platform and return. One continuous four-leg recording verifies entrance, the declared platform1 target2970,2530 (including original E inspection), side passage and road crossing, with no teleport/collision/clock/speed override. Sampled native foot contacts and Juni readback have no failures.

All non-station world objects and all pixels outside the explicit station masks remain exact, including the farm, western house/garden, Muneum/retail, Namsan, Jeju, tracks, shore and amusement artwork. No old station texture is requested by the default live scene. The default review entry now selects the fresh world; old BEFORE art appears only in explicitly labelled historical evidence.

## Review and remaining limits

Human artistic approval is pending. Technical absence/source readback is not artistic approval. The protected attraction projection and tower/retail questions remain; five inherited Jeju route centerlines, full bridge stop/turn clearance and required unplaced Bakery are still open. W0 remains rejected, Q1 land unallocated. No unrelated region was rebuilt. Physical Android/iPhone and hardware WebGL performance remain NOT TESTED.

Extract ZIP, run `python3 start_review.py`, open the private localhost URL. The active fresh world and clean-site proof are the only packaged scene choices; no playable old-station scene is included. Original WASD/arrows/Shift, mobile joystick, Scenic/Tour/Return and test-report export remain. [Physical-device checklist](DEVICE_REVIEW.md).

**STOP for consolidated human visual review.** No main merge, public deployment, separate Korean Arena application change or new paid external image API.
