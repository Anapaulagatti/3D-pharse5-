# Editable pixel sources

Original integer-raster code-authored art, no image model/downscaled concept. Edit directions.json palette, layout.json (before initial map generation), .tmj map in Tiled and tools/export_art.py named geometry functions. Per-direction indexed PNGs are open sprite-editor-compatible masters; four-direction frames use fixed48×64 canvas and foot anchors.

`npm run assets` renders geometry definitions and repacks PNG/Phaser JSON; it preserves existing directions.json palette and plaza.tmj edits. Editing generated individual PNG masters directly is useful for manual iteration but exporter regenerates those frames from Python: incorporate accepted pixel changes into component definitions or archive manually edited frames before re-export. Do not blindly regenerate approved art.

`npm run assets:check` compares every atlas frame pixel with indexed master, all source/production hashes, binary alpha/palette/gutters, distinct gait phases and map/collision/reachability. No external assets/providers/fonts/audio. manifest.json records all file hashes, sizes/provenance and pending art status.
