/** Explicit candidate anchor policy; protected logical coordinates remain continuous. */
export function rasterOrigin(
  anchor: [number, number],
  sourcePivot: [number, number],
): [number, number] {
  const result: [number, number] = [
    anchor[0] - sourcePivot[0],
    anchor[1] - sourcePivot[1],
  ];
  if (!result.every(Number.isInteger))
    throw Error(
      "Fractional raster origin: declare an explicit source pivot; never round the protected anchor",
    );
  return result;
}
export function pixelCenter(
  origin: [number, number],
  column: number,
  row: number,
): [number, number] {
  return [origin[0] + column + 0.5, origin[1] + row + 0.5];
}
