"""Recheck saved Codex cells without claiming a fresh renderer capture."""
import argparse
import hashlib
import json
from pathlib import Path

from tintprobe.agent_gates import assess
from tintprobe.context import load_palette, port_path


def check(recording):
    if not recording.exists() or not recording.with_name('report.json').exists():
        return {'status': 'blocked', 'reason': 'Saved Codex cells and report.json are required; supply CODEX_RECORDING.'}
    provenance = json.loads(recording.with_name('report.json').read_text())
    digest = hashlib.sha256(port_path('codex_theme').read_bytes()).hexdigest()
    if provenance.get('status') != 'pass' or provenance.get('theme_sha256') != digest:
        return {'status': 'blocked', 'reason': 'Recording is not a passing capture of the current exported theme; refresh it explicitly.'}
    report = assess(json.loads(recording.read_text()), load_palette())
    report.update(source_revision=provenance.get('source_revision'),
                  recording_sha256=hashlib.sha256(recording.read_bytes()).hexdigest(),
                  coverage='Saved cells only. Current installed Codex, live interactions, and terminal pixels are unverified.')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recording', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = check(args.recording)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('Saved Codex check: ' + report['status'])
    raise SystemExit(0 if report['status'] == 'pass' else 1)
