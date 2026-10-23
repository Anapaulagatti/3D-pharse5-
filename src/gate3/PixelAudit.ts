import Phaser from "phaser";
/** Opt-in, read-only post-render evidence. No per-frame work unless requested. */
export function installPixelAudit(scene: Phaser.Scene) {
  window.__GATE3_PIXEL_AUDIT__ = () =>
    new Promise((resolve) => {
      scene.game.events.once(Phaser.Core.Events.POST_RENDER, () => {
        const camera = scene.cameras.main;
        resolve({
          png: scene.game.canvas.toDataURL("image/png"),
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
        });
      });
    });
}
declare global {
  interface Window {
    __GATE3_PIXEL_AUDIT__?: () => Promise<unknown>;
  }
}
