/** Deterministic closest eligible target, with14px hysteresis against prompt flicker. */
export function chooseTarget(
  candidates: { id: string; distance: number }[],
  previous?: string,
) {
  const sorted = [...candidates].sort(
    (a, b) => a.distance - b.distance || a.id.localeCompare(b.id),
  );
  const prior = sorted.find((c) => c.id === previous);
  return prior && prior.distance <= (sorted[0]?.distance ?? 0) + 14
    ? prior.id
    : sorted[0]?.id;
}
