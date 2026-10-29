import { defineConfig } from "vite";
import { checkAssetRights } from "./tools/rights-gate.mjs";
export default defineConfig(({ mode }) => {
  const profile =
    mode === "public" || process.env.VITE_RELEASE_PROFILE === "public"
      ? "public"
      : "private-review";
  return {
    plugins: [
      {
        name: "npc-asset-rights-gate",
        buildStart() {
          checkAssetRights(profile);
        },
        transformIndexHtml(html) {
          return html.replace(
            "<head>",
            `<head><meta name="korean-arena-release-profile" content="${profile}">`,
          );
        },
      },
    ],
    define: { "import.meta.env.VITE_RELEASE_PROFILE": JSON.stringify(profile) },
    base: "/3D-pharse5-/",
    publicDir: "public",
    server: { host: "127.0.0.1", port: 4200, strictPort: true },
    build: {
      target: "es2022",
      chunkSizeWarningLimit: 1600,
      rolldownOptions: {
        input: {
          game: "index.html",
          ...(profile === "private-review"
            ? {
                worldReview: "gate3-review.html",
                v10Review: "v10-city-review.html",
              }
            : {}),
        },
      },
    },
  };
});
