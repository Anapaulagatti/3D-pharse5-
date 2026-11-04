export type GroundAllows = (x: number, y: number) => boolean;
/** Subpixel simulation, <=1px swept samples, native integer rendering stays in main.
 * A <=4px corner assist only engages when the requested forward lane is clear beyond
 * a small protrusion. It cannot cross a wall, teleport, increase speed or alter facing. */
export function moveReviewPlayer(
  x: number,
  y: number,
  dx: number,
  dy: number,
  distance: number,
  allows: GroundAllows,
) {
  let assisted = false;
  const steps = Math.max(1, Math.ceil(distance)),
    step = distance / steps;
  for (let i = 0; i < steps; i++) {
    const ox = x,
      oy = y;
    if (allows(x + dx * step, y)) x += dx * step;
    if (allows(x, y + dy * step)) y += dy * step;
    if (
      Math.hypot(x - ox, y - oy) > 0.001 ||
      Math.abs(dx) + Math.abs(dy) < 0.01
    )
      continue;
    // Cardinal-only assistance: diagonal input already slides along the permitted axis.
    if (Math.abs(dx) > 0.05 && Math.abs(dy) > 0.05) continue;
    const fx = Math.sign(dx),
      fy = Math.sign(dy),
      px = -fy,
      py = fx;
    let chosen = 0;
    for (let offset = 1; offset <= 4 && !chosen; offset++)
      for (const sign of [-1, 1]) {
        const tx = x + px * offset * sign,
          ty = y + py * offset * sign;
        if (![0, 1, 2, 3].every((n) => allows(tx + fx * n, ty + fy * n)))
          continue;
        if (
          !Array.from({ length: offset }, (_, n) => n + 1).every((n) =>
            allows(x + px * n * sign, y + py * n * sign),
          )
        )
          continue;
        chosen = sign;
        break;
      }
    const assistStep = step * Math.min(1, Math.hypot(dx, dy));
    if (
      chosen &&
      allows(x + px * assistStep * chosen, y + py * assistStep * chosen)
    ) {
      assisted = true;
      x += px * assistStep * chosen;
      y += py * assistStep * chosen;
    }
  }
  return { x, y, assisted };
}
