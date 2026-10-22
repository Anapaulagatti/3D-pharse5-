/** Raw browser update interval histogram; not a physical hardware FPS certification. */
export class SessionMetrics {
  private bins = new Uint32Array(2001);
  private count = 0;
  private sum = 0;
  private maximum = 0;
  private spikes = 0;
  private hidden = 0;
  add(ms: number) {
    if (document.hidden) {
      this.hidden++;
      return;
    }
    if (!Number.isFinite(ms) || ms <= 0) return;
    this.bins[Math.min(2000, Math.floor(ms * 2))]++;
    this.count++;
    this.sum += ms;
    this.maximum = Math.max(this.maximum, ms);
    if (ms > 50) this.spikes++;
  }
  snapshot() {
    const percentile = (p: number) => {
      let n = 0;
      for (let i = 0; i < this.bins.length; i++) {
        n += this.bins[i];
        if (n >= this.count * p) return i / 2;
      }
      return null;
    };
    return {
      samples: this.count,
      observedVisibleSeconds: this.sum / 1000,
      meanUpdateMs: this.count ? this.sum / this.count : null,
      p50Ms: percentile(0.5),
      p95Ms: percentile(0.95),
      p99Ms: percentile(0.99),
      maxMs: this.maximum,
      over50ms: this.spikes,
      hiddenSamplesExcluded: this.hidden,
      measurement:
        "raw performance.now intervals / histogram0.5ms /overflow>=1000ms / browser update cadence, not certified presentation FPS",
    };
  }
}
