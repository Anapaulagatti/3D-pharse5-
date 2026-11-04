# Exact western hanok blocker

Actor: west-hanok/house-foreground at(545,880),551×479,sortY1360. Correct path is the north/south stone lane west of this house, joining its southern east/west frontage. It is neither a palace gate, station nor Jeju bridge.

BEFORE actual keyboard trace: Juni arrives(534.0768,1390.4984), holdsW and stops(534.0768,1376.9996). Runtime anchor-mask samples report x534/y1096..1376blocked, although native source image shows stone. tools/g3wh_build.py and its historical provenance explicitly retained old collision when replacing the house painting. This stale reservation is the demonstrated cause. No camera/input/resampling root cause and no Arcade/Matter body exists in this controller.

Versioned correction opens ONLY anchor rect[520,1094,34,284]. Visible stone spans approximatelyx490..580. The existing native run-contact offsets range x−27..+24,y−4..−1; these plus3pxedge safety determine the admitted anchor span520..553. Thus the complete conservative run-foot envelope stays on stone.9622previously blocked anchors become walkable;0outsideROIchanges. Originalmaskfiles/PNGs/logicalsolids/bridgeguard unchanged. Walls x600/640,y1200 and side margins495/574remain blocked. Chunk/foreground readiness is still required.

Debug-only overlay shows real mask8pxsamples, world coordinates/camera scroll, conservative footbox, logical solid reservations and actual interactive Zones. Physics bodies: none; path uses custom swept anchor query. Actual movement never teleports or turns off collision. Same foot convention across Juni/Haneul; original sprite/stride/speed/camera code unchanged. Existing house alpha-softening remains position dependent and is not a source-art change.

Initial wider60pxanchor trial was tested then tightened before final acceptance after auditing the real run-foot envelope. The first full E2E run was deliberately interrupted16PASS/1interrupted/56notrun; it is NOT a clean full pass. Final matrix and frozen package results are recorded separately.
