import { defineConfig } from "vite";
export default defineConfig({
  base: "/3D-pharse5-/",
  publicDir: false,
  build: {
    target: "es2022",
    outDir: "dist-gate1",
    chunkSizeWarningLimit: 1800,
    rolldownOptions: { input: { street: "gate1-street.html" } },
  },
});
