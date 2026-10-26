import { build } from "vite";
// One production entry, portable local asset URLs, no history/demo bundles.
await build({
  configFile: false,
  base: "./",
  publicDir: false,
  build: {
    outDir: "/tmp/phase2b-review",
    emptyOutDir: true,
    manifest: true,
    target: "es2022",
    chunkSizeWarningLimit: 1800,
    rolldownOptions: { input: { game: "index.html" } },
  },
});
