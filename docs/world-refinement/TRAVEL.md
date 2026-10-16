# Normal-speed travel measurement

Actual keyboard movement at unchanged60px/s. No Shift/run, speed multiplier, teleport within a timed trip or injected motion. Opt-in QA placement resets only each independent start. Includes acceleration, turning and resolved collisions; same control algorithm and equivalent destination functions, changed streets documented in compact-layout.json. Raw per-frame position samples retained in quality/travel-before.json and travel-after.json.

| Trip | Before s / distance px | After s / distance px | Time change |
|---|---:|---:|---:|
| Gate → Academy front | 34.54 / 2054 | 20.08 / 1191 | -41.9% |
| Academy front → Workshop | 47.11 / 2812 | 22.81 / 1354 | -51.6% |
| Workshop → Museum | 9.91 / 581 | 11.46 / 673 | +15.7% |

Three representative trips total 91.56→54.35s (40.6%less). Not every leg is shorter: workshop→museum gains a purposeful landscaped frontage route and is about1.55s longer. This is disclosed rather than hiding it with faster player movement.

Actual previous playable baseline4096×1728, candidate2304×1920:37.5%less area, same native artwork/Juni dimensions. Original4096×3072plan is retained as reference, not falsely described as the old fully playable world. Palace/academy/workshop/museum whole compound translations preserve internal relationships. Formal avenue x1152remains straight; garden/book/service paths bend around real walls and masses. Every planned public path is checked at centre and shoulders, every8px, with the actual8×4ellipse foot samples against all authored colliders (2931positions PASS). Forge independently checks every anchor/approach and reciprocal room links.
