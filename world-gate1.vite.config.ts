import { defineConfig } from "vite";
export default defineConfig({
  base: "/3D-pharse5-/",
  publicDir: false,
  build: {
    outDir: "dist-world-gate1",
    chunkSizeWarningLimit: 1800,
    rolldownOptions: { input: { world: "world-gate1.html" } },
  },
});
