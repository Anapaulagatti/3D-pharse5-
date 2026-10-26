# Phase1B QA — playable review candidate

Four characters genuinely run in the accepted Phaser world. Human artistic acceptance is pending; Phase2 remains locked.

| Item | Status | Evidence / limitation |
|---|---|---|
| Four genuinely playable character packs | PASS | Original Juni144; 3 new 112-slot atlases,64 distinct gait images each. |
| Four-direction walk/run in actual Phaser | PASS | All 8 frames of all 32 character/action/direction clips observed via real input. |
| Wave / celebrate / start-stop-turn | PASS | Native clips and actual emote recording; turn clips reuse authored directional poses. |
| Selection / switching / one player / persistence | PASS | Real UI switches, saved choice, exact position and nonempty existing visited marker preserved across refresh. |
| Mobile landscape browser input/UI | PASS | Chromium844×390/DPR3 touch emulation, all4 avatars; not physical devices. |
| Both Jeju bridge routes | PASS | 16 out/return legs;8628 sampled poses,0 unsupported contacts; source-body readback exact. |
| World / Juni / collision / camera preservation | PASS | 3082world and224Juni manifest entries unchanged;6868992 paired native world pixels,0 changed. |
| Native1:1 rendering and sampling | PASS | Canvas and software-WebGL smoke;4 player station readbacks exact, nearest textures/integer native camera. |
| Unit / E2E / build / lint / assets | PASS | 50 unit tests,23 E2E tests (8 production,15 retained historical tests); all required commands pass. |
| Existing production interior transition | NOT TESTED | Canonical frozen outdoor world has no supported interior; historical V10 tests do not prove this requirement. |
| Physical Android Chrome / iPhone Safari | NOT TESTED | No recorded physical-device evidence. |
| Hardware/WebGL sustained performance | NOT TESTED | Software-rendered browser evidence is not device certification. |
| Final human character-art acceptance | NOT TESTED | Awaiting review.0final Forge FAIL;11auto-luminance leg-alternation WARNs remain documented, not relabelled PASS. |

Native world evidence uses the same browser launch flags as the accepted Phase1 capture. An initial forced software-backend comparison differed by at most1RGB level; matching launch flags restored exact0 changed pixels. No art, renderer or thresholds were changed to obtain that result.

The live driver still uses the accepted distance phase and60/100 movement speeds; original JuniMotion is byte-exact. Numerical frame uniqueness/contact/readback does not prove appealing anatomy or absence of perceived sliding: inspect actual-speed video and native sheets.

New character texture memory:3×1152×1120×4 =15,482,880decoded RGBA bytes (~14.77MiB), plus browser preview copies and original world/Juni resources. Four identity textures/previews are bounded caches, not a per-switch allocation stream. Real-device memory/performance remains unmeasured.

Current warnings are below verbatim; prior failed iterations in forge-qa/, forge-qa-final/ and forge-qa-native/ are historical diagnostics, not final PASS reports. Final reports are forge-qa-release/. No validator thresholds were weakened.

**minjun-walk-left-motion**

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "far",
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
      true
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
  "near_leading": 2,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8968
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9221
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9152
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8928
      }
    ],
    "adjacent_iou_median": 0.9015,
    "half_cycle_iou_median": 0.906
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**haneul-walk-right-motion**

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
        "iou_best_shift": 0.8808
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8736
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9052
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9108
      }
    ],
    "adjacent_iou_median": 0.8975,
    "half_cycle_iou_median": 0.893
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**minjun-walk-right-motion**

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "far",
    "far",
    "far",
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
      true
    ]
  ],
  "mode": "auto-luminance",
  "near_leading": 2,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8914
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8847
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.911
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9184
      }
    ],
    "adjacent_iou_median": 0.8959,
    "half_cycle_iou_median": 0.9012
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**haneul-run-right-motion**

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
        "iou_best_shift": 0.834
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8608
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9058
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8884
      }
    ],
    "adjacent_iou_median": 0.8358,
    "half_cycle_iou_median": 0.8746
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**bomi-walk-left-motion**

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
        "iou_best_shift": 0.8638
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.919
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.8975
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8503
      }
    ],
    "adjacent_iou_median": 0.9032,
    "half_cycle_iou_median": 0.8806
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**minjun-run-left-motion**

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "near",
    "far",
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
      true
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
  "near_leading": 4,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8671
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9118
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9187
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9078
      }
    ],
    "adjacent_iou_median": 0.8466,
    "half_cycle_iou_median": 0.9098
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**bomi-run-right-motion**

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
        "iou_best_shift": 0.8133
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8563
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.923
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8864
      }
    ],
    "adjacent_iou_median": 0.8537,
    "half_cycle_iou_median": 0.8713
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**bomi-run-left-motion**

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
        "iou_best_shift": 0.8139
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8887
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9251
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8558
      }
    ],
    "adjacent_iou_median": 0.8549,
    "half_cycle_iou_median": 0.8722
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**haneul-walk-left-motion**

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
        "iou_best_shift": 0.8853
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.9126
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9051
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.8736
      }
    ],
    "adjacent_iou_median": 0.8978,
    "half_cycle_iou_median": 0.8952
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**bomi-walk-right-motion**

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
        "iou_best_shift": 0.8633
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8501
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9027
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9188
      }
    ],
    "adjacent_iou_median": 0.9002,
    "half_cycle_iou_median": 0.883
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

**minjun-run-right-motion**

```json
{
  "id": "leg_alternation",
  "status": "warn",
  "value": [
    "far",
    "near",
    "near",
    "far",
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
      true
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
  "near_leading": 4,
  "unclear": 0,
  "half_cycle": {
    "pairs": [
      {
        "pair": [
          0,
          4
        ],
        "iou_best_shift": 0.8484
      },
      {
        "pair": [
          1,
          5
        ],
        "iou_best_shift": 0.8991
      },
      {
        "pair": [
          2,
          6
        ],
        "iou_best_shift": 0.9162
      },
      {
        "pair": [
          3,
          7
        ],
        "iou_best_shift": 0.9008
      }
    ],
    "adjacent_iou_median": 0.8438,
    "half_cycle_iou_median": 0.9
  },
  "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
}
```

Detailed evidence: [checks](checks.json), [native readback](native-pixel-qa.json), [hashes](protected-hashes.json), [gameplay](gameplay-evidence.json), [nonempty progress + refresh](progress-switch-refresh.json), [bridge summaries](bridges-summary.json), [source provenance](SOURCE_PROVENANCE.md).
