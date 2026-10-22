export type Rect = [number, number, number, number];
export type Chunk = {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  image: string;
  mask: string;
  bytes: number;
};
export type Foreground = {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  image: string;
  sortY: number;
  alphaSoftening: number;
  bytes: number;
};
export type Target = { id: string; x: number; y: number; label: string };
export type Manifest = {
  id: string;
  size: number[];
  spawn: number[];
  targets: Target[];
  stops: import("../gate2/TourStops").TourStop[];
  chunks: Chunk[];
  objects: Foreground[];
  overview: string;
  budgetBytes: number;
  maxConcurrent: number;
};
export function intersects(a: Rect, b: Rect) {
  return (
    a[0] < b[0] + b[2] &&
    a[0] + a[2] > b[0] &&
    a[1] < b[1] + b[3] &&
    a[1] + a[3] > b[1]
  );
}
export const bounds = (r: {
  x: number;
  y: number;
  width: number;
  height: number;
}): Rect => [r.x, r.y, r.width, r.height];
