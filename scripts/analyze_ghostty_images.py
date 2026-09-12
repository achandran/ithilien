"""Recheck saved command screenshots without native screen access."""
import argparse
import json
from pathlib import Path
from capture_ghostty import build_helper
from ghostty_quality import analyze

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();output=args.output.resolve()
    report=analyze(output,build_helper(output))
    print('Text-check status: '+report['status'])
    print('Report: '+str(output/'quality.html'))
    raise SystemExit(0 if report['status']=='pass' else 1)
