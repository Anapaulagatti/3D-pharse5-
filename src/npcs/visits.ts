import windows from "../../assets-src/npcs/daily-life/visitor-windows.json";
import { seededChoice } from "./clock";
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
/** Deterministic modern visitor window; legacy wall-clock API remains available. */
export function visitorForGameTime(
  zone: string,
  minute: number,
  seed: number,
  day: number,
) {
  const available = modernVisitors
    .filter(
      (v) =>
        v.homeZone === zone &&
        windows.windows.some(
          (w) =>
            w.npcId === v.id && minute >= w.startMinute && minute < w.endMinute,
        ),
    )
    .sort((a, b) => a.id.localeCompare(b.id));
  if (!available.length) return;
  const slot =
    (1 +
      Math.floor(minute / 15) +
      seededChoice(seed, day, zone, available.length + 1)) %
    (available.length + 1);
  return slot === 0 ? undefined : available[slot - 1];
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
    gameMinute?: number,
    simulation = { seed: 20261029, day: 0 },
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
      if (!this.entries.has(zone) || gameMinute !== undefined)
        this.entries.set(
          zone,
          gameMinute === undefined
            ? visitorForWindow(zone, now - this.epoch)
            : visitorForGameTime(
                zone,
                gameMinute,
                simulation.seed,
                simulation.day,
              ),
        );
    for (const visitor of this.entries.values())
      if (
        visitor &&
        pinned !== visitor.hostResidentId &&
        (gameMinute === undefined ||
          windows.windows.some(
            (w) =>
              w.npcId === visitor.id &&
              gameMinute >= w.startMinute &&
              gameMinute < w.endMinute,
          ))
      ) {
        residents.delete(visitor.hostResidentId);
        residents.add(visitor.id);
      }
    if (pinned) {
      const held = modernVisitors.find((v) => v.id === pinned);
      if (held) residents.delete(held.hostResidentId);
      residents.add(pinned);
    }
    return residents;
  }
}
