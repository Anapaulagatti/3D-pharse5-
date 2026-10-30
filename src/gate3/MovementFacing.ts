import type { Direction } from "../characters/types";

/** Keep the current cardinal view on a diagonal tie. Adding a second key must
 * not restart a turn animation; a blocked axis must not determine facing. */
export function movementFacing(
  dx: number,
  dy: number,
  previous: Direction,
): Direction {
  const ax = Math.abs(dx),
    ay = Math.abs(dy);
  if (Math.max(ax, ay) < 0.000001) return previous;
  const horizontal: Direction = dx > 0 ? "right" : "left";
  const vertical: Direction = dy > 0 ? "front" : "back";
  if (Math.abs(ax - ay) < 0.000001) {
    if (previous === horizontal || previous === vertical) return previous;
    return vertical;
  }
  return ax > ay ? horizontal : vertical;
}
