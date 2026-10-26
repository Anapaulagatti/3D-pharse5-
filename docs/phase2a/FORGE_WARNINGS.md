# Retained automatic motion warnings

No thresholds were weakened.24 Forge commands completed with0hard failures. The following6 leaf warnings remain verbatim. The near/far luminance heuristic is ambiguous at passing/overlapping loose-trouser poses; explicit opposite-foot keys and actual playback are supplied for human review. They are not relabelled numerical PASS. The11 older Phase1B warnings also remain unchanged in the historical approved review.

`docs/phase2a/forge-qa/ara-walk-left-motion/sheet-qc.json`

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
        "iou_best_shift": 0.8704
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9041
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9017
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8652
      }
    ],
    "adjacent_iou_median": 0.8954,
    "half_cycle_iou_median": 0.8861
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2a/forge-qa/doyun-walk-right-motion/sheet-qc.json`

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "far",
    "near",
    "near",
    "near",
    "near",
    "near",
    "far"
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
        "iou_best_shift": 0.8975
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8826
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9108
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9234
      }
    ],
    "adjacent_iou_median": 0.9036,
    "half_cycle_iou_median": 0.9042
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2a/forge-qa/doyun-walk-left-motion/sheet-qc.json`

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
        "iou_best_shift": 0.9006
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9287
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9137
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8821
      }
    ],
    "adjacent_iou_median": 0.9037,
    "half_cycle_iou_median": 0.9071
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2a/forge-qa/doyun-run-left-motion/sheet-qc.json`

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
        "iou_best_shift": 0.86
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9095
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.915
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8844
      }
    ],
    "adjacent_iou_median": 0.8471,
    "half_cycle_iou_median": 0.8969
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2a/forge-qa/ara-run-right-motion/sheet-qc.json`

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "far",
    "near",
    "near",
    "near",
    "near",
    "near",
    "far"
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
        "iou_best_shift": 0.8203
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8448
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9007
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8744
      }
    ],
    "adjacent_iou_median": 0.8266,
    "half_cycle_iou_median": 0.8596
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2a/forge-qa/ara-walk-right-motion/sheet-qc.json`

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "far",
    "near",
    "near",
    "near",
    "near",
    "near",
    "far"
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
        "iou_best_shift": 0.8655
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8682
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9013
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8979
      }
    ],
    "adjacent_iou_median": 0.8925,
    "half_cycle_iou_median": 0.8831
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

