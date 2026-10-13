#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
export npm_config_cache="$repo_root/Studio/.cache/npm"
export npm_config_update_notifier=false
node -e 'const [major,minor]=process.versions.node.split(".").map(Number); if(major<22 || (major===22 && minor<12)) process.exit(1)'
for package_dir in Studio preview; do
  cd "$repo_root/$package_dir"
  if [ -d node_modules ] && npm ls --depth=0 >/dev/null 2>&1; then
    echo "Reusing verified installed packages: $package_dir"
  else
    npm ci --no-fund --no-audit
  fi
done
command -v "${BLENDER_BIN:-blender}" >/dev/null
cd "$repo_root/Studio"
npm run assets:verify
cd "$repo_root/preview"
npm run build
STUDIO_REPORT_DIR="$repo_root/Studio/.cache/recovery-browser-reports" npm run test:smoke
