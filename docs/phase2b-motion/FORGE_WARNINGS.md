# Original Forge diagnostics retained

72 fresh commands run against all six identities (front/back/left/right walk/run and side-motion checks). Original thresholds unchanged. 17 leaf WARNs; 0 hard FAILs. Palette/outline gates without supplied inputs remain SKIPPED, not PASS.

The original18 Phase2B WARNs remain in [historical report](../phase2b/forge-warnings.json). Earlier claims that eight unique poses proved artistic quality are withdrawn. Numeric contact evidence and human motion review are separate gates.

## docs/phase2b-motion/forge-qa/hyunwoo-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

## docs/phase2b-motion/forge-qa/hyunwoo-walk-right-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "near",
    "far",
    "far",
    "far",
    "near",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 5,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8254
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.853
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8997
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8414
      }
    ],
    "adjacent_iou_median": 0.8045,
    "half_cycle_iou_median": 0.8472
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/jiwon-run-left-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "near",
    "near",
    "far",
    "far",
    "far",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      false
    ],
    [
      3,
      7,
      true
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 5,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8227
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8588
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8946
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.869
      }
    ],
    "adjacent_iou_median": 0.8168,
    "half_cycle_iou_median": 0.8639
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/jiwon-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

## docs/phase2b-motion/forge-qa/jiwon-walk-right-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "near",
    "far",
    "far",
    "far",
    "near",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 5,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8237
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8399
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8889
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8312
      }
    ],
    "adjacent_iou_median": 0.7973,
    "half_cycle_iou_median": 0.8356
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/nari-run-left-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "far",
    "far",
    "far",
    "far",
    "far",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 3,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8322
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8747
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8988
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8738
      }
    ],
    "adjacent_iou_median": 0.8285,
    "half_cycle_iou_median": 0.8742
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/nari-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

## docs/phase2b-motion/forge-qa/nari-walk-left-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "far",
    "far",
    "far",
    "far",
    "far",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 3,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8817
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9027
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8997
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8802
      }
    ],
    "adjacent_iou_median": 0.8974,
    "half_cycle_iou_median": 0.8907
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/nari-walk-left-motion/sheet-qc.json

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.52,
  "threshold": 1.5,
  "transitions": [
    [
      7,
      0
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

## docs/phase2b-motion/forge-qa/nari-walk-right-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "far",
    "far",
    "far",
    "far",
    "far",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 3,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8154
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8376
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8941
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8288
      }
    ],
    "adjacent_iou_median": 0.8076,
    "half_cycle_iou_median": 0.8332
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/sori-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

## docs/phase2b-motion/forge-qa/sori-walk-left-motion/sheet-qc.json

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.64,
  "threshold": 1.5,
  "transitions": [
    [
      7,
      0
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

## docs/phase2b-motion/forge-qa/sori-walk-right-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "near",
    "far",
    "far",
    "far",
    "near",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 5,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.7163
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.7521
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8709
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.7231
      }
    ],
    "adjacent_iou_median": 0.7808,
    "half_cycle_iou_median": 0.7376
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/taeyang-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

## docs/phase2b-motion/forge-qa/taeyang-walk-left-motion/sheet-qc.json

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "near",
    "near",
    "far",
    "far",
    "far",
    "near",
    "near"
  ],
  "threshold": "lead differs between i and i+n/2",
  "verdict": "mixed: some half-cycle pairs repeat the lead",
  "pairs": [
    [
      0,
      4,
      false
    ],
    [
      1,
      5,
      false
    ],
    [
      2,
      6,
      true
    ],
    [
      3,
      7,
      false
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 5,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8613
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8914
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8977
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8558
      }
    ],
    "adjacent_iou_median": 0.8881,
    "half_cycle_iou_median": 0.8763
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

## docs/phase2b-motion/forge-qa/taeyang-walk-left-motion/sheet-qc.json

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.54,
  "threshold": 1.5,
  "transitions": [
    [
      7,
      0
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

## docs/phase2b-motion/forge-qa/yuna-run-right-motion/sheet-qc.json

```json
{
  "id": "phase_coverage",
  "status": "warn",
  "value": [
    [
      "contact",
      "contact",
      "narrow",
      "mid"
    ],
    [
      "contact",
      "mid",
      "narrow",
      "contact"
    ]
  ],
  "threshold": null,
  "problems": [
    "half 0 has no flight frame",
    "half 1 has no flight frame"
  ],
  "note": "labels from ground clearance and stride width; they cannot judge the pose itself"
}
```

