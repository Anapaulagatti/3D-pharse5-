import plan from "../../assets-src/world-gate1/plan.json";
export { plan };
export function inside(x: number, y: number, r: number[], margin = 0) {
  return (
    x >= r[0] - margin &&
    y >= r[1] - margin &&
    x <= r[0] + r[2] + margin &&
    y <= r[1] + r[3] + margin
  );
}
export function walkable(x: number, y: number) {
  return (
    plan.land.some((r) => inside(x, y, r, -16)) &&
    ![...plan.buildings, ...plan.boundaries].some((b) =>
      inside(x, y, b.rect, 16),
    )
  );
}
