import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
export function currentAssets() {
  return JSON.parse(
    execFileSync("python3", ["tools/phase3bd/runtime_assets.py"], {
      encoding: "utf8",
    }),
  );
}
/** Same explicit closure for dev and production. No public-directory blanket copy. */
export function canonicalAssetsPlugin() {
  let config;
  let allowed;
  return {
    name: "canonical-world-allowlist",
    configResolved(value) {
      config = value;
      allowed = new Set(currentAssets());
    },
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        let name;
        try {
          name = decodeURIComponent(
            new URL(req.url, "http://localhost").pathname,
          )
            .replace(config.base, "/")
            .replace(/^\//, "");
        } catch {
          res.statusCode = 400;
          res.end();
          return;
        }
        if (!name.startsWith("assets/")) return next();
        if (!allowed.has(name)) {
          res.statusCode = 404;
          res.end("Not in canonical runtime");
          return;
        }
        const p = path.resolve("public", name);
        res.setHeader(
          "Content-Type",
          name.endsWith(".png")
            ? "image/png"
            : name.endsWith(".json")
              ? "application/json"
              : "application/octet-stream",
        );
        fs.createReadStream(p).pipe(res);
      });
    },
    closeBundle() {
      if (config.command !== "build") return;
      for (const name of currentAssets()) {
        const dest = path.join(config.build.outDir, name);
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        fs.copyFileSync(path.join("public", name), dest);
      }
      execFileSync(
        "python3",
        ["tools/phase3bd/world_guard.py", "--artifact", config.build.outDir],
        { stdio: "inherit" },
      );
    },
  };
}
