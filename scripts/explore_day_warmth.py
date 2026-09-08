"""Audit and render foundation-only Day experiments without changing live palettes.

python scripts/explore_day_warmth.py [--png]
Sources: experiments/day-warmth.json and palette/loden-day.json.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import audit_palette
import review_day
from lodenlib import ROOT, delta_e, load_palette, oklch, simulated_hex, wcag

OUT = ROOT / 'reports/day-warmth'
MODES = ('normal', 'protan', 'deutan', 'tritan', 'grayscale')


def audit(palette: dict, stem: str) -> dict:
    """Run the unchanged production audit in an isolated report directory."""
    with tempfile.TemporaryDirectory() as temp:
        with patch.object(audit_palette, 'ROOT', Path(temp)), \
             patch.object(audit_palette, 'load_palette', return_value=palette), \
             contextlib.redirect_stdout(io.StringIO()):
            try:
                audit_palette.main('loden-day')
            except SystemExit as error:
                if error.code != 1:
                    raise
        for suffix in ('json', 'md'):
            data = (Path(temp) / f'reports/loden-day-audit.{suffix}').read_text()
            (OUT / f'{stem}-audit.{suffix}').write_text(data)
        return json.loads((OUT / f'{stem}-audit.json').read_text())


def agent_panel(d, p, x, title):
    """Controlled agent-review specimen, not native Codex or Claude output."""
    b, f, a, diff, hi = (p[k] for k in ('backgrounds', 'foregrounds', 'accents', 'diff', 'highlight'))
    d.rect(x, 0, 760, 1020, b['base'])
    d.rect(x, 0, 760, 42, b['mantle'])
    d.text(x + 18, 12, title, f['text'], 'bold')
    d.rect(x + 16, 60, 728, 92, b['surface0'])
    d.text(x + 28, 72, 'You', f['subtext'], 'bold')
    d.text(x + 28, 98, 'Increase the retry budget, fix the boundary check,', f['text'])
    d.text(x + 28, 121, 'and preserve the existing error message.', f['text'])
    prose = [
        'I found two changes in retry.ts. The request retries up to',
        'three times. A strict comparison excludes the upper bound,',
        'so I will include it and keep partial failures visible.',
        '',
        'The patch below changes one digit and one operator.',
        'The markers identify the line state; the small highlighted',
        'cells identify exactly which characters changed.',
    ]
    for i, line in enumerate(prose):
        d.text(x + 24, 181 + i * 24, line, f['text'])
    d.text(x + 24, 369, 'Patch / explicit character-level annotations', a['gold'], 'bold')
    # Mark only the character that changed; never imply the theme computes a diff.
    rows = [
        ('hunk', '@@ -4,4 +4,4 @@ retry policy', None, None),
        ('delete', '- const retries = 2', '2', 'delete'),
        ('add', '+ const retries = 3', '3', 'add'),
        ('delete', '- if (attempt < limit) {', None, None),
        ('add', '+ if (attempt <= limit) {', '=', 'add'),
        ('change', '~ const retries = 3', '3', 'selection'),
        ('change', '~ if (attempt <= limit) {', '=', 'selection'),
        ('change', '~ return items.map( item => item.id)', ' ', 'space'),
    ]
    for i, (state, text, changed, emphasis) in enumerate(rows):
        y = 405 + i * 28
        d.rect(x + 16, y, 728, 28, diff[state + 'Background'])
        d.text(x + 24, y + 4, text, diff[state + 'Foreground'])
        if changed:
            index = text.index(changed) if emphasis != 'space' else text.index('( ') + 1
            ex = x + 24 + index * 9
            black = emphasis in ('selection', 'space')
            bg = hi['background'] if black else diff[emphasis + 'Emphasis']
            fg = hi['foreground'] if black else diff['inlineForeground']
            d.rect(ex, y, 9, 28, bg)
            d.text(ex, y + 4, '·' if emphasis == 'space' else changed, fg, 'bold')
            if not black:
                d.rect(ex, y + 24, 9, 1, fg)
    d.text(x + 24, 648, 'The visible dot denotes an inserted space in this specimen.', f['comment'], 'italic')
    d.rect(x + 16, 688, 728, 121, b['mantle'])
    for i, (line, fg) in enumerate([
        ('$ python -m unittest tests.test_retry', f['subtext']),
        ('PASS  retry budget and boundary cases', a['sage']),
        ('WARN  network timeout still uses the existing default', a['gold']),
        ('Completed in 0.42s / 2 files reviewed', f['muted']),
    ]):
        d.text(x + 28, 699 + i * 25, line, fg)
    d.text(x + 24, 837, 'The error wording is unchanged. The tests cover the new', f['text'])
    d.text(x + 24, 861, 'boundary and retry count; network behavior needs a live run.', f['text'])
    d.rect(x + 24, 910, 324, 29, hi['background'])
    d.text(x + 32, 915, 'Review changes   /   Enter', hi['foreground'])
    d.text(x + 24, 973, 'Esc cancel   ·   2 files   ·   +2 / -2', f['muted'])


def draw_pair(left, right, title, stem, png, mode='normal', agent=False):
    d = review_day.Drawing()
    d.rect(0, 0, 1540, 1020 if agent else 1080, '#D0CEC5')
    for x, palette, label in ((0, left, 'Current Day'), (780, right, title)):
        p = copy.deepcopy(palette)
        if mode != 'normal':
            for family in ('backgrounds', 'foregrounds', 'accents', 'ansi', 'diff', 'highlight'):
                p[family] = {k: simulated_hex(v, mode) for k, v in p[family].items()}
        if agent:
            agent_panel(d, p, x, label)
        else:
            review_day.panel(d, p, x, label + ' / ' + mode, True, mode)
    with patch.object(review_day, 'OUT', OUT):
        d.save(stem, 1540, 1020 if agent else 1080, png)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / 'experiments/day-warmth.json').read_text())
    current = json.loads((ROOT / config['referencePalette']).read_text()) if 'referencePalette' in config else load_palette('loden-day')
    if args.png:
        subprocess.run(['swiftc', '-module-cache-path', '/private/tmp/loden-swift-cache',
                        str(ROOT / 'scripts/render_review.swift'), '-o', '/private/tmp/loden-render-review'], check=True)
    (OUT / 'current-palette.json').write_text(json.dumps(current, indent=2) + '\n')
    candidates = [('current', 'Current Day', current)]
    for spec in config['candidates']:
        p = copy.deepcopy(current)
        p['backgrounds'] = spec['backgrounds']
        p['name'] = spec['name']
        for family in ('foregrounds', 'accents', 'ansi', 'diff', 'highlight'):
            assert p[family] == current[family]
        order = [oklch(p['backgrounds'][k])[0] for k in ('surface0', 'base', 'surface1', 'mantle', 'crust', 'surface2')]
        assert all(a > b for a, b in zip(order, order[1:])), 'Surface hierarchy inverted'
        candidates.append((spec['id'], spec['name'], p))
        (OUT / f'{spec["id"]}-palette.json').write_text(json.dumps(p, indent=2) + '\n')
    summaries = []
    for stem, name, p in candidates:
        report = audit(p, stem)
        base = p['backgrounds']['base']
        rows = report['contrast']
        summary = dict(id=stem, name=name, base=base, passed=report['passed'],
                       failures=report['failures'],
                       text=round(wcag(p['foregrounds']['text'], base), 3),
                       subtext=round(wcag(p['foregrounds']['subtext'], base), 3),
                       comment=round(wcag(p['foregrounds']['comment'], base), 3),
                       muted=round(wcag(p['foregrounds']['muted'], base), 3),
                       syntaxMinimum=round(min(wcag(c, base) for c in p['accents'].values()), 3),
                       mantleMuted=round(wcag(p['foregrounds']['muted'], p['backgrounds']['mantle']), 3),
                       canvasOklch=[round(v, 5) for v in oklch(base)],
                       changeLineToCanvas={mode:round(delta_e(p['diff']['changeBackground'],base,mode),4) for mode in MODES},
                       failedChecks=[r for r in rows if not r['passed']])
        summaries.append(summary)
        print(name, 'PASS' if summary['passed'] else 'FAIL', summary['failures'])
        if stem != 'current':
            draw_pair(current, p, name, stem + '-code', args.png)
            draw_pair(current, p, name, stem + '-agent', args.png, agent=True)
    # Reference only: borrow one canvas, so its warmth can be isolated from Gruvbox syntax.
    ref = copy.deepcopy(current)
    ref['backgrounds']['base'] = config['gruvboxReference']['background']
    draw_pair(current, ref, 'Gruvbox soft canvas / Loden inks', 'gruvbox-canvas', args.png)
    # Both passing experiments get full simulated code/diff specimens.
    for stem, name, viable in candidates:
        if stem not in ('warm-ivory', 'parchment'):
            continue
        for mode in MODES[1:]:
            draw_pair(current, viable, name, stem + '-' + mode, args.png, mode)
    # Compact code samples show the warmth range without changing syntax or typography.
    d = review_day.Drawing()
    options = [(n, p) for _, n, p in candidates] + [('Gruvbox soft canvas / Loden inks', ref)]
    for i, (name, p) in enumerate(options):
        y = i * 300
        d.rect(0, y, 1000, 300, p['backgrounds']['base'])
        d.text(20, y + 12, name + '  ' + p['backgrounds']['base'], p['foregrounds']['text'], 'bold')
        colors = {**p['foregrounds'], **p['accents']}
        for j, line in enumerate(review_day.CODE[:9]):
            x = 24
            for role, text in line:
                d.text(x, y + 46 + j * 24, text, colors[role],
                       'italic' if role == 'comment' else 'bold' if role == 'clay' else 'regular')
                x += len(text) * 9
        d.text(24, y + 272, 'Same Loden foregrounds and syntax; canvas comparison only.', p['foregrounds']['subtext'])
    with patch.object(review_day, 'OUT', OUT):
        d.save('warmth-range', 1000, 1500, args.png)
    (OUT / 'summary.json').write_text(json.dumps(summaries, indent=2) + '\n')


if __name__ == '__main__':
    main()
