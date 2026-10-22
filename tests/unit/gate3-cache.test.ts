import { describe, it, expect } from "vitest";
import { ResourcePool, type Resource } from "../../src/gate3/ResourcePool";
import { intersects } from "../../src/gate3/types";
const r = (id: string, bytes = 4): Resource => ({ id, bytes });
const drain = async () => {
  for (let i = 0; i < 12; i++) await Promise.resolve();
};
describe("G3 bounded streaming lifecycle", () => {
  it("deduplicates concurrent requests and reserves memory before completion", async () => {
    let resolve!: (v: string) => void;
    let starts = 0;
    const p = new ResourcePool<string>(
      8,
      2,
      () => {
        starts++;
        return new Promise((r) => {
          resolve = r;
        });
      },
      () => {},
    );
    p.update([r("a"), r("a")], new Set(["a"]));
    p.update([r("a")], new Set(["a"]));
    expect(starts).toBe(1);
    expect(p.reservedBytes).toBe(4);
    resolve("native");
    await drain();
    expect(p.resident.size).toBe(1);
    expect(p.reservedBytes).toBe(4);
    p.close();
    expect(p.reservedBytes).toBe(0);
  });
  it("evicts off-view resources, keeps pinned assets, and bounds oversized prefetch without thrashing", async () => {
    const disposed: string[] = [];
    const p = new ResourcePool<string>(
      8,
      2,
      async (r) => r.id,
      (r) => disposed.push(r.id),
    );
    p.update([r("a"), r("b"), r("c")], new Set(["a"]));
    await drain();
    expect(p.loads).toBe(2);
    expect(p.resident.has("a")).toBe(true);
    p.update([r("a"), r("c"), r("d")], new Set(["a", "c"]));
    await drain();
    expect(p.resident.has("a")).toBe(true);
    expect(p.resident.has("c")).toBe(true);
    expect(disposed).toEqual(["b"]);
    expect(p.peakBytes).toBeLessThanOrEqual(8);
    const loads = p.loads;
    await drain();
    expect(p.loads).toBe(loads);
    p.close();
  });
  it("disposes stale work completing after cancellation or shutdown", async () => {
    let resolve!: (v: string) => void;
    let disposed = 0;
    const p = new ResourcePool<string>(
      4,
      1,
      () =>
        new Promise((r) => {
          resolve = r;
        }),
      () => disposed++,
    );
    p.update([r("a")], new Set());
    p.update([], new Set());
    p.close();
    resolve("late");
    await drain();
    expect(disposed).toBe(1);
    expect(p.resident.size).toBe(0);
    expect(p.reservedBytes).toBe(0);
  });
  it("backs off failing loads and reports impossible visible working sets", async () => {
    const p = new ResourcePool<string>(
      4,
      1,
      async () => {
        throw Error("missing texture");
      },
      () => {},
    );
    p.update([r("a"), r("b")], new Set(["a", "b"]));
    await drain();
    expect(p.errors).toBe(1);
    expect(p.admissionBlocked).toBe(true);
    expect(p.reservedBytes).toBe(0);
    p.close();
  });
  it("retains foreground overlapping a boundary even when its support root is outside the view", () => {
    expect(intersects([500, 100, 80, 200], [512, 100, 512, 512])).toBe(true);
    expect(intersects([500, 100, 12, 200], [512, 100, 512, 512])).toBe(false);
  });
});
