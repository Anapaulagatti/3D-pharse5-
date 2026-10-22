import { defineConfig } from "vite";
export default defineConfig({
  base: "/3D-pharse5-/",
  publicDir: false,
  build: {
    outDir: "dist-gate2",
    target: "es2022",
    chunkSizeWarningLimit: 1800,
    rolldownOptions: { input: { review: "gate2-review.html" } },
  },
});
