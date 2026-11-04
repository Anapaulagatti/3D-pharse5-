/** Disabled live-service boundaries. No provider SDK, account, network or real-player claim. */
export const LIVE_FEATURES = Object.freeze({
  multiplayer: false,
  matchmaking: false,
  ranked: false,
  chat: false,
  ads: false,
  learningSync: false,
});
export interface ProfileProgressAdapter {
  readonly mode: "local-demo" | "owner-authorized-server";
  load(): Promise<{ questIds: readonly string[]; appearanceId: string }>;
}
export interface RoomAdapter {
  readonly mode: "DISABLED" | "LOCAL_SIMULATION_NOT_LIVE_PLAYERS";
  join(): Promise<{
    status: "disabled" | "local-simulation";
    actors: readonly string[];
  }>;
}
export const disabledRoom: RoomAdapter = {
  mode: "DISABLED",
  join: async () => ({ status: "disabled", actors: [] }),
};
export interface RewardedAdProvider {
  readonly enabled: false;
  available(): false;
  show(explicitOptIn: boolean): Promise<{ status: "disabled"; granted: 0 }>;
}
export const noAds: RewardedAdProvider = {
  enabled: false,
  available: () => false,
  show: async () => ({ status: "disabled", granted: 0 }),
};
export interface LearningEvidenceContract {
  mode: "local-demo";
  contentId: string;
  review: "PENDING_HUMAN_REVIEW";
  result: "practice-only";
  formalMasteryWrite: false;
}
/** Pure server-boundary validator prototype. NOT a hosted server or client-side security guarantee. */
export class LocalRoomSimulation implements RoomAdapter {
  readonly mode = "LOCAL_SIMULATION_NOT_LIVE_PLAYERS" as const;
  private last = new Map<string, { x: number; y: number; at: number }>();
  private receipts = new Set<string>();
  private count = 0;
  async join() {
    return {
      status: "local-simulation" as const,
      actors: ["TEST_ACTOR_A", "TEST_ACTOR_B"],
    };
  }
  move(actor: string, x: number, y: number, at: number) {
    if (
      !["TEST_ACTOR_A", "TEST_ACTOR_B"].includes(actor) ||
      ![x, y, at].every(Number.isFinite) ||
      x < 0 ||
      x > 4096 ||
      y < 0 ||
      y > 4608
    )
      return false;
    const p = this.last.get(actor);
    if (
      p &&
      (at <= p.at ||
        at - p.at < 80 ||
        Math.hypot(x - p.x, y - p.y) > (at - p.at) * 0.11 + 3)
    )
      return false;
    this.last.set(actor, { x, y, at });
    return true;
  }
  cosmeticReceipt(id: string) {
    if (
      !/^[a-zA-Z0-9:_-]{3,80}$/.test(id) ||
      this.receipts.has(id) ||
      this.count >= 256
    )
      return false;
    this.receipts.add(id);
    this.count++;
    return true;
  }
}
