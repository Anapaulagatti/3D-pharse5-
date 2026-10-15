#!/usr/bin/env bash
set -euo pipefail
cd /workspace/3D-pharse5-
node --input-type=module -e "import p from './package.json' with {type:'json'};if(p.name!=='hangeul-pixel-town')throw Error('Expected verified pixel checkout; do not reset/switch unknown work');if(+process.versions.node.split('.')[0]<24)throw Error('Node24+ required')"
python3 -c "import PIL; assert PIL.__version__ == '12.3.0', 'Install tools/requirements.txt in your Python environment'"
if ! npm ls --depth=0 >/dev/null 2>&1; then
  npm ci --ignore-scripts
fi
export PIXEL_REPORT_DIR="$PWD/.cache/setup-qa"
npm run assets:check
npm run typecheck
npm run lint
npm run format:check
npm test
npm run build
npm run test:e2e
