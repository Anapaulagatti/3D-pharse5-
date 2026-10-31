/** Versioned collision-only amendments. Native artwork, protected logical solids and old masks stay immutable.
 * Four visible doorstep floors were rejected by legacy 14px image-padding reservations.
 * These small entrance lanes stop 3px outside their protected building footprint.
 */
export const entranceRepairs = [
  { id: "cafe-visible-doorstep", rect: [700, 2593, 35, 12] },
  { id: "bookshop-visible-doorstep", rect: [1112, 2593, 33, 12] },
  { id: "learning-visible-doorstep", rect: [1402, 2593, 33, 12] },
  { id: "maru-glass-doorstep", rect: [310, 3333, 33, 11] },
] as const;
export function repairedEntrance(x: number, y: number) {
  return entranceRepairs.some(
    ({ rect: [rx, ry, w, h] }) =>
      x >= rx && y >= ry && x < rx + w && y < ry + h,
  );
}
