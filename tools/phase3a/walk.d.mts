import type { Page } from "@playwright/test";
export function axisTo(
  page: Page,
  axis: "x" | "y",
  target: number,
): Promise<void>;
export function walkPath(
  page: Page,
  points: number[][],
  onPoint?: (index: number, point: number[]) => Promise<void>,
): Promise<void>;
