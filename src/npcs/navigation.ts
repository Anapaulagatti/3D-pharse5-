import type { NPCDefinition, Point } from "./types";
export type GroundQuery = (x: number, y: number) => boolean;
/** Reuses canonical world mask query; this is route validation, not another collision world. */
export function nativeGroundAllows(
  def: NPCDefinition,
  p: Point,
  ground: GroundQuery,
) {
  const [rx, ry] = def.footprint;
  return [-rx, -Math.round(rx / 2), 0, Math.round(rx / 2), rx].every((dx) =>
    [-ry, 0, ry].every((dy) => ground(p[0] + dx, p[1] + dy)),
  );
}
export function routeSegmentAllows(
  def: NPCDefinition,
  a: Point,
  b: Point,
  ground: GroundQuery,
) {
  const steps = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1])));
  for (let i = 0; i <= steps; i++)
    if (
      !nativeGroundAllows(
        def,
        [
          a[0] + ((b[0] - a[0]) * i) / steps,
          a[1] + ((b[1] - a[1]) * i) / steps,
        ],
        ground,
      )
    )
      return false;
  return true;
}
export function onDeclaredRoute(def: NPCDefinition, p: Point) {
  return def.route.some((a, i) => {
    const b = def.route[(i + 1) % def.route.length],
      dx = b[0] - a[0],
      dy = b[1] - a[1],
      t = Math.max(
        0,
        Math.min(
          1,
          ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy),
        ),
      );
    return Math.hypot(p[0] - a[0] - dx * t, p[1] - a[1] - dy * t) <= 1.5;
  });
}
export function clearInteractionLine(a: Point, b: Point, ground: GroundQuery) {
  const steps = Math.max(
    1,
    Math.ceil(Math.hypot(a[0] - b[0], a[1] - b[1]) / 4),
  );
  for (let i = 0; i <= steps; i++)
    if (
      !ground(
        a[0] + ((b[0] - a[0]) * i) / steps,
        a[1] + ((b[1] - a[1]) * i) / steps,
      )
    )
      return false;
  return true;
}
export function moveOnRoute(
  def: NPCDefinition,
  position: Point,
  target: Point,
  distance: number,
  ground: GroundQuery,
  occupied: (p: Point) => boolean,
) {
  let p: Point = [...position];
  const dx = target[0] - p[0],
    dy = target[1] - p[1],
    length = Math.hypot(dx, dy);
  const travel = Math.min(distance, length),
    steps = Math.max(1, Math.ceil(travel));
  let blocked = false;
  for (let i = 0; i < steps; i++) {
    const next: Point = [
      p[0] + ((dx / (length || 1)) * travel) / steps,
      p[1] + ((dy / (length || 1)) * travel) / steps,
    ];
    if (!nativeGroundAllows(def, next, ground) || occupied(next)) {
      blocked = true;
      break;
    }
    p = next;
  }
  return {
    position: p,
    distance: Math.hypot(p[0] - position[0], p[1] - position[1]),
    arrived: Math.hypot(p[0] - target[0], p[1] - target[1]) < 0.2,
    blocked,
  };
}
