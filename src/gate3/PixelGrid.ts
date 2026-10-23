/** Keep a native backing-store pixel at a whole CSS pixel origin.
 * Flex centering otherwise introduces 0.5px offsets in odd-sized windows.
 * Browser zoom / fractional devicePixelRatio remain display-device constraints.
 */
export function nativeCanvasOffset(available: number, nativeSize: number) {
  return Math.floor((available - nativeSize) / 2);
}
