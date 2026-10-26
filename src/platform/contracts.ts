/** Future integration contracts only. No services are instantiated in Phase1. */
export type PlayerAccountId = string;
export interface PlayerProgress {
  readonly level: number;
  readonly experience: number;
  readonly completedLessons: readonly string[];
  readonly completedQuests: readonly string[];
  readonly inventory: Readonly<Record<string, number>>;
  readonly wallet: Readonly<Record<string, number>>;
}
export interface PlayerAccount {
  readonly id: PlayerAccountId;
  readonly progress: PlayerProgress;
  readonly preferences: { readonly selectedCharacterId: string };
}
export interface AccountProgressPersistence {
  load(id: PlayerAccountId): Promise<PlayerProgress>;
  save(id: PlayerAccountId, progress: PlayerProgress): Promise<void>;
}
export interface NPCDefinition {
  id: string;
  characterId: string;
  dialogueId: string;
  questIds: readonly string[];
}
export interface NPCRegistry {
  get(id: string): NPCDefinition | undefined;
}
export interface DialogueEngine {
  open(dialogueId: string, npcId: string): Promise<void>;
}
export type QuestState =
  | "ACTIVE"
  | "OBJECTIVE_DONE"
  | "QUIZ_PENDING"
  | "QUIZ_PASSED"
  | "REWARD_GRANTED";
export interface QuestRecord {
  id: string;
  state: QuestState;
  objectiveId: string;
  learningLevel: string;
  rewardId: string;
}
export interface QuestStateMachine {
  transition(questId: string, event: string): Promise<QuestRecord>;
}
export interface LearningProgress {
  verified: boolean;
  level: string;
  completedLessonIds: readonly string[];
}
export interface LessonProgressProvider {
  load(account: PlayerAccountId): Promise<LearningProgress | null>;
}
export interface KoreanQuestion {
  id: string;
  level: string;
  prompt: string;
  options: readonly string[];
}
export interface KoreanQuestionProvider {
  next(input: {
    progress: LearningProgress | null;
    excludeIds: readonly string[];
  }): Promise<KoreanQuestion>;
  verify(questionId: string, answerId: string): Promise<{ passed: boolean }>;
}
export interface Inventory {
  items(account: PlayerAccountId): Promise<Readonly<Record<string, number>>>;
}
export interface CurrencyWallet {
  balances(account: PlayerAccountId): Promise<Readonly<Record<string, number>>>;
}
export interface FarmingPlots {
  getOwnedPlots(account: PlayerAccountId): Promise<readonly string[]>;
}
export interface CraftingAndGathering {
  recipes(account: PlayerAccountId): Promise<readonly string[]>;
}
export interface Shops {
  catalog(shopId: string): Promise<readonly string[]>;
}
export interface RewardEligibility {
  verify(input: {
    account: PlayerAccountId;
    questId: string;
    quizReceipt: string;
  }): Promise<{ eligible: boolean; idempotencyKey: string }>;
}
export interface OptionalRewardedAdvertisement {
  available(): Promise<boolean>;
  request(): Promise<{
    status: "completed" | "cancelled" | "failed";
    providerReceipt?: string;
  }>;
}
export interface RewardReceiptVerifier {
  verify(
    providerReceipt: string,
    account: PlayerAccountId,
  ): Promise<{ valid: boolean; bonusMultiplier: number }>;
}
