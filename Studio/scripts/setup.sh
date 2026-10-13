#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
export npm_config_cache="$repo_root/Studio/.cache/npm"
export npm_config_update_notifier=false
node -e 'const [major, minor] = process.versions.node.split(".").map(Number); if (major < 22 || (major === 22 && minor < 12)) { console.error("Node 22.12+ required"); process.exit(1) }'
command -v "${BLENDER_BIN:-blender}" >/dev/null || {
  echo 'Blender is required. Install the desktop application from https://www.blender.org/download/ and add it to PATH or set BLENDER_BIN.' >&2
  exit 1
}
cd "$repo_root/Studio"
npm ci --no-fund --no-audit
npm run check:tools
cd "$repo_root/preview"
npm ci --no-fund --no-audit
npm run build
npm ls react react-dom three @react-three/fiber @react-three/drei
