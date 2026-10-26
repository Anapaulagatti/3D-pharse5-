import { build } from "vite";
await build({ configFile: false, base: "./", publicDir: false, build: { outDir: "/tmp/phase2b-motion-review", emptyOutDir: true, manifest: true, target: "es2022", chunkSizeWarningLimit: 1800, rolldownOptions: { input: { game: "index.html" } } } });
