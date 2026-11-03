"""Current approved world check; rejected V10 is not a current preservation target."""
import subprocess,sys
subprocess.run([sys.executable,'tools/phase3bd/world_guard.py'],check=True)
