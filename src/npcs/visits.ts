import { npcRegistry } from "./registry";
import { modernVisitors } from "./catalog";
import type { ModernVisitorMetadata } from "./collections";
/** Stable90s windows include a quiet resident window; no random/preloaded crowd. */
export function visitorForWindow(
  zone: string,
  elapsedMs: number,
  visitors: readonly ModernVisitorMetadata[] = modernVisitors,
) {
  const options = visitors
    .filter((v) => v.homeZone === zone)
    .sort((a, b) => a.id.localeCompare(b.id));
  const slot =
    Math.floor(Math.max(0, elapsedMs) / 90_000) % (options.length + 1);
  return slot === 0 ? undefined : options[slot - 1];
}
export class NPCVisitPolicy {
  private entries = new Map<string, ModernVisitorMetadata | undefined>();
  private epoch = Date.now();
  static readonly key = "korean-arena-npc-visits-v1";
  constructor(storage?: Pick<Storage, "getItem" | "setItem">) {
    try {
      const saved: unknown = JSON.parse(
        storage?.getItem(NPCVisitPolicy.key) ?? "null",
      );
      if (
        saved &&
        typeof saved === "object" &&
        "version" in saved &&
        saved.version === 1 &&
        "epochMs" in saved &&
        typeof saved.epochMs === "number" &&
        Number.isFinite(saved.epochMs) &&
        saved.epochMs > 0 &&
        saved.epochMs <= Date.now()
      )
        this.epoch = saved.epochMs;
      storage?.setItem(
        NPCVisitPolicy.key,
        JSON.stringify({ version: 1, epochMs: this.epoch }),
      );
    } catch {
      /* Optional, NPC-only persistence. Never access player progress storage. */
    }
  }
  eligible(
    activeZones: ReadonlySet<string>,
    pinned?: string,
    review?: string,
    now = Date.now(),
  ) {
    const residents = new Set(npcRegistry.npcs.map((n) => n.id));
    if (review) {
      const visitor = modernVisitors.find((v) => v.id === review);
      if (visitor) {
        residents.delete(visitor.hostResidentId);
        residents.add(visitor.id);
      }
      return residents; // Existing resident QA URLs retain their original deterministic context.
    }
    for (const zone of this.entries.keys())
      if (!activeZones.has(zone)) this.entries.delete(zone);
    for (const zone of activeZones)
      if (!this.entries.has(zone))
        this.entries.set(zone, visitorForWindow(zone, now - this.epoch));
    for (const visitor of this.entries.values())
      if (visitor && pinned !== visitor.hostResidentId) {
        residents.delete(visitor.hostResidentId);
        residents.add(visitor.id);
      }
    if (pinned) residents.add(pinned);
    return residents;
  }
}
