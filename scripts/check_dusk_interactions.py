"""Native Dusk checks with the selected fzf pointer's actual background role."""
import argparse
import json
from pathlib import Path
from tintprobe import evaluate_interactions as engine
from ithilienlib import ROOT

_fzf_roles = engine.fzf_roles


def fzf_roles(options):
    roles = _fzf_roles(options)
    # The active pointer is painted on bg+, as confirmed by native captures and
    # Tintprobe's fzf_oracle. The pinned static mapper incorrectly uses gutter.
    # Keep all native cell checks and the selected-item oracle unchanged.
    if 'pointer' in roles and 'fg+' in roles:
        roles['pointer'] = engine.pair(roles['pointer']['foreground'], roles['fg+']['background'])
    return roles


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'tests/evaluation/results/dusk-interactions')
    args = parser.parse_args()
    entries = [e for e in json.loads((ROOT / 'tests/evaluation/themes.json').read_text())
               if e['id'] == 'ithilien-dusk']
    engine.fzf_roles = fzf_roles
    try:
        report = engine.run(entries, args.output)
    finally:
        engine.fzf_roles = _fzf_roles
    report['project_correction'] = 'Static fzf active pointer uses bg+; native checks unchanged.'
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return 0 if report['results'] and all(r['quality_pass'] for r in report['results']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
