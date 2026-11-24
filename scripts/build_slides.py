"""Rebuild a case's standalone slides from its editable sources."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', default='BV1MssN6ZE1v')
args = parser.parse_args()
script = ROOT / 'cases' / args.case / 'interactive-slides' / 'source' / 'rebuild.py'
if not script.is_file():
    parser.error(f'No rebuild script for case {args.case}')
subprocess.run([sys.executable, str(script)], check=True)
