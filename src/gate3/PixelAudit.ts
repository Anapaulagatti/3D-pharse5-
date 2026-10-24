import Phaser from "phaser";
/** Opt-in, read-only post-render evidence. No per-frame work unless requested. */
export function installPixelAudit(scene: Phaser.Scene) {
  const snapshot = () => {
    const camera = scene.cameras.main;
    return {
      png: scene.game.canvas.toDataURL("image/png"),
      state: window.__GATE3__,
      camera: {
        zoom: camera.zoom,
        scroll: [camera.scrollX, camera.scrollY],
        viewport: [camera.x, camera.y, camera.width, camera.height],
        matrix: Array.from(camera.matrixCombined.matrix),
        roundPixels: camera.roundPixels,
      },
      layers: scene.children.list
        .filter(
          (o): o is Phaser.GameObjects.Image =>
            o instanceof Phaser.GameObjects.Image &&
            /^(g|f)\//.test(o.texture.key),
        )
        .map((o) => ({
          key: o.texture.key,
          alpha: o.alpha,
          depth: o.depth,
          visible: o.visible,
          position: [o.x, o.y],
          origin: [o.originX, o.originY],
          scale: [o.scaleX, o.scaleY],
          screenOrigin: [
            camera.matrixCombined.getX(o.x, o.y),
            camera.matrixCombined.getY(o.x, o.y),
          ],
          scaleMode: o.frame.source.scaleMode,
          minFilter: o.frame.source.glTexture?.minFilter,
          magFilter: o.frame.source.glTexture?.magFilter,
        })),
    };
  };
  window.__GATE3_PIXEL_AUDIT__ = () =>
    new Promise((resolve) => {
      scene.game.events.once(Phaser.Core.Events.POST_RENDER, () =>
        resolve(snapshot()),
      );
    });
  // Capture a genuine animation pose on its actual POST_RENDER. This observes
  // frames only: no position, animation, collision, camera or clock override.
  window.__GATE3_PIXEL_POSE__ = (prefix, timeoutMs = 4000) =>
    new Promise((resolve) => {
      const cleanup = () => {
        clearTimeout(timer);
        scene.game.events.off(Phaser.Core.Events.POST_RENDER, capture);
      };
      const capture = () => {
        const player = scene.children.list.find(
          (o): o is Phaser.GameObjects.Sprite =>
            o instanceof Phaser.GameObjects.Sprite && o.texture.key === "juni",
        );
        if (!player || !String(player.frame.name).startsWith(prefix)) return;
        cleanup();
        resolve({
          ...snapshot(),
          state: window.__GATE3__,
          matched: true,
          actualFrame: String(player.frame.name),
        });
      };
      const timer = setTimeout(
        () => {
          cleanup();
          resolve({ matched: false, prefix });
        },
        Math.min(6000, Math.max(100, timeoutMs)),
      );
      scene.game.events.on(Phaser.Core.Events.POST_RENDER, capture);
    });
}
declare global {
  interface Window {
    __GATE3_PIXEL_AUDIT__?: () => Promise<unknown>;
    __GATE3_PIXEL_POSE__?: (
      prefix: string,
      timeoutMs?: number,
    ) => Promise<unknown>;
  }
}
