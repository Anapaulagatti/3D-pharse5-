export const travelState = { returnNorth: false, transitions: 0 };
declare global {
  interface Window {
    __KOREA__?: {
      district: "heritage" | "namsan" | "room";
      travelTransitions: number;
      scenicStops: number;
      world: number[];
    };
  }
}
