import type { JuniView } from "./JuniMotion";
export type WorldData = {
  width: number;
  height: number;
  spawn: number[];
  npc: number[];
  follow: number;
  role: string;
  mood: string;
  vi: string;
  mapSha256: string;
  objects: {
    id: number;
    kind: string;
    x: number;
    y: number;
    sortY?: number;
    width: number;
    height: number;
    label: string;
    collide: boolean;
  }[];
};
export type ReviewWorld = {
  layout: WorldData;
  bundle: {
    objects: { sortY: number; prop: string; x: number; y: number }[];
    props: Record<string, { anchor_px: number[]; size: number[] }>;
  };
  anchors: Record<string, number[]>;
  assetRoot: string;
  key?: string;
  ambience?: boolean;
};
declare global {
  interface Window {
    __SEOUL_TEST__?: { place: (x: number, y: number) => void };
    __SEOUL__?: {
      ready: boolean;
      area: string;
      x: number;
      y: number;
      world: number[];
      gateOpen: boolean;
      transitions: number;
      activeProps: number;
      totalProps: number;
      ambientClock: number;
      reservedNPCs: string[];
      view: number[];
    };
    __PLAZA_REVIEW__?: {
      ready: boolean;
      district: string;
      player: string;
      direction: JuniView;
      nativeBodyHeight: number;
      staticCharacter: false;
      action: string;
      frame: string;
      phase: number;
      environmentClock: number;
      occludedPixels: number;
      userApproval: "PENDING";
    };
  }
}
