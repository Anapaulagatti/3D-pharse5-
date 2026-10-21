# Korean Arena — V10 original city art review

The approved V10 masterplan now has original Korean town, station, Namsan, amusement, waterfront/ferry and Jeju artwork in Phaser. Final visual approval is pending. No merge to main or public deployment.

Download docs/v10-production/V10_FINAL_REVIEW.zip, extract and run `python3 start.py` (Windows: `py start.py`). Use WASD/arrows, Shift to run and E to interact; landscape touch controls are included. The launcher serves the exact production build locally.

Development: Node24+, Python3.12, Pillow12.3 and Chromium; `npm ci --ignore-scripts`, then `bash tools/setup.sh`. Setup checks stored art without generating images. `npm run dev` serves the internal development view. Open `/3D-pharse5-/v10-city-review.html`.

Review evidence and limits: [production report](docs/v10-production/V10_FINAL_PRODUCTION_REPORT.md), [provenance](docs/v10-production/V10_ART_ASSET_PROVENANCE.md), [source audit](docs/v10-production/V10_FORBIDDEN_SOURCE_AUDIT.md). Native captures, full gameplay walkthrough and playable ZIP are in that folder. Original prompts/sheets/native assets and tool receipts are retained under assets-src/v10-city. Earlier versions remain archived and excluded from the southern production graph.
