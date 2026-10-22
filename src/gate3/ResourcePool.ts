export type Resource = { id: string; bytes: number };
type Pending = { resource: Resource; controller: AbortController };
/** Reservations include in-flight work. Eviction never invalidates the visible/player set. */
export class ResourcePool<T> {
  readonly resident = new Map<
    string,
    { resource: Resource; value: T; used: number }
  >();
  private pending = new Map<string, Pending>();
  private desired: Resource[] = [];
  private pinned = new Set<string>();
  private failures = new Map<string, number>();
  private clock = 0;
  private closed = false;
  loads = 0;
  evictions = 0;
  errors = 0;
  aborted = 0;
  peakBytes = 0;
  admissionBlocked = false;
  constructor(
    readonly budget: number,
    readonly concurrency: number,
    private load: (r: Resource, signal: AbortSignal) => Promise<T>,
    private dispose: (r: Resource, value: T) => void,
  ) {}
  get reservedBytes() {
    return (
      [...this.resident.values()].reduce((n, e) => n + e.resource.bytes, 0) +
      [...this.pending.values()].reduce((n, e) => n + e.resource.bytes, 0)
    );
  }
  update(desired: Resource[], pinned: Set<string>) {
    if (this.closed) return;
    this.clock++;
    // Bound the target set too: otherwise oversized prefetch can evict/reload itself forever.
    this.admissionBlocked = false;
    let committed = 0;
    this.desired = [...new Map(desired.map((r) => [r.id, r])).values()].filter(
      (r) => {
        if (committed + r.bytes > this.budget) {
          if (pinned.has(r.id)) this.admissionBlocked = true;
          return false;
        }
        committed += r.bytes;
        return true;
      },
    );
    this.pinned = pinned;
    const wanted = new Set(this.desired.map((r) => r.id));
    for (const [id, p] of this.pending)
      if (!wanted.has(id)) p.controller.abort();
    for (const r of this.desired) {
      const e = this.resident.get(r.id);
      if (e) e.used = this.clock;
    }
    this.pump();
  }
  private pump() {
    if (this.closed) return;
    for (const r of this.desired) {
      if (this.pending.size >= this.concurrency) break;
      if (
        this.resident.has(r.id) ||
        this.pending.has(r.id) ||
        (this.failures.get(r.id) ?? 0) > Date.now()
      )
        continue;
      while (this.reservedBytes + r.bytes > this.budget) {
        const victim = [...this.resident.entries()]
          .filter(([id]) => !this.pinned.has(id))
          .sort((a, b) => a[1].used - b[1].used)[0];
        if (!victim) break;
        this.dispose(victim[1].resource, victim[1].value);
        this.resident.delete(victim[0]);
        this.evictions++;
      }
      if (this.reservedBytes + r.bytes > this.budget) {
        if (this.pinned.has(r.id)) this.admissionBlocked = true;
        continue;
      }
      const controller = new AbortController();
      this.pending.set(r.id, { resource: r, controller });
      this.peakBytes = Math.max(this.peakBytes, this.reservedBytes);
      void this.load(r, controller.signal)
        .then((value) => {
          if (
            this.closed ||
            controller.signal.aborted ||
            !this.desired.some((d) => d.id === r.id)
          ) {
            this.dispose(r, value);
            this.aborted++;
          } else {
            this.resident.set(r.id, { resource: r, value, used: this.clock });
            this.loads++;
            this.failures.delete(r.id);
          }
        })
        .catch(() => {
          if (controller.signal.aborted) this.aborted++;
          else {
            this.errors++;
            this.failures.set(r.id, Date.now() + 2000);
          }
        })
        .finally(() => {
          this.pending.delete(r.id);
          this.pump();
        });
    }
  }
  close() {
    this.closed = true;
    this.desired = [];
    for (const p of this.pending.values()) p.controller.abort();
    for (const e of this.resident.values()) this.dispose(e.resource, e.value);
    this.resident.clear();
  }
  snapshot() {
    return {
      resident: this.resident.size,
      inflight: this.pending.size,
      reservedBytes: this.reservedBytes,
      budgetBytes: this.budget,
      peakBytes: this.peakBytes,
      loads: this.loads,
      evictions: this.evictions,
      errors: this.errors,
      aborted: this.aborted,
      admissionBlocked: this.admissionBlocked,
    };
  }
}
