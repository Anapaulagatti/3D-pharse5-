"""Manual historical source tools only. Never import from the playable/build graph."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def archived_public(name):
 if name.startswith('assets/gate3/production/'):
  return R/'assets-src/archive/g3bc-production-donor'/name.removeprefix('assets/gate3/production/')
 return R/'public'/name
