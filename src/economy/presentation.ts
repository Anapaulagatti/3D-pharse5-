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
