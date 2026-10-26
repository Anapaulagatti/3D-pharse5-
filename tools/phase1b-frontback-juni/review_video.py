"""Lossy native-scale review crops of actual Playwright recordings. PNGs remain native proof."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b-frontback-juni'
for name in ['juni','haneul','bomi','minjun']:
 subprocess.run(['ffmpeg','-y','-i',str(D/f'{name}-actual-phaser.webm'),'-vf',f'crop=480:900:400:50,drawtext=text={name} actual Phaser gameplay:x=12:y=12:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(D/f'{name}-actual-phaser-crop.mp4')],check=True)
