import { defineConfig } from "vite";
export default defineConfig({
  base: "/3D-pharse5-/",
  publicDir: "public",
  server: { host: "127.0.0.1", port: 4200, strictPort: true },
  build: {
    target: "es2022",
    chunkSizeWarningLimit: 1600,
    rolldownOptions: {
      input: {
        game: "index.html",
        characterReview: "character-review.html",
        plazaReview: "plaza-review.html",
        districtReview: "district-review.html",
        productionReview: "production-review.html",
        refinementReview: "refinement-review.html",
        livingKoreaReview: "living-korea-review.html",
        fullWorldReview: "full-world-review.html",
        v3WorldReview: "v3-world-review.html",
        modernStreetsReview: "modern-streets-review.html",
        v4ReadabilityReview: "v4-readability-review.html",
      },
    },
  },
});
