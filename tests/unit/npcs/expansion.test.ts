import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { npcRegistry } from "../../../src/npcs/registry";
import {
  npcCatalog,
  modernVisitors,
  npcLearningTeasers,
} from "../../../src/npcs/catalog";
import { NPCVisitPolicy, visitorForWindow } from "../../../src/npcs/visits";
import { NPCStateStore } from "../../../src/npcs/state";
import { hasVerifiedSources } from "../../../src/npcs/collections";
import approved from "../../../docs/phase3a-npc-expansion/approved-three-manifest.json";
const sha = (path: string) =>
  createHash("sha256").update(readFileSync(path)).digest("hex");
describe("illustrated NPC continuation — verified scope only", () => {
  it("keeps every approved pilot source, runtime visual and historical evidence byte-identical", () => {
    for (const [path, hash] of Object.entries(approved.files))
      expect(sha(path), path).toBe(hash);
  });
  it("composes20actual definitions through the original validated registry while preserving14resident API", () => {
    expect(npcRegistry.npcs).toHaveLength(14);
    expect(npcCatalog.npcs).toHaveLength(20);
    expect(new Set(npcCatalog.npcs.map((n) => n.id)).size).toBe(20);
    expect(npcCatalog.nodes.size).toBe(100);
    for (const resident of npcRegistry.npcs)
      expect(npcCatalog.get(resident.id)).toEqual(resident);
  });
  it("extends dialogue roots without mutating original nodes or old choices", () => {
    for (const resident of npcRegistry.npcs) {
      const old = npcRegistry.nodes.get(resident.dialogueId)!;
      expect(old.choices).toHaveLength(2);
      const expanded = npcCatalog.nodes.get(resident.dialogueId)!;
      expect(expanded.choices).toHaveLength(4);
      expect(expanded.choices.slice(0, 2)).toEqual(old.choices);
      expect(expanded.content).toEqual(old.content);
    }
    for (const n of npcLearningTeasers) {
      expect(n.vocabulary).toHaveLength(6);
      expect(n.topicCount).toBe(4);
      expect(n.authenticatedLessonProgress).toBe(false);
      for (const w of n.vocabulary) {
        expect(w.ko).toMatch(/[가-힣]/);
        expect(w.vi.length).toBeGreaterThan(1);
      }
    }
  });
  it("keeps fictional visitor registrations on existing verified host routes and native atlas contracts", () => {
    for (const v of modernVisitors) {
      const visitor = npcCatalog.get(v.id)!;
      const host = npcRegistry.get(v.hostResidentId)!;
      expect(visitor.route).toEqual(host.route);
      expect(visitor.reviewSpawn).toEqual(host.reviewSpawn);
      expect(visitor.footprint).toEqual(host.footprint);
      expect(visitor.walkSpeed).toBe(host.walkSpeed);
      expect(v.realPerson).toBe(false);
      expect(v.licensedCameo).toBe(false);
      const meta = JSON.parse(
        readFileSync("public/" + visitor.assets.atlas, "utf8"),
      );
      expect(Object.keys(meta.frames)).toHaveLength(104);
      for (const clip of Object.values(visitor.animations))
        for (const frame of clip.frames)
          expect(meta.frames[frame]).toBeDefined();
      expect(sha("public/" + visitor.assets.texture)).not.toBe(
        sha("public/" + host.assets.texture),
      );
    }
  });
  it("rotates deterministically through a resident window and all visitors without preloading", () => {
    const found = new Set<string>();
    for (const zone of ["modern", "station", "nature-leisure", "coast"]) {
      expect(visitorForWindow(zone, 0)).toBeUndefined();
      for (let slot = 1; slot <= 3; slot++) {
        const v = visitorForWindow(zone, slot * 90_000);
        if (v) found.add(v.id);
        expect(visitorForWindow(zone, slot * 90_000)).toEqual(v);
      }
    }
    expect(found.size).toBe(6);
  });
  it("replaces a host slot, holds the visit during a stay, and defers a new selection to re-entry", () => {
    const memory = new Map<string, string>([
      [NPCVisitPolicy.key, JSON.stringify({ version: 1, epochMs: 1 })],
    ]);
    const store = {
      getItem: (k: string) => memory.get(k) ?? null,
      setItem: (k: string, v: string) => {
        memory.set(k, v);
      },
    };
    const p = new NPCVisitPolicy(store);
    const zones = new Set(["modern"]);
    const first = p.eligible(zones, undefined, undefined, 90_001);
    const visitor = visitorForWindow("modern", 90_000)!;
    expect(first.has(visitor.id)).toBe(true);
    expect(first.has(visitor.hostResidentId)).toBe(false);
    expect(p.eligible(zones, undefined, undefined, 180_001)).toEqual(first);
    p.eligible(new Set(), undefined, undefined, 180_001);
    const next = p.eligible(zones, undefined, undefined, 180_001);
    expect(next.has(visitorForWindow("modern", 180_000)!.id)).toBe(true);
    const pinned = p.eligible(
      zones,
      visitorForWindow("modern", 180_000)!.hostResidentId,
      undefined,
      180_001,
    );
    expect(pinned.has(visitorForWindow("modern", 180_000)!.id)).toBe(false);
    expect([...memory.keys()]).toEqual([NPCVisitPolicy.key]);
  });
  it("keeps all original QA contexts deterministic while allowing an explicit new visitor review", () => {
    const p = new NPCVisitPolicy();
    for (const resident of npcRegistry.npcs) {
      const allowed = p.eligible(
        new Set([resident.homeZone]),
        undefined,
        resident.id,
      );
      expect(
        [...allowed].filter((id) => id.startsWith("npc-modern-")),
      ).toHaveLength(0);
    }
    for (const v of modernVisitors) {
      const allowed = p.eligible(new Set([v.homeZone]), undefined, v.id);
      expect(allowed.has(v.id)).toBe(true);
      expect(allowed.has(v.hostResidentId)).toBe(false);
    }
  });
  it("restores existing NPC state without touching unrelated player or progress keys", () => {
    const memory = new Map<string, string>();
    const storage = {
      getItem: (k: string) => memory.get(k) ?? null,
      setItem: (k: string, v: string) => {
        memory.set(k, v);
      },
    };
    memory.set(
      "korean-arena-player-preferences-v1",
      '{"characterId":"juni","version":1}',
    );
    memory.set("world-visited", '["palace"]');
    const playerBefore = memory.get("korean-arena-player-preferences-v1");
    const old = new NPCStateStore(storage, npcRegistry.npcs);
    old.save();
    const restored = new NPCStateStore(storage, npcCatalog.npcs);
    for (const n of npcRegistry.npcs)
      expect(restored.get(n.id)).toEqual(old.get(n.id));
    restored.save();
    expect(memory.get("world-visited")).toBe('["palace"]');
    expect(memory.get("korean-arena-player-preferences-v1")).toBe(playerBefore);
  });
  it("does not unlock historical archives or factual biographies from unverified/empty sources", () => {
    expect(hasVerifiedSources([])).toBe(false);
    expect(
      hasVerifiedSources([
        {
          url: "https://contents.history.go.kr/",
          accessedAt: "invalid",
          claimReferences: [],
          status: "verified",
        },
      ]),
    ).toBe(false);
    expect(
      hasVerifiedSources([
        {
          url: "https://example.org/record",
          accessedAt: "2026-10-28",
          claimReferences: ["claim-1"],
          status: "verified",
        },
      ]),
    ).toBe(true);
    expect(npcCatalog.npcs.some((n) => n.id.startsWith("npc-history-"))).toBe(
      false,
    );
  });
});
