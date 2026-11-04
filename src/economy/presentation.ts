import { ECONOMY, type PlotState } from "./catalog";
export type FarmTool = "seed" | "water" | "harvest";
export function growthProgress(p: PlotState, now: number) {
  return p.stage !== "watered"
    ? 0
    : Math.max(
        0,
        Math.min(
          1,
          Math.min(ECONOMY.offlineCapMs, now - (p.wateredAt ?? now)) /
            (p.growMs ?? 1),
        ),
      );
}
export function plotPresentation(p: PlotState, now: number) {
  return p.stage === "empty" &&
    p.lastHarvestedAt !== undefined &&
    now - p.lastHarvestedAt < 700
    ? "HARVESTED"
    : p.stage === "empty" || p.stage === "tilled"
      ? "EMPTY"
      : p.stage === "planted"
        ? "PLANTED"
        : growthProgress(p, now) >= 1
          ? "READY"
          : "GROWING";
}

/** Pure visual stage; saved economy schema and reward/timer semantics remain compatible. */
export function cropVisual(p: PlotState, now: number) {
  const progress = growthProgress(p, now);
  const stage =
    p.stage === "empty"
      ? p.lastHarvestedAt === undefined
        ? "empty"
        : "tilled"
      : p.stage === "tilled"
        ? "tilled"
        : p.stage === "planted" || progress < 0.16
          ? "sown"
          : progress < 0.36
            ? "sprout"
            : progress < 0.62
              ? "young"
              : progress < 1
                ? "growing"
                : "ready";
  return {
    stage,
    wet: p.stage === "watered",
    frame: p.crop ? `${p.crop}-${stage}` : undefined,
  };
}
