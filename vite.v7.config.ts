import { mergeConfig } from "vite";
import base from "./vite.config";
export default mergeConfig(base, {
  build: {
    rolldownOptions: { input: { v7WorldReview: "v7-world-review.html" } },
  },
});
