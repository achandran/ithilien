"""Configure explicit project inputs for Tintprobe-backed regression checks."""
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ['TINTPROBE_PROJECT_ROOT'] = str(ROOT)
sys.path.insert(0, str(ROOT / 'tests/workflows'))
