"""Validate actual build and a ZIP transport, without deployment or persistent duplicate packages."""
from pathlib import Path
import subprocess,tempfile,zipfile
R=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='phase3bd-ci-')as tmp:
 z=Path(tmp)/'compiled-play.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_STORED)as out:
  for p in (R/'dist').rglob('*'):
   if p.is_file():out.write(p,'play/'+str(p.relative_to(R/'dist')))
 subprocess.run(['python3','tools/phase3bd/world_guard.py','--artifact','dist','--zip',str(z)],cwd=R,check=True)
