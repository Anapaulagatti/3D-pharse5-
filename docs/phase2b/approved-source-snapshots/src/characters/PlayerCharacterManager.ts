import { RegistryMotion } from "./RegistryMotion";
import { JuniMotion } from "../engine/JuniMotion";
import { characterRegistry, type CharacterRegistry } from "./registry";
import type { CharacterDefinition } from "./types";
import type {
  CharacterPreferences,
  AppearancePreferences,
} from "./preferences";
import type { CharacterAppearance } from "./appearanceTypes";
import {
  appearanceKey,
  defaultAppearance,
  normalizeAppearance,
} from "./appearance";
export interface PlayerSprite {
  setPosition(x: number, y: number): this;
  setDepth(depth: number): this;
  setFrame(name: string): this;
  setVisible(visible: boolean): this;
  setTexture?(key: string, frame?: string): this;
  setData?(key: string, value: string): this;
  destroy(): void;
}
export interface CharacterAssets {
  ensure(
    def: CharacterDefinition,
    appearance?: CharacterAppearance,
  ): Promise<{
    definition: CharacterDefinition;
    appearance: CharacterAppearance;
    fallbackReason?: string;
  } | void>;
  activate?(def: CharacterDefinition): void;
  dispose?(): void;
}
export interface PlayerLocation {
  x: number;
  y: number;
}
/** One live actor; cosmetics only swap its native atlas. Camera, collision,
 * world state, progress and motion speeds remain scene/controller-owned. */
export class PlayerCharacterManager<S extends PlayerSprite> {
  private active: S;
  private definition: CharacterDefinition;
  private look: CharacterAppearance;
  private closed = false;
  private loading = false;
  private transitioning = false;
  private pose: JuniMotion | RegistryMotion;
  constructor(
    private readonly assets: CharacterAssets,
    private readonly create: (
      def: CharacterDefinition,
      position: PlayerLocation,
    ) => S,
    private readonly preferences: CharacterPreferences,
    initial: CharacterDefinition,
    position: PlayerLocation,
    private readonly registry: CharacterRegistry = characterRegistry,
    private readonly appearances?: AppearancePreferences,
  ) {
    this.definition = initial;
    this.look = defaultAppearance(initial.id);
    this.pose =
      initial.id === "juni" ? new JuniMotion() : new RegistryMotion(initial);
    this.active = this.create(initial, position);
    this.assets.activate?.(initial);
  }
  get sprite() {
    return this.active;
  }
  get selected() {
    return this.definition;
  }
  get appearance() {
    return { ...this.look, accessoryIds: [...this.look.accessoryIds] };
  }
  get motion() {
    return this.pose;
  }
  get busy() {
    return this.loading || this.transitioning || this.closed;
  }
  setTransitioning(value: boolean) {
    this.transitioning = value;
  }
  private save(presetName?: string) {
    const oldSaved = this.preferences.save(this.definition.id);
    const lookSaved = this.appearances?.save(this.look, presetName) ?? true;
    return oldSaved && lookSaved;
  }
  async select(
    id: string,
    location: PlayerLocation,
    requested?: CharacterAppearance,
    presetName?: string,
  ) {
    if (this.busy)
      throw Error("Character switch unavailable during scene transition");
    const requestedDef = this.registry.get(id);
    if (requestedDef?.availability.status === "incomplete")
      throw Error("Character art is incomplete");
    const next = this.registry.resolve(id),
      look = normalizeAppearance(
        next.id,
        requested ??
          this.appearances?.read(next.id) ??
          defaultAppearance(next.id),
      );
    if (
      next.id === this.definition.id &&
      appearanceKey(look) === appearanceKey(this.look)
    )
      return { characterId: next.id, saved: this.save(presetName) };
    this.loading = true;
    try {
      const loaded = await this.assets.ensure(next, look);
      if (this.closed || this.transitioning)
        throw Error("Scene changed while loading character");
      const rendered = loaded?.definition ?? next;
      const motion =
        next.id === this.definition.id
          ? this.pose
          : next.id === "juni"
            ? new JuniMotion()
            : new RegistryMotion(next);
      if (motion instanceof RegistryMotion && motion !== this.pose)
        motion.adopt(this.pose.snapshot);
      if (this.active.setTexture) {
        this.active.setTexture(rendered.assets!.key, motion.frame);
        this.active.setData?.("playerCharacter", next.id);
      } else {
        const sprite = this.create(rendered, location)
            .setVisible(false)
            .setFrame(motion.frame),
          old = this.active;
        this.active = sprite;
        old.destroy();
        sprite.setVisible(true);
      }
      this.definition = next;
      this.look = loaded?.appearance ?? look;
      this.pose = motion;
      this.assets.activate?.(rendered);
      return {
        characterId: next.id,
        saved: this.save(presetName),
        ...(loaded?.fallbackReason
          ? { fallbackReason: loaded.fallbackReason }
          : {}),
      };
    } finally {
      this.loading = false;
    }
  }
  dispose() {
    if (this.closed) return;
    this.closed = true;
    this.active.destroy();
    this.assets.dispose?.();
  }
}
