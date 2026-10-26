import { z } from "zod";
import { containsPoint, type Manifest } from "../gate3/types";
const key = "korean-arena-world-session-v1";
const schema = z.object({
  version: z.literal(1),
  scope: z.string(),
  scene: z.string(),
  x: z.number().finite(),
  y: z.number().finite(),
  visited: z.array(z.string()).max(1000),
});
type Snapshot = z.infer<typeof schema>;
export function browserSessionCheckpointStorage(): Storage | undefined {
  try {
    return window.sessionStorage;
  } catch {
    return undefined;
  }
}
/** Per-tab reload continuity for existing position/visited markers only.
 * Separate from character preferences; no new progression or account system. */
export class WorldSessionCheckpoint {
  constructor(
    private storage: Pick<Storage, "getItem" | "setItem"> | undefined,
    private scope: string,
    private world: Manifest,
  ) {}
  read(): Snapshot | null {
    try {
      const value = schema.parse(
        JSON.parse(this.storage?.getItem(key) ?? "null"),
      );
      if (
        value.scope !== this.scope ||
        value.scene !== this.world.id ||
        value.x < 0 ||
        value.y < 0 ||
        value.x >= this.world.size[0] ||
        value.y >= this.world.size[1] ||
        this.world.logicalSolids?.some((s) =>
          containsPoint(value.x, value.y, s.rect),
        )
      )
        return null;
      const known = new Set(this.world.targets.map((t) => t.id));
      return { ...value, visited: value.visited.filter((id) => known.has(id)) };
    } catch {
      return null;
    }
  }
  save(x: number, y: number, visited: Iterable<string>) {
    try {
      this.storage?.setItem(
        key,
        JSON.stringify({
          version: 1,
          scope: this.scope,
          scene: this.world.id,
          x,
          y,
          visited: [...visited],
        }),
      );
    } catch {
      /* Denied/quota storage never interrupts play. */
    }
  }
}
/** Verify a saved point against the unchanged shipped mask before restoring it. */
export async function checkpointGroundIsWalkable(
  world: Manifest,
  x: number,
  y: number,
  base: string,
) {
  x = Math.round(x);
  y = Math.round(y);
  const c = world.chunks.find(
    (c) => x >= c.x && y >= c.y && x < c.x + c.width && y < c.y + c.height,
  );
  if (!c) return false;
  try {
    const response = await fetch(base + c.mask, {
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) return false;
    const mask = new Uint8Array(await response.arrayBuffer());
    return (
      mask.length === c.width * c.height &&
      mask[(y - c.y) * c.width + x - c.x] > 127
    );
  } catch {
    return false;
  }
}
