# Phase2A execution record

The authorized production pass is complete as a review candidate. See [QA](QA.md), [visual review](REVIEW.html), [provenance](source-provenance.json) and [architecture](ARCHITECTURE.md).

Approval freeze committed first at b86ae0f. Ara was completed, inspected and tested in actual Phaser before Doyun production; ara-first-validation.json and ara-pilot-gameplay.json preserve that order.

The initial152-pixel hair/raised-sleeve composition failure is preserved under history/composition-before-occlusion. Four sparse pair-ownership corrections resolved it; all4,032 supported pose combinations now match direct source construction.

A first media recording omitted some gait phases because interval sampling missed render frames under headless load. Only the read-only evidence recorder changed to render-synchronized observation and waits for each actual frame. Animation and speeds did not change. Partial evidence is retained under history/recording-attempt1; final actual-gameplay.json has complete coverage.

Full unit/E2E checks passed. A later landscape preview resize fix passed the targeted orientation regression. Missing-asset fallback, storage migration, world-state retention and bounded caches are covered. Native/technical success is not human artistic acceptance. Six new automatic motion warnings and device/hardware limitations remain documented.

STOP after the consolidated review package; Phase2B, main merge and public deployment remain forbidden.
