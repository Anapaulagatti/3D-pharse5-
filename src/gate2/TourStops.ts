export type TourStop = {
  id: string;
  label: string;
  x: number;
  y: number;
  zoom: number;
  travelMs: number;
  holdMs: number;
};
/** Authored camera centers in unchanged native source pixels, never player destinations. */
export function tourStops(sceneId: string): TourStop[] {
  const c = [
    { id: "coast", label: "1 / 4 · Coastal Arrival", x: 280, y: 435 },
    { id: "oreum", label: "2 / 4 · Volcanic Oreum", x: 670, y: 265 },
    { id: "orchard", label: "3 / 4 · Tangerine Orchard", x: 760, y: 860 },
    { id: "house", label: "4 / 4 · Traditional Jeju House", x: 455, y: 1100 },
  ];
  const stops =
    sceneId === "c" || ["jeju-fit", "jeju25"].includes(sceneId)
      ? c.map((s) => ({
          ...s,
          x: s.x + (["jeju-fit", "jeju25"].includes(sceneId) ? 830 : 0),
          y: s.y + (["jeju-fit", "jeju25"].includes(sceneId) ? 100 : 0),
        }))
      : sceneId === "b"
        ? [
            {
              id: "shops",
              label: "1 / 2 · Muneum storefronts",
              x: 470,
              y: 400,
            },
            {
              id: "street",
              label: "2 / 2 · Commercial street",
              x: 1050,
              y: 590,
            },
          ]
        : [];
  return stops.map((s) => ({ ...s, zoom: 0.5, travelMs: 2000, holdMs: 2100 }));
}
