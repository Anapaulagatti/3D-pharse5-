/** Optional local ground-contact guard, derived from Juni's original atlas.
 * Sprite silhouette is vertical artwork; it is not a49x17 rectangle on the floor.
 * Raised animation feet project onto the unchanged native ground anchor.
 */
export interface ContactSpec {
  physical: string;
  rect: [number, number, number, number];
  footprints: Record<string, [number, number][]>;
}
export class NativeContact {
  constructor(
    readonly spec: ContactSpec,
    readonly pixels: Uint8Array,
  ) {
    if (pixels.length !== spec.rect[2] * spec.rect[3])
      throw Error("Contact field size mismatch");
  }
  allows(x: number, y: number, action: string, facing: string): boolean {
    const [ox, oy, w, h] = this.spec.rect;
    const cx = Math.round(x),
      cy = Math.round(y);
    if (cx < ox || cy < oy || cx >= ox + w || cy >= oy + h) return true;
    const offsets = this.spec.footprints[`${action}-${facing}`];
    if (!offsets) throw Error("Missing native contact footprint");
    return offsets.every(([dx, dy]) => {
      const px = cx + dx - ox,
        py = cy + dy - oy;
      return (
        px < 0 || py < 0 || px >= w || py >= h || this.pixels[py * w + px] > 0
      );
    });
  }
}
export async function loadNativeContact(
  spec: ContactSpec | undefined,
  base: string,
) {
  if (!spec) return null;
  const response = await fetch(base + spec.physical);
  if (!response.ok) throw Error("Missing native contact field");
  return new NativeContact(spec, new Uint8Array(await response.arrayBuffer()));
}
