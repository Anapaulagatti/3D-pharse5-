import { defineConfig } from "vite";
export default defineConfig(({ command }) => ({
  base: "./",
  publicDir: command === "serve" ? "public" : false,
  build: {
    outDir: "dist-gate3",
    target: "es2022",
    chunkSizeWarningLimit: 1800,
    rolldownOptions: { input: { review: "gate3-review.html" } },
  },
}));
