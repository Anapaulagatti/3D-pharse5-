# Forge numerical warnings — retained

72 commands completed with0hard failures. The new packs retain18 leaf WARNs: {'seam': 7, 'leg_alternation': 11}. Earlier11 Phase1B and6 Phase2A warnings remain in their immutable approved reviews.

All eight actual gait poses were observed in Phaser for every direction/action. Native bounds/alpha and source-reference readbacks pass. Internal review investigated these flags against the native sheets, actual gameplay and registered foot targets. Auto-luminance near/far classification is ambiguous for overlapping loose garments and passing poses; source foot targets oppose exactly at contact phases. Seam ratios also weight the large head/garment area moving by1 walk pixel or2 run pixels and near/far leg shading. Geometry is periodic; closure has no additional pose beyond the regular next contact. These observations do not erase numerical WARN or grant human art acceptance. Loop feel remains an explicit human review item.

Palette-specific/outline-specific Forge gates were SKIPPED because no palette or outline color was supplied. The separate native finisher enforces shared96-color source palette and binary alpha; far-layer shading adds derived colors. Do not claim the skipped Forge tests passed.

`docs/phase2b/forge-qa/hyunwoo-walk-right-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.51,
  "threshold": 1.5,
  "transitions": [
    [
      4,
      5
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

`docs/phase2b/forge-qa/jiwon-run-left-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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

`docs/phase2b/forge-qa/jiwon-run-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "near",
    "near",
    "near",
    "near",
    "near",
    "unclear",
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
  "unclear": 1,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8215
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8666
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8953
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8572
      }
    ],
    "adjacent_iou_median": 0.8115,
    "half_cycle_iou_median": 0.8619
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/jiwon-walk-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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
        "iou_best_shift": 0.8781
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.879
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.898
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8905
      }
    ],
    "adjacent_iou_median": 0.8883,
    "half_cycle_iou_median": 0.8847
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/nari-run-left-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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

`docs/phase2b/forge-qa/nari-walk-left-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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

`docs/phase2b/forge-qa/nari-walk-left-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

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

`docs/phase2b/forge-qa/nari-walk-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "far",
    "far",
    "near",
    "near",
    "near",
    "far",
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
  "near_leading": 3,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8826
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.883
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
        "iou_best_shift": 0.9054
      }
    ],
    "adjacent_iou_median": 0.9008,
    "half_cycle_iou_median": 0.8923
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/nari-walk-right-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.54,
  "threshold": 1.5,
  "transitions": [
    [
      4,
      5
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

`docs/phase2b/forge-qa/sori-run-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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
        "iou_best_shift": 0.7918
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8085
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
        "iou_best_shift": 0.83
      }
    ],
    "adjacent_iou_median": 0.8147,
    "half_cycle_iou_median": 0.8193
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/sori-walk-left-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

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

`docs/phase2b/forge-qa/sori-walk-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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
        "iou_best_shift": 0.8246
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8433
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8983
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.874
      }
    ],
    "adjacent_iou_median": 0.873,
    "half_cycle_iou_median": 0.8587
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/sori-walk-right-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.66,
  "threshold": 1.5,
  "transitions": [
    [
      4,
      5
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

`docs/phase2b/forge-qa/taeyang-walk-left-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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

`docs/phase2b/forge-qa/taeyang-walk-left-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

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

`docs/phase2b/forge-qa/taeyang-walk-right-motion/sheet-qc.json`

Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.

```json
{
  "id": "seam",
  "status": "warn",
  "value": 1.62,
  "threshold": 1.5,
  "transitions": [
    [
      4,
      5
    ]
  ],
  "note": "largest frame-to-frame change over the median step; review these joins first"
}
```

`docs/phase2b/forge-qa/yuna-run-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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
        "iou_best_shift": 0.808
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8689
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8973
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8664
      }
    ],
    "adjacent_iou_median": 0.8152,
    "half_cycle_iou_median": 0.8677
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

`docs/phase2b/forge-qa/yuna-walk-right-motion/sheet-qc.json`

Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.

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
        "iou_best_shift": 0.8685
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.87
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.907
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9005
      }
    ],
    "adjacent_iou_median": 0.8893,
    "half_cycle_iou_median": 0.8852
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```
