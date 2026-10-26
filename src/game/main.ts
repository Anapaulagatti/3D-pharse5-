/** Canonical production bootstrap. No historical V10 world is imported. */
document.documentElement.dataset.phase = "1";
await import("../gate3/main");

export {};
