import { mergeConfig } from "vite";
import base from "./vite.v7.config";
export default mergeConfig(base, {
  build: {
    rolldownOptions: { input: { v8CityReview: "v8-city-review.html" } },
  },
});
