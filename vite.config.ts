import { defineConfig } from "vite";
export default defineConfig({
  base: "/3D-pharse5-/",
  publicDir: "public-unified",
  server: { host: "127.0.0.1", port: 4200, strictPort: true },
  build: { target: "es2022", chunkSizeWarningLimit: 1600 },
});
